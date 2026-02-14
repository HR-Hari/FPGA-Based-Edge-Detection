import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog

def convert_hex_to_image():
    # Hide the background tkinter window
    root = tk.Tk()
    root.withdraw()

    # Open the file selection dialog
    file_path = filedialog.askopenfilename(
        title="Select the Verilog Output Hex File",
        filetypes=[("Hex Files", "*.hex *.txt")]
    )

    if not file_path:
        print("No file was selected. Exiting.")
        return

    # Prompt for dimensions to reconstruct the 2D image
    try:
        width = int(input("Enter the image WIDTH (e.g., 64): "))
        height = int(input("Enter the image HEIGHT (e.g., 64): "))
    except ValueError:
        print("Invalid dimensions entered. Please enter integer numbers.")
        return

    pixels = []
    with open(file_path, "r") as f:
        for line in f:
            line = line.strip()
            # Ignore empty lines or 'x'/'z' undefined simulation states
            if line and 'x' not in line.lower() and 'z' not in line.lower():
                pixels.append(int(line, 16))

    expected_pixels = width * height
    actual_pixels = len(pixels)

    if actual_pixels != expected_pixels:
        print(f"Warning: Expected {expected_pixels} pixels based on dimensions, but found {actual_pixels}.")
        # Pad or trim the list to prevent reshaping crashes if the simulation stopped early
        if actual_pixels > expected_pixels:
            pixels = pixels[:expected_pixels]
        else:
            pixels.extend([0] * (expected_pixels - actual_pixels))

    # Convert the 1D list into a 2D NumPy array
    img_array = np.array(pixels, dtype=np.uint8).reshape((height, width))

    # Save the reconstructed image
    output_filename = "hardware_output.jpg"
    cv2.imwrite(output_filename, img_array)
    print(f"Image successfully reconstructed and saved as: {output_filename}")

if __name__ == "__main__":
    convert_hex_to_image()