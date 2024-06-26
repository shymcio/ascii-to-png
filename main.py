import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
import numpy as np

ASCII_CHARS = "@%#*+=-:. "


def image_to_ascii(image_path, output_path, width=100):
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
    image_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
    if image_path:
        output_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if output_path:
            image_to_ascii(image_path, output_path)
            messagebox.showinfo("Success", f"ASCII art saved to {output_path}")


def convert_ascii_to_image():
    ascii_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if ascii_path:
        output_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
        if output_path:
            ascii_to_image(ascii_path, output_path)
            messagebox.showinfo("Success", f"Image saved to {output_path}")


def main():
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
