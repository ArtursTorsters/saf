"""
Data Service — reads JSON files and merges sensor data into a flat,
frontend-friendly format.

This module is the core business logic layer. It:
  1. Loads the 3 JSON files once at startup (cached in memory).
  2. Merges sensors + metrics + sensorTypes into a single list.
  3. Handles all missing-data edge cases gracefully.
"""

import json
import os
from typing import Any

# ── Path to the data directory (mounted via Docker volume) ──────────
DATA_DIR = os.environ.get("DATA_DIR", os.path.join(os.path.dirname(__file__), "..", "data"))


def _load_json(filename: str) -> dict:
    """Read and parse a JSON file from the data directory."""
    filepath = os.path.join(DATA_DIR, filename)
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


class DataService:
    """
    Singleton-style service that loads JSON data once and provides
    a merged, frontend-ready sensor list.
    """

    def __init__(self) -> None:
        # Raw data loaded from disk
        self._sensors_raw: dict = {}
        self._metrics_raw: list = []
        self._sensor_types_raw: dict = {}

        # Processed / cached results
        self._metric_columns: list[str] = []
        self._metrics_lookup: dict[str, dict[str, Any]] = {}

    # ── Loading ─────────────────────────────────────────────────────

    def load(self) -> None:
        """Load all JSON files and pre-process metrics lookup."""
        self._sensors_raw = _load_json("sensors.json")
        self._sensor_types_raw = _load_json("sensorTypes.json")

        metrics_data = _load_json("metrics.json")
        self._metrics_raw = metrics_data.get("data", {}).get("items", [])

        self._build_metrics_lookup()

    def _build_metrics_lookup(self) -> None:
        """
        Build a lookup dict:  metric_id -> { "column_name": "Temperature (°C)", ... }

        The column name is:  metric_name + " (" + active_unit_name + ")"
        The "active" unit is the one with  selected: true.
        """
        self._metrics_lookup = {}
        self._metric_columns = []

        for metric in self._metrics_raw:
            metric_id = str(metric.get("id", ""))
            metric_name = metric.get("name", f"Metric {metric_id}")

            # Find the active unit (the one with selected: true)
            units = metric.get("units", [])
            active_unit = next(
                (u for u in units if u.get("selected")),
                units[0] if units else None,
            )
            unit_name = active_unit.get("name", "") if active_unit else ""

            column_name = f"{metric_name} ({unit_name})" if unit_name else metric_name

            self._metrics_lookup[metric_id] = {
                "column_name": column_name,
                "precision": active_unit.get("precision", 2) if active_unit else 2,
            }
            self._metric_columns.append(column_name)

    # ── Public API ──────────────────────────────────────────────────

    def get_sensor_type_name(self, type_id: Any, variant_id: Any) -> str:
        """
        Look up the human-readable sensor type name.
        Returns "Unknown Type" if the type/variant combo is missing.
        """
        type_str = str(type_id) if type_id is not None else ""
        variant_str = str(variant_id) if variant_id is not None else ""

        type_entry = self._sensor_types_raw.get(type_str, {})
        variant_entry = type_entry.get(variant_str, {})
        return variant_entry.get("name", "Unknown Type")

    def get_sensors(self) -> dict:
        """
        Return the merged sensor list + list of metric column names.

        Response shape:
        {
            "sensors": [
                {
                    "id": "1048609",
                    "name": "Sensor 1",
                    "typeName": "T/RH Sensor",
                    "type": 1,
                    "metrics": {
                        "Temperature (°C)": 21.80,
                        "Humidity (%RH)": null
                    }
                },
                ...
            ],
            "metricColumns": ["Temperature (°C)", "Humidity (%RH)", ...]
        }
        """
        sensors = []

        for sensor_id, sensor_data in self._sensors_raw.items():
            # ── Handle missing sensor name ──
            name = sensor_data.get("name") or f"Unknown Sensor (ID: {sensor_id})"

            # ── Handle missing sensor type ──
            sensor_type = sensor_data.get("type")
            sensor_variant = sensor_data.get("variant")
            type_name = self.get_sensor_type_name(sensor_type, sensor_variant)

            # ── Build metrics dict with all columns (null for missing) ──
            sensor_metrics_raw = sensor_data.get("metrics", {})
            metrics_values: dict[str, float | None] = {}

            for metric_id, meta in self._metrics_lookup.items():
                col_name = meta["column_name"]
                precision = meta["precision"]

                raw = sensor_metrics_raw.get(metric_id)
                if raw is not None and "v" in raw:
                    metrics_values[col_name] = round(raw["v"], precision)
                else:
                    metrics_values[col_name] = None

            sensors.append(
                {
                    "id": sensor_id,
                    "name": name,
                    "typeName": type_name,
                    "type": sensor_type,
                    "metrics": metrics_values,
                }
            )

        return {
            "sensors": sensors,
            "metricColumns": list(self._metric_columns),
        }
