from tkinter import*
from math import*
from copy import deepcopy

# Creation de la fenêtre
grid_window = Tk()
grid_window.title("Pathfinding - A* Algorithm")
grid_window.aspect(1,1,1,1)
grid_window.resizable(False, False)

# Variables à modifier selon les coordonnées de départ




def colorier_case(coord0,col_arg="green"):
    mainCanvas.delete("carre")
    window_coord=[(coord0[0] + abs(coord1[0]))*pas , (coord0[1] + abs(coord1[1]))*pas]
    if not (0<=window_coord[0]<=largeur_bc*pas):
        print("erreur")
    elif not (0<=window_coord[1]<=hauteur_bc*pas):
        print("erreur 2")
        
    mainCanvas.create_rectangle(window_coord[0],window_coord[1],window_coord[0]+pas,window_coord[1]+pas,fill=col_arg,tag="carre")
    
    

# Clique droit pour remettre la bonne taille de fenêtre
def setup(coord1,coord2):
    global largeur_bc,hauteur_bc,pas
    largeur_bc = abs(coord2[0] - coord1[0]) + 1
    hauteur_bc = abs(coord2[1] - coord1[1]) + 1
    
    
    # Le pas doit dépendre des hauteurs/largeurs pour rentrer dans l'écran.
    pas=int(900/((hauteur_bc+largeur_bc)/2))
    
    # La taille de la fenêtre, REEL * PAS
    grid_window.geometry('%dx%d' % (largeur_bc*pas, hauteur_bc*pas))
    
    #create_grid()
    create_grid()
    


# Clique gauche pour tracer à nouveau les lignes
# Objectif principal : assimiler "liste_selon_hauteur" et "liste_selon_largeur" aux vrais coordonnées.
# Une fonction s'impose


def create_grid():
    mainCanvas.delete("ligne")
    
    # On doit pouvoir générer le bon nombre de carré (en ligne, et en colonne)
    # Là, c'est bon !


    # Génération de lignes sur toute la hauteur (haut en bas), avec un pas proportionnel aux coordonnées
    for i in range(0,hauteur,pas):
        mainCanvas.create_line([(0,i), (largeur,i)], tag="ligne")
    
    
    # Génération de lignes sur toute la largeur (gauce à droite), avec un pas proportionnel aux coordonnées
    for i in range(0,largeur,pas):
        mainCanvas.create_line([(i,0), (i,hauteur)], tag="ligne")
    

    mainCanvas.mainloop()


mainCanvas=Canvas(grid_window,bg="lightgray")
mainCanvas.pack(fill=BOTH,expand=1)



grid_window.mainloop()