from db import WrongQuote

for quote in WrongQuote.select().where(WrongQuote.checked == False):
    if quote.contributed_by != "asozialesnetzwerk.github.io/discord":
        print(f'"{quote.quote.quote}"')
        print(
            f"           --{quote.author.author} (eigentlich {quote.quote.author.author})"
        )
        print(f"Eingereicht von {quote.contributed_by}")
        choice = input("Akzeptieren? (y/n) ")
    else:
        choice="n"
    if choice == "y":
        quote.checked = True
        quote.author.checked = True
        quote.quote.author.checked = True
        quote.save()
        quote.author.save()
        quote.quote.author.save()
    elif choice == "n":
        quote.delete_instance()
    print()
    print()
