import sqlite3
import matplotlib.pyplot as plt


def db_1():
    conn = sqlite3.connect("hittite.db")
    c = conn.cursor()
    c.execute("""SELECT *
                       FROM  wordforms""")
    t = c.fetchall()
    d = {}
    j = 1
    for arr in t:
        for i in arr:
            g = arr[2].replace(".", " ")
            d[j] = [arr[0], arr[1], g]
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
    a = ["C", "N", "P", "Q", "V"] 
    for k,v in d.items():
        conn = sqlite3.connect("words.sqlite")
        c4 = conn.cursor()
        if k not in a:
            c4.execute("""SELECT id
                                 FROM words
                                 WHERE glosses
                                 LIKE \"%{}%\"""".format(k))
            t = c4.fetchall()
        else:
            c4.execute("""SELECT id
                                 FROM words
                                 WHERE glosses
                                 LIKE \"% {} %\"""".format(k))
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


def values():
    d = {}
    conn = sqlite3.connect("glosses.sqlite")
    c6 = conn.cursor()
    c6.execute("""SELECT id
                         FROM glosses""")
    m = c6.fetchall()
    graph_1(m)
    graph_2(m)
    graph_3(m)
    graph_4(m)
    graph_5(m)
    graph_6(m)


def graph_1(m):
    x1 = []
    y1 = []
    for arr in m:
        for i in arr:
            if i<= 21:
                conn = sqlite3.connect("w-to-g.sqlite")
                c7 = conn.cursor()
                c7.execute("""SELECT id_gloss
                                     FROM  words_to_glosses
                                     WHERE id_gloss = \"{}\" """.format(i))
                n = c7.fetchall()
                if (len(n)) != 0:
                    y1.append((len(n)))
                    conn = sqlite3.connect("glosses.sqlite")
                    c8 = conn.cursor()
                    c8.execute("""SELECT name
                                         FROM glosses
                                         WHERE id = \"{}\" """.format(i))
                    p = c8.fetchone()
                    for k in p:
                        x1.append(k)
            else:
                    continue
    plt.rc('xtick', labelsize=7) 
    plt.bar(x1, y1)
    plt.title("1")
    plt.xlabel("gloss")
    plt.ylabel("quantity")
    plt.savefig('plot_1.png')
    plt.figure()


def graph_2(m):
    x2 = []
    y2 = []
    for arr in m:
        for i in arr:
            if 22<=i<=24:
                conn = sqlite3.connect("w-to-g.sqlite")
                c10 = conn.cursor()
                c10.execute("""SELECT id_gloss
                                     FROM  words_to_glosses
                                     WHERE id_gloss = \"{}\" """.format(i))
                n = c10.fetchall()
                if (len(n)) != 0:
                    y2.append((len(n)))
                    conn = sqlite3.connect("glosses.sqlite")
                    c11 = conn.cursor()
                    c11.execute("""SELECT name
                                         FROM glosses
                                         WHERE id = \"{}\" """.format(i))
                    p = c11.fetchone()
                    for k in p:
                        x2.append(k)
            else:
                    continue
    plt.bar(x2, y2)
    plt.title("2")
    plt.xlabel("gloss")
    plt.ylabel("quantity")
    plt.savefig('plot_2.png')
    plt.figure()


def graph_3(m):
    x3 = []
    y3 = []
    for arr in m:
        for i in arr:
            if 25<=i<=31:
                conn = sqlite3.connect("w-to-g.sqlite")
                c7 = conn.cursor()
                c7.execute("""SELECT id_gloss
                                     FROM  words_to_glosses
                                     WHERE id_gloss = \"{}\" """.format(i))
                n = c7.fetchall()
                if (len(n)) != 0:
                    y3.append((len(n)))
                    conn = sqlite3.connect("glosses.sqlite")
                    c8 = conn.cursor()
                    c8.execute("""SELECT name
                                         FROM glosses
                                         WHERE id = \"{}\" """.format(i))
                    p = c8.fetchone()
                    for k in p:
                        x3.append(k)
            else:
                    continue
    plt.bar(x3, y3)
    plt.title("3")
    plt.xlabel("gloss")
    plt.ylabel("quantity")
    plt.savefig('plot_3.png')
    plt.figure()


def graph_4(m):
    x4 = []
    y4 = []
    for arr in m:
        for i in arr:
            if 32<=i<=40:
                conn = sqlite3.connect("w-to-g.sqlite")
                c7 = conn.cursor()
                c7.execute("""SELECT id_gloss
                                     FROM  words_to_glosses
                                     WHERE id_gloss = \"{}\" """.format(i))
                n = c7.fetchall()
                if (len(n)) != 0:
                    y4.append((len(n)))
                    conn = sqlite3.connect("glosses.sqlite")
                    c8 = conn.cursor()
                    c8.execute("""SELECT name
                                         FROM glosses
                                         WHERE id = \"{}\" """.format(i))
                    p = c8.fetchone()
                    for k in p:
                        x4.append(k)
            else:
                    continue
    plt.bar(x4, y4)
    plt.title("4")
    plt.xlabel("gloss")
    plt.ylabel("quantity")
    plt.savefig('plot_4.png')
    plt.figure()


def graph_5(m):
    x5 = []
    y5 = []
    for arr in m:
        for i in arr:
            if 41<=i<=42:
                conn = sqlite3.connect("w-to-g.sqlite")
                c7 = conn.cursor()
                c7.execute("""SELECT id_gloss
                                     FROM  words_to_glosses
                                     WHERE id_gloss = \"{}\" """.format(i))
                n = c7.fetchall()
                if (len(n)) != 0:
                    y5.append((len(n)))
                    conn = sqlite3.connect("glosses.sqlite")
                    c8 = conn.cursor()
                    c8.execute("""SELECT name
                                         FROM glosses
                                         WHERE id = \"{}\" """.format(i))
                    p = c8.fetchone()
                    for k in p:
                        x5.append(k)
            else:
                    continue
    plt.bar(x5, y5)
    plt.title("5")
    plt.xlabel("gloss")
    plt.ylabel("quantity")
    plt.savefig('plot_5.png')
    plt.figure()


def graph_6(m):
    x6 = []
    y6 = []
    for arr in m:
        for i in arr:
            if 43<=i<=48:
                conn = sqlite3.connect("w-to-g.sqlite")
                c7 = conn.cursor()
                c7.execute("""SELECT id_gloss
                                     FROM  words_to_glosses
                                     WHERE id_gloss = \"{}\" """.format(i))
                n = c7.fetchall()
                if (len(n)) != 0:
                    y6.append((len(n)))
                    conn = sqlite3.connect("glosses.sqlite")
                    c8 = conn.cursor()
                    c8.execute("""SELECT name
                                         FROM glosses
                                         WHERE id = \"{}\" """.format(i))
                    p = c8.fetchone()
                    for k in p:
                        x6.append(k)
            else:
                    continue
    plt.bar(x6, y6)
    plt.title("6")
    plt.xlabel("gloss")
    plt.ylabel("quantity")
    plt.savefig('plot_6.png')
    plt.figure()


def main():
    db_1()
    d = db_2()
    db_3(d)
    values()

    
if __name__ == "__main__":
        main()
