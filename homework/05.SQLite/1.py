import sqlite3

def db_1():
    conn = sqlite3.connect("hittite.db")
    c = conn.cursor()
    c.execute("""SELECT *
                       FROM  wordforms""")
    t = c.fetchall()
    d = {}
    j = 1
    for arr in t:
        for i in  arr:
            d[j] = [arr[0], arr[1], arr[2]]
            j += 1
            break
    conn = sqlite3.connect("words.sqlite")
    c1 = conn.cursor()
    c1.execute("""CREATE TABLE
                         IF NOT EXISTS words
                         (id INTEGER PRIMARY KEY, lemma TEXT, wordform TEXT, glosses TEXT)""")
    for i in d:
        c1.execute("""INSERT INTO words
                            (lemma, wordform, glosses)
                            VALUES (?,?,?)""", (d[i][0], d[i][1], d[i][2]))
    conn.commit()


def db_2():
    conn = sqlite3.connect("glosses.sqlite")
    c2 = conn.cursor()
    d = {}
    with open ("Glossing_rules.txt", "r", encoding="utf-8") as f:
        text = f.read().replace("\n",  " — ").split(" — ")
        for i in range(0,len(text),2):
            d[text[i]] = text[i+1]
    c2.execute("""CREATE TABLE
                         IF NOT EXISTS glosses
                         (id INTEGER PRIMARY KEY, name TEXT, transcript TEXT)""")
    for k,v in d.items():
        c2.execute("""INSERT INTO glosses
                            (name, transcript)
                            VALUES (?,?)""", (k, v))
    conn.commit()
    return d


def db_3(d):
    for k,v in d.items():
        conn = sqlite3.connect("words.sqlite")
        c4 = conn.cursor()
        c4.execute("""SELECT id
                             FROM words
                             WHERE glosses
                             LIKE \"{}\"""".format(k))
        t = c4.fetchall()
        if t != []:
            conn = sqlite3.connect("glosses.sqlite")
            c5 = conn.cursor()
            c5.execute("""SELECT id
                                 FROM glosses
                                 WHERE name
                                 LIKE \"{}\"""".format(k))
            m = c5.fetchone()
            for arr in t:
                for i in arr:
                    for j in m:
                        conn = sqlite3.connect("w-to-g.sqlite")
                        c3 = conn.cursor()
                        c3.execute("""CREATE TABLE
                                            IF NOT EXISTS words_to_glosses
                                            (id_word INTEGER, id_gloss INTEGER)""")
                        c3.execute("""INSERT INTO words_to_glosses
                                            (id_word, id_gloss)
                                            VALUES (?,?)""", (i, j))
                        conn.commit()


def main():
    db_1()
    d = db_2()
    db_3(d)

    
if __name__ == "__main__":
        main()
