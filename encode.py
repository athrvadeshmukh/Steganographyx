import hashlib
import os.path
import numpy as np
from Crypto.Cipher import AES
from PIL import Image


# class Encode to handle encoding activities
class Encode:
    # Parameterized constructor to receive image path,
    # password and text to be encoded while object initialization
    def __init__(self, image_path, password, text_to_encode):
        self.image_path = image_path
        self.password = password.strip()
        self.text_to_encode = text_to_encode.strip()

    # method to check if the supplied password is valid
    # returns true if the password is valid else returns false
    def is_password_valid(self):
        # checking if the password is empty
        if len(self.password) == 0:
            return False
        return True

    # method to check if the supplied text to be encoded is valid
    # returns true if the text is valid else returns false
    def is_text_valid(self):
        # checking if the given text to encode is empty
        if len(self.text_to_encode) == 0:
            return False
        return True

    # method to check if the supplied path of the image is valid and image exists
    # returns true if the path is valid else returns false
    def is_image_path_valid(self):
        # checking if the image exists on given path
        if os.path.exists(self.image_path):
            return True
        return False

    # method to get binary value of the supplied text to be encoded
    # returns the binary equivalent of the given text
    def get_text_binary(self):
        # generating a 32 bytes hex key from the provided password in order to use it as aes secret key
        secret_key = hashlib.sha1(str(self.password).encode()).hexdigest()[:32]
        # creating an PyCrypto AES object for encryption
        encryption_key = AES.new(secret_key.encode('utf-8'), AES.MODE_EAX, secret_key.encode())
        # generating encrypted text using the AES object and the text to be encoded
        # returns encrypted bytes
        encrypted_text = encryption_key.encrypt(self.text_to_encode.encode('utf-8'))
        # converting encrypted bytes object into string for ease
        encrypted_text = str(encrypted_text)
        # appending a delimiter text into the encrypted string to indicate termination of hidden text
        encrypted_text += "$@&#"
        # generating binary value from the encrypted string
        # the ord function converts each character of encrypted string into its unicode equivalent
        # the format function formats encrypted character's unicode value it into binary bits
        # the join function joins binary value of each character on loop
        binary_value = ''.join([format(ord(character), "08b") for character in encrypted_text])
        return binary_value

    # method to hide/encode the encrypted binary data into the image
    # This is the main method where image pixels are modified to insert our hidden message
    def encode_into_image(self):
        try:
            # reading the image in read only mode from the supplied path
            raw_image = Image.open(self.image_path, 'r')
            # getting the size of the image, required when exporting encoded image at last
            # returns a tuple with width and height
            width, height = raw_image.size
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
            # getting the binary data to be encoded
            binary_value = self.get_text_binary()
            # generating a 5-digit hash value to identify the pixel to start the encoding from
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
                                return ['Image size is not sufficient to encode the given text.', False]
            # getting the size of the binary data to encode
            text_size = len(binary_value)
            # getting the total space available to encode after the position is defined by hash
            encode_space = image_size - int(secret_hash)
            # if the encode space is not sufficient to encode the image,
            # defining a boolean to indicate that encoding must be continued from starting pixel
            retro_encode = False
            if text_size > encode_space:
                retro_encode = True
            # checking if the size of the image is sufficient to encode the given text
            if text_size > image_array.size:
                return ['Image size is not sufficient to encode the given text.', False]
            else:
                # setting a local variable to point to the binary value to encode in each iteration
                bin_index = 0
                # looping over each pixel of the image
                for pixel in range(int(secret_hash), image_size):
                    # looping over each channel of a single pixel of the image
                    for channel in range(0, channels):
                        # tracking binary index to check if it exceeds the size
                        if bin_index < text_size:
                            # modifying the least significant bit (LSB) of the channel or
                            # replacing the last binary value of the selected channel
                            # with value of selected binary index
                            # the bin() function converts the integer value of selected channel into binary
                            # the [2:9] slicing extracts all the bits leaving LSB and '0b' at beginning
                            # the LSB is appended from the binary value of the text
                            # the int() function converts the binary value (base 2) back to integer
                            image_array[pixel, channel] = int(bin(image_array[pixel][channel])[2:9] +
                                                              binary_value[bin_index], 2)
                            # increasing bin_index value to point to next value to encode
                            bin_index += 1

                # Encoding the left bits of the data from the beginning
                if retro_encode:
                    # looping over each pixel of the image from start
                    for pixel in range(int(secret_hash)):
                        for channel in range(0, channels):
                            if bin_index < text_size:
                                image_array[pixel, channel] = int(bin(image_array[pixel][channel])[2:9] +
                                                                  binary_value[bin_index], 2)
                                bin_index += 1

                # reshaping the image array into the image's original dimensions
                image_array = image_array.reshape(height, width, channels)
                # converting the modified image array back to visual image using PIL fromarray function
                # the numpy astype function defines the datatype to cast into -
                # which is unassigned 8-bit integer ranging from 0-255 (uint8) in this case
                stego_image = Image.fromarray(image_array.astype('uint8'), raw_image.mode)
                # returning the encoded image with boolean status value
                return [stego_image, True]
        except Exception:
            return ['Unidentified Error. The possible reasons might be\n'
                    '\n1. Unsupported Image File'
                    '\n2. Invalid text characters', False]

    # method to check for all the supplied values and pass the error messages accordingly
    # returns status and message for validity check
    def are_values_valid(self):
        # calling above methods one by one to check if password, image path and given text are valid
        if not self.is_password_valid():
            return ["Password can't be empty.", False]
        elif not self.is_text_valid():
            return ["Text to encode can't be empty.", False]
        elif not self.is_image_path_valid():
            return ["Selected image doesn't exist anymore.", False]
        else:
            return ["Validated", True]