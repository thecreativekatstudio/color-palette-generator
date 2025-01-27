from flask import Flask, request, send_file
from PIL import Image

app = Flask(__name__)

@app.route('/')
def home():
    return 'Color Palette Generator is running!'

@app.route('/generate', methods=['GET'])
def generate_palette():
    # Get the list of color codes from the query parameter
    hex_codes = request.args.get('colors', '').split(',')
    
    # Ensure there are at least 2 colors (you can change this to suit your app)
    if len(hex_codes) < 2:
        return 'Please provide at least two color codes.'

    # Create a simple image with each color in a stripe format
    width = 100 * len(hex_codes)  # Each stripe will be 100px wide
    height = 100  # Height of the image
    img = Image.new('RGB', (width, height))

    # Draw each stripe of color
    for i, hex_code in enumerate(hex_codes):
        img.paste(Image.new('RGB', (100, height), hex_code), (i * 100, 0))

    # Save the image and return a response
    img.save('/tmp/palette.png')  # Save image temporarily (Heroku's /tmp folder is writable)

    return send_file('/tmp/palette.png', mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)
