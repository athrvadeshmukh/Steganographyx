# Created BY Athrva Deshmukh
# https://github.com/athrvadeshmukh

import os
import wave
import argparse
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

class HiddenWaveGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Steganographyx - Encode Message in Wave Audio")
        
        # Set the window icon using the iconbitmap method
        self.root.iconbitmap('logo.ico')  # Replace 'logo.ico' with the path to your icon file
        
        self.af = ""
        self.string = ""
        self.output = ""
        
        self.create_widgets()

    def create_widgets(self):
          # Create a mini box to show the logo
        self.logo_label = tk.Label(self.root)
        self.logo_label.pack()
        self.display_logo()  # Call the function to display the logo

        self.audio_label = tk.Label(self.root, text="Select Audio File:")
        self.audio_label.pack()
        
        self.audio_entry = tk.Entry(self.root)
        self.audio_entry.pack()
        
        self.audio_button = tk.Button(self.root, text="Browse", command=self.browse_audio)
        self.audio_button.pack()
        
        self.message_label = tk.Label(self.root, text="Enter your Secret Message:")
        self.message_label.pack()
        
        self.message_entry = tk.Entry(self.root)
        self.message_entry.pack()
        
        self.output_label = tk.Label(self.root, text="Your Output file path and name:")
        self.output_label.pack()
        
        self.output_entry = tk.Entry(self.root)
        self.output_entry.pack()
        
        self.hide_button = tk.Button(self.root, text="Hide Message", command=self.hide_message)
        self.hide_button.pack()
        
        self.status_label = tk.Label(self.root, text="")
        self.status_label.pack()

        self.output_button = tk.Button(self.root, text="Browse Output", command=self.browse_output)
        self.output_button.pack()

    

    def browse_audio(self):
        self.af = filedialog.askopenfilename(filetypes=[("Wave Audio Files", "*.wav")])
        self.audio_entry.delete(0, tk.END)
        self.audio_entry.insert(0, self.af)

       
    def browse_output(self):
        self.output = filedialog.asksaveasfilename(defaultextension=".wav", filetypes=[("Wave Audio Files", "*.wav")])
        self.output_entry.delete(0, tk.END)
        self.output_entry.insert(0, self.output)

    

    def hide_message(self):
        self.af = self.audio_entry.get()
        self.string = self.message_entry.get()
        self.output = self.output_entry.get()
        
        if self.af and self.string and self.output:
            try:
                waveaudio = wave.open(self.af, mode='rb')
                frame_bytes = bytearray(list(waveaudio.readframes(waveaudio.getnframes())))
                self.string = self.string + int((len(frame_bytes) - (len(self.string) * 8 * 8)) / 8) * '#'
                bits = list(map(int, ''.join([bin(ord(i)).lstrip('0b').rjust(8, '0') for i in self.string]))
                            )
                for i, bit in enumerate(bits):
                    frame_bytes[i] = (frame_bytes[i] & 254) | bit
                frame_modified = bytes(frame_bytes)
                with wave.open(self.output, 'wb') as fd:
                    fd.setparams(waveaudio.getparams())
                    fd.writeframes(frame_modified)
                waveaudio.close()
                self.status_label.config(text="Message hidden successfully.")
            except Exception as e:
                self.status_label.config(text="Error: " + str(e))
        else:
            self.status_label.config(text="Please fill in all fields.")
 



    def display_logo(self):
        # Load and display the logo image
        logo_image = Image.open("logo.jpg")
        logo_image = logo_image.resize((200, 156), Image.LANCZOS)
        logo_image = ImageTk.PhotoImage(logo_image)
        self.logo_label.config(image=logo_image)
        self.logo_label.image = logo_image

if __name__ == '__main__':
    root = tk.Tk()
    app = HiddenWaveGUI(root)
    root.mainloop()

    
