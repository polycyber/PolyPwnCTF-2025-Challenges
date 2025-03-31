from PIL import Image
import numpy as np

# Load the images
joc1 = Image.open("./ressources/joconde.jpg")
joc2 = Image.open("./ressources/joconde.jpg")
flag = Image.open("./ressources/flag.png")

# Resize the flag to match the size of the Mona Lisa images
flag = flag.resize(joc1.size)

# Convert images to numpy arrays
joc1_array = np.array(joc1)
joc2_array = np.array(joc2)
flag_array = np.array(flag)# [:, :, :3]  # Ensure it's RGB

# Generate random bits for the LSBs of joc1
random_bits = np.random.randint(0, 2, size=joc1_array.shape, dtype=np.uint8)

# Extract the most significant bits (MSBs) from the flag
flag_bits = (flag_array >> 7) & 1  # Get the MSB of each pixel

# Create a mask to clear the LSBs
mask = np.bitwise_not(np.uint8(1))  # Equivalent to 254 in uint8

# Modify the LSBs of joc1 with random bits
joc1_array_modified = (joc1_array & mask) | random_bits

# Modify the LSBs of joc2 so that the XOR of joc1 and joc2's LSBs gives the flag bits
joc2_array_modified = (joc2_array & mask) | (random_bits ^ flag_bits)

# Convert the modified arrays back to images
joc1_modified = Image.fromarray(joc1_array_modified)
joc2_modified = Image.fromarray(joc2_array_modified)

# Save the modified images
joc1_modified.save("./files/joconde1.png")
joc2_modified.save("./files/joconde2.png")
