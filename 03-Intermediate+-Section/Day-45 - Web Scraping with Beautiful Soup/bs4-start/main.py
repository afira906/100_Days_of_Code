from bs4 import BeautifulSoup
import requests

response = requests.get("https://news.ycombinator.com/newest")
yc_webpage = response.text

soup = BeautifulSoup(yc_webpage, "html.parser")
articles = soup.find_all("span", class_="titleline")
article_text = [article.find("a").getText() for article in articles]
article_links = [article.find("a")["href"] for article in articles]
article_upvotes = [int(score.getText().split()[0]) for score in soup.find_all(name="span", class_="score")]

largest_number = max(article_upvotes)
largest_index = article_upvotes.index(largest_number)

print(article_text[largest_index])
print(article_links[largest_index])

# print(article_text)
# print(article_links)
# print(article_upvotes)


# # import lxml
#
# with open ("website.html") as file:
#     contents = file.read()
#
# soup = BeautifulSoup(contents, "html.parser")
#
# # print(soup.title)
# # print(soup.title.string)
# # print(soup.prettify())
#
# all_anchor_tags = soup.find_all(name="a")
# # print(all_anchor_tags)
#
# # for tag in all_anchor_tags:
#     # print(tag.getText())
#     # print(tag.get("href"))
#
# heading = soup.find(name="h1", id="name")
# print(heading.text)
#
# section_heading = soup.find(name="h3", class_="heading")
# print(section_heading)
#
# company_url = soup.select_one(selector="p a")
# print(company_url)
