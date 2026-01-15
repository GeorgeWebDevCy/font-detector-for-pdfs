from PIL import Image
import os

input_path = os.path.join('assets', 'logo.png')
output_path = os.path.join('assets', 'icon.ico')

if os.path.exists(input_path):
    img = Image.open(input_path)
    img.save(output_path, format='ICO')
    print(f"Verified created icon at {output_path}")
else:
    print(f"Error: {input_path} not found")
