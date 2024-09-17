import os
from PIL import Image

# Specify the directory containing the files
directory = "./new_folder"

# List all files in the directory
files = os.listdir(directory)
# # print(files)
# img = Image.open(os.path.join(directory, "P_0819.jpg"))
# print(img.size)
# img = img.resize((256, 256))
# print(img.size)
# img.save(os.path.join("kath_resized_images/folder_8", "P_0831.jpg"))
# # for filename in files:
#     img = Image.open(os.path.join(directory, filename))
#     print(filename, img.size)

# Loop through the files and rename them
for index, filename in enumerate(files):
    # Define the new name, you can customize this part
    new_index = 1001 + index
    new_name = f"P_{new_index}.jpg"

    # Construct full file path
    old_file = os.path.join(directory, filename)
    new_file = os.path.join(directory, new_name)

    # Rename the file
    os.rename(old_file, new_file)
    print(f"Renamed: {old_file} to {new_file}")

print("Renaming complete.")
