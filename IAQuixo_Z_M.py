import cherrypy
import sys
from copy import deepcopy
from random import choice


class Server:
    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def move(self):
        # Deal with CORS
        cherrypy.response.headers['Access-Control-Allow-Origin'] = '*'
        cherrypy.response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
        cherrypy.response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization, X-Requested-With'
        if cherrypy.request.method == "OPTIONS":
            return ''
        body = cherrypy.request.json

        lignes = {0 : [0,1,2,3,4],
        1 : [5,6,7,8,9],
        2 : [10,11,12,13,14],
        3 : [15,16,17,18,19],
        4 : [20,21,22,23,24]
        }
        colonnes = {0 : [0,5,10,15,20],
            1 : [1,6,11,16,21],
            2 : [2,7,12,17,22],
            3:  [3,8,13,18,23],
            4 : [4,9,14,19,24]
            }
        diagonales = {0 : [0,6,12,18,24],
             1 : [4,8,12,16,20]
             }
        def joueurs() :
            """
        Indique si on est le premier joueur
            """
            if body['you'] == body['players'][0] :
                nous = 0
                other = 1
            else:
                nous = 1
                other = 0 
            return [nous,other]
        def coups_possibles(dico):
            tout = {}
            case = [0,1,2,3,4,5,9,10,14,15,19,20,21,22,23,24]
            for i in case:
                if dico[i] != joueurs()[1]:
                    if i in [1,2,3]:
                        tout[i] = ["S","E","W"]
                    elif i in [5,10,15]:
                        tout[i] = ["S","E","N"]
                    elif i in [9,14,19]:
                        tout[i] = ["S","N","W"]
                    elif i in [21,22,23]:
                        tout[i] = ["N","E","W"]
                    elif i ==0:
                        tout[i] = ["S","E"]
                    elif i ==4:
                        tout[i] = ["S","W"]
                    elif i ==20:
                        tout[i] = ["E","N"]
                    elif i == 24:
                        tout[i] = ["N","W"]
            return tout

        def meilleurs_colonnes(dico) :
            score_colonnes = 0
            strat = []
            for i in coups_possibles(dico) :
                for n in colonnes :
                    if i in colonnes[n] :
                        for t in colonnes[n] :
                            if dico[t]== joueurs()[0] :
                                score_colonnes += 1
                strat += [score_colonnes]
                score_colonnes = 0
            return strat 

        def meilleurs_score(dico) :
            score_lignes = 0
            score_colonnes = 0
            score_diagonales = 0
            strat = []
            for i in coups_possibles(dico) :
                for n in lignes :
                    if i in lignes[n] :
                        for t in lignes[n] :
                            if dico[t] == joueurs()[0] :
                                score_lignes += 1
                for n in diagonales :
                    if i in diagonales[n] :
                        for t in diagonales[n] :
                            if dico[t]== joueurs()[0] :
                                score_diagonales += 1
                if score_lignes == 5 or score_colonnes  == 5  :
                    score_lignes = 1000 
                    score_colonnes = 1000
                strat += [score_lignes]
                score_lignes = 0
                score_colonnes = 0
                score_diagonales = 0

            return strat

        def essaier(): 
            best_move = {}
            etat_jeu = deepcopy(body['game'])
            for i in coups_possibles(etat_jeu) :
                for n in lignes : 
                    if i in lignes[n] :
                        S = 20-n* 5
                        N = (4-n)*5 -20
                for n in colonnes : 
                    if i in colonnes[n]:
                        E = 4 - n
                        W = -n
                Nc = 0
                Wc = 0
                Sc = 0
                Ec = 0
                etat_jeu = deepcopy( body['game'])
                print(body['game'])
                if S != 0 :
                    etat_jeu[i+S] = joueurs()[0]
                    t = etat_jeu[i+5]
                    print(t,i)
                    etat_jeu[i] = t 
                    print(etat_jeu)
                    Sc = max(max(meilleurs_score(etat_jeu)),max(meilleurs_colonnes(etat_jeu)))
                etat_jeu = deepcopy( body['game'])
                if N != 0 :
                    etat_jeu[i+N] = joueurs()[0]
                    t = body['game'][i-5]
                    etat_jeu[i] = t 
                    Nc = max(max(meilleurs_score(etat_jeu)),max(meilleurs_colonnes(etat_jeu)))
                etat_jeu = deepcopy( body['game'])
                if E!= 0 :
                    etat_jeu[i+E] = joueurs()[0]
                    t = body['game'][i+1]
                    etat_jeu[i] = t 
                    Ec = max(max(meilleurs_score(etat_jeu)),max(meilleurs_colonnes(etat_jeu)))
                etat_jeu = deepcopy( body['game'])
                if W!=0 :
                    etat_jeu[i+W] = joueurs()[0]
                    t = body['game'][i-1]
                    etat_jeu[i] = t 
                    Wc = max(max(meilleurs_score(etat_jeu)),max(meilleurs_colonnes(etat_jeu)))
                if max(Wc,Nc,Ec,Sc) == Wc and max(Wc,Nc,Ec,Sc) == Ec and max(Wc,Nc,Ec,Sc) == Sc and max(Wc,Nc,Ec,Sc) == Nc :
                    meilleur_direc = choice(['W','E','S','N'])
                elif max(Wc,Nc,Ec,Sc) == Wc and max(Wc,Nc,Ec,Sc) == Nc and max(Wc,Nc,Ec,Sc) == Sc :
                    meilleur_direc = choice(['W','N','S'])
                elif max(Wc,Nc,Ec,Sc) == Nc and max(Wc,Nc,Ec,Sc) == Ec and max(Wc,Nc,Ec,Sc) == Sc :
                    meilleur_direc = choice(['N','E','S'])
                elif max(Wc,Nc,Ec,Sc) == Sc and max(Wc,Nc,Ec,Sc) == Ec and max(Wc,Nc,Ec,Sc) == Wc :
                    meilleur_direc = choice(['S','E','W'])
                elif max(Wc,Nc,Ec,Sc) == Wc and max(Wc,Nc,Ec,Sc) == Ec and max(Wc,Nc,Ec,Sc) == Nc :
                    meilleur_direc = choice(['W','E','N'])
                elif max(Wc,Nc,Ec,Sc) == Nc and max(Wc,Nc,Ec,Sc) == Ec :
                    meilleur_direc = choice(['N','E'])
                elif max(Wc,Nc,Ec,Sc) == Wc and max(Wc,Nc,Ec,Sc) == Ec :
                    meilleur_direc = choice(['W','E'])
                elif max(Wc,Nc,Ec,Sc) == Nc and max(Wc,Nc,Ec,Sc) == Wc :
                    meilleur_direc = choice(['N','W'])
                elif max(Wc,Nc,Ec,Sc) == Wc and max(Wc,Nc,Ec,Sc) == Sc :
                    meilleur_direc = choice(['W','S'])
                elif max(Wc,Nc,Ec,Sc) == Ec and max(Wc,Nc,Ec,Sc) == Sc :
                    meilleur_direc = choice(['S','E'])
                elif max(Wc,Nc,Ec,Sc) == Nc and max(Wc,Nc,Ec,Sc) == Sc :
                    meilleur_direc = choice(['N','S'])
                elif max(Wc,Nc,Ec,Sc) == Wc :
                    meilleur_direc = 'W'
                elif max(Wc,Nc,Ec,Sc) == Ec :
                    meilleur_direc = 'E'
                elif max(Wc,Nc,Ec,Sc) == Nc :
                    meilleur_direc = 'N' 
                elif max(Wc,Nc,Ec,Sc) == Sc :
                    meilleur_direc = 'S'
                best_move[i] = [meilleur_direc,max(Wc,Nc,Ec,Sc)]
            return best_move

        cube = essaier()
        
        print(cube)
        resulti = []
        for i in cube :
            resulti += [cube[i][1]]
        for i in cube : 
            if cube[i][1] == max(resulti) :
                direc = i 
        print(direc)
        print(cube[direc][0])

        return {
	"move": {
		"cube": direc,
		"direction":cube[direc][0]
	},
	"message": "cheh"
}

if __name__ == "__main__":
    if len(sys.argv) > 1:
        port=int(sys.argv[1])
    else:
        port=8082

    cherrypy.config.update({'server.socket_host': '0.0.0.0', 'server.socket_port': port})
    cherrypy.quickstart(Server())