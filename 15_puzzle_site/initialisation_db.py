import sqlite3

# A exécuter dans le dossier 15_puzzle_site

def init_database():
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Game(
            id INTEGER PRIMARY KEY,
            grille VARCHAR(200),
            nbr_lignes INTEGER,
            nbr_colonnes INTEGER,
            nbr_coups INTEGER,
            win BOOLEAN,
            register BOOLEAN
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Winner(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pseudo VARCHAR(200),
            nbr_coups INTEGER
        )
    ''')

    cursor.close()
    conn.close()

def delete_database():
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()

    cursor.execute('''
        DROP TABLE IF EXISTS Game
    ''')

    cursor.execute('''
        DROP TABLE IF EXISTS Winner
    ''')    

    conn.commit()

    cursor.close()
    conn.close()

init_database()
#delete_database()