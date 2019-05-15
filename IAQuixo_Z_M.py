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
        lines = {0 : [0,1,2,3,4],
        1 : [5,6,7,8,9],
        2 : [10,11,12,13,14],
        3 : [15,16,17,18,19],
        4 : [20,21,22,23,24]
        }
        columns = {0 : [0,5,10,15,20],
            1 : [1,6,11,16,21],
            2 : [2,7,12,17,22],
            3:  [3,8,13,18,23],
            4 : [4,9,14,19,24]
            }
        diagonals = {0 : [0,6,12,18,24],
             1 : [4,8,12,16,20]
             }
        def players() :
            """
        Indique le pion qu'on joue
            """
            if body['you'] == body['players'][0] :
                us = 0
                other = 1
            else:
                us = 1
                other = 0 
            return [us,other]

        def moves(dico):
            """
        Regarde si les cases qu'on peut bouger
            """
            play_move = {}
            case = [0,1,2,3,4,5,9,10,14,15,19,20,21,22,23,24]
            for i in case:
                if dico[i] != players()[1]:
                    if i in [1,2,3]:
                        play_move[i] = ["S","E","W"]
                    elif i in [5,10,15]:
                        play_move[i] = ["S","E","N"]
                    elif i in [9,14,19]:
                        play_move[i] = ["S","N","W"]
                    elif i in [21,22,23]:
                        play_move[i] = ["N","E","W"]
                    elif i ==0:
                        play_move[i] = ["S","E"]
                    elif i ==4:
                        play_move[i] = ["S","W"]
                    elif i ==20:
                        play_move[i] = ["E","N"]
                    elif i == 24:
                        play_move[i] = ["N","W"]
            return play_move

        def best_columns(dico) :
            """
        Regarde les nombres de pions dans une colonne
            """
            score_column = 0
            strat = []
            for i in moves(dico) :
                for n in columns :
                    if i in columns[n] :
                        for t in columns[n] :
                            if dico[t]== players()[0] :
                                score_column += 1
                strat += [score_column]
                score_column = 0
            return strat 

        def best_lines(dico) :
            """
        Regarde le nombre de pions dans une ligne
            """
            score_lignes = 0
            strat = []
            for i in moves(dico) :
                for n in lines :
                    if i in lines[n] :
                        for t in lines[n] :
                            if dico[t] == players()[0] :
                                score_lignes += 1
                strat += [score_lignes]
                score_lignes = 0
            return strat

        def best_play(): 
            """
        Prends les coups possibles avec la meilleur direction et le plus grand
        nombre de pions dans une ligne ou colonne
            """
            best_move = {}
            state_game = deepcopy(body['game'])
            for i in moves(state_game) :
                for n in lines : 
                    if i in lines[n] :
                        S = 20-n* 5
                        N = (4-n)*5 -20
                for n in columns : 
                    if i in columns[n]:
                        E = 4 - n
                        W = -n
                Nc = 0
                Wc = 0
                Sc = 0
                Ec = 0
                state_game = deepcopy( body['game'])
                if S != 0 :
                    j = i+5
                    m = i
                    L =S
                    while S >= 5  :
                        t = state_game[j]
                        state_game[m] = t 
                        m+=5
                        j+=5
                        S-=5
                    state_game[i+L] = players()[0]
                    Sc = max(max(best_lines(state_game)),max(best_columns(state_game)))
                state_game = deepcopy( body['game'])
                if N != 0 :
                    j = i-5
                    m = i
                    L =N
                    while N <= -5  :
                        t = state_game[j]
                        state_game[m] = t 
                        m-=5
                        j-=5
                        N+=5
                    state_game[i+L] = players()[0]
                    Nc = max(max(best_lines(state_game)),max(best_columns(state_game)))
                state_game = deepcopy( body['game'])
                if E!= 0 :
                    j = i+1
                    m = i
                    L =E
                    while E>= 1  :
                        t = state_game[j]
                        state_game[m] = t 
                        m+=1
                        j+=1
                        E-=1
                    state_game[i+L] = players()[0]
                    Ec = max(max(best_lines(state_game)),max(best_columns(state_game)))
                state_game = deepcopy( body['game'])
                if W!=0 :
                    j = i-1
                    m = i
                    L =W
                    while W<= -1  :
                        t = state_game[j]
                        state_game[m] = t 
                        m-=1
                        j-=1
                        W+=1
                    state_game[i+L] = players()[0]
                    Wc = max(max(best_lines(state_game)),max(best_columns(state_game)))
                if max(Wc,Nc,Ec,Sc) == Wc and max(Wc,Nc,Ec,Sc) == Ec and max(Wc,Nc,Ec,Sc) == Sc and max(Wc,Nc,Ec,Sc) == Nc :
                    best_direc = choice(['W','E','S','N'])
                elif max(Wc,Nc,Ec,Sc) == Wc and max(Wc,Nc,Ec,Sc) == Nc and max(Wc,Nc,Ec,Sc) == Sc :
                    best_direc = choice(['W','N','S'])
                elif max(Wc,Nc,Ec,Sc) == Nc and max(Wc,Nc,Ec,Sc) == Ec and max(Wc,Nc,Ec,Sc) == Sc :
                    best_direc = choice(['N','E','S'])
                elif max(Wc,Nc,Ec,Sc) == Sc and max(Wc,Nc,Ec,Sc) == Ec and max(Wc,Nc,Ec,Sc) == Wc :
                    best_direc = choice(['S','E','W'])
                elif max(Wc,Nc,Ec,Sc) == Wc and max(Wc,Nc,Ec,Sc) == Ec and max(Wc,Nc,Ec,Sc) == Nc :
                    best_direc = choice(['W','E','N'])
                elif max(Wc,Nc,Ec,Sc) == Nc and max(Wc,Nc,Ec,Sc) == Ec :
                    best_direc = choice(['N','E'])
                elif max(Wc,Nc,Ec,Sc) == Wc and max(Wc,Nc,Ec,Sc) == Ec :
                    best_direc = choice(['W','E'])
                elif max(Wc,Nc,Ec,Sc) == Nc and max(Wc,Nc,Ec,Sc) == Wc :
                    best_direc = choice(['N','W'])
                elif max(Wc,Nc,Ec,Sc) == Wc and max(Wc,Nc,Ec,Sc) == Sc :
                    best_direc = choice(['W','S'])
                elif max(Wc,Nc,Ec,Sc) == Ec and max(Wc,Nc,Ec,Sc) == Sc :
                    best_direc = choice(['S','E'])
                elif max(Wc,Nc,Ec,Sc) == Nc and max(Wc,Nc,Ec,Sc) == Sc :
                    best_direc = choice(['N','S'])
                elif max(Wc,Nc,Ec,Sc) == Wc :
                    best_direc = 'W'
                elif max(Wc,Nc,Ec,Sc) == Ec :
                    best_direc = 'E'
                elif max(Wc,Nc,Ec,Sc) == Nc :
                    best_direc = 'N' 
                elif max(Wc,Nc,Ec,Sc) == Sc :
                    best_direc = 'S'
                best_move[i] = [best_direc,max(Wc,Nc,Ec,Sc)]
            return best_move
        cube = best_play()
        result = []
        direc_max = []
        for i in cube :
            result += [cube[i][1]]
        for i in cube : 
            if cube[i][1] == max(result) :
                direc_max += [i]
        direc = choice(direc_max)
        message = choice(['Sah quel plaisir' , 'Cheh','/ff', 'Go jouer à OXO', 'Libérez Lacrim'])
        return {
	"move": {
		"cube": direc,
		"direction":cube[direc][0]
	},
	"message": message
}

if __name__ == "__main__":
    if len(sys.argv) > 1:
        port=int(sys.argv[1])
    else:
        port=8080

    cherrypy.config.update({'server.socket_host': '0.0.0.0', 'server.socket_port': port})
    cherrypy.quickstart(Server())