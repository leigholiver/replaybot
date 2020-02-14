import hashlib, os, json, sys
from _hashlib import HASH as Hash
from pathlib import Path
from typing import Union

class HashUtil():
    basePath = os.path.dirname(__file__) + '/..'
    output_file = basePath + '/pkghash.json'

    def __init__(self):
        try:
            with open(self.output_file, 'r') as infile:
                self.data_file = json.load(infile)
        except:
            self.data_file = {}

    def save(self):
        with open(self.output_file, 'w') as outfile:
            json.dump(self.data_file, outfile)

    def hasChanged(self, path, ignore = []):
        file_hash = ""
        path_hash = hashlib.md5(path.encode('utf-8')).hexdigest()
        
        ignore = list(map(lambda item: os.path.abspath(self.basePath + item), ignore))

        if Path(path).is_dir():
            file_hash = md5_dir(path, ignore);
        else:
            file_hash = md5_file(path, ignore);

        if path_hash in self.data_file.keys() and file_hash == self.data_file[path_hash]:
            return False

        self.data_file[path_hash] = file_hash
        self.save()
        return True

def md5_update_from_file(filename: Union[str, Path], hash: Hash, ignore) -> Hash:
    if str(filename) in ignore:
        return hash
    assert Path(filename).is_file()
    with open(str(filename), "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash.update(chunk)
    return hash

def md5_file(filename: Union[str, Path], ignore) -> str:
    return str(md5_update_from_file(filename, hashlib.md5(), ignore).hexdigest())

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

def md5_dir(directory: Union[str, Path], ignore) -> str:
    return str(md5_update_from_dir(directory, hashlib.md5(), ignore).hexdigest())