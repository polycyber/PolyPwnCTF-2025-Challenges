from PIL import Image, ImageDraw, ImageFont
import numpy as np
from scipy.io.wavfile import write

msg = """Come alone... or the Gotham Academy will burn.
polycyber{Wayne_Tower_22_30}.
HAHAHA! You're too slow.
The game starts now. TIC TAC TIC TAC

- The Joker"""

sample_rate = 10e6
symbole_rate = 50e3

def generate_image_with_text(text, output_filename="output.png", image_size=(800, 400)):
    # Générer une image avec un dégradé de couleur et du texte centré
    img = Image.new('RGB', image_size)
    draw = ImageDraw.Draw(img)
    
    start_color = (0, 50, 0) 
    end_color = (128, 0, 128)  
    
    for x in range(img.width):
        ratio = x / img.width
        r = int(start_color[0] * (1 - ratio) + end_color[0] * ratio)
        g = int(start_color[1] * (1 - ratio) + end_color[1] * ratio)
        b = int(start_color[2] * (1 - ratio) + end_color[2] * ratio)
        draw.line([(x, 0), (x, img.height)], fill=(r, g, b))

    try:
        font = ImageFont.truetype("arial.ttf", 35) 
    except IOError:
        font = ImageFont.load_default() 
    
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]  # largeur
    text_height = bbox[3] - bbox[1]  # hauteur
    position = ((image_size[0] - text_width) // 2, (image_size[1] - text_height) // 2)
    
    draw.text(position, text, font=font, fill=(255, 255, 255))
    img.save(output_filename, "PNG")
    print(f"Image générée et sauvegardée sous {output_filename}")

def read_image_as_binary(image_path):
    # Ouvrir l'image et la convertir en binaire
    with open(image_path, 'rb') as file:
        return file.read()

def modulate_256_ASK(binary_data):
    # Calculer le nombre d'échantillons par bit
    t_symbole = np.linspace(0, 5/symbole_rate, int(sample_rate/symbole_rate), endpoint=False)
    symbol = (np.sin(2*np.pi*t_symbole*symbole_rate)/255).tolist()

    signal = []
    for i in binary_data:
        signal += [i*s for s in symbol]
    return np.array(signal)

def save_signal_to_file(signal, output_filename="output_signal.wav"):
    # Sauvegarder le signal dans un fichier WAV
    signal_norm = (signal * 32767).astype(np.int16)
    write(output_filename, int(sample_rate), signal_norm)
    print(f"Signal émis sauvegardé sous {output_filename}")

generate_image_with_text(msg)
binary_data = read_image_as_binary("output.png")
signal = modulate_256_ASK(binary_data)
save_signal_to_file(signal)