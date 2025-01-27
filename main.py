from flask import Flask, request, jsonify, send_file
from PIL import Image, ImageDraw, ImageFont
import os
import urllib.parse

app = Flask(__name__)

@app.route('/')
def home():
    return 'Color Palette Generator is running!'

@app.route('/generate', methods=['GET'])
def generate_palette():
    # Get the 'colors' query parameter and decode it if necessary
    colors_param = request.args.get('colors', '').strip()

    # Ensure the 'colors' query parameter is not empty or contains invalid colors
    if not colors_param:
        return jsonify({'error': 'No colors provided. Please provide a comma-separated list of hex colors.'}), 400
    
    # URL-decode the colors parameter in case it contains encoded characters
    colors_param = urllib.parse.unquote(colors_param)
    
    # Split the colors into a list
    hex_codes = colors_param.split(',')

    # Ensure no empty color values exist
    if '' in hex_codes:
        return jsonify({'error': 'Invalid colors format. Please provide valid comma-separated hex colors.'}), 400

    try:
        # Create a new image to store the color palette
        palette_width = len(hex_codes) * 100  # 100px for each color
        palette_height = 150  # Height increased to fit the color code text
        palette_image = Image.new('RGB', (palette_width, palette_height), (255, 255, 255))

        # Load a font (you can adjust this or add a font path if needed)
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 12)
        except IOError:
            font = ImageFont.load_default()

        # Add each color to the image with the hex code below it
        for i, color in enumerate(hex_codes):
            try:
                # Get RGB from hex code directly (no need for conversion)
                rgb_color = ImageColor.getrgb(color.strip())  # Get RGB from hex code
                # Draw color block
                ImageDraw.Draw(palette_image).rectangle([i * 100, 0, (i + 1) * 100, 100], fill=rgb_color)
                # Draw hex code below the color block
                ImageDraw.Draw(palette_image).text((i * 100 + 10, 105), color.strip(), font=font, fill=(0, 0, 0))
            except ValueError:
                # If a color is invalid, return an error message for that specific color
                return jsonify({'error': f'Invalid color specifier: {color}'}), 400

        # Save the image to a temporary file and return it
        palette_image.save('/tmp/palette_with_hex.png')
        return send_file('/tmp/palette_with_hex.png', mimetype='image/png')

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Get PORT from Heroku's environment variable or use 5000 locally
    port = int(os.environ.get('PORT', 5000))
    # Run the Flask app with the correct host and port
    app.run(host='0.0.0.0', port=port)
