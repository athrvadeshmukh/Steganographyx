# Import necessary libraries
from tkinter import *
from ctypes import windll
from tkinter import filedialog, messagebox
from PIL import ImageTk, Image
import subprocess
import encode
import decode
import HiddenWave
import ExWave
import os

# Define global variables to track child window states
encode_opened = False
decode_opened = False
help_opened = False
windows = True  # Set to 'False' for non-Windows environments
file_path = " "  # Store the path of the selected image

# Function to open the encoding window
def open_encode_window():
    global encode_opened
    if not encode_opened:
        encode_window = Toplevel(window)
        encode_window.title("Steganographyx - Encode")
        encode_window.geometry('800x500')
        encode_window.resizable(False, False)
        encode_window.transient(window)
        if windows:
            windll.shcore.SetProcessDpiAwareness(1)

        raw_image_label = Label(encode_window, text="Select Raw Image", height=20, width=50, relief="solid", bg="#FFFFFF")
        raw_image_label.place(x=20, y=20)

        text_to_encode_label = Label(encode_window, text="Text to Encode")
        text_to_encode_label.config(font=("Open Sans", 12))
        text_to_encode_label.place(x=400, y=20)

        text_to_encode = Text(encode_window, height=7, width=34)
        text_to_encode.config(relief="solid", font=("Open Sans", 15))
        text_to_encode.place(x=400, y=51)

        pass_to_encode_label = Label(encode_window, text="Password")
        pass_to_encode_label.config(font=("Open Sans", 12))
        pass_to_encode_label.place(x=400, y=262)

        pass_to_encode = Entry(encode_window, width=34)
        pass_to_encode.config(relief="solid", font=("Open Sans", 15), show="*")
        pass_to_encode.place(x=400, y=293)

        browse_image_btn = Button(encode_window, text="Browse Raw Image", width=29, cursor="hand2",
                                  command=lambda: browse_image(raw_image_label))
        browse_image_btn.config(font=("Open Sans", 15), bg="#36923B", fg="white", borderwidth=0)
        browse_image_btn.place(x=20, y=350)

        encode_image_btn = Button(encode_window, text="Encode", width=15, cursor="hand2",
                                  command=lambda: encode_image(file_path, pass_to_encode.get(), text_to_encode.get("1.0", END)))
        encode_image_btn.config(font=("Open Sans", 15), bg="#FF0000", fg="white", borderwidth=0)
        encode_image_btn.place(x=592, y=420)

        encode_opened = True
        encode_window.protocol("WM_DELETE_WINDOW", lambda: close_encode_window(encode_window))

# Function to save the encoded image
def save_image(stego_image):
    save_path = filedialog.asksaveasfile(initialfile="encryptstego.png", mode="wb", defaultextension=".png",
                                         filetypes=(("Image File", "*.png"), ("All Files", "*.*")))
    stego_image.save(save_path)

# Function to handle encoding
def encode_image(image_path, password, text_to_encode):
    encode_action = encode.Encode(image_path, password, text_to_encode)
    msg = encode_action.are_values_valid()
    if not msg[1]:
        messagebox.showerror("Error Encoding", msg[0])
    else:
        stego_image = encode_action.encode_into_image()
        if stego_image[1]:
            if save_image(stego_image[0]) is None:
                messagebox.showinfo("Image Saved", "Encode operation was successful.")
        else:
            messagebox.showerror("Error Encoding", stego_image[0])

def encode_audio():
    try:
        subprocess.run(["python", "HiddenWave.py"])
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

def decode_audio():
    try:
        subprocess.run(["python", "ExWave.py"])
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")


