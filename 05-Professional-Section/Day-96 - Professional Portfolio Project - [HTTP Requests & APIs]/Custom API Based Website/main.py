import requests
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Harry Potter API base URL
HP_API_BASE = "https://hp-api.onrender.com/api"


def get_all_characters():
    """Fetch all characters from the Harry Potter API"""
    try:
        response = requests.get(f"{HP_API_BASE}/characters")
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching characters: {e}")
        return []


def get_character_by_name(name):
    """Fetch a specific character by name"""
    try:
        characters = get_all_characters()
        for character in characters:
            if character['name'].lower() == name.lower():
                return character
        return None
    except Exception as e:
        print(f"Error fetching character {name}: {e}")
        return None


@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')


@app.route('/characters')
def characters():
    """API endpoint to get all characters"""
    try:
        characters_data = get_all_characters()
        return jsonify(characters_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/character/<name>')
def character(name):
    """API endpoint to get a specific character by name"""
    try:
        character_data = get_character_by_name(name)
        if character_data:
            return jsonify(character_data)
        else:
            return jsonify({"error": "Character not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/search')
def search():
    """Search for characters by name"""
    query = request.args.get('q', '')
    if not query:
        return jsonify([])

    try:
        characters_data = get_all_characters()
        results = [char for char in characters_data if query.lower() in char['name'].lower()]
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
