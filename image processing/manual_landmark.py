import tkinter as tk
from PIL import Image, ImageTk
import cv2
import numpy as np
import math
import os
from tkinter import filedialog
import csv

coordinates = []
measurements = []

landmark_description = {
    "first_landmark": "Base of alveolus(left)",
    "second_landmark": "Base of alveolus(right)",
    "third_landmark": "hard-soft palate junction(left)",
    "forth_landmark": "hard-soft palate junction(right)",
    "fifth_landmark": "anterior border of the cleft",
    "sixth_landmark": "Tip of uvula",
    "seventh_landmark": "central midalveolus",
    "eight_landmark": "tip of uvula",
}


def process_images_in_folder():
    """creates an interactive dialogue box for selecting folders containing images for display"""
    folder_path = filedialog.askdirectory(
        title="Select Folder of Images"
    )  # Folder path

    # List to store processed images
    processed_images = []

    # Iterating through all files in the directory
    for filename in os.listdir(folder_path):
        if filename.endswith((".png", ".jpg", ".jpeg")):
            file_path = os.path.join(folder_path, filename)

            # Open an image file
            image = Image.open(file_path)

            # Convert the image to a NumPy array
            cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

            # Convert to ImageTk format for displaying
            tk_image = ImageTk.PhotoImage(image=image)

            # Store processed images and their corresponding labels
            processed_images.append((image, cv_image, tk_image, filename))

    return processed_images


def get_pixel_location(event):
    """Gets the coordinates of a pixel location, stores it in a list and displays it on an image."""
    global cv_image, tk_image
    x, y = event.x, event.y
    coordinates.append((x, y))
    print(f"Clicked at: ({x}, {y})")
    color = (255, 0, 0)  # blue color
    if 0 <= x < cv_image.shape[1] and 0 <= y < cv_image.shape[0]:
        cv2.circle(cv_image, (x, y), 2, color, -1)

    # Convert the image to RGB
    image_rgb = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)

    # Convert to PIL image and to ImageTk format for display
    pil_image = Image.fromarray(image_rgb)
    tk_image = ImageTk.PhotoImage(image=pil_image)

    # Update the label to display the modified image
    label.config(image=tk_image)
    label.image = tk_image  # reference to avoid garbage collection


def draw_lines_between_points():
    """Calculates the distance between two keypoints/landmarks and displays the distance using lines to connect the keypoints"""
    global cv_image, coordinates
    measurements.clear()
    for i in range(0, len(coordinates) - 1, 2):
        point1 = coordinates[i]
        point2 = coordinates[i + 1]
        cv2.line(cv_image, point1, point2, (0, 255, 0), 1)
        # Calculate the Euclidean distance
        distance = round(
            math.sqrt((point2[0] - point1[0]) ** 2 + (point2[1] - point1[1]) ** 2), 4
        )
        measurements.append(distance)
    print(measurements)

    image_rgb = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)

    # Convert to PIL image and then to ImageTk format
    pil_image = Image.fromarray(image_rgb)
    tk_image = ImageTk.PhotoImage(image=pil_image)

    # Update the label to display the modified image
    label.config(image=tk_image)
    label.image = tk_image

    update_measurement_label()


def update_measurement_label():
    """Updates the status bar with the measurements"""
    score_label.config(text=f"Measurements: {measurements}")


def show_image(index, processed_images):
    """
    Displays the images in the selected folder and
    shows the measurements at the status bar of the windows when the lines are drawn.
    Coordinates of and distances are stored in seperate csv files when a window is closed and
    measurements are cleared once a new image appears.
    """
    global image, cv_image, tk_image, coordinates, measurements
    if index >= len(processed_images):
        root.quit()
        return
    # Reset coordinates and measurements for the new image
    coordinates = []
    measurements = []

    image, cv_image, tk_image, filename = processed_images[index]

    label.config(image=tk_image)
    label.image = tk_image  #  reference to avoid garbage collection
    label.pack(pady=20)

    button.config(
        text=f"Show image {filename} with lines", command=draw_lines_between_points
    )
    button.pack(pady=20)

    update_measurement_label()

    def on_close():
        """Appends the keypoints/coordinates and measurements to seperate csv files when a window is closed"""
        # Append coordinates to CSV file
        flat_coordinates = [item for coord in coordinates for item in coord]
        with open("landmarks.csv", "a", newline="") as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow([filename] + flat_coordinates)
        print(f"New coordinates has been appended to csv file")

        # Append measurements to another CSV file
        with open("measurements.csv", "a", newline="") as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow([filename] + measurements)
        print(f"New measurements have been appended to csv file")

        label.pack_forget()
        button.pack_forget()
        show_image(index + 1, processed_images)

    root.protocol("WM_DELETE_WINDOW", on_close)


# Initialize Tkinter window
root = tk.Tk()
root.title("Keypoints Annotation Application")

# Create a label to display the image
label = tk.Label(root)
label.pack(pady=20)

# Bind the click event to the image label
label.bind("<Button-1>", get_pixel_location)

# Create a button to display the image with points and lines
button = tk.Button(root, text="Show Image with lines")
button.pack(pady=20)


# Create a label for the status bar
score_label = tk.Label(
    root, text=f"Measurements: {measurements}", bd=1, relief=tk.SUNKEN, anchor=tk.W
)
score_label.pack(side=tk.BOTTOM, fill=tk.X)

# Load and process images in the selected folder
processed_images = process_images_in_folder()

# Start displaying images
show_image(0, processed_images)

# Run the Tkinter application
root.mainloop()
