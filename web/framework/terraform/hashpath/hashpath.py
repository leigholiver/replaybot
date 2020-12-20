import hashlib, os, json, sys
from _hashlib import HASH as Hash
from pathlib import Path
from typing import Union

def hash_path(path, ignore = []):
    path = os.path.abspath(path)
    if Path(path).is_dir():
        file_hash = md5_dir(path, ignore);
    elif Path(path).is_file():
        file_hash = md5_file(path, ignore);
    else:
        return 0
    return file_hash

def md5_file(filename: Union[str, Path], ignore) -> str:
    return str(md5_update_from_file(filename, hashlib.md5(), ignore).hexdigest())

def md5_dir(directory: Union[str, Path], ignore) -> str:
    return str(md5_update_from_dir(directory, hashlib.md5(), ignore).hexdigest())

def md5_update_from_file(filename: Union[str, Path], hash: Hash, ignore) -> Hash:
    if str(filename) in ignore:
        return hash
    assert Path(filename).is_file()
    with open(str(filename), "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash.update(chunk)
    return hash

def md5_update_from_dir(directory: Union[str, Path], hash: Hash, ignore) -> Hash:
    if str(directory) in ignore:
        return hash
    assert Path(directory).is_dir()
    for path in sorted(Path(directory).iterdir(), key=lambda p: str(p).lower()):
        hash.update(path.name.encode())
        if path.is_file():
            hash = md5_update_from_file(path, hash, ignore)
        elif path.is_dir():
            hash = md5_update_from_dir(path, hash, ignore)
    return hash

if __name__ == "__main__":
    print("{\"hash\":\"%s\"}" % hash_path(sys.argv[1]))
