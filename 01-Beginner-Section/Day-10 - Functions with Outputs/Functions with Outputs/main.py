# Functions with outputs
def my_function():
    result = 3 * 2
    return result
output = my_function()
print(output)


# .title() convert to title case
print("she knows".title())


def format_name(first_name, last_name):
    formated_first_name = (first_name.title())
    formated_last_name = (last_name.title())
    return f"{formated_first_name} {formated_last_name}"
print(format_name("afira", "arif"))


# Output of 1st function as input in 2nd function
def function_1(text):
    return text + text

def function_2(text):
    return text.title()

output = function_2(function_1("Hello"))
print(output)
