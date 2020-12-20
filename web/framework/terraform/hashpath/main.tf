variable "paths" {
  description = "list of file/directory paths to hash"
  type        = list(string)
}

data "external" "src_hash" {
  count   = length(var.paths)
  program = ["python3", "${path.module}/hashpath.py", var.paths[count.index]]
}

output "hashes" {
  value = [for hash_key, hash in data.external.src_hash : hash.result["hash"]]
}
