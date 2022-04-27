import json
from scipy.stats import poisson
import numpy as np
import matplotlib.pyplot as plt


campionato_home =[]
campionato_away=[]
campionato_form=[]

f= open('serie-a_33.json')
#dati presi da fotmob.com
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
    
    tmp['partite']= int(partite)
    tmp['goal_fatti']= int(goal_fatti)
    tmp['goal_subiti']= int(goal_subiti)
    tmp['media_goal_fatti']= float(goal_fatti)/int(partite)
    
    tmp['media_goal_subiti']= float(goal_subiti)/int(partite)
    tmp['attacking_strength'] = float(tmp['media_goal_fatti'])/float(avgleague_fatti)
    
    tmp['defensive_strength'] = float(tmp['media_goal_subiti'])/float(avgleague_subiti)
    
    #per ogni squadra calcolo un attacking e defensive strength sia in casa che fuori
    #di base calcola quanto meglio o peggio è quella squadra rispetto alla media
    #es. se una squadra ha un attacking strength di 1.1 significa che è poco sopra alla media, incrementando quindi leggermente i suoi xgoal
    #se una squadra ha un defensive strength di 1.7 chiaramente va ad aumentare molto i goal avversari attesi ecc...
    #di fatto si misura dividendo il dato della squadra per la media del campionato, semplice semplice no? ;-)

    return tmp

def parse_seriea():
    #stringhe il percorso per prendere dati dal json
    totale=data['table']['all']
    home=data['table']['home']
    away=data['table']['away']
    form=data['table']['form']

    totale_partite=0
    totale_goal=0
    avg_goalp90=0

    totale_goal_home_fatti=0
    totale_goal_home_subiti=0
    totale_goal_away_fatti=0
    totale_goal_away_subiti=0
    totale_goal_last5_fatti=0
    totale_goal_last5_subiti=0
    
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

    for squadra in form: 
        
        totale_goal_last5_fatti+=parse_goal(squadra['scoresStr'], 0) 
        totale_goal_last5_subiti+=parse_goal(squadra['scoresStr'], 2) 
    
    avg_goal_fattip90_last5= float(totale_goal_away_fatti) / 5
    avg_goal_subitip90_last5= float(totale_goal_away_subiti) / 5

    
    for squadra in home: 
        #print ("HOME")
        fatti=parse_goal(squadra['scoresStr'], 0)
        subiti=parse_goal(squadra['scoresStr'], 2)
        campionato_home.append(dictify_element(squadra['name'], squadra['played'], fatti, subiti, avg_goal_fattip90_home, avg_goal_subitip90_home))

    for squadra in away: 
        #print ("AWAY")
        fatti=parse_goal(squadra['scoresStr'], 0)
        subiti=parse_goal(squadra['scoresStr'], 2)
        campionato_away.append(dictify_element(squadra['name'],squadra['played'], fatti, subiti, avg_goal_fattip90_away, avg_goal_subitip90_away))

    for squadra in form: 
        #print ("AWAY")
        fatti=parse_goal(squadra['scoresStr'], 0)
        subiti=parse_goal(squadra['scoresStr'], 2)
        campionato_form.append(dictify_element(squadra['name'],squadra['played'], fatti, subiti, avg_goal_fattip90_last5, avg_goal_subitip90_last5))


#expected goals per squadra di casa di un match
#attacking strength casa * defensive strength away * media goal casa

def plot_goal (goal_home, goal_away, home_team, away_team, goal_home_form, goal_away_form):
    barWidth=0.25
    aa= np.linspace(0, 7, num=8)
    bb=[x + barWidth for x in aa]
    cc=[x + barWidth for x in bb]
    dd=[x + barWidth for x in cc]
    
    home_team_form=home_team+ " form"
    away_team_form=away_team+ " form"

    fig, ax = plt.subplots()

    #funzioni che aggiungono colonne nell'istogramma: le prime due sono i goal senza tener conto della forma, le altre due il contrario
    plt.bar(aa, goal_home, label=home_team, align='center', color='b', width = barWidth)
    plt.bar(bb, goal_away, label=away_team, align='center', color='r', width = barWidth)
    plt.bar(cc, goal_home_form, label=home_team_form, align='center', color='g', width = barWidth)
    plt.bar(dd, goal_away_form, label=away_team_form, align='center', color='y', width = barWidth)
    
    plt.legend()
    plt.show()
    

