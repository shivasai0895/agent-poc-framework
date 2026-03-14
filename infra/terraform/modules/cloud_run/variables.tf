variable "project_id" { type = string }
variable "region" { type = string }
variable "image" { type = string }
variable "service_name" {
  type    = string
  default = "adk-agent"
}
