import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd

# function takes in character name and scrapes information from wiki
def scrape_char_info(character_name):
    url = f"https://onepiece.fandom.com/wiki/{character_name.replace(' ', '_')}"
    html = requests.get(url)

    if html.status_code == 200:
        soup = BeautifulSoup(html.content, "html.parser")

        #extract relevant information from wiki
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
            "Origin" : origin,
            "Affiliation" : affiliation,
            "Bounty" : bounty
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

    # store character information in a csv file
    with open("one_piece_characters.csv", "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = character_info_list[0].keys()
        writer = csv.DictWriter(csvfile,fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(character_info_list)

    # read data from csv file using pandas
    df = pd.read_csv("one_piece_characters.csv")
    
    # display data in structured format (Data Frame)
    print(df)

if __name__ == "__main__":
    main()