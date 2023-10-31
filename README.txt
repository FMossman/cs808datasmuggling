Project: 
Steg Demonstration

Authors: CS808 Group L

Description:
This is a project that demonstrates 24 bit bmp steganography. 
Users can decide whether to use the program for encoding or decoding
a message.

This was created for CS808 as a demonstartion of the LSB algorithm.

Currently, the program works only with 24 bit bmp images.

Requirements:
This program uses python and the Pillow library.

How to Use the Project:
When running the program, type 'e' or 'd' to decide whether you
wish to encode or decode a message.

Encoding:
1. Enter the path to a 24 bit bmp image for use as the cover image and hit enter.
2. Enter the message in text you wish to encode and hit enter.
This will combine the payload with the cover image to create a stego-image.

Decoding:
1. Enter the path to a 24 bit bmp image with a message encoded in it and hit enter.
This will decode the message and it will be displayed in text.


