# programming_dictionary = {"Bug": "An error in a program that prevents the program from running as expected.",
#                           "Function": "A piece of code that you can easily call over and over again.",
#                           "Loop": "The action of doing something over and over again."
# }
# Retrieve an item from dictionary
# print(programming_dictionary["Bug"])

# Add new items to an existing dictionary

# Wipe an existing dictionary
# programming_dictionary = {}
# print(programming_dictionary)

# Edit an item in dictionary
# programming_dictionary["Bug"] = "A moth in your computer."

# Loop through a dictionary


# Coding Exercise to convert score into grades
student_scores = {
    'Harry': 88,
    'Ron': 78,
    'Hermione': 95,
    'Draco': 75,
    'Neville': 60
}
# Initialize an empty dictionary to store the grades
student_grades = {}

# Iterate over each student in the student_scores dictionary
for student, score in student_scores.items():

    # Assign grades based on the score
    if 91 <= score <= 100:
        student_grades[student] = "Outstanding"
    elif 81 <= score <= 90:
        student_grades[student] = "Exceeds Expectations"
    elif 71 <= score <= 80:
        student_grades[student] = "Acceptable"
    else:
        student_grades[student] = "Fail"

# Print the final student_grades dictionary to check the result
print(student_grades)
