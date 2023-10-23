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


def len_in_binary(msg_len):
      """modifies a pixel to store the length of the hidden message.
      Changes the last digits of the RGB values to match the message length

      Inputs:
            msg_len (int): length of message to be hidden
            pxl_to_modify (list): RGB pixel that needs to be modified

      Returns:
            list: modified pixel value with info on message length
      
      Example:
            store_len_in_pxl(16, [37, 37, 35]) -> [30, 31, 36] \n
            store_len_in_pxl(8, [37, 37, 35]) -> [30, 30, 38]
      """

      binary_length = format(msg_len, '015b')

      return binary_length


def change_lsb(pixel_list, message):
      """Changes the least significant bit of the RGB values in pixels to store the message in binary form

      Inputs:
            pixel_list (list): list containing sublist containing RGB value of the pixel
            message (str): binary message that needs to be hidden

      Returns:
            list: list of lists which contains the modified pixels with binary message
      
      Example:
            change_lsb([[37, 37, 35], [37, 37, 35], [37, 37, 35], [38, 38, 36]], '01101000') -> [[36, 37, 35], [36, 37, 34], [36, 36, 36], [38, 38, 36]]
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

                  lsb = 0 if rgb[i] % 2 == 0 else 1  # least sig bit will be 0 if rgb val even, 1 if rgb val odd

                  if binary_message[0] == lsb:
                        # message bit is same as least sig bit
                        new_rgb.append(rgb[i])
                        binary_message.pop(0)
                        continue

                  elif binary_message[0] == 1:
                        #add 1 to rgb value
                        new_rgb.append(rgb[i] + 1)
                        binary_message.pop(0)
                              
                  elif binary_message[0] == 0:
                        #subtract 1 from rgb value
                        new_rgb.append(rgb[i] - 1)
                        binary_message.pop(0)

                  
            # store the pixel in list
            new_pixels.append(list(new_rgb))


      return new_pixels




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









img = Image.open("cocktail_24bit.bmp")

#list of pixels. The list does not contain the header info
original_pxls = list(img.getdata())

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

        message = input('Enter your text for encoding: ')

        binary_msg = convert_to_binary(message)

        msg_len = len(binary_msg)

        required_pxls = find_pixels_needed(msg_len) + 5  # one extra pixel used to store length of the message
        
        if len(original_pxls) < required_pxls:
                print("The message is too long to hide!")
        elif msg_len > 32767:
                print("The message is too long to hide!")
        else:
                break
        

    # get list of pixels that need to be modified, convert to list of lists
    pxls_to_modify = original_pxls[:required_pxls]
    pxls_to_modify = [list(x) for x in pxls_to_modify]

    # store the length of message in the first pixel
    binary_msg = len_in_binary(msg_len) + binary_msg


    modified_pxls = change_lsb(pxls_to_modify, binary_msg)

    # convert modified pixels back to list of tuples
    modified_pxls = [tuple(x) for x in modified_pxls]

    # testing
    print(f'Message in binary: {binary_msg}')
    print(f'Orginal pixels: {pxls_to_modify}')
    print(f'List of changed pixels: {modified_pxls}')



    # add coded pixels back into image
    img.putdata(modified_pxls)

    # save the steg image
    img.save('outputimage1234.bmp')
    print('Operation Successful! Your message has been hidden in the image')


# decode the message from an image
else:

    while True:

        steg_file = input('Please enter your file name: ')
        try:
            steg_img = Image.open(steg_file)
            break
        except: 
            print("The path does not lead to a image.")
        

    

    # get pixels and convert to list
    stego_pxls = list(steg_img.getdata())
    stego_pxls = [list(x) for x in stego_pxls]

    # get the length of the hidden message from the first pixel
    hidden_msg_len = decode(stego_pxls, 15)
    print(f"Message length in binary: {hidden_msg_len}")
    binary_length = int(hidden_msg_len, 2)
    print(f"Message length in decimal: {binary_length}")
    # get the pixel list that needs to be decoded
    pxls_req = find_pixels_needed(binary_length)
    # TODO
    pxls_to_decode = stego_pxls[5: pxls_req+4]

    # binary message
    binary_msg = decode(pxls_to_decode, hidden_msg_len)

    # converted to string
    decoded_string = convert_bin_to_str(binary_msg)

    print(f'The hidden message is : {decoded_string}')