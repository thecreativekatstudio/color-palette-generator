from flask import Flask, request, jsonify
from PIL import Image, ImageColor
import random

app = Flask(__name__)

# Default route to check if app is running
@app.route('/')
def home():
    return 'Color Palette Generator is running!'

# Route to generate color palette
@app.route('/generate', methods=['GET'])
def generate_palette():
    # Get the list of color codes from the query parameter
    hex_codes = request.args.get('colors', '').split(',')

    # If no colors were provided, return an error
    if not hex_codes or hex_codes == ['']:
        return jsonify({'error': 'No colors provided. Please provide a comma-separated list of hex colors.'}), 400

    try:
        # Create a new image to store the color palette
        palette_width = len(hex_codes) * 100  # 100px for each color
        palette_height = 100  # Height of the palette
        palette_image = Image.new('RGB', (palette_width, palette_height))

        # Add each color to the image
        for i, color in enumerate(hex_codes):
            try:
                rgb_color = ImageColor.getrgb(color.strip())  # Get RGB from hex code
                palette_image.paste(rgb_color, (i * 100, 0, (i + 1) * 100, palette_height))
            except ValueError:
                # If a color is invalid, return an error message for that specific color
                return jsonify({'error': f'Invalid color specifier: {color}'}), 400

        # Save the image to a file and return the URL (or return the image directly)
        palette_image.save('static/palette.png')
        return jsonify({'message': 'Palette generated successfully', 'image_url': 'static/palette.png'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
