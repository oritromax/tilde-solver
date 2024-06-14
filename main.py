import os
import re
import shutil

# Define the root directory to search for folders
root_dir = "/path/to/your/root/directory"

# ANSI escape codes for coloring the output
RESET = "\033[0m"
BOLD = "\033[1m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"

def list_folders_with_tilde(root_dir):
    return [f for f in os.listdir(root_dir) if os.path.isdir(os.path.join(root_dir, f)) and '~' in f]

# Function to extract base name by removing numbers and special characters
def extract_base_name(folder_name):
    base_name = re.sub(r'[0-9()~]', '', folder_name).strip()
    return base_name

# Function to find corresponding folders based on the base name
def find_corresponding_folders(folders_with_tilde, root_dir):
    corresponding_folders = {}
    multiple_matches = {}
    all_folders = [f for f in os.listdir(root_dir) if os.path.isdir(os.path.join(root_dir, f))]

    for folder_with_tilde in folders_with_tilde:
        base_name = extract_base_name(folder_with_tilde)
        print(f"{BLUE}Extracted base name for '{folder_with_tilde}': '{base_name}'{RESET}")  # Debug
        possible_matches = [f for f in all_folders if extract_base_name(f) == base_name and '~' not in f]
        print(f"{BLUE}Possible matches for '{folder_with_tilde}': {possible_matches}{RESET}")  # Debug
        if len(possible_matches) == 1:
            corresponding_folders[folder_with_tilde] = possible_matches[0]
        elif len(possible_matches) > 1:
            multiple_matches[folder_with_tilde] = possible_matches
        else:
            corresponding_folders[folder_with_tilde] = None
            print(f"{RED}No match found for '{folder_with_tilde}'{RESET}")  # Debug

    return corresponding_folders, multiple_matches

# Function to get movie files larger than 600 MB in a folder
def get_large_movie_files(folder):
    movie_files = []
    for file in os.listdir(folder):
        if file.endswith(('.mkv', '.mp4')):
            file_path = os.path.join(folder, file)
            if os.path.getsize(file_path) > 600 * 1024 * 1024:  # size in bytes
                movie_files.append(file_path)
    return movie_files

# Refine multiple matches by matching until the first '('
def refine_multiple_matches(multiple_matches, root_dir):
    refined_matches = {}
    for folder_with_tilde, matches in multiple_matches.items():
        base_name = re.split(r'\s*\(', folder_with_tilde)[0].strip()
        possible_matches = [f for f in matches if base_name in f]
        if len(possible_matches) == 1:
            refined_matches[folder_with_tilde] = possible_matches[0]
        else:
            refined_matches[folder_with_tilde] = None
            print(f"{YELLOW}Multiple matches found for '{folder_with_tilde}' after refinement: {possible_matches}{RESET}")  # Debug
    return refined_matches

# Step 1: Delete folders with ~ if corresponding folder has movie file
folders_with_tilde = list_folders_with_tilde(root_dir)
corresponding_folders, multiple_matches = find_corresponding_folders(folders_with_tilde, root_dir)

folders_to_delete = []
for folder_with_tilde, corresponding_folder in corresponding_folders.items():
    if corresponding_folder:
        corresponding_folder_path = os.path.join(root_dir, corresponding_folder)
        large_movie_files = get_large_movie_files(corresponding_folder_path)
        if large_movie_files:
            folders_to_delete.append(folder_with_tilde)

# Print the folders that are about to be deleted and ask for confirmation
print(f"{BOLD}The following folders are about to be deleted (corresponding folder has a movie file):{RESET}")
for folder in folders_to_delete:
    print(f"{RED}{folder}{RESET}")

confirmation = input(f"{BOLD}Do you want to proceed with deletion? (Y/N): {RESET}")

if confirmation.lower() == 'y':
    for folder_with_tilde in folders_to_delete:
        folder_with_tilde_path = os.path.join(root_dir, folder_with_tilde)
        shutil.rmtree(folder_with_tilde_path)
        print(f"{GREEN}Deleted folder: {folder_with_tilde_path}{RESET}")
else:
    print(f"{YELLOW}Deletion aborted.{RESET}")

# Re-scan the directory for the next step
folders_with_tilde = list_folders_with_tilde(root_dir)
corresponding_folders, multiple_matches = find_corresponding_folders(folders_with_tilde, root_dir)

# Refine multiple matches
refined_multiple_matches = refine_multiple_matches(multiple_matches, root_dir)
corresponding_folders.update(refined_multiple_matches)

