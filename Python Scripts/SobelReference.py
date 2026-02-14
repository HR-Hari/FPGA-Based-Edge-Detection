import cv2
import numpy as np


def generate_sobel_reference(input_image_path, output_image_path):
    # 1. Load the image in grayscale (easier for hardware logic)
    img = cv2.imread(input_image_path, cv2.IMREAD_GRAYSCALE)
    
    if img is None:
        print("Error: Could not load image.")
        return

    # 2. Define the exact 3x3 kernels you will build in Verilog
    Kx = np.array([[-1,  0,  1], 
                   [-2,  0,  2], 
                   [-1,  0,  1]], dtype=np.float32)
                   
    Ky = np.array([[-1, -2, -1], 
                   [ 0,  0,  0], 
                   [ 1,  2,  1]], dtype=np.float32)

    # 3. Apply the convolution (sliding the window)
    # We use cv2.CV_16S to keep negative numbers before taking the absolute value
    Gx = cv2.filter2D(img, cv2.CV_16S, Kx)
    Gy = cv2.filter2D(img, cv2.CV_16S, Ky)

    # 4. Take the absolute value of the gradients
    abs_Gx = np.absolute(Gx)
    abs_Gy = np.absolute(Gy)

    # 5. Combine them into the final edge magnitude
    # HARDWARE TIP: The exact math is G = sqrt(Gx^2 + Gy^2). 
    # However, square roots are very resource-heavy on an FPGA. 
    # Hardware designs typically use the approximation: G = |Gx| + |Gy|. 
    # We use that approximation here so your reference matches your future Verilog output.
    edges = abs_Gx + abs_Gy
    
    # Clip values to stay within the valid 0-255 range for an 8-bit image
    edges = np.clip(edges, 0, 255).astype(np.uint8)

    # 6. Save the golden reference
    cv2.imwrite(output_image_path, edges)
    print(f"Reference image saved to {output_image_path}")

# Run the function
# Replace 'test_image.jpg' with a small, simple image (e.g., 64x64 or 128x128 pixels)
generate_sobel_reference('Wallpaper_imresizer.jpg', 'golden_reference.jpg')