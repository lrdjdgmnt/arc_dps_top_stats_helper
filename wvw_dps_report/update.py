import requests
import os
import shutil
import zipfile

def fetch_latest_release(user, repo):
    #Fetch the latest release from GitHub repository using GitHub API.
    url = f"https://api.github.com/repos/{user}/{repo}/releases/latest"
    response = requests.get(url)
    response.raise_for_status()  # Raises stored HTTPError, if one occurred.
    return response.json()

def download_archive(download_url, file_name):
    # Download the archive from the constructed URL.
    response = requests.get(download_url)
    with open(file_name, 'wb') as file:
        file.write(response.content)
    print(f"Downloaded {file_name}")
    return file_name

def extract_files(zip_path, extract_to):
    #Extract files from a zip archive to a specified directory, after clearing the directory.
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        # Extract each item from the zip file
        for member in zip_ref.infolist():
            # Build the path for extraction
            target_path = os.path.join(extract_to, member.filename.split('/', 1)[-1])
            # Ensure target directory exists
            os.makedirs(os.path.dirname(target_path), exist_ok=True)
            # Extract each file based on its adjusted path
            if member.filename.endswith('/'):
                os.makedirs(target_path, exist_ok=True)
            else:
                with zip_ref.open(member) as source, open(target_path, 'wb') as target:
                    shutil.copyfileobj(source, target)
    print(f"Extracted files to {extract_to}")
    os.remove(zip_path)  # Delete the zip file after extraction
    print(f"Deleted {zip_path}")

def check_and_update_version(repo_info, version_file, extract_to):
    #Check the current version against the recorded version, download if different, and extract files.
    user = repo_info['user']
    repo = repo_info['repo']
    latest_release = fetch_latest_release(user, repo)
    latest_version = latest_release['tag_name']

    # Read the last version from file
    if os.path.exists(version_file):
        with open(version_file, 'r') as file:
            last_version = file.read().strip()
    else:
        last_version = None

    # Compare versions and download if new version is found
    if last_version != latest_version:
        print(f"New version detected: {latest_version}. Preparing to download...")

        if repo == "GW2-Elite-Insights-Parser":
            download_url = f"https://github.com/{user}/{repo}/releases/download/{latest_version}/GW2EI.zip"
            zip_file = download_archive(download_url, f"GW2EI-{latest_version}.zip")
            extract_files(zip_file, extract_to)

        elif repo == "arcdps_top_stats_parser":
            download_url = f"https://github.com/{user}/{repo}/archive/refs/tags/{latest_version}.zip"
            zip_file = download_archive(download_url, f"{repo}-{latest_version}.zip")
            extract_files(zip_file, extract_to)
        
        # Update the version file
        with open(version_file, 'w') as file:
            file.write(latest_version)
        print(f"Updated version file with {latest_version}")
    else:
        print("No new version. Current version is up-to-date.")

def main():
    repos = [
        {'user': 'baaron4', 'repo': 'GW2-Elite-Insights-Parser', 'extract_to': 'parser'},
        {'user': 'Drevarr', 'repo': 'arcdps_top_stats_parser', 'extract_to': 'wvw_parser'}  # Extract directly to the current directory
    ]
    for repo_info in repos:
        version_file = f"{repo_info['repo']}_version.txt"
        check_and_update_version(repo_info, version_file, repo_info['extract_to'])

if __name__ == "__main__":
    main()
