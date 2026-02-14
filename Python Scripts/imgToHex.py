import cv2
import tkinter as tk
from tkinter import filedialog

def convert_image_to_hex():
    # Hide the background tkinter window
    root = tk.Tk()
    root.withdraw()

    # Open the file selection dialog
    file_path = filedialog.askopenfilename(
        title="Select an Image to Convert",
        filetypes=[("Image Files", "*.jpg *.jpeg *.png *.bmp")]
    )

    if not file_path:
        print("No file was selected. Exiting.")
        return

    # Load the image in grayscale (8-bit)
    img = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        print("Error: Could not read the image file.")
        return

    # Grab dimensions to remind you what to put in the Verilog testbench
    height, width = img.shape
    print(f"Loaded image successfully. Dimensions: {width} x {height}")
    print(f"** IMPORTANT: Set WIDTH = {width} and HEIGHT = {height} in your Verilog testbench! **")

    # Save to hex format
    output_filename = "input_image.hex"
    with open(output_filename, "w") as f:
        for row in img:
            for pixel in row:
                f.write(f"{pixel:02x}\n")
                
    print(f"Hex file successfully saved as: {output_filename}")

if __name__ == "__main__":
    convert_image_to_hex()