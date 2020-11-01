from db import Quote

for quote in Quote.select().where(Quote.checked == False):
    print(f'"{quote.quote}"')
    print(f"           --{quote.new_author} (eigentlich {quote.real_author})")
    print(f"Eingereicht von {quote.contributed_by}")
    choice = input("Akzeptieren? (y/n) ")
    if choice == "y":
        quote.checked = True
        quote.save()
    elif choice == "n":
        quote.delete_instance()
    print()
    print()
