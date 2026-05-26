import os
import shutil


def copy_contents(src, dest):
    shutil.rmtree(dest, True)

    if not os.path.exists(src):
        raise Exception(f"{src} directory doesn't exist")

    os.mkdir(dest)

    if os.path.isfile(src):
        return

    for entry in os.listdir(src):
        if os.path.isfile(os.path.join(src, entry)):
            shutil.copy(os.path.join(src, entry), os.path.join(dest, entry))
        else:
            copy_contents(os.path.join(src, entry), os.path.join(dest, entry))
