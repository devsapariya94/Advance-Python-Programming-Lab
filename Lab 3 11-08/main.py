import tkinter as tk
from tkinter import filedialog, simpledialog
from PIL import Image, ImageTk, ImageOps, ImageFilter, ImageEnhance
import matplotlib.pyplot as plt
from scipy import ndimage
from tkinter import Scale

class ImageManipulationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Manipulation App")
        
        self.left_frame = tk.Frame(root)
        self.left_frame.pack(side=tk.LEFT, padx=10, pady=10)
        
        self.right_frame = tk.Frame(root)
        self.right_frame.pack(side=tk.LEFT, padx=10, pady=10)
        
        self.canvas = tk.Canvas(self.right_frame)
        self.canvas.pack()
        
        self.load_button = tk.Button(self.left_frame, text="Load Image", command=self.load_image)
        self.load_button.pack()
        
        self.blur_button = tk.Button(self.left_frame, text="Apply Blur", command=self.apply_blur)
        self.blur_button.pack()

        self.reset_button = tk.Button(self.left_frame, text="Reset to Default Image", command=self.reset_to_default)
        self.reset_button.pack(fill=tk.X, padx=10, pady=5)
        
        self.grayscale_button = tk.Button(root, text="Convert to Grayscale", command=self.convert_to_grayscale)
        self.grayscale_button.pack()
        
        self.invert_button = tk.Button(root, text="Invert Colors", command=self.invert_colors)
        self.invert_button.pack()
        
        self.rotate_button = tk.Button(root, text="Rotate Image", command=self.rotate_image)
        self.rotate_button.pack()
        
        self.edge_button = tk.Button(root, text="Edge Detection", command=self.detect_edges)
        self.edge_button.pack()
        
        self.crop_button = tk.Button(root, text="Crop Image", command=self.crop_image)
        self.crop_button.pack()
        
        self.brightness_scale = Scale(root, label="Brightness", from_=0.1, to=2, resolution=0.1, orient=tk.HORIZONTAL)
        self.brightness_scale.pack()
        
        self.contrast_scale = Scale(root, label="Contrast", from_=0.1, to=2, resolution=0.1, orient=tk.HORIZONTAL)
        self.contrast_scale.pack()
        
        self.saturation_scale = Scale(root, label="Saturation", from_=0.1, to=2, resolution=0.1, orient=tk.HORIZONTAL)
        self.saturation_scale.pack()
        
        self.adjust_button = tk.Button(root, text="Adjust Image", command=self.adjust_image)
        self.adjust_button.pack()
        
        self.save_button = tk.Button(self.left_frame, text="Save Image", command=self.save_image)
        self.save_button.pack()
        
        self.histogram_button = tk.Button(self.left_frame, text="Show Histogram", command=self.show_histogram)
        self.histogram_button.pack()
        

        self.histogram_frame = tk.Frame(self.left_frame)
        self.histogram_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.calculate_histogram_button = tk.Button(self.histogram_frame, text="Calculate Histogram", command=self.calculate_histogram)
        self.calculate_histogram_button.pack()
        
        self.histogram_canvas = tk.Canvas(self.histogram_frame, bg='white')
        self.histogram_canvas.pack(fill=tk.BOTH, expand=True)
        
        self.r_adjust_scale = tk.Scale(self.histogram_frame, label="R Adjustment", from_=-255, to=255, orient=tk.HORIZONTAL)
        self.r_adjust_scale.pack()
        
        self.g_adjust_scale = tk.Scale(self.histogram_frame, label="G Adjustment", from_=-255, to=255, orient=tk.HORIZONTAL)
        self.g_adjust_scale.pack()
        
        self.b_adjust_scale = tk.Scale(self.histogram_frame, label="B Adjustment", from_=-255, to=255, orient=tk.HORIZONTAL)
        self.b_adjust_scale.pack()
        
        self.histogram_adjust_button = tk.Button(self.histogram_frame, text="Apply Adjustment", command=self.adjust_histogram)
        self.histogram_adjust_button.pack()

















        self.image = None
        self.original_image = None
        self.photo = None
        self.operations = []  # List to store applied operations
    

        
    def load_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.image = Image.open(file_path)
            self.original_image = self.image.copy() 
            self.original_image_copy = self.image.copy()
             # Store a copy of the original image
            self.update_canvas()
            self.reset_slider_values()
    
    def reset_slider_values(self):
        self.r_adjust_scale.set(0)
        self.g_adjust_scale.set(0)
        self.b_adjust_scale.set(0)
        self.brightness_scale.set(1)    
        self.contrast_scale.set(1)
        self.saturation_scale.set(1)



    def reset_to_default(self):
        if self.original_image:
            self.image = self.original_image_copy.copy()
            self.update_canvas()
            self.reset_slider_values()

    def update_canvas(self):
        if self.image:
            canvas_width = self.canvas.winfo_width()
            canvas_height = self.canvas.winfo_height()
            self.image = self.image.resize((canvas_width, canvas_height), Image.BILINEAR)
            self.photo = ImageTk.PhotoImage(self.image)
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
        
        
    def apply_blur(self):
        if not self.image:
            return
        self.image = self.image.filter(ImageFilter.GaussianBlur(5))
        self.original_image = self.original_image.filter(ImageFilter.GaussianBlur(5))
        self.update_canvas()
        
    def convert_to_grayscale(self):
        if not self.image:
            return
        self.image = ImageOps.grayscale(self.image)
        self.original_image = ImageOps.grayscale(self.original_image)
        self.update_canvas()
        
    def invert_colors(self):
        if not self.image:
            return
        self.image = ImageOps.invert(self.image)
        self.original_image = ImageOps.invert(self.original_image)
        self.update_canvas()
        
    def rotate_image(self):
        if not self.image:
            return
        degrees = simpledialog.askinteger("Rotate Image", "Enter rotation angle:")
        self.image = self.image.rotate(degrees)
        self.original_image = self.original_image.rotate(degrees)
        self.update_canvas()
        
    def detect_edges(self):
        if not self.image:
            return
        img_array = ndimage.sobel(ImageOps.grayscale(self.image), mode="constant")
        self.image = Image.fromarray(img_array)
        original_img_array = ndimage.sobel(ImageOps.grayscale(self.original_image), mode="constant")
        self.original_image = Image.fromarray(original_img_array)
        self.update_canvas()
        
    def crop_image(self):
        if not self.image:
            return
        percentage = simpledialog.askfloat("Crop Image", "Enter cropping percentage:")
        width, height = self.image.size
        left = int(percentage * width / 100)
        upper = int(percentage * height / 100)
        right = int((100 - percentage) * width / 100)
        lower = int((100 - percentage) * height / 100)
        self.image = self.image.crop((left, upper, right, lower))
        self.original_image = self.original_image.crop((left, upper, right, lower))
        self.update_canvas()
        
    def adjust_image(self):
        if not self.image or not self.original_image:
            return
        brightness_factor = self.brightness_scale.get()
        contrast_factor = self.contrast_scale.get()
        saturation_factor = self.saturation_scale.get()
        
        # Apply adjustments using ImageEnhance module
        adjusted_image = self.original_image_copy.copy()
        
        enhancer = ImageEnhance.Brightness(adjusted_image)
        adjusted_image = enhancer.enhance(brightness_factor)
        
        enhancer = ImageEnhance.Contrast(adjusted_image)
        adjusted_image = enhancer.enhance(contrast_factor)
        
        enhancer = ImageEnhance.Color(adjusted_image)
        adjusted_image = enhancer.enhance(saturation_factor)
        
        self.original_image = adjusted_image
        self.image = adjusted_image

        self.update_canvas()
        
    def apply_operation(self, operation_func, *args):
        if not self.image:
            return
        edited_image = operation_func(self.image, *args)
        self.image = edited_image
        self.operations.append((operation_func, args))
        self.update_canvas()
        
    def save_image(self):
        if self.original_image:
            edited_image = self.original_image.copy()
            for operation_func, args in self.operations:
                edited_image = operation_func(edited_image, *args)
            file_path = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("JPEG files", "*.jpg")])
            if file_path:
                edited_image.save(file_path, quality=100)  # Save with high quality
                print("Image saved successfully!")

        
    def show_histogram(self):
        if not self.image:
            return
        
        r, g, b = self.image.split()
        r_histogram = r.histogram()
        g_histogram = g.histogram()
        b_histogram = b.histogram()
        
        # Plot histograms using matplotlib
        plt.figure(figsize=(8, 6))
        plt.title("Color Histogram")
        plt.xlabel("Pixel Value")
        plt.ylabel("Frequency")
        plt.plot(r_histogram, color="red", label="Red")
        plt.plot(g_histogram, color="green", label="Green")
        plt.plot(b_histogram, color="blue", label="Blue")
        plt.legend()
        plt.show()
        

    def calculate_histogram(self):
        if not self.image:
            return
        
        r, g, b = self.image.split()
        self.r_histogram = r.histogram()
        self.g_histogram = g.histogram()
        self.b_histogram = b.histogram()
        
        self.plot_histogram(self.r_histogram, "Red", 0, 'red')
        self.plot_histogram(self.g_histogram, "Green", 1, 'green')
        self.plot_histogram(self.b_histogram, "Blue", 2, 'blue')
    
    def plot_histogram(self, histogram, channel_name, offset, color):
        self.histogram_canvas.delete(f"{channel_name}_histogram")
        
        canvas_width = self.histogram_canvas.winfo_width()
        canvas_height = self.histogram_canvas.winfo_height()
        
        max_value = max(histogram)
        
        for i, value in enumerate(histogram):
            x0 = i * (canvas_width / 256)
            y0 = canvas_height - (value / max_value * canvas_height)
            x1 = (i + 1) * (canvas_width / 256)
            y1 = canvas_height
            
            self.histogram_canvas.create_rectangle(x0 + offset * canvas_width / 3, y0, x1 + offset * canvas_width / 3, y1, fill=color, outline=color, tags=f"{channel_name}_histogram")
    
    def adjust_histogram(self):
        if not self.image:
            return
        
        r, g, b = self.image.split()
        r_adjusted = self.adjust_channel_histogram(r, self.r_histogram, self.r_adjust_scale.get())
        g_adjusted = self.adjust_channel_histogram(g, self.g_histogram, self.g_adjust_scale.get())
        b_adjusted = self.adjust_channel_histogram(b, self.b_histogram, self.b_adjust_scale.get())
        
        self.image = Image.merge("RGB", (r_adjusted, g_adjusted, b_adjusted))
        self.update_canvas()
    
    def adjust_channel_histogram(self, channel, original_histogram, adjustment_value):
        lut = [min(255, max(0, i + adjustment_value)) for i in range(256)]
        adjusted_channel = channel.point(lut)
        return adjusted_channel
  
if __name__ == "__main__":
    root = tk.Tk()
    app = ImageManipulationApp(root)
    root.mainloop()
