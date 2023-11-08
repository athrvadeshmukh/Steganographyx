import os
import wave
import argparse
import tkinter as tk
from tkinter import filedialog

class ExtractWaveGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("HiddenWave Ver 1.0 - Secret Message Extractor")
        self.af = ""

        self.create_widgets()

    def create_widgets(self):
        self.audio_label = tk.Label(self.root, text="Select Audio File:")
        self.audio_label.pack()

        self.audio_entry = tk.Entry(self.root)
        self.audio_entry.pack()

        self.audio_button = tk.Button(self.root, text="Browse", command=self.browse_audio)
        self.audio_button.pack()

        self.extract_button = tk.Button(self.root, text="Extract Message", command=self.extract_message)
        self.extract_button.pack()

        self.message_label = tk.Label(self.root, text="Extracted Message:")
        self.message_label.pack()

        self.message_text = tk.Text(self.root, height=5, width=40)
        self.message_text.pack()

    def browse_audio(self):
        self.af = filedialog.askopenfilename(filetypes=[("Wave Audio Files", "*.wav")])
        self.audio_entry.delete(0, tk.END)
        self.audio_entry.insert(0, self.af)

    def extract_message(self):
        self.af = self.audio_entry.get()
        
        if self.af:
            try:
                waveaudio = wave.open(self.af, mode='rb')
                frame_bytes = bytearray(list(waveaudio.readframes(waveaudio.getnframes())))
                extracted = [frame_bytes[i] & 1 for i in range(len(frame_bytes))
                            ]
                string = "".join(chr(int("".join(map(str, extracted[i:i + 8])), 2)) for i in range(0, len(extracted), 8))
                msg = string.split("###")[0]
                self.message_text.delete(1.0, tk.END)
                self.message_text.insert(tk.END, msg)
                waveaudio.close()
            except Exception as e:
                self.message_text.delete(1.0, tk.END)
                self.message_text.insert(tk.END, "Error: " + str(e))
        else:
            self.message_text.delete(1.0, tk.END)
            self.message_text.insert(tk.END, "Please select an audio file.")

if __name__ == '__main__':
    root = tk.Tk()
    app = ExtractWaveGUI(root)
    root.mainloop()
