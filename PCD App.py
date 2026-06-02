import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import cv2
import numpy as np
from PIL import Image, ImageTk
import matplotlib.pyplot as plt


class ImageProcessingApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Aplikasi Pengolahan Citra Digital")
        self.root.geometry("1200x700")

        self.img = None
        self.original_img = None
        self.processed = None

        self.create_widgets()

    # ================= UI =================
    def create_widgets(self):

        main_frame = tk.Frame(self.root)
        main_frame.pack(fill="both", expand=True)

        # ================= SIDEBAR =================
        sidebar_container = tk.Frame(main_frame, width=280, bg="#e6e6e6")
        sidebar_container.pack(side=tk.LEFT, fill=tk.Y)
        sidebar_container.pack_propagate(False)

        canvas = tk.Canvas(sidebar_container, bg="#e6e6e6", highlightthickness=0)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(sidebar_container, orient="vertical", command=canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        canvas.configure(yscrollcommand=scrollbar.set)

        menu_frame = tk.Frame(canvas, bg="#e6e6e6")
        canvas.create_window((0,0), window=menu_frame, anchor="nw")

        # update scrollregion otomatis
        def on_frame_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        menu_frame.bind("<Configure>", on_frame_configure)

        # mouse wheel support
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")

        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        # ================= IMAGE AREA =================
        image_frame = tk.Frame(main_frame, bg="white")
        image_frame.pack(side=tk.RIGHT, fill="both", expand=True)

        self.result_label = tk.Label(image_frame, bg="white")
        self.result_label.pack(expand=True, fill="both")

        # ================= FILE =================
        file_frame = tk.LabelFrame(menu_frame, text="File", padx=5, pady=5)
        file_frame.pack(fill="x", padx=10, pady=5)

        tk.Button(file_frame, text="Buka Gambar", command=self.open_image).pack(fill="x", pady=2)
        tk.Button(file_frame, text="Simpan Hasil", command=self.save_image).pack(fill="x", pady=2)
        tk.Button(file_frame, text="Reset", command=self.reset_image).pack(fill="x", pady=2)

        # ================= PROSES DASAR =================
        process_frame = tk.LabelFrame(menu_frame, text="Proses Dasar", padx=5, pady=5)
        process_frame.pack(fill="x", padx=10, pady=5)

        tk.Button(process_frame, text="Grayscale", command=self.grayscale).pack(fill="x", pady=2)
        tk.Button(process_frame, text="Biner", command=self.binary).pack(fill="x", pady=2)

        tk.Label(process_frame, text="Brightness").pack(anchor="w")

        self.brightness_scale = tk.Scale(
            process_frame,
            from_=-100,
            to=100,
            orient="horizontal"
        )
        self.brightness_scale.set(0)
        self.brightness_scale.pack(fill="x")

        tk.Button(process_frame, text="Apply Brightness", command=self.adjust_brightness).pack(fill="x", pady=3)

        # ================= OPERASI LOGIKA =================
        logic_frame = tk.LabelFrame(menu_frame, text="Operasi Logika", padx=5, pady=5)
        logic_frame.pack(fill="x", padx=10, pady=5)

        self.logic_combo = ttk.Combobox(
            logic_frame,
            values=["NOT", "AND", "OR", "XOR"],
            state="readonly"
        )
        self.logic_combo.pack(fill="x", pady=3)

        tk.Button(logic_frame, text="Terapkan", command=self.logic_menu).pack(fill="x")

        # ================= HISTOGRAM =================
        hist_frame = tk.LabelFrame(menu_frame, text="Histogram", padx=5, pady=5)
        hist_frame.pack(fill="x", padx=10, pady=5)

        tk.Button(hist_frame, text="Tampilkan Histogram", command=self.show_histogram).pack(fill="x")

        # ================= KONVOLUSI =================
        conv_frame = tk.LabelFrame(menu_frame, text="Konvolusi", padx=5, pady=5)
        conv_frame.pack(fill="x", padx=10, pady=5)

        self.conv_combo = ttk.Combobox(
            conv_frame,
            values=["Blur", "Sharpen", "Edge Detection"],
            state="readonly"
        )
        self.conv_combo.pack(fill="x", pady=3)

        tk.Button(conv_frame, text="Terapkan", command=self.konvolusi_menu).pack(fill="x")

        # ================= MORFOLOGI =================
        morph_frame = tk.LabelFrame(menu_frame, text="Morfologi", padx=5, pady=5)
        morph_frame.pack(fill="x", padx=10, pady=5)

        self.morph_combo = ttk.Combobox(
            morph_frame,
            values=["Erosi Rect", "Dilasi Rect", "Erosi Ellipse", "Dilasi Ellipse"],
            state="readonly"
        )
        self.morph_combo.pack(fill="x", pady=3)

        tk.Button(morph_frame, text="Terapkan", command=self.morfologi_menu).pack(fill="x")

    # ================= FILE =================
    def open_image(self):
        path = filedialog.askopenfilename(filetypes=[("Image","*.jpg *.png *.bmp *.jpeg")])
        if path:
            self.img = cv2.imread(path)
            self.original_img = self.img.copy()
            self.processed = self.img.copy()
            self.show_result()

    def save_image(self):
        if self.processed is None:
            messagebox.showwarning("Peringatan", "Tidak ada gambar")
            return

        path = filedialog.asksaveasfilename(defaultextension=".png")
        if path:
            cv2.imwrite(path, self.processed)
            messagebox.showinfo("Sukses", "Gambar tersimpan")

    def reset_image(self):
        if self.original_img is not None:
            self.img = self.original_img.copy()
            self.processed = self.original_img.copy()
            self.show_result()

    # ================= DISPLAY =================
    def show_result(self):
        img = self.processed

        if len(img.shape) == 2:
            img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
        else:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        img = Image.fromarray(img)
        img.thumbnail((900, 650))

        imgtk = ImageTk.PhotoImage(img)

        self.result_label.config(image=imgtk)
        self.result_label.image = imgtk

    # ================= PROSES DASAR =================
    def grayscale(self):
        if self.img is None: return
        self.processed = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        self.show_result()

    def binary(self):
        if self.img is None: return
        gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        _, self.processed = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
        self.show_result()

    def adjust_brightness(self):
        if self.img is None: return
        value = self.brightness_scale.get()
        self.processed = cv2.convertScaleAbs(self.img, alpha=1, beta=value)
        self.show_result()

    # ================= LOGIKA =================
    def logic_menu(self):
        if self.img is None: return

        choice = self.logic_combo.get()

        if choice == "NOT":
            self.processed = cv2.bitwise_not(self.img)

        elif choice == "AND":
            self.processed = cv2.bitwise_and(self.img, self.img)

        elif choice == "OR":
            self.processed = cv2.bitwise_or(self.img, self.img)

        elif choice == "XOR":
            self.processed = cv2.bitwise_xor(self.img, self.img)

        self.show_result()

    # ================= HISTOGRAM =================
    def show_histogram(self):
        if self.img is None: return

        colors = ("b","g","r")
        for i,c in enumerate(colors):
            hist = cv2.calcHist([self.img],[i],None,[256],[0,256])
            plt.plot(hist, color=c)

        plt.title("Histogram RGB")
        plt.show()

    # ================= KONVOLUSI =================
    def konvolusi_menu(self):
        if self.img is None: return

        choice = self.conv_combo.get()

        if choice == "Blur":
            self.processed = cv2.GaussianBlur(self.img,(9,9),0)

        elif choice == "Sharpen":
            kernel = np.array([[0,-1,0],[-1,5,-1],[0,-1,0]])
            self.processed = cv2.filter2D(self.img,-1,kernel)

        elif choice == "Edge Detection":
            gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
            self.processed = cv2.Canny(gray,100,200)

        self.show_result()

    # ================= MORFOLOGI =================
    def get_binary(self):
        gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        _, binary = cv2.threshold(gray,127,255,cv2.THRESH_BINARY)
        return binary

    def morfologi_menu(self):
        if self.img is None: return

        choice = self.morph_combo.get()
        binary = self.get_binary()

        if choice == "Erosi Rect":
            kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(5,5))
            self.processed = cv2.erode(binary,kernel,1)

        elif choice == "Dilasi Rect":
            kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(5,5))
            self.processed = cv2.dilate(binary,kernel,1)

        elif choice == "Erosi Ellipse":
            kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))
            self.processed = cv2.erode(binary,kernel,1)

        elif choice == "Dilasi Ellipse":
            kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))
            self.processed = cv2.dilate(binary,kernel,1)

        self.show_result()


# ================= RUN =================
if __name__ == "__main__":
    root = tk.Tk()
    app = ImageProcessingApp(root)
    root.mainloop()