from db import WrongQuote
import requests
import os
import pickle


if os.path.isfile("apikeys.pkl"):
    print("apikeys.pkl already exists.")
else:
    with open("apikeys.pkl", "wb") as file:
        pickle.dump(["123456"], file)
    print("created apikey.pkl with '123456' as a key")


if len(WrongQuote.select()) > 0:
    print("quotes.db is already populated.")
else:
    response = requests.get("https://zitate.prapsschnalinen.de/api/wrongquotes").json()
    for wrongquote in response:
        WrongQuote.get_or_create(
            wrongquote["quote"]["quote"],
            wrongauthor=wrongquote["author"]["author"],
            realauthor=wrongquote["quote"]["author"]["author"],
            voted=wrongquote["voted"],
            showed=wrongquote["showed"],
            rating=wrongquote["rating"],
            checked=wrongquote["checked"],
            contributed_by="idk"
        )
    print("added quotes to quotes.db (attention: they are not the same as on zitate.prapsschnalinen.de)")

