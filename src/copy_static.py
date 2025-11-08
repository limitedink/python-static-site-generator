import os
import shutil


def copy_static(src, destination):
    if os.path.exists(destination):
        shutil.rmtree(destination)

    os.mkdir(destination)

    if os.path.isdir(src):
        static_files = os.listdir(src)
        for file in static_files:
            if os.path.isfile(os.path.join(src, file)):
                shutil.copy(os.path.join(src, file), os.path.join(destination, file))
                print(
                    f'copied "{file}" from {os.path.join(src, file)} to {os.path.join(destination, file)}.'
                )

            elif os.path.isdir(os.path.join(src, file)):
                os.mkdir(os.path.join(destination, file))
                print(
                    f'creating "{file}" sub-directory in {os.path.join(destination, file)}.'
                )
                copy_static(os.path.join(src, file), os.path.join(destination, file))
                print(
                    f"Recursively copying contents from {os.path.join(src, file)} to {os.path.join(destination, file)}"
                )
    else:
        raise FileNotFoundError("static source file directory not found.")
