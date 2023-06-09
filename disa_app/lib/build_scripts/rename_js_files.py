import os
import re
import subprocess
import hashlib


def main(project_directory):
    js_directory = os.path.join(project_directory, "app/static/js/")
    
    if not os.path.exists(js_directory):
        print(f"Directory {js_directory} does not exist.")
        return
    
    for filename in os.listdir(js_directory):
        if filename.endswith('.js'):
            file_path = os.path.join(js_directory, filename)
            pre_existing_hash = re.search(r'__(\w+)\.js', filename)
            if pre_existing_hash:
                pre_existing_hash = pre_existing_hash.group(1)
                actual_hash = md5(file_path)

                if actual_hash != pre_existing_hash:
                    new_filename = re.sub(r'__(\w+)\.js', f'__{actual_hash}.js', filename)
                    new_file_path = os.path.join(js_directory, new_filename)
                    os.rename(file_path, new_file_path)
                    update_references(project_directory, filename, new_filename)
                    print(f"Updated {filename} to {new_filename}")
                else:
                    print(f"Hash matched for {filename}")
            else:
                print(f"File {filename} does not have a pre-existing hash in its name")


def md5(file_path):
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def update_references(directory, old_filename, new_filename):
    for foldername, subfolders, filenames in os.walk(directory):
        for filename in filenames:
            file_path = os.path.join(foldername, filename)
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
                filedata = file.read()
            
            # Replace the target string
            new_data = filedata.replace(old_filename, new_filename)
            
            # Write the file out again
            with open(file_path, 'w', encoding='utf-8', errors='ignore') as file:
                file.write(new_data)




if __name__ == "__main__":
    PROJECT_DIR_PATH = os.environ['DISA_DJ__PROJECT_DIR_PATH']
    main( PROJECT_DIR_PATH )
