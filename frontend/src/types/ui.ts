export interface AppButtonProps {
  variant?: 'primary' | 'secondary'
  type?: 'button' | 'submit' | 'reset'
}

export interface AppInputProps {
  modelValue?: string
  id?: string
  type?: string
  placeholder?: string
  clearable?: boolean
}

export interface AppInputEmits {
  'update:modelValue': [value: string]
}

export interface AppLabelProps {
  htmlFor?: string
}

export interface AppSelectProps {
  modelValue?: string
  id?: string
}

export interface AppSelectEmits {
  'update:modelValue': [value: string]
}
