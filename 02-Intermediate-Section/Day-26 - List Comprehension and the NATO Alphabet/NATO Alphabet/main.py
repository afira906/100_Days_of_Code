import pandas

DataFrame = pandas.read_csv("nato_phonetic_alphabet.csv")
nato_dict = {row.letter: row.code for (index,row) in DataFrame.iterrows()}

user_input = input("Enter a Word: ").upper()
phonetic_code = [nato_dict[letter] for letter in user_input]
print(phonetic_code)
