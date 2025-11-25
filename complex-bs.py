import requests
import csv
from bs4 import BeautifulSoup


url = "https://www.foodnetwork.com/recipes/food-network-kitchen/baked-feta-pasta-9867689"
response = requests.get(url, headers={
        "User-Agent": "Mozilla/5.0 (Scrapegoat)",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Accept": "*/*",
        "DNT": "1",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
})
response.raise_for_status()

soup = BeautifulSoup(response.text, 'html.parser')

ingredients_section = soup.find("section", class_="o-Ingredients")
ingredients_body = ingredients_section.find("div", class_="o-Ingredients__m-Body")

ingredients = []

for p in ingredients_body.find_all("p"):
    label = p.find("label")
    if not label:
        continue

    spans = label.find_all("span")
    if len(spans) >= 2:
        ingredient_text = spans[1].get_text(strip=True)
        if ingredient_text.lower() == "deselect all":
            continue
        ingredients.append(ingredient_text)

with open("ingredients.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["body"])
    for ingredient in ingredients:
        writer.writerow([ingredient])