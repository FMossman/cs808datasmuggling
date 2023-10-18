
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


def check_color_to_compare(bit):
      # determines whether to compare bit to red, green or blue value
      if bit % 3 == 0:
            #compare to red value
            color = 0
      elif bit % 3 == 1:
            color = 1
            #compare to green
      elif bit % 3 == 2:
            color = 2
            #compare to blue
      return color


def compare_LSB(message_bit, least_sig_bit):
      # compares a bit of the message to the corresponding LSB from the image
      if least_sig_bit % 2 == 0:
            least_sig_bit = 0
      else:
            least_sig_bit = 1
      if int(message_bit) == least_sig_bit:
            return True
      else:
            return False



mode = ''
while mode != 'h' or mode != 'r':
      mode = input("Would you like to hide (h) a message in an image or retreive (r) a message from a picture? ( h or r )")
      print(mode)


message = input('Enter your text for encoding: ')
binary_message = convert_to_binary(message)
message_length = len(binary_message)
pixels_required = find_pixels_needed(message_length)

img = Image.open("cocktail_24bit.bmp")

# puts the tuple information from each pixel into a list
all_pixels = list(img.getdata())

while len(all_pixels) < pixels_required:
      print("The message is too long to hide!")
      # could this be changed to ask for message again?
      quit()
# use splice to have a list of just the pixels required for hiding message
needed_pixel = all_pixels[:pixels_required]

# get the pixel information as lists of integers
pixel_list = get_pixel_ints(pixels_required, needed_pixels)


# loops over each bit in the message and compares to LSB and changes bit if required
for bit in range(0, message_length):
      color = check_color_to_compare(bit)
      match = compare_LSB(binary_message[bit], pixel_list[bit//3][color])
      if match == True:
            continue
      else:
            if int(binary_message[bit]) == 1:
                  pixel_list[bit//3][color] = pixel_list[bit//3][color] + 1
            else:
                  pixel_list[bit//3][color] = pixel_list[bit//3][color] - 1

# convert pixels of steg image back to tuples
pixel_tuples = []
for pixel in pixel_list:
      pixel_tuples.append(tuple(pixel))


# add coded pixels back into image
img.putdata(pixel_tuples)

# save the steg image
img.save('outputimage.bmp')