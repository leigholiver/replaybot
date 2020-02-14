# lamb.py -project specific configuration
# do not store secrets in this file

# API Lambda
use_api = True

# Database
use_db = True

# Single page site S3 bucket from the /public folder
use_public = True

# if True, force to https://[domain name] 
# instead of https://www.[domain name]
no_www = True

# Tests to run before deployment
deploy_tests = [
    'router'
]