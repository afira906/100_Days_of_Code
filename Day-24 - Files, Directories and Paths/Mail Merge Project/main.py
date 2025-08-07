PLACEHOLDER = "[name]"

# Read the names from the file
with open("./input/Names/invited_names.txt") as name_file:
    names = name_file.readlines()

# Read the starting_letter
with open("./input/Letters/starting_letter.txt") as letter_file:
    letter_contents = letter_file.read()

    # Strip newline characters from names and create personalized letters
    for name in names:
        stripped_name = name.strip()
        new_letter = letter_contents.replace(PLACEHOLDER, stripped_name)

        # Save each personalized letter to a file
        with open(f"./output/ReadyToSend/letter_for_{stripped_name}.txt", mode="w") as completed_letter:
            completed_letter.write(new_letter)
