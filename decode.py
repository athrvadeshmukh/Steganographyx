import hashlib
import os.path
import numpy as np
from Crypto.Cipher import AES
from PIL import Image


# class Decode to handle decoding activities
class Decode:
    # Parameterized constructor to receive image path and password while object initialization
    def __init__(self, image_path, password):
        self.image_path = image_path
        self.password = password.strip()

    # method to check if the supplied password is valid
    # returns true if the password is valid else returns false
    def is_password_valid(self):
        # checking if the password is empty
        if len(self.password) == 0:
            return False
        return True
    

    # method to check if the supplied path of the image is valid and image file exists
    # returns true if the path is valid else returns false
    def is_image_path_valid(self):
        # checking if the image exists on given path
        if os.path.exists(self.image_path):
            return True
        return False

    def get_decoded_text(self, bytes_string):
        # generating a 32 bytes hex key from the provided password in order to use it as aes secret key
        secret_key = hashlib.sha1(str(self.password).encode()).hexdigest()[:32]
        # creating new PyCrypto AES object to decrypt the converted bytes
        decryption_key = AES.new(secret_key.encode('utf-8'), AES.MODE_EAX, secret_key.encode())
        # converting extracted bytes string into bytes
        # the eval function evaluates or runs the python expression operation for bytes string
        bytes_value = eval(bytes_string)
        # decrypting and returning the extracted text
        return decryption_key.decrypt(bytes_value).decode('utf-8')

    # method to extract the encoded binary data from the image
    # this is the main decoding method where each image pixels are analyzed to extract hidden data
    def decode_from_image(self):
        try:
            # reading the image in read only mode from the supplied path
            raw_image = Image.open(self.image_path, 'r')
            # considering the image type as RGB by default and setting channels value to 3
            channels = 3
            # identifying the channels and updating channels value to 4 for RGBA images
            if raw_image.mode == 'RGBA':
                channels = 4
            # converting uploaded image into a numpy array to manipulate pixels
            # the getdata() method from PIL returns an iterable image object
            # the list method converts the iterable image pixels object into a list
            # the returned list is converted to numpy array
            image_array = np.array(list(raw_image.getdata()))
            # getting the size of the image or the total number of all channels in the image
            # performing the floor division to get the total number of pixels in the image
            image_size = image_array.size // channels
            # generating a 5-digit hash value to identify the pixel to start the decoding from
            secret_hash = str(int(hashlib.md5(self.password.encode('utf-8')).hexdigest(), 16))[:5]
            # checking if the generated hash number exceeds the number of pixels in the image
            # if yes, stripping down the generated hash number by one digit and re-verifying
            if int(secret_hash) > image_size:
                secret_hash = secret_hash[:4]
                if int(secret_hash) > image_size:
                    secret_hash = secret_hash[:3]
                    if int(secret_hash) > image_size:
                        secret_hash = secret_hash[:2]
                        if int(secret_hash) > image_size:
                            secret_hash = secret_hash[:1]
                            if int(secret_hash) > image_size:
                                return ["Encoded text not found. The possible reasons might be:\n"
                                        "\n1. Incorrect Password"
                                        "\n2. Wrong Image", False]
            # defining a variable to store the extracted binary value
            binary_value = ""
            # looping over each pixel of the image from hash generated pixel number
            for pixel in range(int(secret_hash), image_size):
                # looping over each channel in a single pixel of the image
                for channel in range(0, channels):
                    # appending the LSB of each channel value
                    binary_value += bin(image_array[pixel][channel])[-1]

            # looping over each pixel from the beginning in case retro encoding is applied
            for pixel in range(int(secret_hash)):
                for channel in range(0, channels):
                    binary_value += bin(image_array[pixel][channel])[-1]

            # converting the extracted binary value into list of binary values
            # where each element of the list contains a byte or 8-bits binary value
            binary_list = [binary_value[value:value + 8] for value in range(0, len(binary_value), 8)]
            # defining a variable to store the decoded text from binary
            decoded_text = ""
            # looping over the list of binary values to extract the decoded text
            for i in range(len(binary_list)):
                # checking if the decoded text contains delimiter value
                # breaking the loop if value is found
                if decoded_text[-4:] == "$@&#":
                    break
                else:
                    # converting each byte of the binary list into text and appending them
                    # the int function converts each byte in the list to its integer equivalent
                    # the chr function decodes each integer value into its equivalent unicode character
                    decoded_text += chr(int(binary_list[i], 2))

            # Checking again if the decoded text contains delimiter characters and slicing them if found
            if "$@&#" in decoded_text:
                # slicing the delimiter characters and extracting only encrypted text
                decoded_text = decoded_text[:-4]
                # calling function to get the decrypted plain text from the decoded bytes string
                try:
                    decoded_text = self.get_decoded_text(decoded_text)
                    # returning decoded plain text with status
                    return [decoded_text, True]
                except UnicodeDecodeError:
                    # returning error message if the text is not found
                    return ["Encoded text not found. The possible reasons might be:\n"
                            "\n1. Incorrect Password"
                            "\n2. Wrong Image", False]
            else:
                # returning error message if the text is not found
                return ["Encoded text not found. The possible reasons might be:\n"
                        "\n1. Incorrect Password"
                        "\n2. Wrong Image", False]
        except Exception:
            return ["Encoded text not found. The possible reasons might be:\n"
                    "\n1. Incorrect Password"
                    "\n2. Wrong Image", False]

    # method to check for all the supplied values and pass the error messages accordingly
    # returns status and message for validity check
    def are_values_valid(self):
        # calling above methods one by one to check if password and image path are valid
        if not self.is_password_valid():
            return ["Password can't be empty.", False]
        elif not self.is_image_path_valid():
            return ["Selected image doesn't exist anymore.", False]
        else:
            return ["Valid", True]