import sqlite3
import random as rnd
from . import parametres as pr

def find_identifiant(id):
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()    
    cursor.execute('''SELECT * FROM Game WHERE id= ?''',(id,))
    result = cursor.fetchall()
    cursor.close()
    conn.close() 
    if result == []:
        return None
    else:
        first_row = result[0]
        return {'id' : str(first_row[0]), 'grille' : chaine_to_grille(first_row[1]), 'nbr_lignes' : first_row[2], 'nbr_colonnes' : first_row[3], 'nbr_coups' : first_row[4], \
            'win' : first_row[5], 'register' : first_row[6]}

def nouvelle_partie():
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    new_id = rnd.randint(0, 1000000000000000)
    while find_identifiant(new_id) != None:
        new_id = rnd.randint(0, 1000000000000000)
    grille = [[i * pr.nbr_colonnes + j for j in range(pr.nbr_colonnes)] for i in range(pr.nbr_lignes)]
    for _ in range(pr.nbr_melange):
        i, j, k, l = 0, 0, 0, 0
        while (i == k and j == l) or grille[i][j] == 0 or grille[k][l] == 0:
            i = rnd.randint(0, pr.nbr_lignes - 1)
            k = rnd.randint(0, pr.nbr_lignes - 1)
            j = rnd.randint(0, pr.nbr_colonnes - 1)
            l = rnd.randint(0, pr.nbr_colonnes - 1)
        grille[i][j], grille[k][l] = grille[k][l], grille[i][j]
    chaine = grille_to_chaine(grille)
    cursor.execute('''INSERT INTO Game (id, grille, nbr_lignes, nbr_colonnes, nbr_coups, win, register)  VALUES (?, ?, ?, ?, 0, 'False', 'False')''', \
        (new_id, chaine, pr.nbr_lignes, pr.nbr_colonnes))
    conn.commit()
    cursor.close()
    conn.close()
    return new_id

def update(game):
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    cursor.execute('''UPDATE Game SET grille = ? WHERE id = ?''', (grille_to_chaine(game['grille']), game['id']))
    cursor.execute('''UPDATE Game SET nbr_coups = ? WHERE id = ?''', (game['nbr_coups'], game['id']))    
    cursor.execute('''UPDATE Game SET win = ? WHERE id = ?''', (str(game['win']), game['id']))
    cursor.execute('''UPDATE Game SET register = ? WHERE id = ?''', (str(game['register']), game['id']))
    conn.commit()
    cursor.close()
    conn.close()

def register(nom, nbr_coups):
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO Winner (pseudo,nbr_coups)  VALUES (?, ?)''', (nom, nbr_coups))
    conn.commit()
    cursor.close()
    conn.close()

def score():
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()    
    cursor.execute('''SELECT pseudo, nbr_coups FROM Winner ORDER BY nbr_coups ASC''')
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

def grille_to_chaine(grille):
    chaine = ""
    for i in range(pr.nbr_lignes):
        for j in range(pr.nbr_colonnes):
            chaine += str(grille[i][j]) + "\t"
        chaine += "\n"
    return chaine

def chaine_to_grille(chaine):
    grille = []
    for row in chaine[:-1].split("\n"):
        ligne = []
        for n in row[:-1].split("\t"):
            ligne.append(int(n))
        grille.append(ligne)
    return grille

def test_victoire(grille):
    nbr_lignes = len(grille)
    nbr_colonnes = len(grille[0])
    for i in range(nbr_lignes):
        for j in range(nbr_colonnes):
            if grille[i][j] != i*nbr_colonnes + j:
                return False
    return True