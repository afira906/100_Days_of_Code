import tkinter as tk
from tkinter import filedialog, messagebox, colorchooser
from PIL import Image, ImageTk, ImageDraw, ImageFont


# Global variables to store images
original_image = None
watermarked_image = None


# ---------------------------- Upload Image ------------------------------- #
def upload_image():
    global original_image

    """Open file dialog to select and load an image"""

    file_path = filedialog.askopenfilename(title="Select an Image:", filetypes=[("Image files","*.png;*.jpg;*.jpeg;*.bmp;*.gif;*.tiff")])
    if file_path:
        original_image = Image.open(file_path)
        original_image.thumbnail((500, 500), Image.Resampling.LANCZOS)
        tk_image = ImageTk.PhotoImage(original_image)

        # Update Preview
        preview_label.config(image=tk_image, text="")
        preview_label.image = tk_image


# ---------------------------- Color Function ------------------------------- #
def choose_color():
    color = colorchooser.askcolor(color=color_entry.get())
    if color[1]:
        color_entry.delete(0, tk.END)
        color_entry.insert(0, color[1])
        color_preview.config(bg=color[1])


# ---------------------------- Apply WaterMark ------------------------------- #
def apply_watermark():
    global original_image, watermarked_image

    if original_image is None:
        messagebox.showwarning("Warning", "Please upload an image first!")
        return

    """Apply watermark to the image"""
    watermarked_image = original_image.copy()
    draw = ImageDraw.Draw(watermarked_image, 'RGBA')

    watermark_text = text_entry.get()
    font_size = float(font_var.get())
    position_selection = position_var.get()
    text_color = color_entry.get()
    opacity_value = int(opacity_spinbox.get())
    alpha = int(255 * opacity_value / 100)

    # Convert hex color to RGB
    hex_color = text_color.lstrip("#")
    rgb_color = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

    rgba = rgb_color + (alpha,)

    # Load font
    font = ImageFont.truetype("arial.ttf", font_size)

    # Calculate text dimensions
    text_bbox = draw.textbbox((0, 0), watermark_text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]

    if position_selection == "top-right":
        position = (watermarked_image.width - text_width - 20, 20)
    elif position_selection == "bottom-right":
        position = (watermarked_image.width - text_width - 20, watermarked_image.height - text_height - 20)
    elif position_selection == "top-left":
        position = (20, 20)
    elif position_selection == "bottom-left":
        position = (20, watermarked_image.height - text_height - 20)
    else:
        position = ((watermarked_image.width - text_width) // 2,
                    (watermarked_image.height - text_height) // 2)

    # Draw watermark
    draw.text(position, watermark_text, fill=rgba, font=font)

    # Update preview
    tk_image = ImageTk.PhotoImage(watermarked_image)
    preview_label.config(image=tk_image)
    preview_label.image = tk_image

# ---------------------------- Save Image ------------------------------- #
def save_image():
    global watermarked_image

    if watermarked_image is None:
        messagebox.showwarning("Warning", "Please apply watermark first!")
        return

    save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")])
    if save_path:
        watermarked_image.save(save_path)
        messagebox.showinfo("Success", "Image Saved Successfully!")


# ---------------------------- UI Setup ------------------------------- #
window = tk.Tk()
window.title("Image WaterMarking App")
window.geometry("1180x650")
window.config(padx=50, pady=50, bg="#f0f2f5")

# Control frame
control_frame = tk.Frame(window, width=300, padx=20, pady=20, bg="#e8f4f8", relief=tk.RAISED, borderwidth=1)
control_frame.pack(side=tk.LEFT, fill=tk.Y)
control_frame.pack_propagate(False)  # Prevent frame from shrinking

# Preview frame
preview_frame = tk.Frame(window, width=620, padx=20, pady=20, bg="#f8f9fa", relief=tk.SUNKEN, borderwidth=1)
preview_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

# Header
label = tk.Label(control_frame, text="Add WaterMark text to your Image", font=("Arial", 14, "bold"), bg="#e8f4f8", fg="#2c3e50")
label.grid(row=0, column=0, columnspan=2, pady=(0, 20), sticky="w")

# Upload button
upload_button = tk.Button(control_frame, text="Upload Image", font=("Arial", 11, "bold"), bg="#3498db", fg="white", width=20, height=2, command=upload_image)
upload_button.grid(row=1, column=0, columnspan=2, pady=15, sticky="ew")

# Watermark Text
text_label = tk.Label(control_frame, text="Watermark Text:", font=("Arial", 11, "bold"), bg="#e8f4f8", fg="#2c3e50")
text_label.grid(row=2, column=0, sticky="w", pady=(10, 5))

text_entry = tk.Entry(control_frame, width=25, font=("Arial", 10), bg="white", relief=tk.SUNKEN, borderwidth=1)
text_entry.grid(row=3, column=0, columnspan=2, sticky="ew", pady=(0, 15))
text_entry.insert(0, "Your Watermark")

# Font Size
font_label = tk.Label(control_frame, text="Font Size:", font=("Arial", 11, "bold"), bg="#e8f4f8", fg="#2c3e50")
font_label.grid(row=4, column=0, sticky="w", pady=(5, 5))

font_var = tk.StringVar(value="24")
font_sizes = ["12", "14", "16", "18", "20", "22", "24", "28", "32", "36", "40", "48", "56", "64", "72"]
font_dropdown = tk.OptionMenu(control_frame, font_var, *font_sizes)
font_dropdown.config(width=12, font=("Arial", 10), bg="white", relief=tk.RAISED)
font_dropdown.grid(row=4, column=1, padx=(10, 0), pady=(5, 5), sticky="w")

# Color
color_label = tk.Label(control_frame, text="Color (Hex):", font=("Arial", 11, "bold"), bg="#e8f4f8", fg="#2c3e50")
color_label.grid(row=5, column=0, sticky="w", pady=(15, 5))

color_entry = tk.Entry(control_frame, width=8, font=("Arial", 10), justify=tk.CENTER, bg="white", relief=tk.SUNKEN, borderwidth=1)
color_entry.grid(row=5, column=1, padx=(15, 0), pady=(15, 5), sticky="w")
color_entry.insert(0, "#000000")

# Color preview
color_preview = tk.Label(control_frame, width=3, height=1, bg="#000000", relief=tk.SUNKEN, borderwidth=1)
color_preview.grid(row=5, column=1, padx=(80, 0), pady=(15, 5), sticky="w")
color_preview.bind("<Button-1>", lambda e: choose_color())

# Opacity
opacity_label = tk.Label(control_frame, text="Opacity(%):", font=("Arial", 11, "bold"), bg="#e8f4f8", fg="#2c3e50")
opacity_label.grid(row=6, column=0, sticky="w", pady=(15, 5))

opacity_spinbox = tk.Spinbox(control_frame, from_=0, to=100, increment=5, width=12, font=("Arial", 10), justify=tk.CENTER, bg="white", relief=tk.SUNKEN, borderwidth=1)
opacity_spinbox.grid(row=6, column=1, padx=(15, 0), pady=(15, 5), sticky="w")
opacity_spinbox.delete(0, tk.END)
opacity_spinbox.insert(0, "100")

# Font Size
position_label = tk.Label(control_frame, text="Position", font=("Arial", 11, "bold"), bg="#e8f4f8", fg="#2c3e50")
position_label.grid(row=7, column=0, sticky="w", pady=(15, 5))

position_var = tk.StringVar(value="bottom-right")
positions = ["top-right", "bottom-right", "top-left", "bottom-left", "centre"]
position_dropdown = tk.OptionMenu(control_frame, position_var, *positions)
position_dropdown.config(width=12, font=("Arial", 10), bg="white", relief=tk.RAISED)
position_dropdown.grid(row=7, column=1, padx=(10, 0), pady=(5, 5), sticky="w")

# Apply button
apply_button = tk.Button(control_frame, text="Apply Watermark", font=("Arial", 12, "bold"), bg="#27ae60", fg="white", width=20, height=2, command=apply_watermark)
apply_button.grid(row=8, column=0, pady=(15, 5), sticky="ew")

# Save button
save_button = tk.Button(control_frame, text="Save Image", font=("Arial", 12, "bold"), bg="#27ae60", fg="white", width=20, height=2, command=save_image)
save_button.grid(row=8, column=1, pady=(15, 5), sticky="ew")

# Configure grid weights for proper alignment
control_frame.columnconfigure(0, weight=1)
control_frame.columnconfigure(1, weight=1)

# Preview area label
preview_label = tk.Label(preview_frame, text="Image Preview Area", font=("Arial", 16, "bold"), bg="#f8f9fa", fg="#6c757d")
preview_label.pack(expand=True)


window.mainloop()
