from flask import Flask, request, jsonify, send_file
from PIL import Image, ImageDraw, ImageFont, ImageColor
import io

app = Flask(__name__)

def generate_color_palette(colors):
    # Ensure we have a valid list of colors
    color_list = colors.split(',')

    # Limit number of colors to 10 for better performance
    max_colors = 10
    if len(color_list) > max_colors:
        color_list = color_list[:max_colors]

    # Image size (reduced for performance)
    width = 800
    height = 300
    num_colors = len(color_list)
    swatch_width = width // num_colors
    swatch_height = height

    # Create a new image with white background
    img = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(img)

    # Set up font for hex codes
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 24)
    except IOError:
        font = ImageFont.load_default()

    for i, color in enumerate(color_list):
        # Draw the color swatch
        hex_color = color.strip()  # Remove any extra spaces
        try:
            color_rgb = ImageColor.getrgb(hex_color)
        except ValueError:
            color_rgb = (255, 255, 255)  # Default to white if the color is invalid
        draw.rectangle([i * swatch_width, 0, (i + 1) * swatch_width, swatch_height], fill=color_rgb)
        
        # Add hex code text below the swatch
        text_width, text_height = draw.textsize(hex_color, font=font)
        text_x = i * swatch_width + (swatch_width - text_width) / 2
        text_y = swatch_height - text_height
        draw.text((text_x, text_y), hex_color, fill="black", font=font)

    # Return image
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)

    return img_byte_arr

@app.route('/')
def home():
    return 'Color Palette Generator is running!'

@app.route('/generate', methods=['GET'])
def generate_palette():
    # Get the list of color codes from the query parameter
    colors = request.args.get('colors', '')
    
    if not colors:
        return jsonify({"error": "No colors provided or invalid colors. Please provide a comma-separated list of hex colors."})

    # Generate the palette image
    img_byte_arr = generate_color_palette(colors)

    return send_file(img_byte_arr, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
