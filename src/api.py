import zipfile
import os

import requests
from tqdm import tqdm


def request_json():
    ''' Get url to dl tisseo gtfs '''
    api_url = "https://data.toulouse-metropole.fr/api/explore/v2.1/catalog/datasets/tisseo-gtfs/records?limit=20"
    try:
        response = requests.get(api_url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Request failed {api_url}: {e}")
        return None
    except ValueError as e:
        print(f"Failed to parse JSON: {e}")
        return None


def dl_zip(url, local_filename):
    try:
        with requests.get(url, stream=True, timeout=10) as r:
            r.raise_for_status()
            total_size = int(r.headers.get('content-length', 0))

            with open(local_filename, 'wb') as f, tqdm(
                total=total_size, unit='B', unit_scale=True, desc=local_filename
            ) as pbar:
                for chunk in r.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
                        pbar.update(len(chunk))

        print(f"Download completed: {local_filename}")
        return local_filename

    except requests.RequestException as e:
        print(f"Download failed: {e}")
        return None


def unzip_data(zip_path, extract_to=None):

    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
        print(f"Extracted '{zip_path}' to '{extract_to}'")
        return extract_to
    except zipfile.BadZipFile as e:
        print(f"Failed to unzip file: {e}")
        return None



def dl_tisseo_gfts():
    ''' Download full tisseo gtfs .zip file '''

    # cree le dossier data/ si il n'existe pas
    path = "data/"
    os.makedirs(path, exist_ok=True)
    print(f"INFO: Dossier {path} crée ou existant")

    print("INFO: Requete de l'url a jour de tisseo_gtfs_zip")
    data = request_json()
    if data is None:
        print("Problem getting the json")
        exit()

    url = data["results"][0]["file"]["url"]
    name = data["results"][0]["file"]["filename"]
    print(f"Filename:{name} URL:{url}")

    print("INFO: Download du dataset")
    zip_path = f"data/{name}"
    dl_zip(url, zip_path)

    print("INFO: Decompressage du fichier zip")
    unzip_data(zip_path, zip_path.replace(".zip", '/'))


if __name__ == '__main__':
    dl_tisseo_gfts()
