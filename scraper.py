import json

campionato_home =[]
campionato_away=[]

giornata= [
    ["Cagliari", "Sassuolo"],
    ["Milan", "Genoa"],
    ["Inter", "Spezia"],
    ["Napoli", "Roma"],
    ["Udinese", "Empoli"],
    ["Lazio", "Torino"],
    ["Juventus", "Bologna"],
    ["Sampdoria", "Salernitana"],
    ["Atalanta", "Hellas Verona"],
    ["Fiorentina", "Venezia"],

]

f= open('seriea.json')
#dati presi da fotmob
data=json.load(f)

def parse_goal (stringa, num) :
    #formato stringa "goal_fatti-goal_subiti
    #num=0 ritorna fatti, num=2 ritorna subiti
    goal_fatti= stringa.partition("-")[num]
    return int(goal_fatti)

def dictify_element(nome, partite, goal_fatti, goal_subiti, avgleague_fatti, avgleague_subiti):
    #funzione che ritorna qualcosa da appendere a alla matrice
    #Nome partite - goal fatti - goal subiti - media goal fatti - media goal subiti - attacking/defensive strenght
    tmp={}

    tmp['nome']= nome
    print(tmp['nome'])
    tmp['partite']= int(partite)
    tmp['goal_fatti']= int(goal_fatti)
    tmp['goal_subiti']= int(goal_subiti)
    tmp['media_goal_fatti']= float(goal_fatti)/int(partite)
    print("media goal fatti")
    print(tmp['media_goal_fatti'])
    tmp['media_goal_subiti']= float(goal_subiti)/int(partite)
    tmp['attacking_strength'] = float(tmp['media_goal_fatti'])/float(avgleague_fatti)
    print("attacking strength")
    print(tmp['attacking_strength'])
    tmp['defensive_strength'] = float(tmp['media_goal_subiti'])/float(avgleague_subiti)
    print("defensive strength")
    print(tmp['defensive_strength'])
    print("////////////")
    return tmp

def parse_seriea():
    #stringhe il percorso per prendere dati dal json
    totale=data['table']['all']
    home=data['table']['home']
    away=data['table']['away']

    totale_partite=0
    totale_goal=0
    avg_goalp90=0

    totale_goal_home_fatti=0
    totale_goal_home_subiti=0
    totale_goal_away_fatti=0
    totale_goal_away_subiti=0
    
    totale_partite_home=0
    totale_partite_away=0
    #le due tabelle che contengono i dati dei goal di tutte le squadre, nello specifico vengono salvate
    #nome, partite disputate, goal fatti e subiti (in casa e fuori, ma in tab separate),
    #media dei goal fatti e subiti, forza difensiva e offensiva rispetto alla media del campionato
    

    

    for squadra in home: 
        
        totale_partite_home+=squadra['played']
        totale_goal_home_fatti+=parse_goal(squadra['scoresStr'], 0)
        totale_goal_home_subiti+=parse_goal(squadra['scoresStr'], 2)
    
    avg_goal_fattip90_home= float(totale_goal_home_fatti) / float(totale_partite_home)   
    avg_goal_subitip90_home= float(totale_goal_home_subiti) / float(totale_partite_home)   

    for squadra in away: 
        
        totale_partite_away+=squadra['played']
        totale_goal_away_fatti+=parse_goal(squadra['scoresStr'], 0) 
        totale_goal_away_subiti+=parse_goal(squadra['scoresStr'], 2) 
    
    avg_goal_fattip90_away= float(totale_goal_away_fatti) / float(totale_partite_away) 
    avg_goal_subitip90_away= float(totale_goal_away_subiti) / float(totale_partite_away) 


    
    for squadra in home: 
        print ("HOME")
        fatti=parse_goal(squadra['scoresStr'], 0)
        subiti=parse_goal(squadra['scoresStr'], 2)
        campionato_home.append(dictify_element(squadra['name'], squadra['played'], fatti, subiti, avg_goal_fattip90_home, avg_goal_subitip90_home))

    for squadra in away: 
        print ("AWAY")
        fatti=parse_goal(squadra['scoresStr'], 0)
        subiti=parse_goal(squadra['scoresStr'], 2)
        campionato_away.append(dictify_element(squadra['name'],squadra['played'], fatti, subiti, avg_goal_fattip90_away, avg_goal_subitip90_away))


#expected goals per squadra di casa di un match
#attacking strength casa * defensive strength away * media goal casa

def calcola_giornata(home_team, away_team):
    #cerco home_team in campionato_home
    att_str_casa=1
    def_str_casa=1
    avg_goal_casa=0

    att_str_away=1
    def_str_away=1
    avg_goal_away=0

    for squadra in campionato_home:
        if squadra['nome']== home_team:
            att_str_casa=squadra['attacking_strength']
            def_str_casa=squadra['defensive_strength']
            avg_goal_casa=squadra['media_goal_fatti']
            break
    
    for squadra in campionato_away:
        if squadra['nome']== away_team:
            att_str_away=squadra['attacking_strength']
            def_str_away=squadra['defensive_strength']
            avg_goal_away=squadra['media_goal_fatti']
            break
    
    xgcasa=att_str_casa*def_str_away*avg_goal_casa
    print(xgcasa)
    xgaway=att_str_away*def_str_casa*avg_goal_away
    print(xgaway)



parse_seriea()
calcola_giornata("Udinese", "Empoli")
