import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
import numpy as np

ASCII_CHARS = "@%#*+=-:. "


def image_to_ascii(image_path, output_path, width=100):
    """
    Convert an image to ASCII art and save it to a text file.

    Parameters:
    image_path (str): Path to the input image file.
    output_path (str): Path to save the output ASCII art text file.
    width (int): Width of the output ASCII art in characters. Default is 100 characters.
    """
    image = Image.open(image_path)
    aspect_ratio = image.height / image.width
    new_height = int(aspect_ratio * width)
    image = image.resize((width, new_height))
    image = image.convert("L")

    pixels = np.array(image)
    ascii_str = ""
    for row in pixels:
        for pixel in row:
            ascii_str += ASCII_CHARS[pixel // 32]
        ascii_str += "\n"

    with open(output_path, "w") as f:
        f.write(ascii_str)


def ascii_to_image(ascii_path, output_path):
    """
    Convert ASCII art to an image and save it as a PNG file.

    Parameters:
    ascii_path (str): Path to the input ASCII art text file.
    output_path (str): Path to save the output image file.
    """
    char_to_gray = {char: i * 32 for i, char in enumerate(ASCII_CHARS)}

    with open(ascii_path, "r") as f:
        ascii_art = f.read()

    ascii_lines = ascii_art.split("\n")
    height = len(ascii_lines)
    width = max(len(line) for line in ascii_lines)
    image = Image.new("L", (width, height), "white")
    pixels = image.load()

    for y, line in enumerate(ascii_lines):
        for x, char in enumerate(line):
            if char in char_to_gray:
                pixels[x, y] = char_to_gray[char]

    image.save(output_path)


def convert_image_to_ascii():
    """
    Open a file dialog to select an image and convert it to ASCII art.
    The ASCII art is then saved to a user-specified text file.
    """
    image_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
    if image_path:
        output_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if output_path:
            image_to_ascii(image_path, output_path)
            messagebox.showinfo("Success", f"ASCII art saved to {output_path}")


def convert_ascii_to_image():
    """
    Open a file dialog to select an ASCII art text file and convert it to an image.
    The image is then saved to a user-specified PNG file.
    """
    ascii_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if ascii_path:
        output_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
        if output_path:
            ascii_to_image(ascii_path, output_path)
            messagebox.showinfo("Success", f"Image saved to {output_path}")


def main():
    """
    Create the main application window and add buttons for converting images to ASCII art and vice versa.
    """
    root = tk.Tk()
    root.title("Image to ASCII Art Converter")
    root.geometry("400x200")

    btn_image_to_ascii = tk.Button(root, text="Convert Image to ASCII Art", command=convert_image_to_ascii)
    btn_image_to_ascii.pack(pady=20)

    btn_ascii_to_image = tk.Button(root, text="Convert ASCII Art to Image", command=convert_ascii_to_image)
    btn_ascii_to_image.pack(pady=20)

    root.mainloop()


if __name__ == "__main__":
    main()