# Function to open the decoding window
def open_decode_window():
    global decode_opened
    if not decode_opened:
        decode_window = Toplevel(window)
        decode_window.title("Steganographyx - Decode")
        decode_window.geometry('800x500')
        decode_window.resizable(False, False)
        decode_window.transient(window)
        if windows:
            windll.shcore.SetProcessDpiAwareness(1)

        stego_image_label = Label(decode_window, text="Select Stego Image", height=20, width=50, relief="solid", bg="#FFFFFF")
        stego_image_label.place(x=20, y=20)

        text_to_decode_label = Label(decode_window, text="Decoded Text")
        text_to_decode_label.config(font=("Open Sans", 12))
        text_to_decode_label.place(x=400, y=20)

        text_to_decode = Text(decode_window, height=7, width=34)
        text_to_decode.config(relief="solid", font=("Open Sans", 15), state=DISABLED)
        text_to_decode.place(x=400, y=51)

        pass_to_decode_label = Label(decode_window, text="Password")
        pass_to_decode_label.config(font=("Open Sans", 12))
        pass_to_decode_label.place(x=400, y=262)

        pass_to_decode = Entry(decode_window, width=34)
        pass_to_decode.config(relief="solid", font=("Open Sans", 15), show="*")
        pass_to_decode.place(x=400, y=293)

        browse_stego_btn = Button(decode_window, text="Browse Stego Image", width=29, cursor="hand2",
                                  command=lambda: browse_image(stego_image_label))
        browse_stego_btn.config(font=("Open Sans", 15), bg="#FF0000", fg="white", borderwidth=0)
        browse_stego_btn.place(x=20, y=350)

        decode_stego_btn = Button(decode_window, text="Decode", width=15, cursor="hand2",
                                  command=lambda: decode_image(file_path, pass_to_decode.get(), text_to_decode))
        decode_stego_btn.config(font=("Open Sans", 15), bg="#36923B", fg="white", borderwidth=0)
        decode_stego_btn.place(x=592, y=420)

        decode_opened = True
        decode_window.protocol("WM_DELETE_WINDOW", lambda: close_decode_window(decode_window))

# Function to handle decoding
def decode_image(image_path, password, text_field):
    decode_action = decode.Decode(image_path, password)
    msg = decode_action.are_values_valid()
    if not msg[1]:
        messagebox.showerror("Error Decoding", msg[0])
    else:
        decoded_text = decode_action.decode_from_image()
        if decoded_text[1]:
            text_field.config(state=NORMAL)
            text_field.delete(1.0, END)
            text_field.insert(1.0, decoded_text[0])
            text_field.config(state=DISABLED)
            messagebox.showinfo("Text Decoded", "Decode operation was successful.")
        else:
            messagebox.showerror("Error Decoding", decoded_text[0])

# Function to open a file dialog and select an image
def browse_image(image_frame):
    global file_path
    file_path = filedialog.askopenfilename(title="Choose an Image",
                                           filetypes=(("Image Files", "*.png"), ("All Files", "*.*")))
    
    if file_path:
        selected_image = Image.open(file_path)
        max_width = 350
        aspect_ratio = max_width / float(selected_image.size[0])
        max_height = int((float(selected_image.size[1]) * float(aspect_ratio)))
        selected_image = selected_image.resize((max_width, max_height), Image.LANCZOS)
        selected_image = ImageTk.PhotoImage(selected_image)
        image_frame.config(image=selected_image, height=304, width=354)
        image_frame.image = selected_image

# Function to handle closing of encoding window
def close_encode_window(encode_window):
    global encode_opened
    encode_window.destroy()
    encode_opened = False

# Function to handle closing of help window
def close_help_window(help_window):
    global help_opened
    help_window.destroy()
    help_opened = False

# Function to handle closing of decoding window
def close_decode_window(decode_window):
    global decode_opened
    decode_window.destroy()
    decode_opened = False

