import os
from pathlib import Path

def lock(db_filename):
    os.system("mkdir -p .localdb")
    lockfile_path = "%s.lock" % db_filename
    while os.path.exists(lockfile_path): pass
    Path(lockfile_path).touch()

def unlock(db_filename):
    lockfile_path = "%s.lock" % db_filename
    if os.path.exists(lockfile_path):
        os.remove(lockfile_path)
