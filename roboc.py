# -*-coding:Utf-8 -*

"""Code principal du jeu."""

import os, re

from carte import *
from robot import *


# Chargement des parties en cours
# Si le fichier encours n'existe pas : création avec un dictionnaire vide
try:
    with open("encours", "rb") as fichier:
        encours = pickle.load(fichier)
except FileNotFoundError:
    with open("encours", "wb") as fichier:
        a = pickle.Pickler(fichier)
        a.dump(dict())
    encours = dict()

print("Contenu de 'encours' : {0}".format(encours))

# Liste des cartes existantes
cartes = list()
# Liste des parties en cours
parties = list()


def choix(liste_cartes):

    """Renvoie l'objet Carte correspondant au choix de l'utilisateur parmi la
    liste de cartes passée en paramètres (cartes existantes ou parties en cours)."""

    while 1:
        try:
            choix = int(input("\nSur quelle carte souhaitez-vous jouer ? "))
            assert choix in range(1, len(liste_cartes)+1)
        except ValueError:
            print("Saisie incorrecte ! Merci de saisir un nombre uniquement...")
            continue
        except AssertionError:
            print("Saisie incorrecte ! Le numero de carte n'existe pas...")
            continue
        else:
            index = choix-1
            carte_choisie = liste_cartes[index]
            break

    return carte_choisie


# Chargement des cartes existantes dans la liste 'cartes' et des parties en cours dans la liste 'parties'
# (chaque carte ou partie est un objet construit sur la classe Carte)
for fichier in os.listdir("cartes"):
    if fichier.endswith(".txt"):
        chemin = os.path.join("cartes", fichier)
        nom_carte = fichier[:-4]
        nom_carte = nom_carte[0].upper() + nom_carte[1:].lower()
        with open(chemin, "r") as fichier:
            contenu = fichier.read()
            carte = Carte(nom_carte, contenu)
            cartes.append(carte)
            for key, value in encours.items():
                if carte.nom == key:
                    carte.robot = value
                    parties.append(carte)

print("Cartes existantes : {0}".format(cartes, "\n"))
print("Parties en cours : {0}".format(parties, "\n"))

# S'il existe une partie en cours
if len(parties) > 0:

    # Stockage du choix de l'utilisateur dans 'reprendre'
    while 1:
        try:
            reprendre = int(input("Il existe une (des) partie(s) en cours, que souhaitez-vous faire ?\n\n  1 - Reprendre une partie\n  2 - Démarrer une nouvelle partie\n\nChoix : "))
            assert reprendre in range(1, 3)
        except ValueError:
            print("Saisie incorrecte ! Merci de saisir un nombre uniquement...")
            continue
        except AssertionError:
            print("Le choix doit être 1 ou 2... Recommencez !")
        else:
            reprendre = True if reprendre == 1 else False
            break

# Sinon, reprendre = False (aucune partie en cours)
else:
    reprendre = False


if reprendre:
    # Affichage des parties en cours
    print("Parties en cours :\n")
    for i, partie in enumerate(parties):
        print("  {0} - {1}".format(i + 1, partie.nom))
    carte_choisie = choix(parties)
else:
    # Affichage des cartes existantes
    print("Cartes existantes :\n")
    for i, carte in enumerate(cartes):
        print("  {0} - {1}".format(i + 1, carte.nom))
    carte_choisie = choix(cartes)


# Debut partie
print("{0}DEBUT DE LA PARTIE{0}(carte : {1})".format("\n", carte_choisie.nom))

# Instanciation d'un robot
robot = Robot(carte_choisie.robot)

# Affichage de la carte de départ
print("\n{0}\n".format(carte_choisie.chaine))

# Entrées actions utilisateur
while 1:

    action = input("Action : ").lower()
    pattern = "^q|([neso][1-9]*)$"

    if not re.fullmatch(pattern, action):
        print("Saisie erronée...")
        continue

    elif action == "q":
        robot.save_position(robot.coord, carte_choisie.succes, carte_choisie.nom)
        break

    else:
        # Calcul de la nouvelle position du robot
        coord = robot.set_position(action)
        x, y = coord

        # Si le robot tombe sur la sortie
        if coord == carte_choisie.succes:
            # Récupération de la grille mise à jour
            grille = carte_choisie.grille(coord)
            # Suppression de la partie en cours dans le fichier 'encours'
            robot.save_position(coord, carte_choisie.succes, carte_choisie.nom)
            # Affichage de la grille
            print("{1}{0}{1}{2}".format(grille, "\n", "Partie gagnee !"))
            # Fin de la partie
            break

        # Si la nouvelle position du robot tombe dans la grille
        if (0 < x < carte_choisie.largeur-1 and 0 < y < carte_choisie.hauteur-1):

            # Si la nouvelle position du robot ne tombe pas sur un obstacle
            if coord not in carte_choisie.obstacles:

                # Récupération de la grille mise à jour
                grille = carte_choisie.grille(coord)

                # Affichage de la grille
                print("{1}{0}{1}".format(grille, "\n"))

                # Mise à jour de la position du robot
                robot.coord = coord

                # Sauvegarde de la position du robot
                # robot.save_position(coord, carte_choisie.succes, carte_choisie.nom)

                continue

            # Si la nouvelle position du robot tombe sur un obstacle
            else:
                print("Le robot est tombé sur un obstacle. Recommencez !")
                continue
        # Si la nouvelle position du robot tombe hors-grille
        else:
            print("Action impossible ! Le robot serait sorti de la carte. Recommencez !")
            continue
