variable "environment" {
  description = "Environment name"
  type        = string
  default     = "local"
}

variable "service_name" {
  description = "service name"
  type        = string
  default     = "pub-service"
}

variable "max_delivery_attempts" {
  description = "max amount of retries"
  type        = number
  default     = 3
}

variable "service_url" {
  description = "service url"
  type        = string
  default     = "https://merry-warm-buck.ngrok-free.app"
}