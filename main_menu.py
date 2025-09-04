# main_menu.py
import tkinter as tk
from PIL import Image, ImageTk
from subscreen import SubScreen

class MainMenu(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.setup_ui()
        self.pack(fill=tk.BOTH, expand=True)
        
    def setup_ui(self):
        # Background
        bg_image = tk.PhotoImage(file=r"D:\SQL\porject\porject\Background.png")
        bg_label = tk.Label(self, image=bg_image)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        bg_label.image = bg_image

        # Country flags
        image_files = [
            r"D:\SQL\porject\porject\flags\China.jpeg",
            r"D:\SQL\porject\porject\flags\Egypt.png",
            r"D:\SQL\porject\porject\flags\Spain.png",
            r"D:\SQL\porject\porject\flags\France.png",
            r"D:\SQL\porject\porject\flags\Italy.png",
            r"D:\SQL\porject\porject\flags\Japan.png",
            r"D:\SQL\porject\porject\flags\Mexico.png",
        ]

        # Load and resize images
        self.images = []
        for img_path in image_files:
            try:
                img = Image.open(img_path)
                img = img.resize((250, 150), Image.LANCZOS)
                self.images.append(ImageTk.PhotoImage(img))
            except:
                self.images.append(None)

        # Create buttons for first 6 countries
        for i in range(6):
            if self.images[i]:
                btn = tk.Button(
                    self,
                    width=250,
                    height=150,
                    image=self.images[i],
                    command=lambda idx=i: self.open_subscreen(idx)
                )
            else:
                btn = tk.Button(
                    self,
                    width=250,
                    height=150,
                    text=f"Country {i+1}",
                    command=lambda idx=i: self.open_subscreen(idx)
                )
            
            row = i // 3
            col = i % 3
            btn.grid(row=row, column=col, padx=20, pady=20)

        # 7th button (Spain)
        if len(self.images) > 6 and self.images[6]:
            btn7 = tk.Button(
                self,
                width=250,
                height=150,
                image=self.images[6],
                command=lambda: self.open_subscreen(6)
            )
        else:
            btn7 = tk.Button(
                self,
                width=250,
                height=150,
                text="Country 7",
                command=lambda: self.open_subscreen(6)
            )
        btn7.grid(row=2, column=1, padx=20, pady=20)

        # Configure grid
        for i in range(3):
            self.grid_columnconfigure(i, weight=1)
        for i in range(3):
            self.grid_rowconfigure(i, weight=1)
    
    def open_subscreen(self, index):
        self.pack_forget()
        SubScreen(self.parent, index)