"""
decoupling은 테스트를 위해서도 중요하다.
단순히 코드가 간단해지는 것 이상으로 e2e, unit 등 다양한 경우에 편의를 제공해준다.
"""
from pathlib import Path

from coupling_and_abstraction.abstracted_sync import determine_actions, sync


class FakeFileSystem(list):
    def copy(self, src, dest):
        self.append(("copy",src,dest))

    def move(self, src, dest):
        self.append(("move",src,dest))

    def delete(self, dest):
        self.append(("delete",dest))

def test_when_a_file_exists_in_the_source_but_not_the_destination():
    source={"sha1":"my-file"}
    dest={}
    filesystem=FakeFileSystem()

    reader={"/source":source, "/dest":dest}
    sync(reader.pop, filesystem, "/source", "/dest")
    assert filesystem==[('copy', Path('/source/my-file'), Path('/dest/my-file'))]

def test_when_a_file_has_been_renamed_in_the_source():
    source = {"sha1": "renamed-file"}
    dest = {"sha1": "original-file"}
    filesystem = FakeFileSystem()

    reader = {"/source": source, "/dest": dest}
    sync(reader.pop, filesystem, "/source", "/dest")
    assert filesystem==[('move', Path('/dest/original-file'), Path('/dest/renamed-file'))]