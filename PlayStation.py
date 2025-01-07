import requests
from bs4 import BeautifulSoup
import json


class PlayStation:

    def __init__(self):
        
        self.url = "https://store.playstation.com/pt-pt/category/298b428c-0c39-4ec8-abd5-237484e5a2ea/1"

        self.list_dict = {}

    def response(self):
        response = requests.get(self.url)
        soup = BeautifulSoup(response.text, "html.parser")

        self.next_page(soup)
        for games in soup.find_all("li", class_="psw-l-w-1/2@mobile-s psw-l-w-1/2@mobile-l psw-l-w-1/6@tablet-l psw-l-w-1/4@tablet-s psw-l-w-1/6@laptop psw-l-w-1/8@desktop psw-l-w-1/8@max"):
            links = games.find("a").get("href")
            link = ("https://store.playstation.com" + links)
            response = requests.get(link)
            soup = BeautifulSoup(response.text, "html.parser")

            path_json = soup.find("script", type="application/ld+json").text
            data_json = json.loads(path_json)
            #self.processing(data_json,soup, link)
    def processing(self, data_json, soup, link):
        dict_games = {}
        details = []

        dict_games["Title"] = data_json["name"].replace("PS4 & PS5", "")
        dict_games["Game_Status"] = data_json["category"]
        dict_games["Price"] = data_json["offers"]["price"]
        dict_games["Link"] = link
        for date in soup.find_all("dd", class_="psw-p-r-6 psw-p-r-0@tablet-s psw-t-bold psw-l-w-1/2 psw-l-w-1/6@tablet-s psw-l-w-1/6@tablet-l psw-l-w-1/8@laptop psw-l-w-1/6@desktop psw-l-w-1/6@max"):
            details.append(" ".join(date.text.split()))  
        dict_games["Platforms"] = details[0] 
        dict_games["date"] = details[1]
        dict_games["Publisher"] = details[2]
        genus = soup.find("div", class_="psw-l-w-1/1 psw-l-w-1/3@tablet-s psw-l-w-1/3@tablet-l psw-l-w-1/4@laptop psw-l-w-1/4@desktop psw-l-w-1/4@max").find("span").text
        dict_games["Category"] = genus
        
        for key, value in dict_games.items():
            self.list_dict[key] = value 


    def next_page(self,soup):
        page = soup.find("div", class_="psw-l-stack-center").find("button")
        print(page)
        #print(self.list_dict)
        #print("*" * 120)
PlayStation().response()