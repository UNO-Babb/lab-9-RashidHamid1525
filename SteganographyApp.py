# Lab 9 - CIST 1600
# Steganography App
# This app will encode or decode text messages in an image file.
# The app will use RGB channels so only PNG files will be accepted.
# This technique will focus on Least Significant Bit (LSB) encoding.

from PIL import Image
import os

def numberToBinary(num):
    """Takes a base10 number and converts it to an 8-bit binary string."""
    # Convert number to binary and pad with leading zeros to 8 bits
    binary = format(num, '08b')
    return binary

def binaryToNumber(binStr):
    """Takes a binary string and converts it to a base10 integer."""
    decimal = int(binStr, 2)
    return decimal


def encode(img, msg):
    """
    Encodes a text message inside an image using LSB steganography.
    Each letter uses 3 pixels (9 color channels total, but only 8 bits are used).
    """
    pixels = img.load()  # pixels is a 2D list of pixel data
    width, height = img.size
    letterSpot = 0
    pixel = 0
    letterBinary = ""
    msgLength = len(msg)

    # Store message length in the red value of the first pixel
    red, green, blue = pixels[0, 0]
    pixels[0, 0] = (msgLength, green, blue)

    # Encode each character
    for i in range(msgLength * 3):
        x = i % width
        y = i // width

        red, green, blue = pixels[x, y]
        redBinary = numberToBinary(red)
        greenBinary = numberToBinary(green)
        blueBinary = numberToBinary(blue)

        if pixel % 3 == 0:
            letterBinary = numberToBinary(ord(msg[letterSpot]))
            # Ignore red on the first pixel of each letter
            greenBinary = greenBinary[0:7] + letterBinary[0]
            blueBinary = blueBinary[0:7] + letterBinary[1]

        elif pixel % 3 == 1:
            redBinary = redBinary[0:7] + letterBinary[2]
            greenBinary = greenBinary[0:7] + letterBinary[3]
            blueBinary = blueBinary[0:7] + letterBinary[4]

        else:
            redBinary = redBinary[0:7] + letterBinary[5]
            greenBinary = greenBinary[0:7] + letterBinary[6]
            blueBinary = blueBinary[0:7] + letterBinary[7]
            letterSpot += 1

        # Convert binary values back to integers
        red = binaryToNumber(redBinary)
        green = binaryToNumber(greenBinary)
        blue = binaryToNumber(blueBinary)

        pixels[x, y] = (red, green, blue)
        pixel += 1

    # Save encoded image
    img.save("secretImg.png", "png")
    print("✅ Message encoded successfully as 'secretImg.png'.")


def decode(img):
    """
    Decodes and returns the hidden text message from an image.
    Reads the least significant bits of each color channel.
    """
    msg = ""
    pixels = img.load()
    red, green, blue = pixels[0, 0]
    msgLength = red  # message length stored here

    width, height = img.size
    pixel = 0
    letterBinary = ""
    x = 0
    y = 0

    while len(msg) < msgLength:
        red, green, blue = pixels[x, y]
        redBinary = numberToBinary(red)
        greenBinary = numberToBinary(green)
        blueBinary = numberToBinary(blue)

        if pixel % 3 == 0:
            letterBinary = greenBinary[7] + blueBinary[7]

        elif pixel % 3 == 1:
            letterBinary = letterBinary + redBinary[7] + greenBinary[7] + blueBinary[7]

        else:
            letterBinary = letterBinary + redBinary[7] + greenBinary[7] + blueBinary[7]
            letterAscii = binaryToNumber(letterBinary)
            msg += chr(letterAscii)

        pixel += 1
        x = pixel % width
        y = pixel // width

    return msg


def main():
    print("=== Steganography App ===")
    print("This app encodes or decodes hidden text messages inside PNG images.")
    choice = input("Would you like to (E)ncode or (D)ecode? ").lower().strip()

    if choice == "e":
        filename = input("Enter image filename (PNG only): ").strip()
        if not filename.lower().endswith(".png"):
            print("❌ Only PNG files are supported.")
            return

        if not os.path.exists(filename):
            print("❌ File not found.")
            return

        img = Image.open(filename)
        msg = input("Enter your secret message: ")
        encode(img, msg)
        img.close()

    elif choice == "d":
        filename = input("Enter encoded image filename: ").strip()
        if not os.path.exists(filename):
            print("❌ File not found.")
            return

        img = Image.open(filename)
        hidden_message = decode(img)
        img.close()
        print("💬 Hidden message found:")
        print(hidden_message)

    else:
        print("Invalid option. Please enter E or D.")


if __name__ == '__main__':
    main()
