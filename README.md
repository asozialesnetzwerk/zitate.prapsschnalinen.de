# Falsch Zugeordnete Zitate

https://zitate.prapsschnalinen.de

### API

#### api/wrongquotes

| Methode | URI              | Parameter| Beschreibung |
|---------|-----             |---       |--------------|
|GET      | /api/wrongquotes | quote(id), author(id) | Falschzugeordneten Zitate bekommen |
|POST     | /api/wrongquotes | quote(id), author(id) | Ein neues Falschzugeordnetes Zitat erstellen |
|GET      | /api/wrongquotes/[id]|                              |Ein Falschzugeordnetes Zitat bekommen |

#### api/quotes
|Methode | URI | Parameter | Beschreibung |
|--------|-----|-----------|--------------|
|GET     | /api/quotes | author(id)| Zitate bekommen|
|POST    | /api/quotes | quote, author(id) |Zitat erstellen |
|GET     | /api/quotes/[id]| |Ein Zitat bekoommen|

#### api/authors

|Methode | URI | Parameter | Beschreibung |
|--------|-----|-----------|--------------|
|GET | /api/authors | | Autoren bekommen |
|POST| /api/authors | author | Autor erstellen |
|GET| /api/authors/[id]| | Ein Autor bekommen |
