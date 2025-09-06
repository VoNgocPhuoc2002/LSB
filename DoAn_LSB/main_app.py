# main_app.py
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import image_steg
import audio_steg
import steganalysis

class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Công cụ Ẩn thông tin và Phân tích - Đồ án IE406")
        self.root.geometry("700x500")

        # Tạo các tab
        self.notebook = ttk.Notebook(root)
        self.tab_image = ttk.Frame(self.notebook)
        self.tab_audio = ttk.Frame(self.notebook)
        self.tab_analysis = ttk.Frame(self.notebook)

        self.notebook.add(self.tab_image, text="Giấu/Trích tin (Ảnh)")
        self.notebook.add(self.tab_audio, text="Giấu/Trích tin (Âm thanh)")
        self.notebook.add(self.tab_analysis, text="Phát hiện tin ẩn")
        self.notebook.pack(expand=True, fill="both")

        # Tạo giao diện cho từng tab
        self.create_image_tab()
        self.create_audio_tab()
        self.create_analysis_tab()

    # --- TAB XỬ LÝ ẢNH ---
    def create_image_tab(self):
        # ... Giao diện tương tự code GUI trước đây ...
        lbl_title = tk.Label(self.tab_image, text="Giấu tin trong Ảnh (LSB)", font=("Arial", 16))
        lbl_title.pack(pady=10)

        # Chọn ảnh
        frame_img_select = tk.Frame(self.tab_image)
        frame_img_select.pack(pady=5, padx=10, fill="x")
        self.lbl_img_path = tk.Label(frame_img_select, text="Chưa chọn ảnh...", width=70, anchor="w")
        self.lbl_img_path.pack(side=tk.LEFT)
        btn_select_img = tk.Button(frame_img_select, text="Chọn Ảnh", command=self.select_cover_image)
        btn_select_img.pack(side=tk.RIGHT)

        # Nhập thông điệp
        lbl_msg = tk.Label(self.tab_image, text="Nhập thông điệp:")
        lbl_msg.pack(pady=(10,0))
        self.txt_img_message = scrolledtext.ScrolledText(self.tab_image, height=10)
        self.txt_img_message.pack(pady=5, padx=10, fill="x")

        # Nút chức năng
        frame_buttons = tk.Frame(self.tab_image)
        frame_buttons.pack(pady=20)
        btn_embed = tk.Button(frame_buttons, text="Nhúng tin vào Ảnh", command=self.embed_image, width=20)
        btn_embed.pack(side=tk.LEFT, padx=20)
        btn_extract = tk.Button(frame_buttons, text="Trích xuất tin từ Ảnh", command=self.extract_image, width=20)
        btn_extract.pack(side=tk.LEFT, padx=20)

    # --- TAB XỬ LÝ ÂM THANH ---
    def create_audio_tab(self):
        lbl_title = tk.Label(self.tab_audio, text="Giấu tin trong Âm thanh (LSB)", font=("Arial", 16))
        lbl_title.pack(pady=10)

        # Chọn file audio
        frame_audio_select = tk.Frame(self.tab_audio)
        frame_audio_select.pack(pady=5, padx=10, fill="x")
        self.lbl_audio_path = tk.Label(frame_audio_select, text="Chưa chọn file âm thanh...", width=70, anchor="w")
        self.lbl_audio_path.pack(side=tk.LEFT)
        btn_select_audio = tk.Button(frame_audio_select, text="Chọn Âm thanh (.wav)", command=self.select_cover_audio)
        btn_select_audio.pack(side=tk.RIGHT)

        # Nhập thông điệp
        lbl_msg = tk.Label(self.tab_audio, text="Nhập thông điệp:")
        lbl_msg.pack(pady=(10,0))
        self.txt_audio_message = scrolledtext.ScrolledText(self.tab_audio, height=10)
        self.txt_audio_message.pack(pady=5, padx=10, fill="x")

        # Nút chức năng
        frame_buttons = tk.Frame(self.tab_audio)
        frame_buttons.pack(pady=20)
        btn_embed = tk.Button(frame_buttons, text="Nhúng tin vào Âm thanh", command=self.embed_audio, width=25)
        btn_embed.pack(side=tk.LEFT, padx=20)
        btn_extract = tk.Button(frame_buttons, text="Trích xuất tin từ Âm thanh", command=self.extract_audio, width=25)
        btn_extract.pack(side=tk.LEFT, padx=20)

    # --- TAB PHÂN TÍCH ---
    def create_analysis_tab(self):
        lbl_title = tk.Label(self.tab_analysis, text="Phân tích Phát hiện tin ẩn (Steganalysis)", font=("Arial", 16))
        lbl_title.pack(pady=10)

        btn_analyze = tk.Button(self.tab_analysis, text="Chọn File để Phân tích (Ảnh/Âm thanh)", command=self.analyze_file, width=40)
        btn_analyze.pack(pady=20)
        
        lbl_result = tk.Label(self.tab_analysis, text="Kết quả phân tích:")
        lbl_result.pack(pady=(10,0))
        self.txt_analysis_result = scrolledtext.ScrolledText(self.tab_analysis, height=15, state="disabled")
        self.txt_analysis_result.pack(pady=5, padx=10, fill="both", expand=True)

    # --- Các hàm xử lý sự kiện ---
    def select_cover_image(self):
        path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.bmp")])
        if path: self.lbl_img_path.config(text=path)

    def select_cover_audio(self):
        path = filedialog.askopenfilename(filetypes=[("Audio files", "*.wav")])
        if path: self.lbl_audio_path.config(text=path)

    def embed_image(self):
        cover_path = self.lbl_img_path.cget("text")
        if "Chưa chọn" in cover_path:
            messagebox.showerror("Lỗi", "Vui lòng chọn ảnh gốc!")
            return
        message = self.txt_img_message.get("1.0", tk.END).strip()
        if not message:
            messagebox.showerror("Lỗi", "Vui lòng nhập thông điệp!")
            return
        save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG file", "*.png")])
        if save_path:
            result = image_steg.embed_message_in_image(cover_path, message, save_path)
            messagebox.showinfo("Thông báo", result)

    def extract_image(self):
        stego_path = filedialog.askopenfilename(filetypes=[("Stego Image files", "*.png;*.bmp")])
        if stego_path:
            message = image_steg.extract_message_from_image(stego_path)
            messagebox.showinfo("Thông điệp được trích xuất", message)

    def embed_audio(self):
        cover_path = self.lbl_audio_path.cget("text")
        if "Chưa chọn" in cover_path:
            messagebox.showerror("Lỗi", "Vui lòng chọn file âm thanh!")
            return
        message = self.txt_audio_message.get("1.0", tk.END).strip()
        if not message:
            messagebox.showerror("Lỗi", "Vui lòng nhập thông điệp!")
            return
        save_path = filedialog.asksaveasfilename(defaultextension=".wav", filetypes=[("WAV file", "*.wav")])
        if save_path:
            result = audio_steg.embed_message_in_audio(cover_path, message, save_path)
            messagebox.showinfo("Thông báo", result)

    def extract_audio(self):
        stego_path = filedialog.askopenfilename(filetypes=[("Stego Audio files", "*.wav")])
        if stego_path:
            message = audio_steg.extract_message_from_audio(stego_path)
            messagebox.showinfo("Thông điệp được trích xuất", message)
    
    def analyze_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("All files", "*.*"), ("Image files", "*.png;*.bmp"), ("Audio files", "*.wav")])
        if not file_path:
            return

        result = ""
        if file_path.lower().endswith(('.png', '.bmp')):
            result = steganalysis.analyze_image_lsb(file_path)
        elif file_path.lower().endswith('.wav'):
            result = steganalysis.analyze_audio_lsb(file_path)
        else:
            result = "Định dạng file không được hỗ trợ để phân tích."
        
        self.txt_analysis_result.config(state="normal")
        self.txt_analysis_result.delete("1.0", tk.END)
        self.txt_analysis_result.insert(tk.END, result)
        self.txt_analysis_result.config(state="disabled")

# --- Khởi chạy chương trình ---
if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()