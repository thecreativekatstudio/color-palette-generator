from flask import Flask, request, jsonify, send_file
from PIL import Image, ImageDraw, ImageFont
import os
import urllib.parse
import io

app = Flask(__name__)

@app.route('/')
def home():
    return 'Color Palette Generator is running!'

@app.route('/generate', methods=['GET'])
def generate_palette():
    # Get the 'colors' query parameter and decode it if necessary
    colors_param = request.args.get('colors', '').strip()

    # Log the received colors query for debugging purposes
    print(f"Received colors query: {colors_param}")

    # Ensure the 'colors' query parameter is not empty or contains invalid colors
    if not colors_param:
        return jsonify({'error': 'No colors provided. Please provide a comma-separated list of hex colors.'}), 400

    # URL-decode the colors parameter in case it contains encoded characters
    colors_param = urllib.parse.unquote(colors_param)

    # Split the colors into a list
    hex_codes = [color.strip() for color in colors_param.split(',') if color.strip()]

    # Ensure no empty color values exist
    if not hex_codes:
        return jsonify({'error': 'Invalid colors format. Please provide valid comma-separated hex colors.'}), 400

    try:
        # Create a new image to store the color palette
        num_colors = len(hex_codes)
        palette_width = num_colors * 100  # 100px for each color
        palette_height = 150  # Increased to fit text below the colors
        palette_image = Image.new('RGB', (palette_width, palette_height), "white")
        draw = ImageDraw.Draw(palette_image)

        # Load a font
        try:
            font = ImageFont.truetype("arial.ttf", size=18)  # You can use a font available on your system
        except IOError:
            font = ImageFont.load_default()  # Fallback to default font if arial.ttf is unavailable

        # Add each color block and hex code to the image
        for i, color in enumerate(hex_codes):
            try:
                # Convert hex color to RGB
                rgb_color = ImageColor.getrgb(color)

                # Define coordinates for the color block
                x0, y0 = i * 100, 0
                x1, y1 = (i + 1) * 100, 100

                # Draw the color block
                draw.rectangle([x0, y0, x1, y1], fill=rgb_color)

                # Draw the hex code below the color block
                text_width, text_height = draw.textsize(color, font=font)
                text_x = x0 + (100 - text_width) // 2  # Center-align text
                text_y = y1 + 10  # Position text below the block
                draw.text((text_x, text_y), color, fill="black", font=font)
            except ValueError:
                return jsonify({'error': f'Invalid color specifier: {color}'}), 400

        # Save the image to a BytesIO object
        img_io = io.BytesIO()
        palette_image.save(img_io, 'PNG')
        img_io.seek(0)
        return send_file(img_io, mimetype='image/png')

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Get PORT from Heroku's environment variable or use 5000 locally
    port = int(os.environ.get('PORT', 5000))
    # Run the Flask app with the correct host and port
    app.run(host='0.0.0.0', port=port)
