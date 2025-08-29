from flask import Flask

app = Flask(__name__)

# Decorators to add a tag around text on web page.
def make_bold(function):
    def wrapper():
        return "<b>" + function() + "</b>"
    return wrapper

def make_emphasis(function):
    def wrapper():
        return "<em>" + function() + "</em>"
    return wrapper

def make_underline(function):
    def wrapper():
        return "<u>" + function() + "</u>"
    return wrapper

# Different routes using the app.route decorator
@app.route('/')
def hello_world():
    # Rendering HTML elements
    return ('<h1 style="text-align: center">Hello, World!</h1>'
            '<p>This is Chandler.</p>'
            '<img src="https://media.press.amazonmgmstudios.com/userfiles/images/00_Unscripted/Beast_Games/Season_1/Files/Headshots/Chandler_Hallow_S1_GL_06_240904_SCHSCO_00041_thumb.JPG" width=200px>')


@app.route("/bye")
@make_bold
@make_emphasis
@make_underline
def say_bye():
    # return "<u><em><b>Bye</u></em></b>"
    return "Bye"


# Creating variables path and converting the path to a specified data type
@app.route("/username/<name>/<int:number>")
def greet(name, number):
    return f"Hello {name}, You are {number} years old!"


if __name__ == "__main__":
    # Run the app in debug mode to auto-reload
    app.run(debug=True)
