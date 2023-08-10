import os
from datetime import datetime

class Inode:
    def __init__(self, name, data="", permissions="rw"):
        self.name = name
        self.data = data
        self.permissions = permissions
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def change_permissions(self, permissions):
        self.permissions = permissions

    def get_permissions(self):
        return self.permissions

class Directory:
    def __init__(self):
        self.entries = {}

    def add_entry(self, name, inode):
        self.entries[name] = inode

    def remove_entry(self, name):
        if name in self.entries:
            del self.entries[name]

class FileSystem:
    def __init__(self):
        self.root = Directory()

    def create_file(self, path, data="", permissions="rw"):
        file_name = os.path.basename(path)
        directory_path = os.path.dirname(path)
        directory = self._traverse_path(directory_path)
        if directory:
            inode = Inode(file_name, data, permissions)
            directory.add_entry(file_name, inode)

    def delete_file(self, path):
        file_name = os.path.basename(path)
        directory_path = os.path.dirname(path)
        directory = self._traverse_path(directory_path)
        if directory and file_name in directory.entries:
            del directory.entries[file_name]

    def write_file(self, path, data):
        file_name = os.path.basename(path)
        directory_path = os.path.dirname(path)
        directory = self._traverse_path(directory_path)
        if directory and file_name in directory.entries:
            inode = directory.entries[file_name]
            inode.data = data
            inode.updated_at = datetime.now()

    def read_file(self, path):
        file_name = os.path.basename(path)
        directory_path = os.path.dirname(path)
        directory = self._traverse_path(directory_path)
        if directory and file_name in directory.entries:
            return directory.entries[file_name].data

    def copy_file(self, src_path, dest_path):
        src_file_name = os.path.basename(src_path)
        dest_file_name = os.path.basename(dest_path)
        dest_directory_path = os.path.dirname(dest_path)

        src_directory = self._traverse_path(os.path.dirname(src_path))
        dest_directory = self._traverse_path(dest_directory_path)

        if src_directory and src_file_name in src_directory.entries:
            src_inode = src_directory.entries[src_file_name]
            dest_inode = Inode(dest_file_name, src_inode.data, src_inode.permissions)
            dest_directory.add_entry(dest_file_name, dest_inode)
        else:
            print("Error: Source file not found.")

    def rename_file(self, path, new_name):
        file_name = os.path.basename(path)
        directory_path = os.path.dirname(path)
        directory = self._traverse_path(directory_path)

        if directory and file_name in directory.entries:
            inode = directory.entries[file_name]
            inode.name = new_name
            directory.remove_entry(file_name)
            directory.add_entry(new_name, inode)
        else:
            print("Error: File not found.")

    def change_file_permissions(self, path, permissions):
        file_name = os.path.basename(path)
        directory_path = os.path.dirname(path)
        directory = self._traverse_path(directory_path)

        if directory and file_name in directory.entries:
            inode = directory.entries[file_name]
            inode.change_permissions(permissions)
            print(f"File '{file_name}' permissions changed to '{permissions}' successfully.")
        else:
            print("Error: File not found.")

    def show_file_permissions(self, path):
        file_name = os.path.basename(path)
        directory_path = os.path.dirname(path)
        directory = self._traverse_path(directory_path)

        if directory and file_name in directory.entries:
            permissions = directory.entries[file_name].get_permissions()
            print(f"File '{file_name}' permissions: {permissions}")
        else:
            print("Error: File not found.")

    def _traverse_path(self, path):
        if path == "/":
            return self.root

        directories = path.split("/")
        current_directory = self.root
        for directory in directories[1:]:
            if directory in current_directory.entries:
                current_directory = current_directory.entries[directory]
            else:
                return None
        return current_directory

def main():
    fs = FileSystem()

    while True:
        print("\nOptions:")
        print("1. Create File")
        print("2. Write to File")
        print("3. Read File")
        print("4. Delete File")
        print("5. Copy File")
        print("6. Rename File")
        print("7. Change File Permissions")
        print("8. Show File Permissions")
        print("9. Exit")

        try:
            choice = int(input("Enter your choice: "))
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue

        if choice == 1:
            filename = input("Enter the filename: ")
            fs.create_file(filename)
            if fs.create_file(filename):
                print(f"File '{filename}' created successfully.")
            else:
                print(f"File '{filename}' created successfull")

        elif choice == 2:
            filename = input("Enter the filename: ")
            data = input("Enter data to write: ")
            fs.write_file(filename, data)
            print(f"File '{filename}' written successfully")

        elif choice == 3:
            filename = input("Enter the filename: ")
            data = fs.read_file(filename)
            if data:
                print("File content:")
                print(data)

        elif choice == 4:
           filename = input("Enter the filename: ")
           directory_path = os.path.dirname(filename)
           file_name = os.path.basename(filename)

           directory = fs._traverse_path(directory_path)
           if directory and file_name in directory.entries:
                try:
                 fs.delete_file(filename)
                 print(f"File '{filename}' deleted successfully.")
                except PermissionError:
                 print(f"Permission denied. Unable to delete file '{filename}'.")
           else:
               print(f"File '{filename}' not found. It might have1 already been deleted.")


        elif choice == 5:
            src_filename = input("Enter the source filename: ")
            dest_filename = input("Enter the destination filename: ")
            fs.copy_file(src_filename, dest_filename)
            print(f"File '{filename}' copy to a '{dest_filename}' file successfully")

        elif choice == 6:
            filename = input("Enter the filename: ")
            new_filename = input("Enter the new filename: ")
            new_name = fs.rename_file(filename, new_filename)
            if new_name:
             print(f"File '{filename}' renamed successfully. New file name: '{new_name}'.")
            else:
             print(f"File '{filename}' has been renamed.")


        elif choice == 7:
            filename = input("Enter the filename: ")
            permissions = input("Enter the new permissions (e.g., 'rwx' or 'rw' or 'r'): ")

            perm_octal = 0
            if 'r' in permissions:
             perm_octal += 4
            if 'w' in permissions:
             perm_octal += 2
            if 'x' in permissions:
             perm_octal += 1
        
            fs.change_file_permissions(filename, oct(perm_octal))
            print(f"File '{filename}' permissions change successful")
        
        elif choice == 8:
         filename = input("Enter the filename: ")
         fs.show_file_permissions(filename)


        elif choice == 9:
         print("Exiting...")
         break

        else:
         print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
