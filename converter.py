import glob
import os
from time import sleep
import hashlib
from subprocess import call


def main():
    while True:
        for filename in glob.glob("*.ase"):

            # Try to find an existing instance for that file
            file = AseFile.find_file(filename)

            if file:
                # check if md5 changed between passes
                newFile = AseFile(filename)
                if (newFile.hash != file.hash):
                    newFile.export()
                    AseFile.files.remove(file)
                    AseFile.files.append(newFile)
            else:
                # Create an instance and save it
                file = AseFile(filename)
                file.export()
                AseFile.files.append(file)

        sleep(2)


class AseFile:
    files = []

    def __init__(self, name):
        self.name = name
        self.hash = self.get_hash()
        self.png_name = os.path.splitext(self.name)[0] + ".png"

    def get_hash(self):
        fullpath = os.path.abspath(self.name)
        return hashlib.md5(open(fullpath, 'rb').read()).hexdigest()

    def export(self):
        call(["path\\to\\aseprite.exe", "--batch", self.name, "--sheet", self.png_name])

    @classmethod
    def find_file(cls, filename):
        for file in cls.files:
            if file.name == filename:
                return file
            return false

if __name__ == "__main__":
    main()
