# Falschzugeordnete Zitate

https://zitate.prapsschnalinen.de

### API

#### api/wrongquotes

| Methode | URI              | Parameter| Beschreibung |
|---------|-----             |---       |--------------|
|GET      | /api/wrongquotes | quote(id), author(id), simulate, no_text, sort[author, quote, score, random], search | Falschzugeordnete Zitate bekommen |
|POST     | /api/wrongquotes | quote(id), author(id) | Ein neues Falschzugeordnetes Zitat erstellen |
|GET      | /api/wrongquotes/[id]|                   |Ein falschzugeordnetes Zitat bekommen |
|POST     | /api/wrongquotes/[id]| vote              | Ein falschzugeordnetes Zitat bewerten |
|GET      | /api/wrongquotes/count|                  | Anzahl der falschzugeordneten Zitate bekommen |
|GET      | /api/wrongquotes/random | min_rating, count | Zufällige falschzugeordnete Zitate bekommen |

#### api/quotes
|Methode | URI | Parameter | Beschreibung |
|--------|-----|-----------|--------------|
|GET     | /api/quotes | author(id)| Zitate bekommen|
|POST    | /api/quotes | quote, author(id) |Zitat erstellen |
|GET     | /api/quotes/[id]| |Ein Zitat bekoommen|
|GET     | /api/quotes/count| | Anzahl der Zitate bekommen |

#### api/authors

|Methode | URI | Parameter | Beschreibung |
|--------|-----|-----------|--------------|
|GET | /api/authors | | Alle Autoren bekommen |
|POST| /api/authors | author | Autor erstellen |
|GET| /api/authors/[id]| | Einen Autor bekommen |
|GET | /api/authors/count| |Anzahl der Autoren bekommen|
