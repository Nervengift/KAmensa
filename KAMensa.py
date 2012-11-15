# -*- coding: utf-8 -*-
#!/usr/bin/python2ö
# coding: utf8
import urllib.request
import base64
import json
from datetime import date

class mensaplan:

    def __init__(self):
        username = "jsonapi"
        password = "AhVai6OoCh3Quoo6ji"
        theurl = "https://www.studentenwerk-karlsruhe.de/json_interface/canteen/"

        req = urllib.request.Request(theurl)
        userstring = "%s:%s" % (username, password)
        base64string = base64.encodestring(userstring.encode())[:-1]
        req.add_header("Authorization", "Basic %s" % base64string.decode())

        try:
            handle = urllib.request.urlopen(req)
        except IOError as e:
            print("error!")
            if hasattr(e, "code"):
                if e.code != 401:
                    print("We got another error")
                    print(e.code)
                else:
                    print(e.headers)
                    print(e.headers["www-authenticate"])

        self.json_response = json.loads(handle.read().decode())

    def meal(self, mensa, line, date = date.today()):
        timestamp = date.strftime("%s")

        if (mensa in self.json_response.keys()
            and timestamp in self.json_response[mensa].keys()
            and line in self.json_response[mensa][timestamp].keys()):

            return self.json_response[mensa][timestamp][line]
        else:
            return None

    def meal_string(self, mensa, line, date = date.today()):
        if date.weekday() > 4 :
            return "Wochenende"

        meals = self.meal(mensa,line,date)
        if meals != None :
            result = "" + str(key_to_name(line)) + ":"
            for item in meals:
                if "nodata" not in item.keys():
                    result += "\t" + item["meal"] + " " + item["dish"] + " " + str(item["price_1"]) + " " + item["info"]
                else:
                    result += "\tNo Data"
            return result
        else:
            return "No Data Available"

    def keys(self, type):    
        mensen = { "adenauerring":  ["l1", "l2", "l3", "l45", "schnitzelbar", "update", "abend", "aktion", "heisstheke", "nmtisch"],
                      "erzberger":     ["wahl1", "wahl2"],
                      "gottesaue":     ["wahl1", "wahl2"],
                      "holzgarten":    ["gut","gut2"],
                      "moltke":        ["wahl1", "wahl2", "aktion", "gut", "buffet", "schnitzelbar"],
                      "tiefenbronner": ["wahl1", "wahl2", "gut", "buffet"]
                    }
        meals = ["add", "bio", "cow", "cow_aw", "dish", "fish", "info", "meal", "pork", "price_1", "price_2", "price_3", "price_4", "price_flag", "veg", "vegan"]
        if type == "mensa":
            return mensen.keys()
        elif type in mensen.keys():
            return mensen[type]
        elif type == "meal":
            return meals
        else:
            return "unknown type"

    def available_dates(self, mensa):
        return map(lambda x: date.fromtimestamp(int(x)).strftime("%d.%m.%Y"),sorted(self.json_response[mensa].keys()))


    ## Mapping keys to Names
def key_to_name(key):
    if key == "adenauerring":
        return "Mensa am Adenauerring"
    elif key == "erzberger":
        return "Mensa Erzbergstraße"
    elif key == "gottesaue":
        return "Mensa Schloss Gottesaue"
    elif key == "holzgarten":
        return "Mensa Holzgartenstraße"
    elif key == "moltke":
        return "Mensa Moltke"
    elif key == "tiefenbronner":
        return "Mensa Tiefenbronner Straße"
    elif key == "l1":
        return "Linie 1"
    elif key == "l2": 
        return "Linie 2"
    elif key == "l3": 
        return "Linie 3"
    elif key == "l45": 
        return "Linie 4/5"
    elif key == "schnitzelbar": 
        return "Schnitzelbar"
    elif key == "update": 
        return "L6 Update"
    elif key == "abend": 
        return "Abend"
    elif key == "aktion": 
        return "Aktionstheke"
    elif key == "heisstheke": 
        return "Cafeteria Heiße Theke"
    elif key == "nmtisch": 
        return "Cafeteria ab 14:30"
    elif key == "wahl1": 
        return "Wahlessen 1"
    elif key == "wahl2": 
        return "Wahlessen 2"
    elif key == "aktion": 
        return "Aktionstheke"
    elif key == "gut": 
        return "Gut&Guenstig"
    elif key == "gut2": 
        return "Gut&Guenstig 2"
    elif key == "buffet": 
        return "Buffet"
    elif key == "schnitzelbar":
        return "Schnitzelbar"
    else:
        return "unknown key"
