import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image
import os

def convert_images():
    file_paths = filedialog.askopenfilenames(
        title="Select images",
        filetypes=[
            ("Image files", "*.jpg *.jpeg *.png *.webp *.bmp *.gif *.tiff *.ico"),
            ("JPEG", "*.jpg *.jpeg"),
            ("PNG", "*.png"),
            ("WEBP", "*.webp"),
            ("BMP", "*.bmp"),
            ("GIF", "*.gif"),
            ("TIFF", "*.tiff"),
            ("ICO", "*.ico")
        ])
    if not file_paths:
        return

    format_choice = format_var.get()
    output_format, extension = format_settings[format_choice]

    for file_path in file_paths:
        try:
            img = Image.open(file_path)
            if img.mode != "RGBA" and img.mode != "RGB":
                img = img.convert("RGBA")

            file_dir, file_name = os.path.split(file_path)
            base_name = os.path.splitext(file_name)[0]
            output_path = os.path.join(file_dir, f"{base_name}.{extension}")

            # Ensure no overwriting by incrementing filename
            original_output_path = output_path
            counter = 1
            while os.path.exists(output_path):
                output_path = os.path.join(file_dir, f"{base_name}({counter}).{extension}")
                counter += 1

            if output_format in ["JPEG", "BMP"]:
                # For formats that do not support transparency
                if img.mode == "RGBA":
                    background = Image.new("RGB", img.size, (255, 255, 255))
                    background.paste(img, mask=img.split()[3])  # Mask for transparency
                    img = background

            elif output_format == "GIF":
                # Convert transparency for GIF
                img = img.convert("RGBA")
                background = Image.new("RGB", img.size, (255, 255, 255))
                background.paste(img, mask=img.split()[3])
                img = background.convert('P', palette=Image.ADAPTIVE, colors=256)

            if output_format == "ICO":
                # Handle ICO conversion; save it with the appropriate sizes
                img.save(output_path, format='ICO', sizes=[(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)])
            else:
                img.save(output_path, format=output_format)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to convert {file_path}\n{str(e)}")
            return

    messagebox.showinfo("Success", f"All selected images have been converted to {output_format} and saved in the same directory.")

root = tk.Tk()
root.title("Batch Image Converter")
root.geometry("500x500")

style = ttk.Style()
style.configure('TButton', font=('Helvetica', 10), padding=10)
style.configure('TRadiobutton', font=('Helvetica', 10), padding=10)
style.configure('TLabel', font=('Helvetica', 12), padding=5)

frame = ttk.Frame(root, padding="30 30 30 30")
frame.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

format_var = tk.StringVar(value="PNG")
format_settings = {
    'PNG': ('PNG', 'png'),
    'JPG': ('JPEG', 'jpg'),
    'WEBP': ('WEBP', 'webp'),
    'BMP': ('BMP', 'bmp'),
    'GIF': ('GIF', 'gif'),
    'TIFF': ('TIFF', 'tiff'),
    'ICO': ('ICO', 'ico')
}

ttk.Label(frame, text="Select output format:").grid(column=0, row=0, sticky=tk.W, pady=5)
for i, (fmt, settings) in enumerate(format_settings.items(), start=1):
    ttk.Radiobutton(frame, text=fmt, value=fmt, variable=format_var).grid(column=0, row=i, sticky=tk.W)

convert_button = ttk.Button(frame, text="Convert Images", command=convert_images)
convert_button.grid(column=0, row=len(format_settings) + 1, pady=20, padx=10, sticky=tk.EW)

root.mainloop()
