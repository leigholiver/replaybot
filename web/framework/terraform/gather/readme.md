# gather
[requires pip] utility module to gather pip dependencies and source code into a zip file for a lambda

#### variables
* `src_dir` path to the source code
* `requirements` path to the requirements file
* `additional_dirs` list of additional directories to package
    * `dir` the path to the directory
    * `basepath` (optional) the path within the package to put the files (default root)
* `build_dir` path to build the code + dependencies into
* `zip_path` path to output the zip file to

#### outputs
* `zip_path` path to the packaged zip file
