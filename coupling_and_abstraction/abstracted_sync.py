import hashlib
import os
import shutil
from pathlib import Path

BLOCKSIZE=65536

def hash_file(path: Path):
    hasher=hashlib.sha1()
    with path.open("rb") as file:
        buf=file.read(BLOCKSIZE)
        while buf:
            hasher.update(buf)
            buf=file.read(BLOCKSIZE)
    return hasher.hexdigest()

def read_path_and_hashes(root):

    hashes={}
    for folder, _, files in os.walk(root):
        for fn in files:
            hashes[hash_file(Path(folder)/fn)]=fn
    return hashes

def determine_actions(src_hashes, dst_hashes, src_folder, dst_folder, filesystem):
    for sha, filename in src_hashes.items():
        if sha not in dst_hashes:
            sourcepath=Path(src_folder)/filename
            destpath=Path(dst_folder)/filename
            filesystem.copy(sourcepath, destpath)
        elif dst_hashes[sha]!=filename:
            olddestpath=Path(dst_folder)/dst_hashes[sha]
            newdestpath=Path(dst_folder)/filename
            filesystem.move(olddestpath, newdestpath)
    for sha, filename in dst_hashes.items():
        if sha not in src_hashes:
            filesystem.delete(dst_folder+"/"+filename)

class FakeFileSystem(list):
    def copy(self, src, dest):
        self.append(("copy",src,dest))

    def move(self, src, dest):
        self.append(("move",src,dest))

    def delete(self, src, dest):
        self.append(("delete",src,dest))

# params: reader=read_path_and_hashes, filesystem=FakeFileSystem
def sync(reader, filesystem, source, dest):
    # step1 gather inputs
    source_hashes=reader(source)
    dest_hashes=reader(dest)

    #step2 call functional core
    determine_actions(source_hashes, dest_hashes, source, dest, filesystem)