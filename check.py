from db import WrongQuote

for quote in WrongQuote.select().where(WrongQuote.checked == False):
    print(f'"{quote.quote.quote}"')
    print(f"           --{quote.author.author} (eigentlich {quote.quote.author.author})")
    print(f"Eingereicht von {quote.contributed_by}")
    choice = input("Akzeptieren? (y/n) ")
    if choice == "y":
        quote.checked = True
        quote.save()
    elif choice == "n":
        quote.delete_instance()
    print()
    print()
