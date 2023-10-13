from PIL import Image
import binascii
import os
import io

#Create a secret message
message = "This is my secret message"

#Convert the secret message to binary
message = ' '.join(format(ord(x), 'b') for x in message)

# Open the Image of choice, Dump all binary of BMP file
with open("sample.bmp", "rb") as imageFile:
    f = imageFile.read()
    b = bytearray(f)
    

# BMP Header size (start of pixel data)
BMP_Header_End = 54

# Count to keep track of where we are in the secret message
count = 0

# Variable to store bit data
bit = ""

# For the total length of the secret message
for i in range(BMP_Header_End, BMP_Header_End + len(message)):
    print(count)
    # Get the LSB of the image file byte
    bit = str(b[i] & 1)

    # If the LSB is not equal to the bit of the message
    if bit != message[count]:

        # Change the byte value by 1 (effectively changing the LSB by 1)
        if b[i] == 255:
            b[i] = b[i] - 1
        else:
            b[i] = b[i] + 1

    # Move to the next character in the message
    count += 1
print(b[54:])

# Write the binary to an image file
image = Image.open(io.BytesIO(b))
image.save('my_image.bmp', 'bmp')