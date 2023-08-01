import requests
from bs4 import BeautifulSoup
import csv

# Write a function that takes a character name as input and scrapes their information from the One Piece wiki. 
# The function should use the requests library to fetch the HTML content and BeautifulSoup to parse it.

def scrape_char_info(character_name):
    url = f"https://onepiece.fandom.com/wiki/{character_name.replace(' ', '_')}"
    html = requests.get(url)

    if html.status_code == 200:
        soup = BeautifulSoup(html.content, "html.parser")
        # use beautifulsoup to extract relevant info from site

        affiliation_element = soup.find("div", {"data-source" : "affiliation"})
        if affiliation_element:
            affiliation = affiliation_element.findNext("div").text.strip()
        else:
            affiliation = "Unknown"

        bounty_element = soup.find("div", {"data-source" : "bounty"})
        if bounty_element:
            bounty = bounty_element.findNext("div").text.strip()
        else:
            bounty = "Unknown"

        origin_element = soup.find("div", {"data-source" : "origin"})
        if origin_element:
            origin = origin_element.findNext("div").text.strip()
        else:
            origin = "Unknown"

        # return extracted info as a dictionary
        character_info = {
            "Name" : character_name,
            "Affiliation" : affiliation,
            "Bounty" : bounty,
            "Origin" : origin
        }
        return character_info
    else:
        print(f"Error: Could not fetch data for {character_name}")
        return None
    
def main():
    characters_to_scrape = ["Monkey D. Luffy", "Roronoa Zoro", "Nami", "Usopp", "Sanji", "Tony Tony Chopper", "Nico Robin", "Jinbe", "Franky", "Brook"]
    character_info_list = []

    for character in characters_to_scrape:
        character_info = scrape_char_info(character)
        if character_info:
            character_info_list.append(character_info)

    # store info in csv file
    with open("one_piece_characters.csv", "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = character_info_list[0].keys()
        writer = csv.DictWriter(csvfile,fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(character_info_list)

if __name__ == "__main__":
    main()