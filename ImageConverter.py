import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image

def convert_image():
    file_path = filedialog.askopenfilename(title="Select an image", filetypes=[("Image files", "*.jpg *.jpeg *.png *.webp")])
    if not file_path:
        return

    format_choice = format_var.get()
    output_format, extension = format_settings[format_choice]

    output_path = filedialog.asksaveasfilename(title="Save as", defaultextension=f".{extension}", filetypes=[("Image files", f"*.{extension}")])
    if not output_path:
        return

    try:
        with Image.open(file_path) as img:
            img.save(output_path, format=output_format)
        messagebox.showinfo("Success", f"Image successfully converted to {output_format} and saved as {output_path}")
    except Exception as e:
        messagebox.showerror("Error", str(e))

root = tk.Tk()
root.title("Image Converter")
root.geometry("500x300")  # Increased size for better layout

style = ttk.Style()
style.configure('TButton', font=('Helvetica', 10), padding=10)
style.configure('TRadiobutton', font=('Helvetica', 10), padding=10)
style.configure('TLabel', font=('Helvetica', 12), padding=5)

frame = ttk.Frame(root, padding="20 20 20 20")
frame.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))

format_var = tk.StringVar(value="PNG")
format_settings = {'PNG': ('PNG', 'png'), 'JPG': ('JPEG', 'jpg'), 'WEBP': ('WEBP', 'webp')}

ttk.Label(frame, text="Select output format:").grid(column=0, row=0, sticky=tk.W)
for i, (fmt, settings) in enumerate(format_settings.items(), start=1):
    ttk.Radiobutton(frame, text=fmt, value=fmt, variable=format_var).grid(column=0, row=i, sticky=tk.W)

convert_button = ttk.Button(frame, text="Convert Image", command=convert_image)
convert_button.grid(column=0, row=5, pady=20)

root.resizable(False, False)

root.mainloop()
