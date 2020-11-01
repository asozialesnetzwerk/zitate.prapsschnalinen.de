from db import Quote

with open("quotes.txt") as f:
    file = f.readlines()
    a = 0
    for line in file:
        print(a)
        a += 1
        quote, new_author, real_author = line.strip().split(" - ")
        Quote.create(
            quote=quote,
            new_author=new_author,
            real_author=real_author,
            contributed_by="Marc-Uwe Kling",
            checked=True,
        )
