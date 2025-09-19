import pandas

data = pandas.read_csv("squirrel_count.csv")
gray_squirrels_count = len(data[data["Primary Fur Color"] == "Gray"])
red_squirrels_count = len(data[data["Primary Fur Color"] == "Cinnamon"])
black_squirrels_count = len(data[data["Primary Fur Color"] == "Black"])

print(f"gray squirrels count: {gray_squirrels_count}")
print(f"red squirrels count: {red_squirrels_count}")
print(f"black squirrels count: {black_squirrels_count}")

data_dict = {
    "Fur Color": ["Gray", "Cinnamon", "Black"],
    "Count": [gray_squirrels_count, red_squirrels_count, black_squirrels_count]
}

df =pandas.DataFrame(data_dict)
df.to_csv("squirrel_color_count.csv")