# Function to open the help window
def help_menu():
    global help_opened
    if not help_opened:
        help_window = Toplevel(window)
        help_window.title("Help")
        help_window.geometry('650x620')
        help_window.resizable(False, False)
        help_window.transient(window)
        if windows:
            windll.shcore.SetProcessDpiAwareness(1)

        text_to_decode_label = Label(help_window, text="\n Steganographyx\nDeveloped by @athrvadeshmukh\nLinkedIn-https://www.linkedin.com/in/athrva-deshmukh\nGithub-https://github.com/athrvadeshmukh\n")
        text_to_decode_label.config(font=("Open Sans", 10))
        text_to_decode_label.pack()

        text_to_decode_label = Label(help_window,
                                     text="\nSteganographyx is an Image and Audio Steganography tool "
                                          "used to embed text messages into an Image and Audio. The "
                                          "embedded text is encrypted using the password."
                                          "\n\n 1)To encode a message into an image, click on Encode"
                                          " and select an Image. Choose a password and the text to embed."
                                          " Then click Encode to embed and save your image with the message."
                                          "\n\n 2)To decode a message from an encoded image, click Decode and select"
                                          " the encoded image, provide the password used to encode and click Decode."
                                          " Your decoded message will be displayed on the window. If the provided "
                                          "password is incorrect, the message cannot be extracted."
                                          "\n\n 3)To encode a message into an audio, click on Encode Audio"
                                          " and select an Audio. Write the text to embed."
                                          " Then click Encode to embed and save your image with the message."
                                          "\n\n 4)To decode a message from an encoded audio, click Decode/ Extract and select"
                                          " the encoded audio,click Decode."
                                          " Your decoded message will be displayed on the window. If the provided")
        text_to_decode_label.config(font=("Open Sans", 12),  justify="left", wraplength=450)
        text_to_decode_label.pack(padx=20, pady=20)

        help_opened = True
        help_window.protocol("WM_DELETE_WINDOW", lambda: close_help_window(help_window))

# Create the main window
window = Tk()
window.title("Steganographyx")
window.geometry('800x500')
window.resizable(False, False)
if windows:
    windll.shcore.SetProcessDpiAwareness(1)

# Load the logo image
logo = Image.open("icon.jpg")
logo = logo.resize((250, 250), Image.LANCZOS)
logo = ImageTk.PhotoImage(logo)
window.iconphoto(True, logo)

# Display the logo on the window
image_label = Label(window, image=logo, height=250, width=250)
image_label.pack(pady=20)

# Display the title label on the window
title_label = Label(window, text="Steganographyx")
title_label.config(font=("Open Sans", 32))
title_label.pack()

# Button for encoding
encode_btn = Button(window, text="Encode Image", height=2, width=15, bg="#FF0000", fg="white", cursor="hand2", borderwidth=0,
                    command=open_encode_window)
encode_btn.config(font=("Open Sans", 15, "bold"))
encode_btn.pack(side=LEFT, padx=10)

# Button for decoding
decode_btn = Button(window, text="Decode Image", height=2, width=15, bg="#36923B", fg="white", cursor="hand2", borderwidth=0,
                    command=open_decode_window)
decode_btn.config(font=("Open Sans", 15, "bold"))
decode_btn.pack(side=LEFT, padx=10)

encode_audio_btn = Button(window, text="Encode Audio", height=2, width=15, bg="#0066CC", fg="white", cursor="hand2", borderwidth=0, command=encode_audio)
encode_audio_btn.config(font=("Open Sans", 15, "bold"))
encode_audio_btn.pack(side=LEFT, padx=10)

decode_audio_btn = Button(window, text="Decode Audio", height=2, width=15, bg="#FF6600", fg="white", cursor="hand2", borderwidth=0, command=decode_audio)
decode_audio_btn.config(font=("Open Sans", 15, "bold"))
decode_audio_btn.pack(side=RIGHT, padx=10)


# Footer label
footer_label = Label(window, text="Developed By Athrva Deshmukh")
footer_label.pack(side=BOTTOM, pady=20)

# Create a menu bar
menu = Menu(window)
menu.add_command(label="Help", command=help_menu)
window.config(menu=menu)

# Start the main loop
window.mainloop()
