from PIL import Image
import os

# img = Image.open("cleft_images/p.jpg")

# print(img.size)

# Input and output directories
input_dir = "new_folder"
output_dir = "resized_data2"

# List all images in the input directory
cleft_img = os.listdir(input_dir)

for image in cleft_img:
    img_path = os.path.join(input_dir, image)
    img = Image.open(img_path)

    # Convert to RGB mode if the image is in RGBA mode
    if img.mode == "RGBA":
        img = img.convert("RGB")

    # Resize the image
    resized_img = img.resize((256, 256))

    # Save the resized image
    output_path = os.path.join(output_dir, image)
    resized_img.save(output_path)

print("Resize done!!!")
