import os
import shutil
import subprocess


def clean_contents(dir_path):
    # Check if the directory exists
    if not os.path.exists(dir_path):
        print(f"The directory {dir_path} does not exist.")
        return

    # Check if the path is a directory
    if not os.path.isdir(dir_path):
        print(f"The path {dir_path} is not a directory.")
        return

    # Iterate over the contents of the directory
    for item in os.listdir(dir_path):
        item_path = os.path.join(dir_path, item)

        # Check if the item is a file or a directory
        if os.path.isfile(item_path) or os.path.islink(item_path):
            os.unlink(item_path)  # Remove the file or link
            print(f"File {item_path} has been deleted.")
        elif os.path.isdir(item_path):
            shutil.rmtree(item_path)  # Remove the directory
            print(f"Directory {item_path} has been deleted.")

    print(f"All contents of {dir_path} have been deleted.")


def copy_directory_contents(source_dir, destination_dir):
    # Check if source directory exists
    if not os.path.exists(source_dir):
        print(f"Source directory '{source_dir}' does not exist.")
        return

    # Check if destination directory exists, if not, create it
    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)
        print(f"Destination directory '{destination_dir}' created.")

    # Get list of files and directories in the source directory
    contents = os.listdir(source_dir)

    # Copy each file/directory from source to destination
    for item in contents:
        source_item = os.path.join(source_dir, item)
        destination_item = os.path.join(destination_dir, item)

        if os.path.isdir(source_item):
            shutil.copytree(source_item, destination_item, symlinks=True)
            print(f"Directory '{source_item}' copied to '{destination_item}'.")
        else:
            shutil.copy2(source_item, destination_item)
            print(f"File '{source_item}' copied to '{destination_item}'.")


def npm_build(directory_path):
    try:
        # Run npm build command
        npm_path = shutil.which("npm")
        if npm_path is not None:
            print("npm path:", npm_path)
        else:
            print("npm not found.")
        subprocess.run([npm_path, "run", "build"], check=True, cwd=directory_path)
        print("npm build completed successfully.")
    except subprocess.CalledProcessError as e:
        print("npm build failed:", e)


if __name__ == "__main__":
    while True:
        input("press enter to build ...")
        build_path = "D:/fax/diplomski/distributedLauncher/fe/nodestartergui/build"
        static_path = "D:/fax/diplomski/distributedLauncher/master/static"
        base_npm_path = "D:/fax/diplomski/distributedLauncher/fe/nodestartergui"
        npm_build(base_npm_path)
        clean_contents(static_path)
        copy_directory_contents(build_path, static_path)
