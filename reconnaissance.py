import tkinter as tk
from tkinter import filedialog
import os
import pytesseract
from PIL import Image, ImageEnhance, ImageFilter
import openai

pytesseract.pytesseract.tesseract_cmd = 'tesseract.exe'

openai.api_key = "Mettre Clé API"

def browse_file():
    filepath = filedialog.askopenfilename()
    filename = os.path.basename(filepath)
    file_label.config(text="Selected file: " + filename)
    
    # Traitement de l'image sélectionnée
    im = Image.open(filepath) # Ouverture du fichier image
    # Filtrage (augmentation du contraste)
    im = im.filter(ImageFilter.MedianFilter())
    enhancer = ImageEnhance.Contrast(im)
    im = enhancer.enhance(2)
    im = im.convert('1')
    # Lancement de la procédure de reconnaissance
    text = pytesseract.image_to_string(im)
    result_label.config(text=text)  # Ajout de cette ligne pour afficher le résultat
    
    # Utilisation de la variable du label pour le prompt de l'API OpenAI
    prompt = f"Explique moi ça : {text}"
    completions = openai.Completion.create(
        engine="davinci",
        prompt=prompt,
        max_tokens=50,
        n=1,
        stop=None,
        temperature=0.5,
    )
    message = completions.choices[0].text
    openai_result_label.config(text=message)
    #print(prompt)
    print(message)

root = tk.Tk()

browse_button = tk.Button(root, text="Browse", command=browse_file)
browse_button.pack()

file_label = tk.Label(root, text="")
file_label.pack()

result_label = tk.Label(root, text="")
result_label.pack()

openai_result_label = tk.Label(root, text="")
openai_result_label.pack()

root.mainloop()