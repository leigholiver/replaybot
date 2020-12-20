output "zip_path" {
  value = var.zip_path
}

output "base64sha256" {
  value = data.archive_file.lambda_zip.output_base64sha256
}
