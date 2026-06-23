import os
import shutil

source_folder = "sign_data/train"

genuine_folder = "dataset/genuine"
forged_folder = "dataset/forged"

os.makedirs(genuine_folder, exist_ok=True)
os.makedirs(forged_folder, exist_ok=True)

for folder in os.listdir(source_folder):

    folder_path = os.path.join(source_folder, folder)

    if not os.path.isdir(folder_path):
        continue

    for image in os.listdir(folder_path):

        image_path = os.path.join(folder_path, image)

        if "_forg" in folder.lower():
            shutil.copy(image_path, forged_folder)
        else:
            shutil.copy(image_path, genuine_folder)

print("Dataset organized successfully!")