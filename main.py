from flask import Flask, request, send_file
from PIL import Image, ImageDraw
import os

app = Flask(__name__)

@app.route('/')
def home():
    return 'Color Palette Generator is running!'

@app.route('/generate', methods=['GET'])
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

    # Save the generated image to a temporary file
    img_path = "/tmp/palette.png"
    img.save(img_path)

    # Send the image as a response
    return send_file(img_path, mimetype='image/png', as_attachment=True, download_name='palette.png')

@app.route('/favicon.ico')
def favicon():
    return '', 204  # Return no content for favicon.ico

if __name__ == "__main__":
    # Run the app with the correct host and port for Heroku
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
