#!/usr/bin/env python3

# polycyber{3D4_S4YS_TH4NKS}

import argparse
import struct

def swap_dimensions(bmp_data):
    """
    Swap the width and height fields in the BMP header.
    (For BITMAPINFOHEADER, width is at offset 18 and height at offset 22.)
    """
    # Unpack width and height (4 bytes each, little-endian unsigned int)
    width = struct.unpack_from('<I', bmp_data, 18)[0]
    height = struct.unpack_from('<I', bmp_data, 22)[0]
    print(f"[swap_dimensions] Original width: {width}, height: {height}")

    # Pack the swapped values back
    struct.pack_into('<I', bmp_data, 18, height)
    struct.pack_into('<I', bmp_data, 22, width)
    print(f"[swap_dimensions] Swapped width: {height}, height: {width}")

    return bmp_data

def change_bit_depth(bmp_data, new_bit_depth):
    """
    Change the bit depth (biBitCount) in the header without altering the pixel data.
    The bit depth field is 2 bytes at offset 28.
    """
    old_bit_depth = struct.unpack_from('<H', bmp_data, 28)[0]
    print(f"[change_bit_depth] Original bit depth: {old_bit_depth}")

    struct.pack_into('<H', bmp_data, 28, new_bit_depth)
    print(f"[change_bit_depth] New bit depth: {new_bit_depth}")

    return bmp_data

def redden_image(bmp_data):
    """
    Increase the red channel value of every pixel.
    This function currently assumes a 24-bit BMP (each pixel is 3 bytes: B, G, R)
    and properly handles per-row padding.
    """
    # Get the offset to pixel data from the BMP file header (4 bytes at offset 10)
    pixel_offset = struct.unpack_from('<I', bmp_data, 10)[0]

    # Read image dimensions and bit depth from the BITMAPINFOHEADER
    width = struct.unpack_from('<I', bmp_data, 18)[0]
    height = struct.unpack_from('<I', bmp_data, 22)[0]
    bit_depth = struct.unpack_from('<H', bmp_data, 28)[0]
    print(f"[redden_image] Image dimensions: {width}x{height}, Bit depth: {bit_depth}")

    # This implementation supports only 24-bit images.
    if bit_depth != 24:
        print("Error: redden_image currently supports only 24-bit BMP images.")
        return bmp_data

    # Calculate the row size in bytes (each row is padded to a multiple of 4 bytes)
    row_size = ((bit_depth * width + 31) // 32) * 4

    # BMP images are stored bottom-up (the first row in the file is the bottom row).
    # Iterate over each row and each pixel in the row.
    for row in range(height):
        row_start = pixel_offset + row * row_size
        for col in range(width):
            # Each pixel is 3 bytes: blue, green, red.
            pixel_index = row_start + col * 3
            # Read original pixel values
            blue = bmp_data[pixel_index]
            green = bmp_data[pixel_index + 1]
            red = bmp_data[pixel_index + 2]

            # Increase the red channel (saturate at 255)
            # new_red = min(red + 50, 255)
            new_blue = (blue-blue%2)
            new_green = (green-green%2)
            new_red = min((red+100-red%2), 254)
            # if red == 255:
            #     print(red)
            #     new_red = 255
            # else:
            #     # new_red = red-red%4
            #     new_red = red//2
            bmp_data[pixel_index + 0] = new_blue
            bmp_data[pixel_index + 1] = new_green
            bmp_data[pixel_index + 2] = new_red

    print("[redden_image] Finished processing pixels to add red tint.")
    return bmp_data

def main():
    parser = argparse.ArgumentParser(
        description="Modify a BMP image header (or pixel data) for a CTF challenge."
    )
    parser.add_argument("input", help="Input BMP file")
    parser.add_argument("output", help="Output BMP file")
    parser.add_argument("--swap", action="store_true",
                        help="Swap the width and height in the header (without changing image data)")
    parser.add_argument("--depth", type=int,
                        help="Change the bit depth in the header to the given value (without changing image data)")
    parser.add_argument("--red", action="store_true",
                        help="Increase the red channel of every pixel in the image")

    args = parser.parse_args()

    # Read the BMP file into a mutable bytearray
    with open(args.input, "rb") as f:
        bmp_data = bytearray(f.read())

    # Apply modifications according to the flags provided
    if args.swap:
        bmp_data = swap_dimensions(bmp_data)

    if args.depth is not None:
        bmp_data = change_bit_depth(bmp_data, args.depth)

    if args.red:
        bmp_data = redden_image(bmp_data)

    # Write the modified BMP data to the output file
    with open(args.output, "wb") as f:
        f.write(bmp_data)

    print("Modifications complete. Output written to:", args.output)

if __name__ == "__main__":
    main()
