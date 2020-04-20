from django.http import JsonResponse, HttpRequest, HttpResponse
from . import database as db

def play(request):
    monobjet = {}
    id = db.nouvelle_partie()
    res = db.find_identifiant(id)
    return JsonResponse(res)

def deplacement(request):
    i = int(request.GET["i"])
    j = int(request.GET["j"])
    id = int(request.GET["id"])
    res = db.find_identifiant(id)
    grille = res['grille']
    if i > 0 and grille[i-1][j] == 0:
        grille[i-1][j], grille[i][j] = grille[i][j], grille[i-1][j]
        res['nbr_coups'] += 1
    elif i < res['nbr_lignes'] - 1 and grille[i+1][j] == 0:
        grille[i+1][j], grille[i][j] = grille[i][j], grille[i+1][j]
        res['nbr_coups'] += 1
    elif j > 0 and grille[i][j-1] == 0:
        grille[i][j-1], grille[i][j] = grille[i][j], grille[i][j-1]
        res['nbr_coups'] += 1
    elif j < res['nbr_colonnes'] - 1 and grille[i][j+1] == 0:
        grille[i][j+1], grille[i][j] = grille[i][j], grille[i][j+1]
        res['nbr_coups'] += 1
    res['win'] = db.test_victoire(grille)
    res['register'] = res['register'] == 'True'
    db.update(res)
    return JsonResponse(res)

def victoire(request):
    id = int(request.GET["id"])
    res = db.find_identifiant(id)
    nom = request.GET["nom"]
    if res["win"] == "True" and res["register"] == "False":
        db.register(nom, res["nbr_coups"])
        res["register"] = True
        db.update(res)
    return JsonResponse({})

def score(request):
    res = db.score()
    return JsonResponse({'res' : res})