# Hackside Out 2

## Write-up FR

Nous commençons par séparer l’image en trois canaux distincts : Rouge, Vert et Bleu.

```python
image = Image.open("captivating-painting.png")

red, green, blue = image.split()

red.save("red_channel.png")
green.save("green_channel.png")
blue.save("blue_channel.png")
```

Chaque canal révèle une partie du flag. En analysant les images dans l’ordre Rouge -> Vert -> Bleu (RGB en anglais), il est possible d’extraire et de reconstruire le flag complet.

## Write-up EN

We begin by splitting the image into three separate color channels: Red, Green, and Blue.

```python
image = Image.open("captivating-painting.png")

red, green, blue = image.split()

red.save("red_channel.png")
green.save("green_channel.png")
blue.save("blue_channel.png")
```

Each channel reveals part of the flag. By carefully inspecting the images in the order Red -> Green -> Blue (RGB), we can extract and reconstruct the full flag.

## Flag

`polycyber{VO1R_1A_v!3_En_reD_gRe3N_@nd_81u3}`
