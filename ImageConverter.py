import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image
import os

def toggle_all_formats(value):
    for var in format_vars.values():
        var.set(value)

def convert_images():
    file_paths = filedialog.askopenfilenames(
        title="Select images",
        filetypes=[
            ("Image files", "*.jpg *.jpeg *.png *.webp *.bmp *.gif *.tiff *.ico"),
            ("JPG", "*.jpg *.jpeg"),
            ("PNG", "*.png"),
            ("WEBP", "*.webp"),
            ("BMP", "*.bmp"),
            ("GIF", "*.gif"),
            ("TIFF", "*.tiff"),
            ("ICO", "*.ico")
        ])
    if not file_paths:
        return

    selected_formats = [fmt for fmt, var in format_vars.items() if var.get()]

    for file_path in file_paths:
        try:
            img = Image.open(file_path)
            file_dir, file_name = os.path.split(file_path)
            base_name = os.path.splitext(file_name)[0]

            for fmt in selected_formats:
                extension, pil_format = format_settings[fmt]
                output_path = os.path.join(file_dir, f"{base_name}.{extension}")

                counter = 1
                while os.path.exists(output_path):
                    output_path = os.path.join(file_dir, f"{base_name}({counter}).{extension}")
                    counter += 1

                if fmt in ["JPG", "BMP"]:
                    if img.mode in ['RGBA', 'LA'] or (img.mode == 'P' and 'transparency' in img.info):
                        background = Image.new("RGB", img.size, (255, 255, 255))
                        background.paste(img, (0, 0), img.convert('RGBA'))
                        img_to_save = background
                    else:
                        img_to_save = img.convert('RGB')
                elif fmt == "GIF":
                    if img.mode == 'RGBA':
                        img_to_save = img.convert('P', palette=Image.ADAPTIVE, colors=256)
                    else:
                        img_to_save = img
                elif fmt == "ICO":
                    icon_sizes = [(16, 16), (32, 32), (48, 48), (64, 64)]  # Typical icon sizes
                    img_to_save = img.resize(icon_sizes[-1])  # Resize to the largest size in the list
                    img_to_save.save(output_path, format=pil_format, sizes=icon_sizes)
                else:
                    img_to_save = img

                img_to_save.save(output_path, format=pil_format)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to convert {file_path}\nError type: {type(e).__name__}, Message: {e}")
            return

    messagebox.showinfo("Success", "All selected images have been converted to the selected formats.")

root = tk.Tk()
root.title("Batch Image Converter")
root.geometry("550x600")

style = ttk.Style()
style.configure('TButton', font=('Helvetica', 10), padding=10)
style.configure('TRadiobutton', font=('Helvetica', 10), padding=10)
style.configure('TLabel', font=('Helvetica', 12), padding=5)

frame = ttk.Frame(root, padding="30 30 30 30")
frame.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

format_vars = {}
select_all_var = tk.BooleanVar(value=False)

format_settings = {
    'PNG': ('png', 'PNG'),
    'JPG': ('jpg', 'JPEG'),
    'WEBP': ('webp', 'WEBP'),
    'BMP': ('bmp', 'BMP'),
    'GIF': ('gif', 'GIF'),
    'TIFF': ('tiff', 'TIFF'),
    'ICO': ('ico', 'ICO')
}

select_all_button = ttk.Checkbutton(frame, text="Select/Deselect All", variable=select_all_var,
                                    command=lambda: toggle_all_formats(select_all_var.get()))
select_all_button.grid(column=0, row=0, sticky=tk.W)

row = 1
for fmt, ext in format_settings.items():
    var = tk.BooleanVar(value=False)
    format_vars[fmt] = var
    ttk.Checkbutton(frame, text=fmt, variable=var).grid(column=0, row=row, sticky=tk.W)
    row += 1

convert_button = ttk.Button(frame, text="Convert Images", command=convert_images)
convert_button.grid(column=0, row=row, pady=20, padx=10, sticky=tk.EW)

root.mainloop()
