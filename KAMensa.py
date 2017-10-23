# -*- coding: utf-8 -*-
#!/usr/bin/python3
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
        mensen = {"adenauerring":  ["l1", "l2", "l3", "l45", "schnitzelbar", "update", "abend", "aktion", "heisstheke", "nmtisch"],
                  "erzberger":     ["wahl1", "wahl2"],
                  "gottesaue":     ["wahl1", "wahl2"],
                  "holzgarten":    ["gut","gut2"],
                  "moltke":        ["wahl1", "wahl2", "aktion", "gut", "buffet", "schnitzelbar"],
                  "tiefenbronner": ["wahl1", "wahl2", "gut", "buffet"]}
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
    name = {"adenauerring":"Mensa am Adenauerring",
            "erzberger":"Mensa Erzbergstraße",
            "gottesaue":"Mensa Schloss Gottesaue",
            "holzgarten":"Mensa Holzgartenstraße",
            "moltke":"Mensa Moltke",
            "tiefenbronner":"Mensa Tiefenbronner Straße",
            "l1":"Linie 1",
            "l2":"Linie 2",
            "l3":"Linie 3",
            "l45":"Linie 4/5",
            "schnitzelbar":"Schnitzelbar",
            "update":"L6 Update",
            "abend":"Abend",
            "aktion":"Aktionstheke",
            "heisstheke":"Cafeteria Heiße Theke",
            "nmtisch":"Cafeteria ab 14:30",
            "wahl1":"Wahlessen 1",
            "wahl2":"Wahlessen 2",
            "aktion":"Aktionstheke",
            "gut":"Gut&Guenstig",
            "gut2":"Gut&Guenstig 2",
            "buffet":"Buffet",
            "schnitzelbar":"Schnitzelbar"}.get(key, "unknown key")
    return name
