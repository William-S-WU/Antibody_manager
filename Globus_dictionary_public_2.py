import os
import urllib.parse
import pandas as pd

directory = os.getcwd()  # Working directory
print("Working Directory:", directory)


SHARED_COLLECTION_ID =  # Replace with your actual shared collection ID
REMOTE_BASE_PATH =   # Path on the Globus endpoint

BASE_URL = "https://app.globus.org/file-manager"

# search folders in working directory
folders = [f for f in os.listdir(directory) if os.path.isdir(os.path.join(directory, f))]
data = []

# generate links
print("Globus Sharing Links:")
for folder in folders:
    remote_path = f"{REMOTE_BASE_PATH}/{folder}/"
    encoded_path = urllib.parse.quote(remote_path)
    link = f"{BASE_URL}?origin_id={SHARED_COLLECTION_ID}&origin_path={encoded_path}"
    print(f"{folder}: {link}")
    data.append({"Folder": folder, "Globus Link": link})

# return links as csv
df = pd.DataFrame(data)
csv_filename = "globus_links.csv"
df.to_csv(csv_filename, index=False)

print(f"\n Links saved to {csv_filename}")

