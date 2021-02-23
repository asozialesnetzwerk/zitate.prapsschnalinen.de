from db import WrongQuote
import csv

with open("zitate.csv") as f:
    reader = csv.reader(f, delimiter=",", quotechar='"') 
    a = 0
    for line in reader:
        print(a)
        a += 1
        quote, new_author, real_author = line 
        print(quote, new_author)
        WrongQuote.get_or_create(
            quote=quote.strip(),
            wrongauthor=new_author.strip(),
            realauthor=real_author.strip(),
            contributed_by="asozialesnetzwerk.github.io",
            checked=True,
            rating=1
        )
