import pyppeteer
from requests_html import HTMLSession
import random

# creates html session
url = 'https://www.tasteofhome.com/collection/easy-family-recipes/'  # recipe link
session = HTMLSession()
response = session.get(url)

# tries to render all the html, sometimes it takes a long time so there's a try block to except a timeout
try:
    response.html.render(timeout=30)
except pyppeteer.errors.TimeoutError:
    print('This is taking a while')

meal = response.html.find('.listicle-page__title')  # scrapes all the meals from the recipe site
meal_list = []
for idx, item in enumerate(meal):
    data = item.find('a', first=True)  # finds the meal title and href
    try:
        meal_list.append([data.text, data.absolute_links])
    except pyppeteer.errors.NetworkError:
        pass

random_meal = random.choice(meal_list)  # randomly chooses a meal to use


def get_meal_info(meal):
    for i in meal[1]:  # extracting the link from the set... for loop seems a bit overkill but idk how to make better
        link = i
    response2 = session.get(link)  # making another response to scrape info

    try:  # rendering html
        response2.html.render(timeout=30)
    except pyppeteer.errors.TimeoutError:
        print('This is taking a while')

    # finding the list that contains all recipe directions
    directions_container = response2.html.find('.recipe-directions__list', first=True)
    # makes a list that has all the directions
    directions_list = directions_container.find('li')
    # loops through each item and extracts the text
    directions = []
    for direction in directions_list:
        try:
            directions.append(direction.text)

        except pyppeteer.errors.NetworkError:
            pass

    ingredients_container = response2.html.find(
        '#content > div:nth-child(4) > section.pure-u-1.pure-u-lg-17-24.pure-u-xl-17-24 > div.recipe-single-container > div.recipe-ingredients > ul',
        first=True)
    ingredients_list = ingredients_container.find('li')
    ingredients = []
    for ingredient in ingredients_list:
        try:
            ingredients.append(ingredient.text)

        except pyppeteer.errors.NetworkError:
            pass

    # close response or you get os error
    response2.close()
    return ingredients, directions, link


ingredients, directions, link = get_meal_info(random_meal)
print(f"Meal Name: {random_meal[0]}")
print(f"Link: {link}")
print('\n Ingredients', *ingredients, sep='\n')
print('\n Directions', *directions, sep='\n')
