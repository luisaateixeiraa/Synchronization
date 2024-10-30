import os
import hashlib
import shutil
import sys
import time
    
# => Prints help and presents error if exists.
def print_help():
    print("Usage: python synchronization.py [directory_path] [sync_interval] [logs]")
    print("Options:")
    print("  -h, --help\t\tShow this help message and exit")

#=> Initial conditions to run the synchronization script.
def initial_conditions():
    if len(sys.argv) < 4:
        print("Error: Invalid number of arguments. Expected 3 arguments.")
        print_help()
        sys.exit(1)
    elif sys.argv[1] in ["-h", "--help"]:
        print_help()
        sys.exit(0)
    elif not os.path.exists(sys.argv[1]):
        print("Error: Directory path does not exist.")
        print_help()
        sys.exit(1)
    elif not sys.argv[2].isdigit():
        print("Error: Synchronization interval must be an integer.")
        print_help()
        sys.exit(1)
    elif not os.path.exists(sys.argv[3]):
        print("Error: Log path does not exist.")
        print_help()
        sys.exit(1)
        
# check if directory path exists, if not, create it
def verify_directory_path(directory_path):
    print("Checking the directory path...")
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
        print("Directory created!")
    else:
        print("Directory path already exists!")

# verify if folder exists, if not, create it
def verify_folder(folder_path):
    print(f"Checking if folder {folder_path} exists...")
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f"Folder {folder_path} created!")
    else:
        print(f"Folder {folder_path} exists!")

# check if the source folder is empty
def is_folder_empty(folder_path):
    if not os.listdir(folder_path):  # Check if the folder is empty
        print(f"Folder {folder_path} is empty!")
    else:
        print(f"Folder {folder_path} is not empty!")
                
# ensure the log file exists in the log path
def verify_log_path(log_path):
    print("Checking if a file logs.txt exist...")
    file_name = "logs.txt"
    if not os.path.isfile(file_name):
        file_path = os.path.join(log_path, file_name)
        with open(file_path, "w") as f:
            f.write("Log file created at: " + time.strftime("%Y-%m-%d %H:%M:%S"))
        print(f"File {file_name} created!")
    else:
        print(f"File {file_name} exist!")

# write a log message to the log file
def log_message(message):
    log_file_path = os.path.join(log_path, "logs.txt")
    with open(log_file_path, "a") as f:
        f.write(message + "\n")

# SHA-256 hash for a file
def sha256_hash_files(file_name):
    sha256 = hashlib.sha256()
    with open(file_name, "rb") as f:
        while True:
            data = f.read(4096)  
            if not data:
                break
            sha256.update(data)
    file_hash = sha256.hexdigest().encode('utf-8')
    return file_hash
            
# SHA-256 hash for a directory
def sha256_hash_directory(folder_name):
    sha256 = hashlib.sha256()
    file_path = os.path.join(folder_name)
    for file in sorted(file_path):  # Sort to ensure consistent ordering
            if os.path.isfile(file):
                file_hash = sha256_hash_files(file_path)
                sha256.update(file_hash)
    return sha256.hexdigest()

# copy files from the source directory to the replica directory
def copy_files():
    for file_name in os.listdir(source):
        source_file = os.path.join(source, file_name)
        replica_file = os.path.join(replica, file_name)           
        if os.path.isfile(source_file) and not os.path.isfile(replica_file):
            log_message(f"'{file_name}' added!")
            print(f"{file_name} added!")
            shutil.copy2(source_file, replica_file)
            log_message(f"File '{file_name}' copied!")
            print(f"File {file_name} copied!")
        elif sha256_hash_files(source_file) != sha256_hash_files(replica_file):
            shutil.copy2(source_file, replica_file)
            log_message(f"File '{file_name}' updated!")
            print(f"File {file_name} updated!")              

# remove files from replica that are not in the source
def remove_files():
    for file_name in os.listdir(replica):
        source_file = os.path.join(source, file_name)
        replica_file = os.path.join(replica, file_name)
        if os.path.isfile(replica_file) and not os.path.isfile(source_file):
            print("Removing extra files from replica folder...")
            os.remove(replica_file)
            log_message(f"File '{file_name}' removed!")
            print(f"File {file_name} removed!")

# main synchronization logic
def main():      
    print("Synchronization started!")
    
    # Verify if the source and replica directories exist
    verify_directory_path(directory_path)
    verify_folder(source)
    verify_folder(replica)
    
    # ensure the log file exists
    verify_log_path(log_path)
    
    # calculate hashes
    source_hash = sha256_hash_directory(source)
    print(f"Source hash: {source_hash}")
    replica_hash = sha256_hash_directory(replica)
    print(f"Replica hash: {replica_hash}")
    
     # Check if the source folder is empty before copying files
    if not is_folder_empty(source):
        if source_hash == replica_hash:
            copy_files()
            remove_files()
            print("Synchronization finished!")
        else:
            print("Hashes are different. Updating replica...")
            copy_files()
    else:
        log_message("Source folder is empty!")  

# run synchronization at the specified interval  
def sync_interval(interval): 
    while True:
        main()  # run the main synchronization logic
        time.sleep(interval) # wait for the next interval

if __name__ == "__main__":
    initial_conditions() # check for required conditions
    
    #environment variables
    directory_path = str(sys.argv[1])
    interval = int(sys.argv[2])
    log_path = str(sys.argv[3])
    source = os.path.join(directory_path, "source")
    replica = os.path.join(directory_path, "replica")
    
    sync_interval(interval) # start synchronization with interval timing

    

