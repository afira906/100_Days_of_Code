from flask import Flask, render_template, request, jsonify
from collections import Counter
from PIL import Image
import io
import math

app = Flask(__name__)

# CSS color names to hex mapping
CSS_COLORS = {
    '#f0f8ff': 'aliceblue', '#faebd7': 'antiquewhite', '#00ffff': 'aqua', '#7fffd4': 'aquamarine',
    '#f0ffff': 'azure', '#f5f5dc': 'beige', '#ffe4c4': 'bisque', '#000000': 'black',
    '#ffebcd': 'blanchedalmond', '#0000ff': 'blue', '#8a2be2': 'blueviolet', '#a52a2a': 'brown',
    '#deb887': 'burlywood', '#5f9ea0': 'cadetblue', '#7fff00': 'chartreuse', '#d2691e': 'chocolate',
    '#ff7f50': 'coral', '#6495ed': 'cornflowerblue', '#fff8dc': 'cornsilk', '#dc143c': 'crimson',
    '#00ffff': 'cyan', '#00008b': 'darkblue', '#008b8b': 'darkcyan', '#b8860b': 'darkgoldenrod',
    '#a9a9a9': 'darkgray', '#006400': 'darkgreen', '#a9a9a9': 'darkgrey', '#bdb76b': 'darkkhaki',
    '#8b008b': 'darkmagenta', '#556b2f': 'darkolivegreen', '#ff8c00': 'darkorange', '#9932cc': 'darkorchid',
    '#8b0000': 'darkred', '#e9967a': 'darksalmon', '#8fbc8f': 'darkseagreen', '#483d8b': 'darkslateblue',
    '#2f4f4f': 'darkslategray', '#2f4f4f': 'darkslategrey', '#00ced1': 'darkturquoise', '#9400d3': 'darkviolet',
    '#ff1493': 'deeppink', '#00bfff': 'deepskyblue', '#696969': 'dimgray', '#696969': 'dimgrey',
    '#1e90ff': 'dodgerblue', '#b22222': 'firebrick', '#fffaf0': 'floralwhite', '#228b22': 'forestgreen',
    '#ff00ff': 'fuchsia', '#dcdcdc': 'gainsboro', '#f8f8ff': 'ghostwhite', '#ffd700': 'gold',
    '#daa520': 'goldenrod', '#808080': 'gray', '#008000': 'green', '#adff2f': 'greenyellow',
    '#808080': 'grey', '#f0fff0': 'honeydew', '#ff69b4': 'hotpink', '#cd5c5c': 'indianred',
    '#4b0082': 'indigo', '#fffff0': 'ivory', '#f0e68c': 'khaki', '#e6e6fa': 'lavender',
    '#fff0f5': 'lavenderblush', '#7cfc00': 'lawngreen', '#fffacd': 'lemonchiffon', '#add8e6': 'lightblue',
    '#f08080': 'lightcoral', '#e0ffff': 'lightcyan', '#fafad2': 'lightgoldenrodyellow', '#d3d3d3': 'lightgray',
    '#90ee90': 'lightgreen', '#d3d3d3': 'lightgrey', '#ffb6c1': 'lightpink', '#ffa07a': 'lightsalmon',
    '#20b2aa': 'lightseagreen', '#87cefa': 'lightskyblue', '#778899': 'lightslategray', '#778899': 'lightslategrey',
    '#b0c4de': 'lightsteelblue', '#ffffe0': 'lightyellow', '#00ff00': 'lime', '#32cd32': 'limegreen',
    '#faf0e6': 'linen', '#ff00ff': 'magenta', '#800000': 'maroon', '#66cdaa': 'mediumaquamarine',
    '#0000cd': 'mediumblue', '#ba55d3': 'mediumorchid', '#9370db': 'mediumpurple', '#3cb371': 'mediumseagreen',
    '#7b68ee': 'mediumslateblue', '#00fa9a': 'mediumspringgreen', '#48d1cc': 'mediumturquoise',
    '#c71585': 'mediumvioletred',
    '#191970': 'midnightblue', '#f5fffa': 'mintcream', '#ffe4e1': 'mistyrose', '#ffe4b5': 'moccasin',
    '#ffdead': 'navajowhite', '#000080': 'navy', '#fdf5e6': 'oldlace', '#808000': 'olive',
    '#6b8e23': 'olivedrab', '#ffa500': 'orange', '#ff4500': 'orangered', '#da70d6': 'orchid',
    '#eee8aa': 'palegoldenrod', '#98fb98': 'palegreen', '#afeeee': 'paleturquoise', '#db7093': 'palevioletred',
    '#ffefd5': 'papayawhip', '#ffdab9': 'peachpuff', '#cd853f': 'peru', '#ffc0cb': 'pink',
    '#dda0dd': 'plum', '#b0e0e6': 'powderblue', '#800080': 'purple', '#663399': 'rebeccapurple',
    '#ff0000': 'red', '#bc8f8f': 'rosybrown', '#4169e1': 'royalblue', '#8b4513': 'saddlebrown',
    '#fa8072': 'salmon', '#f4a460': 'sandybrown', '#2e8b57': 'seagreen', '#fff5ee': 'seashell',
    '#a0522d': 'sienna', '#c0c0c0': 'silver', '#87ceeb': 'skyblue', '#6a5acd': 'slateblue',
    '#708090': 'slategray', '#708090': 'slategrey', '#fffafa': 'snow', '#00ff7f': 'springgreen',
    '#4682b4': 'steelblue', '#d2b48c': 'tan', '#008080': 'teal', '#d8bfd8': 'thistle',
    '#ff6347': 'tomato', '#40e0d0': 'turquoise', '#ee82ee': 'violet', '#f5deb3': 'wheat',
    '#ffffff': 'white', '#f5f5f5': 'whitesmoke', '#ffff00': 'yellow', '#9acd32': 'yellowgreen'
}


