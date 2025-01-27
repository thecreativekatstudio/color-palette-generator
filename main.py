from flask import Flask, request, jsonify, send_file
from PIL import Image, ImageColor
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

    # Log the received colors query for debugging purposes
    print(f"Received colors query: {colors_param}")

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
        palette_height = 100  # Height of the image
        palette_image = Image.new('RGB', (palette_width, palette_height))

        # Add each color to the image
        for i, color in enumerate(hex_codes):
            try:
                # Get RGB from hex code directly (no need for conversion)
                rgb_color = ImageColor.getrgb(color.strip())  # Get RGB from hex code
                palette_image.paste(rgb_color, (i * 100, 0, (i + 1) * 100, palette_height))
            except ValueError:
                # If a color is invalid, return an error message for that specific color
                return jsonify({'error': f'Invalid color specifier: {color}'}), 400

        # Save the image to a temporary file and return it
        palette_image.save('/tmp/palette.png')
        return send_file('/tmp/palette.png', mimetype='image/png')

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Get PORT from Heroku's environment variable or use 5000 locally
    port = int(os.environ.get('PORT', 5000))
    # Run the Flask app with the correct host and port
    app.run(host='0.0.0.0', port=port)
