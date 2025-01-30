#!/usr/bin/env python3
import os

###############################################################################
# USER-EDITABLE SETTINGS
###############################################################################
# List of folder names to look for under the root path:
FoldersToMerge = ["Simulation", "View", "QuantumUser"]
# Extensions to gather from those folders. The FIRST in this list is what
# the final merged file will be named with, e.g. "Simulation.cs"
Extensions     = ["cs", "qtn"]

# You can hardcode a default root path here or prompt the user:
# e.g. root_path = "/path/to/your/project"
# or read from input:
# root_path = input("Enter the root folder to search in: ")
###############################################################################


def gather_all_files_in_subtree(folder_path, allowed_exts):
    """
    Recursively walk through 'folder_path' and find all files whose
    extension is in allowed_exts. Return a list of full file paths.
    """
    matched_files = []
    for dirpath, dirnames, filenames in os.walk(folder_path):
        for filename in filenames:
            _, ext = os.path.splitext(filename)
            if ext.lstrip('.') in allowed_exts:
                full_path = os.path.join(dirpath, filename)
                matched_files.append(full_path)
    return matched_files


def merge_files_into_single_output(files_list, output_path):
    """
    Read the content of all files in 'files_list' and write them
    concatenated into 'output_path'.
    """
    with open(output_path, 'w', encoding='utf-8') as outfile:
        for fpath in files_list:
            # Write a small header for clarity (optional):
            outfile.write(f"\n// BEGIN FILE: {os.path.basename(fpath)}\n")
            with open(fpath, 'r', encoding='utf-8') as infile:
                outfile.write(infile.read())
            outfile.write(f"\n// END FILE: {os.path.basename(fpath)}\n")


def main():
    # Prompt user for root folder (or hardcode this if desired)
    root_path = input("Enter the root folder to search in: ").strip()
    if not os.path.isdir(root_path):
        print(f"The path '{root_path}' is not a valid directory.")
        return
    
    # Build a dictionary to keep track of file paths for each folder key.
    # For instance: merges["Simulation"] = [list_of_file_paths, ...]
    merges = {folder: [] for folder in FoldersToMerge}
    
    # We'll do a manual walk of the root folder to find any directory
    # whose basename is in FoldersToMerge. Once found, gather all files
    # recursively in that subtree, then skip further recursion below that folder.
    for dirpath, dirnames, filenames in os.walk(root_path):
        basename = os.path.basename(dirpath)
        
        # If this folder is in our FoldersToMerge list, gather files
        # from its entire subtree:
        if basename in merges:
            all_files = gather_all_files_in_subtree(dirpath, Extensions)
            merges[basename].extend(all_files)
            
            # Now remove this directory from dirnames so we don't keep
            # recursing further in the main loop.
            # This stops the main .walk() from descending into the subtree again.
            dirnames.clear()

    # Determine the output directory under the user's home folder:
    home_dir = os.path.expanduser("~")
    output_dir = os.path.join(home_dir, "PyCodeMergeOutput")
    os.makedirs(output_dir, exist_ok=True)

    # The first extension in Extensions will be used for the output files:
    output_extension = Extensions[0]

    # For each folder key in merges, if we collected any files, merge them:
    for folder_name, files_list in merges.items():
        if not files_list:
            continue  # skip if no files found in that folder subtree

        output_filename = f"{folder_name}.{output_extension}"
        output_path = os.path.join(output_dir, output_filename)

        # Merge and write out:
        print(f"Merging {len(files_list)} files into {output_path} ...")
        merge_files_into_single_output(files_list, output_path)

    print("Merging complete!")
    print(f"Check your files in: {output_dir}")


if __name__ == "__main__":
    main()
