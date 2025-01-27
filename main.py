from flask import Flask, request, send_file
from PIL import Image, ImageDraw
import io
import os

app = Flask(__name__)

@app.route('/generate_palette', methods=['GET'])
def generate_palette():
    # Get the list of color codes from the query parameter
    hex_codes = request.args.get('colors', '').split(',')
    
    if not hex_codes:
        return "Please provide color codes in the 'colors' query parameter.", 400

    # Create a simple image with the color palette
    width, height = 1000, 360
    img = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(img)
    column_width = width // len(hex_codes)

    # Draw each color as a vertical strip
    for i, color in enumerate(hex_codes):
        x1 = i * column_width
        x2 = (i + 1) * column_width
        draw.rectangle([x1, 0, x2, height], fill=color)

    # Convert the image to a byte array
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)

    # Return the image as a downloadable file
    return s
