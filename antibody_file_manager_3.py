import pandas as pd
import os
import subprocess
import platform

directory = os.getcwd()  # Working directory
print("Working Directory:", directory)

def process_files(directory):
    staging_path = os.path.join(directory, "Staging")
    for filename in os.listdir(staging_path):
        if filename.lower().endswith((".csv", ".xlsx")):  # Accept both CSV and XLSX files
            print(f"Processing: {filename}")

            file_path = os.path.join(staging_path, filename)
            try:
                if filename.lower().endswith(".csv"):
                    antibody_ids = pd.read_csv(file_path, usecols=['antibody_id'])['antibody_id']
                elif filename.lower().endswith(".xlsx"):
                    antibody_ids = pd.read_excel(file_path, usecols=['antibody_id'])['antibody_id']

                antibody_ids = antibody_ids.dropna().tolist()  # Drop NaN values and convert to list
                print(antibody_ids)
                return antibody_ids, file_path, filename
            except Exception as e:
                print(f"Error reading file {file_path}: {e}")
                return None, None, None


def create_directories_from_list(antibody_ids, directory):
    for antibody_id in antibody_ids:
        directory_path = os.path.join(directory, str(antibody_id))
        #print(directory_path)
        if not os.path.exists(directory_path):
            try:
                os.makedirs(directory_path)
                print(f"Created directory: {directory_path}")
            except subprocess.CalledProcessError as e:
                print(f"Error creating directory {directory_path}: {e}")
        else:
            print(f"Directory already exists: {directory_path}")



def experiment_directory(directory):
    directory_path = os.path.join(directory, "Experiment_Directory")
    if not os.path.exists(directory_path):
        try:
            os.makedirs(directory_path)
            print(f"Created directory: {directory_path}")
        except subprocess.CalledProcessError as e:
            print(f"Error creating directory {directory_path}: {e}")
    else:
        print(f"Directory already exists: {directory_path}")
    return(directory_path)

def copy_csv_to_directory(csv_path, experiment_directory):

    # Check OS
    system = platform.system()

    try:
        if system == "Windows":
            subprocess.run(['copy', csv_path, experiment_directory], check=True, shell=True)
        else:
            subprocess.run(['cp', csv_path, experiment_directory], check=True)

        print(f"Copied {csv_path} to {experiment_directory}")
    except subprocess.CalledProcessError as e:
        print(f"Error copying {csv_path} to {experiment_directory}: {e}")


################


def link_antibodys(antibody_ids, directory, filename, experiment_directory):
    hard_link_path = os.path.join(directory, experiment_directory, filename)
    system = platform.system()

    for antibody_id in antibody_ids:
        antibody_link_path = os.path.join(directory, str(antibody_id), filename)
        #print("hard link path is:", hard_link_path)
        #print("file link path is:", antibody_link_path)

        try:
            # Ensure target file exists
            if not os.path.isfile(hard_link_path):
                raise FileNotFoundError(f"Target file does not exist: {hard_link_path}")

            # Skip if link already exists
            if os.path.exists(antibody_link_path):
                print(f"Link already exists at {antibody_link_path}, skipping.")
                continue

            if system == "Windows":
                cmd = f'mklink /h "{antibody_link_path}" "{hard_link_path}"'
                print("Running command:", cmd)
                subprocess.run(cmd, shell=True, check=True)
            else:
                subprocess.run(['ln', hard_link_path, antibody_link_path], check=True)

            print(f"Created hard link: {antibody_link_path}")

        except Exception as e:
            print(f"Error creating hard link {antibody_link_path}: {e}")
            return None
################




        
            
antibody_ids, csv_path, filename = process_files(directory)
create_directories_from_list(antibody_ids, directory)
experiment_directory = experiment_directory(directory)
copy_csv_to_directory(csv_path, experiment_directory)
link_antibodys(antibody_ids, directory, filename, experiment_directory)
