import tkinter as tk
from tkinter import filedialog, ttk
import cv2
from PIL import Image, ImageTk
import numpy as np
from poseCompare import poseCompare

class DanceOrDieApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Dance or Die!")
        self.model_type = 'yolo'
        self.mode = 'pose'
        self.streaming = False
        self.model = None
        self.create_widgets()

    def create_widgets(self):
        # Control Frame
        control_frame = tk.Frame(self.root, padx=10, pady=10)
        control_frame.pack(side=tk.TOP, fill=tk.X)

        # Model Selection
        tk.Label(control_frame, text="Vision Model:").grid(row=0, column=0, sticky=tk.W)
        self.model_var = tk.StringVar(value=self.model_type)
        tk.Radiobutton(control_frame, text="YOLO", variable=self.model_var, value='yolo', command=self.update_model).grid(row=0, column=1, sticky=tk.W)
        tk.Radiobutton(control_frame, text="MediaPipe", variable=self.model_var, value='mediapipe', command=self.update_model).grid(row=0, column=2, sticky=tk.W)

        # Start/Stop/Exit Streaming Button
        tk.Button(control_frame, text="Start", command=self.start_stream).grid(row=3, column=0, pady=10)
        tk.Button(control_frame, text="Stop", command=self.stop_stream).grid(row=3, column=1, pady=10)
        tk.Button(control_frame, text="Exit", command=self.root.quit).grid(row=3, column=2, pady=10)

        # File Selection
        tk.Button(control_frame, text="Select Video File", command=self.select_file).grid(row=1, column=0, pady=5)
        self.file_label = tk.Label(control_frame, text="No file selected")
        self.file_label.grid(row=1, column=1, columnspan=2, sticky=tk.W)

        # Video Display
        self.display_frame = tk.Frame(self.root, width=800, height=600)
        self.display_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        self.display_label = tk.Label(self.display_frame)
        self.display_label.pack(fill=tk.BOTH, expand=True)

        # Mode Selection
        tk.Label(control_frame, text="Mode:").grid(row=1, column=0, sticky=tk.W)
        self.mode_var = tk.StringVar(value=self.mode)
        tk.Radiobutton(control_frame, text="Pose Compare", variable=self.mode_var, value='pose').grid(row=1, column=1, sticky=tk.W)
        tk.Radiobutton(control_frame, text="Dance Compare", variable=self.mode_var, value='dance').grid(row=1, column=2, sticky=tk.W)

    def start_stream(self):
        if self.streaming:
            return
        
        self.streaming = True
        if self.model_type == 'yolo':
            self.model = poseCompare('yolo')
        else:
            self.model = poseCompare('mediapipe')
        return
    
    def stop_stream(self):
        self.streaming = False
    
    def select_file(self):
        self.path = filedialog.askopenfilename(
            title="Select File",
            filetypes=[("Video Files", "*.mp4 *.avi *.mov"), ("Image Files", "*.jpg *.jpeg *.png"), ("All Files", "*.*")]
        )
        if self.path:
            self.file_label.config(text=self.path.split("/")[-1])

    def update_model(self):
        self.model_type = self.model_var.get()
        if self.model:
            self.model = poseCompare(self.model_type)

root = tk.Tk()
app = DanceOrDieApp(root)
root.mainloop()