# Step 2: Move movie files and delete folders with ~ if corresponding folder does not have a movie file
folders_to_move_and_delete = []
for folder_with_tilde, corresponding_folder in corresponding_folders.items():
    if corresponding_folder:
        folder_with_tilde_path = os.path.join(root_dir, folder_with_tilde)
        corresponding_folder_path = os.path.join(root_dir, corresponding_folder)
        
        large_movie_files_with_tilde = get_large_movie_files(folder_with_tilde_path)
        large_movie_files_corresponding = get_large_movie_files(corresponding_folder_path)
        
        if large_movie_files_with_tilde and not large_movie_files_corresponding:
            folders_to_move_and_delete.append((folder_with_tilde, corresponding_folder, large_movie_files_with_tilde))

# Print the folders that are about to be moved and deleted and ask for confirmation
print(f"{BOLD}The following folders are about to have their movie files moved and then be deleted (corresponding folder does not have a movie file):{RESET}")
for folder_with_tilde, corresponding_folder, movie_files in folders_to_move_and_delete:
    print(f"{RED}{folder_with_tilde} -> {corresponding_folder}{RESET}")
    for movie_file in movie_files:
        print(f"  {BLUE}Movie file: {movie_file}{RESET}")

confirmation = input(f"{BOLD}Do you want to proceed with moving files and deletion? (Y/N): {RESET}")

if confirmation.lower() == 'y':
    for folder_with_tilde, corresponding_folder, movie_files in folders_to_move_and_delete:
        corresponding_folder_path = os.path.join(root_dir, corresponding_folder)
        for movie_file in movie_files:
            shutil.move(movie_file, corresponding_folder_path)
            print(f"{GREEN}Moved movie file: {movie_file} -> {corresponding_folder_path}{RESET}")
        folder_with_tilde_path = os.path.join(root_dir, folder_with_tilde)
        shutil.rmtree(folder_with_tilde_path)
        print(f"{GREEN}Deleted folder: {folder_with_tilde_path}{RESET}")
else:
    print(f"{YELLOW}Moving files and deletion aborted.{RESET}")

# Re-scan the directory for the next step
folders_with_tilde = list_folders_with_tilde(root_dir)
corresponding_folders, multiple_matches = find_corresponding_folders(folders_with_tilde, root_dir)

# Step 3: Delete folders with ~ if both folders have movie files
folders_to_delete = []
for folder_with_tilde, corresponding_folder in corresponding_folders.items():
    if corresponding_folder:
        folder_with_tilde_path = os.path.join(root_dir, folder_with_tilde)
        corresponding_folder_path = os.path.join(root_dir, corresponding_folder)
        
        large_movie_files_with_tilde = get_large_movie_files(folder_with_tilde_path)
        large_movie_files_corresponding = get_large_movie_files(corresponding_folder_path)
        
        if large_movie_files_with_tilde and large_movie_files_corresponding:
            print(f"{BLUE}Both folders have large movie files: {folder_with_tilde} and {corresponding_folder}{RESET}")  # Debug
            folders_to_delete.append(folder_with_tilde)

# Print the folders that are about to be deleted and ask for confirmation
print(f"{BOLD}The following folders are about to be deleted (both folders have movie files):{RESET}")
for folder in folders_to_delete:
    print(f"{RED}{folder}{RESET}")

confirmation = input(f"{BOLD}Do you want to proceed with deletion? (Y/N): {RESET}")

if confirmation.lower() == 'y':
    for folder_with_tilde in folders_to_delete:
        folder_with_tilde_path = os.path.join(root_dir, folder_with_tilde)
        shutil.rmtree(folder_with_tilde_path)
        print(f"{GREEN}Deleted folder: {folder_with_tilde_path}{RESET}")
else:
    print(f"{YELLOW}Deletion aborted.{RESET}")

# Print the final results
print(f"\n{BOLD}Remaining folders with '~' in their name:{RESET}")
for folder_with_tilde in os.listdir(root_dir):
    if os.path.isdir(os.path.join(root_dir, folder_with_tilde)) and '~' in folder_with_tilde:
        print(f"{RED}{folder_with_tilde}{RESET}")

# Print the folders that have multiple matches and ask for further action
print(f"\n{BOLD}Folders with multiple corresponding matches:{RESET}")
for folder_with_tilde, matches in multiple_matches.items():
    print(f"{YELLOW}{folder_with_tilde}: {matches}{RESET}")
