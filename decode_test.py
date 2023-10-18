from PIL import Image

img = Image.open("outputimage1234.bmp")

stego_pxls = list(img.getdata())

pxls_to_decode = stego_pxls[:6]

pxls_to_decode = [list(ele) for ele in pxls_to_decode]

binary_message = ''

for pixel in pxls_to_decode:
    for i in range(3):
        bit = 0 if pixel[i] % 2 == 0 else 1
        if bit == 0:
            binary_message += '0'
        elif bit == 1:
            binary_message += '1'

print(binary_message)

