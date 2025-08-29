from flask import Flask
import random

STARTING_IMG_URL = "https://www.quickanddirtytips.com/wp-content/uploads/2022/04/how-to-write-numbers-compressor.png"
LOW_IMAGE_URL = "https://media.giphy.com/media/jD4DwBtqPXRXa/giphy.gif"
HIGH_IMAGE_URL = "https://media.giphy.com/media/3o6ZtaO9BZHcOjmErm/giphy.gif"
OK_IMAGE_URL = "https://media0.giphy.com/media/1xONIE9kieqf4VTX50/giphy.webp?cid=ecf05e47nrzy5ewoti6817zbzkfmfts16aljvmkaqpmzcacy&ep=v1_gifs_search&rid=giphy.webp&ct=g"

random_number = random.randint(0, 9)
print(random_number)

app = Flask(__name__)


@app.route('/')
def home():
    return ('<h1>Guess a number between 0 and 9</h1>'
            f'<img src={STARTING_IMG_URL} width=400>')


@app.route('/<int:guess>')
def guessed_number(guess):
    if guess > random_number:
        return ('<h1 style="color: purple">Too high, Try again!</h1>'
                f'<img src={HIGH_IMAGE_URL} width=400>')

    elif guess < random_number:
        return ('<h1 style="color: red">Too low, Try again!</h1>'
                f'<img src={LOW_IMAGE_URL} width=400>')

    else:
        return ('<h1 style="color: green">You found me!</h2>'
                f'<img src={OK_IMAGE_URL} width=400>')


if __name__ == "__main__":
    app.run(debug=True)
