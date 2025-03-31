# SherlHack

## Write-up FR

Le but de ce challenge est de comparer deux images pour trouver les différences. Pour cela, nous pouvons analyser les deux images.

Il suffit de faire la différence des deux images pour obtenir le flag.

## Write-up EN

The goal of this challenge is to compare two images to find the differences. To do this, we can analyze the two images.

We just need to difference the two images to get the flag.

```python
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
```

![flag_recovered](./solution/flag_recovered.png)

## Flag

`polycyber{54CR3M0R14R7Y}`