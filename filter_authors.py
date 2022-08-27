from db import Author

def lcs(s1, s2):
    if not (s1 and s2):
        return (0, "")
    matrix = [["" for x in range(len(s2))] for x in range(len(s1))]
    for i in range(len(s1)):
        for j in range(len(s2)):
            if s1[i] == s2[j]:
                if i == 0 or j == 0:
                    matrix[i][j] = s1[i]
                else:
                    matrix[i][j] = matrix[i-1][j-1] + s1[i]
            else:
                matrix[i][j] = max(matrix[i-1][j], matrix[i][j-1], key=len)
    cs = matrix[-1][-1]

    return len(cs), cs    
print("abcdef", "acqef", lcs("abcdef", "acqef"))

matches = []

for a in Author.select():
    for b in Author.select().where((Author.id > a.id) & True):
        l, ss = lcs(a.author, b.author)
        if l > 0:
            score = round((l/max(len(a.author), len(b.author))) *100)
            if score > 50:
                matches.append((f"{a._pk} {b._pk} {a.author} {b.author} {score}%", score))

for match in sorted(matches, key=lambda a: a[1]):
    print(match[0])
