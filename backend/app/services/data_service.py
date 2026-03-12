# loads JSON, merges sensors + metrics + types into a flat list

import json
import os
from typing import Any

_app_data_dir = os.path.join(os.path.dirname(__file__), "..", "data")
_shared_data_dir = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "shared_data"))

_default_dir = _app_data_dir
if not os.path.exists(os.path.join(_app_data_dir, "sensors.json")) and os.path.exists(os.path.join(_shared_data_dir, "sensors.json")):
    _default_dir = _shared_data_dir

DATA_DIR = os.environ.get("DATA_DIR", _default_dir)


# read and parse a JSON file from data dir
def _load_json(filename: str) -> dict:
    filepath = os.path.join(DATA_DIR, filename)
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


class DataService:

    def __init__(self) -> None:
        self._sensors_raw: dict = {}
        self._metrics_raw: list = []
        self._sensor_types_raw: dict = {}

        self._metric_columns: list[str] = []
        self._metrics_lookup: dict[str, dict[str, Any]] = {}

    # load all JSON files and build metrics lookup
    def load(self) -> None:
        self._sensors_raw = _load_json("sensors.json")
        self._sensor_types_raw = _load_json("sensorTypes.json")

        metrics_data = _load_json("metrics.json")
        self._metrics_raw = metrics_data.get("data", {}).get("items", [])

        self._build_metrics_lookup()

    # build metric_id -> column_name lookup
    def _build_metrics_lookup(self) -> None:
        self._metrics_lookup = {}
        self._metric_columns = []

        for metric in self._metrics_raw:
            metric_id = str(metric.get("id", ""))
            metric_name = metric.get("name", f"Metric {metric_id}")


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

    # lookup sensor type name by type_id + variant_id
    def get_sensor_type_name(self, type_id: Any, variant_id: Any) -> str:
        type_str = str(type_id) if type_id is not None else ""
        variant_str = str(variant_id) if variant_id is not None else ""

        type_entry = self._sensor_types_raw.get(type_str, {})
        variant_entry = type_entry.get(variant_str, {})
        return variant_entry.get("name", "Unknown Type")

    # return merged sensor list + metric column names
    def get_sensors(self) -> dict:
        sensors = []

        for sensor_id, sensor_data in self._sensors_raw.items():

            name = sensor_data.get("name") or f"Unknown Sensor (ID: {sensor_id})"


            sensor_type = sensor_data.get("type")
            sensor_variant = sensor_data.get("variant")
            type_name = self.get_sensor_type_name(sensor_type, sensor_variant)


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
