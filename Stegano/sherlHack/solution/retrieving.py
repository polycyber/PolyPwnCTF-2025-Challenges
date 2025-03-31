from PIL import Image
import numpy as np

# Load the modified images
joc1_mod = Image.open("./files/joconde1.png")
joc2_mod = Image.open("./files/joconde2.png")

# Convert images to numpy arrays
joc1_mod_array = np.array(joc1_mod)
joc2_mod_array = np.array(joc2_mod)

# Difference the two images
flag_recovered_array = joc1_mod_array - joc2_mod_array
flag_recovered = Image.fromarray(flag_recovered_array.astype(np.uint8))

# Save the recovered flag
flag_recovered.save("./solution/flag_recovered.png")


# # Alternative solution
# # Extract the LSBs from both images
# joc1_lsb = joc1_mod_array & 1
# joc2_lsb = joc2_mod_array & 1

# # Retrieve the flag bits by XORing the LSBs
# flag_bits_recovered = joc1_lsb ^ joc2_lsb

# # Scale the bits back to full intensity (0 or 255)
# flag_recovered_array = flag_bits_recovered * 255

# # Convert the numpy array back to an image
# flag_recovered = Image.fromarray(flag_recovered_array.astype(np.uint8))
