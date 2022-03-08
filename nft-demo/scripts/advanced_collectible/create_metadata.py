from brownie import AdvancedCollectible, network
from scripts.helpful_scripts import get_breed
from metadata.sample_metadata import metadata_template
from pathlib import Path
import requests
import json


def main():
    advanced_collectible = AdvancedCollectible[-1]
    token_counter = advanced_collectible.tokenCounter()
    print(f"You have created {token_counter} collectible(s)!")
    for token_id in range(token_counter):
        breed = get_breed(advanced_collectible.tokenIdToBreed(token_id))
        metadata_filename = (
            f"./metadata/{network.show_active()}/{token_id}-{breed}.json"
        )
        collectible_metadata = metadata_template
        if Path(metadata_filename).exists():
            print(f"File {metadata_filename} already exists. Delete for overwriting")
        else:
            print(f"Creating Metadata file: {metadata_filename}")
            collectible_metadata["name"] = breed
            collectible_metadata["description"] = f"An adorable {breed} pup! WOW!"
            image_path = "./img/" + breed.lower().replace("_", "-") + ".png"

            # image_uri = None
            image_uri = upload_to_ipfs(image_path)

            collectible_metadata["image"] = image_uri
            with open(metadata_filename, "w") as file:
                json.dump(collectible_metadata, file)
            upload_to_ipfs(metadata_filename)


def upload_to_ipfs(filepath):
    with Path(filepath).open("rb") as fp:
        image_binary = fp.read()
        # print(image_binary)
        ipfs_url = "http://127.0.0.1:5001"
        endpoint = "/api/v0/add"
        response = requests.post(ipfs_url + endpoint, files={"file": image_binary})
        print(response.status_code)
        ipfs_hash = response.json()["Hash"]
        # "./img/0-PUG.png" -> "0-PUG.png"
        filename = filepath.split("/")[-1:][0]
        print(filename)
        image_uri = f"https://ipfs.io/ipfs/{ipfs_hash}?filename={filename}"
        print(image_uri)
        return image_uri


# "https://ipfs.io/ipfs/Qmd9MCGtdVz2miNumBHDbvj8bigSgTwnr4SbyH6DNnpWdt?filename=0-PUG.json"

breed_to_image_uri = {
    "PUG": "https://ipfs.io/ipfs/QmSsYRx3LpDAb1GZQm7zZ1AuHZjfbPkD6J7s9r41xu1mf8?filename=pug.png",
    "SHIBA_INU": "https://ipfs.io/ipfs/QmYx6GsYAKnNzZ9A6NvEKV9nf1VaDzJrqDR23Y8YSkebLU?filename=shiba-inu.png",
    "ST_BERNARD": "https://ipfs.io/ipfs/QmUPjADFGEKmfohdTaNcWhp7VGk26h5jXDA7v3VtTnTLcW?filename=st-bernard.png",
}
