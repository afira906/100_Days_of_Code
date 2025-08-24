# FUNCTIONS WITH INPUTS
# def greet_with_name(name):
#     print(f"Hello {name}")
#     print(f"How do you do {name}?")
# greet_with_name("Jack Bauer")


# FUNCTIONS WITH MORE THAN ONE INPUTS
# def greet_with(name, location):
#     print(f"Hello {name}")
#     print(f"What is it like in {location}?")
# greet_with("Afira", "Lahore")
# greet_with(location = "Lahore", name = "Afira")


# LOVE CALCULATOR
first_name = (input("Type first name : "))
second_name = (input("Type second name: "))

def calculate_love_score(name1, name2):
    # Combine both names into one string and convert to uppercase
    names = (name1 + name2).upper()

    # Define the letters to check
    true_letters = ['T','R','U','E']
    love_letters = ['L','O','V','E']

    # Initialize counters for TRUE and LOVE
    true_score = 0
    love_score = 0

    # Count occurrences of letters in TRUE
    for letter in true_letters:
        count = names.count(letter)
        true_score += count

    # Count occurrences of letters in LOVE
    for letter in love_letters:
        count = names.count(letter)
        love_score += count

    # Combine the two scores into a two-digit number
    total_love_score = int(f"{true_score}{love_score}")

    # Print only the love score
    print(total_love_score)

calculate_love_score(first_name, second_name)
