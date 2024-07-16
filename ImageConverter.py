import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image

def convert_image():
    # Get the file path from the user
    file_path = filedialog.askopenfilename()
    if not file_path:
        return

    # Get the format choice from the user
    format_choice = format_var.get()
    if format_choice == 'PNG':
        output_format = 'PNG'
        extension = 'png'
    elif format_choice == 'JPG':
        output_format = 'JPEG'
        extension = 'jpg'
    elif format_choice == 'WEBP':
        output_format = 'WEBP'
        extension = 'webp'
    else:
        messagebox.showerror("Error", "Unsupported format selected.")
        return

    # Set the output path
    output_path = filedialog.asksaveasfilename(defaultextension=f".{extension}")

    if not output_path:
        return

    try:
        # Open the original image
        with Image.open(file_path) as img:
            # Convert and save the image
            img.save(output_path, format=output_format)
        messagebox.showinfo("Success", f"Image successfully converted to {output_format} and saved as {output_path}")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Create the main window
root = tk.Tk()
root.title("Image Converter")

# Set up the layout
frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

format_var = tk.StringVar(value="PNG")  # Default format
formats = ['PNG', 'JPG', 'WEBP']
tk.Label(frame, text="Select output format:").pack()
for fmt in formats:
    tk.Radiobutton(frame, text=fmt, value=fmt, variable=format_var).pack(anchor='w')

convert_button = tk.Button(frame, text="Convert Image", command=convert_image)
convert_button.pack(pady=20)

root.mainloop()
