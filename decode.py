from PIL import Image


def get_msg_len(pxl):
    """find the length of the hidden message

    Inputs:
        pxl (list): pixel that store the message length

    Returns:
        int: length of the hidden message
    """
    
    msg_len = ''

    for i in range(3):
        msg_len += str(pxl[i])[-1]
    
    return int(msg_len)


def find_pixels_needed(message_length):
    """calculate the number of pixels required to store the message

      Inputs:
            msg_len (int): length of the message to be hidden

      Returns:
            int: number of pixels needed
      
      Example:
            find_pixels_needed(8) -> 6
      """
    
    if message_length % 3 == 0:
        pixels_needed = int(message_length / 3)
    else:
        pixels_needed = (message_length // 3) + 1

    return pixels_needed


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


def decode(pixel_list, msg_len):
    """get the binary message hidden in the pixels of the image

    Args:
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

            bit = 0 if rgb[i] % 2 == 0 else 1

            if bit == 1:
                binary_message += '1'
                        
            if bit == 0:
                binary_message += '0'

    return binary_message


img = Image.open("outputimage1234.bmp")

# get pixels and convert to list
stego_pxls = list(img.getdata())
stego_pxls = [list(x) for x in stego_pxls]

# get the length of the hidden message from the first pixel
hidden_msg_len = get_msg_len(stego_pxls[0])

# get the pixel list that needs to be decoded
pxls_req = find_pixels_needed(hidden_msg_len)
pxls_to_decode = stego_pxls[1 : pxls_req + 1]

# binary message
binary_msg = decode(pxls_to_decode, hidden_msg_len)

# converted to string
decoded_string = convert_bin_to_str(binary_msg)

print(f'The hidden message is : {decoded_string}')
