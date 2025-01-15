import os
import tarfile
import kagglehub

def download_and_extract_lfw(dataset_name, extract_to):
    print("Downloading LFW dataset from Kaggle...")
    dataset_path = kagglehub.dataset_download(dataset_name)
    tar_file_path = os.path.join(dataset_path, "lfw-funneled.tgz")

    if not os.path.exists(tar_file_path):
        raise FileNotFoundError("lfw-funneled.tgz not found in the downloaded dataset.")

    # Extract the dataset
    if not os.path.exists(extract_to):
        print("Extracting LFW dataset...")
        with tarfile.open(tar_file_path, "r:gz") as tar:
            tar.extractall(path=extract_to)
        print(f"LFW dataset extracted to {extract_to}")
    else:
        print(f"LFW dataset already extracted at {extract_to}")

if __name__ == "__main__":
    # Kaggle dataset name and extraction folder
    kaggle_dataset = "atulanandjha/lfwpeople"
    extracted_folder = "lfw-funneled"

    # Download and extract the dataset
    download_and_extract_lfw(kaggle_dataset, extracted_folder)
