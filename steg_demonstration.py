"""
This program can take a 24bmp image and hide a text message 
inside it using the LSB algorithm or take a stego-image 
and extract a hidden message.
"""

from PIL import Image

def convert_to_binary(text):
    """converts string to binary
    Inputs:
        text (str): text that needs to be converted
    Returns:
        str: binary value of text
    Example:
        convert_to_binary('h') -> '01101000'
    """

    binary = ''
    for x in text:
        binary += format(ord(x), '08b')
    return binary


def find_pixels_needed(msg_len):
    """calculate the number of pixels required to store the message
    Inputs:
        msg_len (int): length of the message to be hidden
    Returns:
        int: number of pixels needed
    Example:
        find_pixels_needed(8) -> 6
    """

    if msg_len % 3 == 0:
        pixels_needed = int(msg_len / 3)
    else:
        pixels_needed = (msg_len // 3) + 1
    return pixels_needed


def change_lsb(pixel_list, message):
    """changes the LSB of the RGB values in pixels to store the message in binary form
    Inputs:
        pixel_list (list): list containing sublist containing RGB value of the pixel
        message (str): binary message that needs to be hidden
    Returns:
        list: list of lists which contains the modified pixels with binary message
    Example:
        change_lsb([[37, 37, 35], [37, 37, 35], [37, 37, 35], [38, 38, 36]], '01101000') 
        -> [[36, 37, 35], [36, 37, 34], [36, 36, 36], [38, 38, 36]]
    """

    binary_message = [int(x) for x in str(message)]

    new_rgb = []  # list of rbg vals [37, 37, 35]
    new_pixels = []  # list of modified pixels  [[37, 37, 35], [37, 36, 34]...]

    for rgb in pixel_list:
        new_rgb.clear()

        # modified rgb values
        for i in range(3):
            if len(binary_message) == 0:
                # full message hidden, fill the remaining rgb list with original values and exit the loop
                new_rgb += pixel_list[-1][len(new_rgb):]
                break

            # least sig bit will be 0 if rgb val even, 1 if rgb val odd
            lsb = 0 if rgb[i] % 2 == 0 else 1

            if binary_message[0] == lsb:
                # message bit is same as least sig bit
                new_rgb.append(rgb[i])
                binary_message.pop(0)
                continue
            else:
                # add 1 to rgb value
                new_rgb.append(rgb[i] + 1)
                binary_message.pop(0)         

        # store the pixel in list
        new_pixels.append(list(new_rgb))
    return new_pixels


def extract(pixel_list, msg_len):
    """get the binary message hidden in the pixels of the image
    Inputs:
        pixel_list (list): list of pixels that contain the hidden message
        msg_len (int): the length of the hidden message
    Returns:
        str: the binary message
    """

    binary_message = ''

    for rgb in pixel_list:
        for i in range(3):
            if len(binary_message) == msg_len:
                # all letters converted, exit loop
                break
                  
            # bit is 0 if rgb value is even, 1 if rgb is odd
            bit = 0 if rgb[i] % 2 == 0 else 1

            if bit == 1:
                binary_message += '1'
            if bit == 0:
                binary_message += '0'
    return binary_message

def convert_bin_to_str(binary_msg):
    """convert from binary back to string
    Inputs:
        binary_msg (str): binary message
    Returns:
        str: decoded string
    """

    decoded_string = ''

    # take groups of 8 bits for each letter
    for i in range(0, len(binary_msg), 8):
        letter = binary_msg[i : i + 8]  
        dec_letter = int(letter, 2)  # '01101000' --> 104
        str_letter = chr(dec_letter)  # 104 --> 'h'
        decoded_string += str_letter
    return decoded_string


# determines if user want to encode or decode 
while True:
    mode = input("Would you like to encode(e) a message or decode(d) a message? (e or d): ")
    if mode.lower() == 'e':
        encode = True
        break
    elif mode.lower() == 'd':
        encode = False
        break


# encode the message to an image
if encode:
    while True:
        image_name = input('Enter the name of the image file you want to encode:')
        try:
            img = Image.open(image_name)
            # Check if image is 24 bit bmp
            if img.format.lower() == 'bmp' and img.mode.lower() == 'rgb':
                break
            else:
                print('Invalid file. Please select a 24 bit BMP image')
        except:
            print('File does not exist. Select a file in the directory!')

    # get list of pixels. The list does not contain the header info and pixel info is in tuples
    original_pxls = list(img.getdata())

    while True:
        message = input('Enter your text for encoding: ')
        binary_msg = convert_to_binary(message)
        msg_len = len(binary_msg)
        required_pxls = find_pixels_needed(msg_len) + 5  # five extra pixel used to store length of the message  
        if len(original_pxls) < required_pxls:
            print("The message is too long to hide!")
        elif msg_len > 32767:
            print("The message is too long to hide!")
        else:
            # convert length of message to binary, pad it out to 15 digits
            msg_len_binary = format(int(msg_len), 'b')
            msg_len_binary = msg_len_binary.rjust(15, '0')
            break

    # get list of first pixels for hiding length, convert to list of lists
    length_pixels = original_pxls[:5]
    length_pixels = [list(x) for x in length_pixels]
    # convert first five pixels to store length
    length_pixels = change_lsb(length_pixels, msg_len_binary)

    # get list of pixels that need to be modified, convert to list of lists
    pxls_to_modify = original_pxls[5:required_pxls]
    pxls_to_modify = [list(x) for x in pxls_to_modify]
    # convert pixels to store message and add pixels hiding length
    modified_pxls = change_lsb(pxls_to_modify, binary_msg)
    modified_pxls = length_pixels + modified_pxls

    # convert modified pixels back to list of tuples
    modified_pxls = [tuple(x) for x in modified_pxls]

    # add coded pixels back into image
    img.putdata(modified_pxls)

    # save the steg image
    img.save(f'{image_name[:-4]}_encoded.bmp')
    print('Operation Successful! Your message has been hidden in the image')
    print(f'Message hidden in {image_name[:-4]}_encoded.bmp')


# decode the message from an image
else:
    while True:
        image_name = input('Enter the name of the image file you want to decode:')
        try:
            img = Image.open(image_name)
            # Check if image is 24 bit bmp
            if img.format.lower() == 'bmp' and img.mode.lower() == 'rgb':
                break
            else:
                print('Invalid file. Please select a 24 bit BMP image with hidden message')
        except:
            print('File does not exist. Select a file in the directory!')

    # get pixels and convert to list
    stego_pxls = list(img.getdata())
    stego_pxls = [list(x) for x in stego_pxls]

    # get the length of the hidden message from first 5 pixels and convert to decimal
    hidden_msg_len = extract(stego_pxls[:5], 15)
    hidden_msg_len = int(hidden_msg_len, 2)

    # get the pixel list that needs to be decoded
    pxls_req = find_pixels_needed(hidden_msg_len)
    pxls_to_decode = stego_pxls[5 : pxls_req + 5]

    # extract binary message
    binary_msg = extract(pxls_to_decode, hidden_msg_len)

    # converted to string and print
    decoded_string = convert_bin_to_str(binary_msg)
    print(f'The hidden message is : {decoded_string}')
