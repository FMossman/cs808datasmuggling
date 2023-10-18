from PIL import Image


def convert_to_binary(text):
      # converts message to binary
      binary = ''
      for x in text:
            binary += format(ord(x), '08b')
      return binary


def find_pixels_needed(message_length):
      # calculates the number of pixels required to hide message
      if message_length % 3 == 0:
            pixels_needed = int(message_length / 3)
      else:
            pixels_needed = (message_length // 3) + 1
      return pixels_needed


def get_pixel_ints(pixels_required, needed_pixels):
      # converts the pixels in tuples to lists of integers
      pixel_list = []
      for i in range(0, pixels_required):
            color_values = list(needed_pixels[i])
            pixel_list.append(color_values)
      return pixel_list


def change_lsb(pixel_list, message):

    binary_message = [int(x) for x in str(message)]
    
    new_rgb = []
    new_pixels = []

    for rgb in pixel_list:
        

      new_rgb.clear()
      for i in range(3):

            lsb = 0 if rgb[i] % 2 == 0 else 1

            if binary_message[0] == lsb:
                  new_rgb.append(rgb[i])
                  binary_message.pop(0)
                  continue

            elif binary_message[0] == 1:
                  #add 1 to rgb value
                  new_rgb.append(rgb[i] + 1)
                        
            elif binary_message[0] == 0:
                  #subtract 1 from rgb value
                  new_rgb.append(rgb[i] - 1)

            binary_message.pop(0)

            new_pixels.append(list(new_rgb))


            return new_pixels



img = Image.open("cocktail_24bit.bmp")

original_pxls = list(img.getdata())

while True:

      message = input('Enter your text for encoding: ')

      binary_message = convert_to_binary(message)
      message_length = len(binary_message)
      required_pxls = find_pixels_needed(message_length)

      if len(original_pxls) < required_pxls:
            print("The message is too long to hide!")
      else:
            break
    


pxls_to_modify = original_pxls[:required_pxls]
pxls_to_modify = [list(ele) for ele in pxls_to_modify]

modified_pixels = change_lsb(pxls_to_modify, binary_message)

modified_img = modified_pixels + original_pxls[required_pxls:]

modified_img = [tuple(ele) for ele in modified_img]


# # add coded pixels back into image
img.putdata(modified_img)

# # save the steg image
img.save('outputimage1234.bmp')