def get_color_name(rgb_triplet):
    """Convert RGB values to the closest color name"""
    hex_color = '#{:02x}{:02x}{:02x}'.format(*rgb_triplet)

    # Check for exact match first
    if hex_color in CSS_COLORS:
        return CSS_COLORS[hex_color]

    # Find the closest color name if not exact match
    min_distance = float('inf')
    closest_color = "unknown"

    for hex_key, name in CSS_COLORS.items():
        # Convert hex to RGB
        r_c, g_c, b_c = int(hex_key[1:3], 16), int(hex_key[3:5], 16), int(hex_key[5:7], 16)

        # Calculate color distance
        rd = (r_c - rgb_triplet[0]) ** 2
        gd = (g_c - rgb_triplet[1]) ** 2
        bd = (b_c - rgb_triplet[2]) ** 2
        distance = rd + gd + bd

        if distance < min_distance:
            min_distance = distance
            closest_color = name

    return closest_color


def extract_colors(image, num_colors=10):
    """Extract the top colors from an image"""
    # Convert to RGB if necessary
    if image.mode != 'RGB':
        image = image.convert('RGB')

    # Resize for faster processing while maintaining aspect ratio
    max_size = (200, 200)
    image.thumbnail(max_size)

    # Get all pixels
    pixels = list(image.getdata())

    # Count color frequency
    color_counts = Counter(pixels)

    # Get most common colors
    most_common = color_counts.most_common(num_colors)

    # Format results
    results = []
    for color, count in most_common:
        hex_color = '#{:02x}{:02x}{:02x}'.format(*color)
        color_name = get_color_name(color)
        results.append({
            'rgb': color,
            'hex': hex_color,
            'name': color_name,
            'count': count
        })

    return results


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/extract-colors', methods=['POST'])
def process_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No image selected'}), 400

    try:
        # Open and process the image
        image = Image.open(io.BytesIO(file.read()))
        colors = extract_colors(image)
        return jsonify({'colors': colors})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
