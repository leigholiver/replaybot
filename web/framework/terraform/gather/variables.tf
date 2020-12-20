variable "src_dir" {
  description = "path to the source code"
  type        = string
}

variable "requirements" {
  description = "path to the requirements file"
  type        = string
}

variable "build_dir" {
  description = "path to install the dependencies to"
  type        = string
}

variable "zip_path" {
  description = "path to output the zip file to"
  type        = string
}

variable "additional_dirs" {
  description = "additional paths to include in the zip package"
  type        = list(map(string))
  default     = []
}
