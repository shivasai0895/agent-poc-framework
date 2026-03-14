variable "project_id" { type = string }
variable "region" { type = string }
variable "db_name" { type = string }
variable "instance_name" {
  type    = string
  default = "adk-agent-db"
}
variable "db_tier" {
  type    = string
  default = "db-f1-micro"
}
