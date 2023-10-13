
from PIL import Image

im = Image.open("cocktail_24bit.bmp")


def convert_to_binary(text):
      #use for converting message to binary
      binary = ''
      for x in text:
            binary += format(ord(x), '08b')
      return binary
    

def find_pixels_needed(message_length):
      if message_length % 3 == 0:
            pixels_needed = int(message_length / 3)
      else:
            pixels_needed = (message_length // 3) + 1
      return pixels_needed


def compare_LSB(message_bit, least_sig_bit):
      if least_sig_bit % 2:
            least_sig_bit = 0
      else:
            least_sig_bit = 1
      if message_bit == least_sig_bit:
            return True
      else:
            return False


message = 'fi'
binary_message = convert_to_binary(message)
message_length = len(binary_message)
pixels_required = find_pixels_needed(message_length)

print(f"The message is: {message}")
print(f"This is the message in binary: {binary_message}")
print(f"The message in binary is {message_length} bits long.")
print(f"The number of pixels required to hide the message is {pixels_required}")


# puts the information from each pixel into a list
pixels = list(im.getdata())
# use splice to have a list of just the pixels required for hiding message
needed_pixels = pixels[:pixels_required]


# creates a empty list for adding pixel information in integers to
pixel_list = []
#loop over each tuple pixel to convert it to just the integer and adds it to pixel_list
for i in range(0, pixels_required):
            #convert to a string and remove extra characters
            pixel_string = str(needed_pixels[i])
            pixel_string = pixel_string.replace("(", "")
            pixel_string = pixel_string.replace(")", "")
            #split into a list of the color values
            color_values = [int(color) for color in pixel_string.split(", ")]
            pixel_list.append(color_values)
            
print("This is the cover image pixels as integers")
print(pixel_list)


#each bit in the message
for bit in range(0, message_length):
      if bit % 3 == 0:
            #compare to red value
            j = 0
      elif bit % 3 == 1:
            j = 1
            #compare to green
      elif bit % 3 == 2:
            j = 2
            #compare to blue
      match = compare_LSB(binary_message[bit], pixel_list[bit//3 - 1][j])

      if match == True:
            continue
      else:
            if binary_message[bit] == 1:
                  pixel_list[bit//3][j] = pixel_list[bit//3][j] + 1
            else:
                  pixel_list[bit//3][j] = pixel_list[bit//3][j] - 1
print("This is the steg image in pixels with hidden message")
print(pixel_list)


im.save('outputimage.bmp')






