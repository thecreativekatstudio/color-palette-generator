import os
from flask import Flask, request, jsonify
from PIL import Image, ImageColor

app = Flask(__name__)

@app.route('/')
def home():
    return 'Color Palette Generator is running!'

@app.route('/generate', methods=['GET'])
def generate_palette():
    # Get the list of color codes from the query parameter
    hex_codes = request.args.get('colors', '').split(',')
    try:
        # Generate a simple palette image
        width = len(hex_codes) * 100
        height = 100
        palette = Image.new('RGB', (width, height))

        for i, color in enumerate(hex_codes):
            # Convert hex to RGB
            rgb = ImageColor.getrgb(color)
            for x in range(i * 100, (i + 1) * 100):
                for y in range(height):
                    palette.putpixel((x, y), rgb)

        # Save the image to a byte stream to serve
        from io import BytesIO
        img_byte_arr = BytesIO()
        palette.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)

        return send_file(img_byte_arr, mimetype='image/png')

    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Get PORT from Heroku's environment variable or use 5000 locally
    app.run(host='0.0.0.0', port=port)  # Bind to all IP addresses on the given port