def plot_results (goal_home, goal_away, goal_home_form, goal_away_form):

    a=np.array(goal_home)
    b=np.array(goal_away)
    print("+++++++++++++")
    data=np.outer(a, b)
    indice=0
    np.set_printoptions(precision=3, suppress=True)
    print(data)
        
    """"
    for a in data:
        somma=0
        print(a)
        for q in a:
            somma+=q
        print("squadra A segna " + str(indice) + " goal")
        indice+=1
        print(somma)
    """    

    plt.imshow(data, cmap="rainbow")
    plt.colorbar()
    plt.show()

def calcola_giornata(home_team, away_team):

    #cerco home_team in campionato_home
    att_str_casa=1
    def_str_casa=1
    avg_goal_casa=0

    att_str_away=1
    def_str_away=1
    avg_goal_away=0

    att_str_last5_home=1
    def_str_last5_home=1
    avg_goal_last5_home=0

    att_str_last5_away=1
    def_str_last5_away=1
    avg_goal_last5_away=0

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

    for squadra in campionato_form:
        if squadra['nome']== home_team:
            att_str_last5_home=squadra['attacking_strength']
            def_str_last5_home=squadra['defensive_strength']
            avg_goal_last5_home=squadra['media_goal_fatti']
            

        if squadra['nome']== away_team:
            att_str_last5_away=squadra['attacking_strength']
            def_str_last5_away=squadra['defensive_strength']
            avg_goal_last5_away=squadra['media_goal_fatti']

    #questo numero è la quantità di goal che si aspetta che la squadra di casa segni 
    #è un numero decimale che poi passo alla distribuzione di poisson per elaborare le probabilità per ciascuna fascia di goal
    xgcasa=att_str_casa*def_str_away*avg_goal_casa
    np.round(xgcasa, decimals=3)
    #stessa roba, ma squadra ospite
    xgaway=att_str_away*def_str_casa*avg_goal_away
    np.round(xgaway, decimals=3)
    
    #questa è la misura dei goal attesi integrando anche un attacking strenght della squadra basata sulle ultime 5 di campionato
    #non è manco necessario aggiungere che questa roba produca una monnezza immonda quando la ficchi dentro poisson, però la lascio qui
    #sia mai che un giorno.... chissà, crescendo magari...
    xgcasa_form=att_str_casa*def_str_away*avg_goal_casa*att_str_last5_home*def_str_last5_away
    
    xgaway_form=att_str_away*def_str_casa*avg_goal_away*att_str_last5_away*def_str_last5_away
    
    #array in cui salvo le probabilità dei goal 
    #(goal_home[0] conterrà la probabilità che la squadra di casa segni 0 goal ecc...)
    goal_home=[]
    goal_away=[]
    goal_home_form=[]
    goal_away_form=[]
    for i in range (0,8):
        print(i)
        #ora uso i goal attesi per fare robe con poisson
        x = poisson.pmf(i, mu=xgcasa, loc=0)
        y = poisson.pmf(i, mu=xgaway, loc=0)
        z = poisson.pmf(i, mu=xgcasa_form, loc=0)
        k = poisson.pmf(i, mu=xgaway_form, loc=0)
        
        
        goal_home.append(x)
        goal_away.append(y)
        goal_home_form.append(z)
        goal_away_form.append(k)

    
    #funzione che fa un istogramma in cui mostra le probabilità delle squadre di fare 0,1 ecc... goal
    #ci sono anche le probabilità usando gli xgoal con la forma, mostrando appieno quanto sia disgustoso il risultato
    plot_goal(goal_home, goal_away, home_team, away_team, goal_home_form, goal_away_form)
    #plot_goal(goal_home_form ,goal_away_form, home_team, away_team)

    #funzione deliziosa che mostra con un amabile grafico colorato quanto è probabile ogni esito
    #plot_results(goal_home, goal_away)


    

parse_seriea()
#chiaramente per inserire le squadre in calcola giornata è necessario attenersi ai nomi di fotmob altrimenti è tutto un cazzo... PORCODIO!
calcola_giornata("Inter", "Roma")
