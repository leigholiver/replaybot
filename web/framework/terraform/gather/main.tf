locals {
  additional_dirs = [
    for path_key, path in var.additional_dirs : {
      dir      = path.dir
      basepath = lookup(path, "basepath", "")
    }
  ]
  dir_paths = concat([{
    dir      = var.src_dir
    basepath = ""
  }], local.additional_dirs)
}

module "hashes" {
  source = "../hashpath"
  paths  = [for path in local.dir_paths : path.dir]
}

module "piphash" {
  source = "../hashpath"
  paths  = [var.requirements]
}

resource "null_resource" "package_deps" {
  triggers = {
    reqs_changed = module.piphash.hashes[0]
  }

  provisioner "local-exec" {
    command = "mkdir -p ${var.build_dir} && pip3 install -r ${var.requirements} -t ${var.build_dir}"
  }
}

resource "null_resource" "package_dirs" {
  count = length(local.dir_paths)
  triggers = {
    src_changed = module.hashes.hashes[count.index]
  }

  provisioner "local-exec" {
    command = "${local.dir_paths[count.index].basepath == "" ? "" : "mkdir -p ${var.build_dir}/${local.dir_paths[count.index].basepath} && "} cp -r ${local.dir_paths[count.index].dir}/* ${var.build_dir}/${local.dir_paths[count.index].basepath}"
  }
  depends_on = [null_resource.package_deps]
}

# hack to make sure that everything is finished
# packaging before building the zip file
data "null_data_source" "wait_for_packaging" {
  inputs = {
    lambda_exporter_id = null_resource.package_dirs[0].id
    build_dir          = var.build_dir
  }
  depends_on = [null_resource.package_dirs]
}

data "archive_file" "lambda_zip" {
  type        = "zip"
  source_dir  = data.null_data_source.wait_for_packaging.outputs["build_dir"]
  output_path = var.zip_path
  depends_on = [null_resource.package_dirs, null_resource.package_deps]
}
