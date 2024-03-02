#PERICICA MEDEEA-MARIA, GRUPA 144
#ISCRU BIANCA, GRUPA 144

# Avem 3 fisiere de input.
# "input_joc.in" - este configuration file pentru joc
# "input_CFG.in" - este configuration file pentru CFG pentru comenzi
# "comenzi.in" - contine comenzile pe care le da jucatorul pentru un traseu.
# "comenzi.in" - trebuie sa contina fiecare comanda una sub alta, neseparte prin virgula

# Urmatoarele functii pana la linia 80 sunt cele de la subiectul 2 si verifica ca fisierul de input_joc dat sa fie corect

# Se verifica ca fisierul "input_CFG.in" sa fie valid prin functia verificare_fisier_CFG()
# Vom verifica ca comenzile primite in "comenzi.in" sa fie validate de catre CFG, adica sa nu existe o comanda de forma "go invitation" sau "take kitchen" sau "look diningRoom"


def citire_date(fisier):
    f=open(fisier, "r")
    linie=f.readline()
    ok=0
    while(linie):
        linie=linie.strip()
        if linie in ["alfabet input:", "alfabet lista:", "stari LA:", "tranzitii:"]: # verificam la ce linie am ajuns pentru a sti in ce cheie a dictionarului bagam urmatoarele linii citite
            x = linie[:len(linie)-1] #scoatem semnul : de la fiecare cheie a dictionarului si memoram cheia dictionarului la care ne aflam
        elif "#" not in linie: # daca totusi linia nu este nici un subtitlu si nici un #, atunci inseamna ca adaugam liniile citite in d[x]

            if(x == "tranzitii"): # tranzitiile sunt singurele linii care vor avea ", " in ele, pe care vrem sa le separam intr o lista de liste
                linie = linie.split(", ")
                d[x].append(linie) # adaugam lista nou formata la d["tranzitii"], astfel vom avea o lista de liste

            elif (x == "stari LA"):  # starile LA pot avea 4 formate: "q0", "q0, S" ; "q0, F"; "q0, S, F"
                poz = linie.find(",") # verificam daca exista virgula in formatul citit si ii aflam pozitia
                nr = linie.count(",") # memoram de cate ori apare virgula in format. Variantele sunt 0, 1 sau 2
                if poz != -1: # daca am gasit virgula inseamna ca acea stare este ori de start, ori finala, ori ambele
                    if(nr == 2): # nr = 2 => starea este si de strat si de final
                        d["stari finale"].append(linie[:poz]) # adaugam starea
                        d["stare start"].append(linie[:poz])
                    elif(nr == 1): #nr = 1 => starea actuala este ori stare initiala ori finala
                        if linie[len(linie) - 1:] == "S": 
                            d["stare start"].append(linie[:poz])
                        else:
                            d["stari finale"].append(linie[:poz])
                    d[x].append(linie[:poz])
                elif poz == -1: # nu am gasit nicio virgula => starea este una normala, fara caz special
                    d[x].append(linie)
            else:
                d[x].append(linie) # adaugam restul liniilor la cheia potrivita
        linie=f.readline()

def verificare_stari(d):  # functie pentru a verificare daca starile din tranzitii exista in starile LA date in input
    for t in d["tranzitii"]:
        if( t[0] not in d["stari LA"] or t[3] not in d["stari LA"]):
            return 0

def verificare_input(d): # functie pentru a verifica daca w1 , w2 ... wm se afla in alfabetul LA, unde w = string citit = w1w2...wm
    for t in d["tranzitii"]:
        if( t[1] not in d["alfabet input"] ):
            return 0

def verificare_alfabet_lista(d): # functie pentru a verifica daca ce cautam in lista, ce adaugam si ce vrem sa scoatem din lista exista in alfabetul listei
    for t in d["tranzitii"]:
        if( (t[2] not in d["alfabet lista"] and t[2] != "E")  or ( t[4] not in d["alfabet lista"] and t[4] != "E")  or ( t[5] not in d["alfabet lista"] and t[5] != "E" ))  :
            return 0
        
def verificare_numar_stari_start_final(d): # functie pentru a verifica daca avem o singura stare initiala si cel putin una finala
    if ( len(d["stare start"]) != 1 or len(d["stari finale"]) < 1):
        return 0

def adaugare_lista(l, c):
    if c not in l:
        l.append(c)

def verificare_lista(l, c):
    if c in l:
        return 1
    return 0

def scoatere_lista(l, c):
    l=l.remove(c)

def parcurgere_lista_comenzi(listaComenzi):
    camera_curenta = d["stare start"][0] # camera_curenta = camera din care pornim = entrance hall
    l=[]
    for comandaCurenta in listaComenzi: # lista comenzi o sa fie de un tip dintre: [take item], [go room_name], [inventory], [drop item], [look]
        if(comandaCurenta[0] == "inventory"):
            print("lucrurile din posesia jucatorului cand a ajuns la camera ", camera_curenta, ": ", l) # printam lista de iteme curenta
        elif(comandaCurenta[0] == "drop"):
            scoatere_lista(l, comandaCurenta[1]) # dam drop la item-ul cerut
        elif(comandaCurenta[0] == "look"): # pentru comanda look am facut o functie separata
            camereAdiacente(camera_curenta)
        else: # cazurile "take" si "go" sunt mai sepciale si vor fi tratate aici:
            for t in d["tranzitii"]:  # parcurgem fiecare tranzitie
                tranzitie_gasita = 0
                if t[0] == camera_curenta and t[1] == comandaCurenta[0] and tranzitie_gasita == 0: # am gasit o tranzitie care sa inceapa din camera noastra curenta si sa aiba comanda egala cu coamnda din lista ( take sau go)
                    if(comandaCurenta[0] == "take"): #daca comanda este take 
                        if(t[5] == comandaCurenta[1]): #atunci vreau sa verific ca item-ul din tranzitie sa fie egal cu itemul din din comanda 
                            tranzitie_gasita = 1 # am gasit tranzitia care sa mi indeplineasca conditiile, nu e nevoie sa schimb camera curenta, raman in aceeasi camera 
                            if (tranzitie_gasita == 1):
                                camera_curenta = t[0]
                                if( t[4] != "E"): # daca tranzitia implica sa dam drop la un obiect, il scoatem din lista
                                    scoatere_lista(l, t[4])
                                if( t[5] != "E"): #daca tranzitia implica sa adaugam un obiect, il punem in lista
                                    adaugare_lista(l, t[5])
                                break
                    elif(comandaCurenta[0] == "go"): #daca actiunea este go 
                        if(t[3] == comandaCurenta[1]): #atunci vreau sa verific ca camera in care ajung din tranzitie (starea in care ajung) sa fie egal cu camera in care vreau sa ajung din comanda data
                            if ( (t[2] != "E" and verificare_lista(l, t[2]) == 1) or t[2]== "E"): # pentru a intra in anumite camere, avem nevoie sa verificam ca avem obiectul necesar. 
                                tranzitie_gasita = 1 # am gasit tranzitia care sa mi indeplineasca conditiile 
                            if (tranzitie_gasita == 1):
                                camera_curenta = t[3]
                if(tranzitie_gasita  == 1):
                    break
            if(tranzitie_gasita == 0): # daca am terminat de parcurs toate tranzitiile si nu am gasit niciuna potrivita, returnam 0
                return 0
    if(camera_curenta in d["stari finale"]): # pana acum au fost gsite toate tranzitiile. daca starea curenta face parte din starile finale, string-ul este acceptat
        return 1
    return 0

def camereAdiacente(camera_curenta):
    print("camera curenta este ", descriere_camere[camera_curenta], ", iar camerele adiacente sunt: ")
    for t in d["tranzitii"]:
        if t[0] == camera_curenta and t[1]=="go":
            print(descriere_camere[t[3]])

def citireComenzi(fisier):
    f=open(fisier, "r") #vom crea o lista de liste ce va contine fiecare comanda
    linie=f.readline()
    while(linie):
        linie=linie.strip()
        listaComenzi.append([x for x in linie.split(" ")])
        linie=f.readline()

def citire_date_CFG(fisier):
    f=open(fisier, "r")
    linie=f.readline()
    ok=0
    while(linie):
        linie=linie.strip()

        if linie == "Variables:":
            ok=1
        elif linie == "Terminals:":
            ok=2
        elif linie == "Productions:":
            ok=3

        if "#" not in linie and linie not in ["End", "Variables:", "Terminals:", "Productions:"]:
            if ok == 1 and linie !="Variables":
                dictCfg["variables"].append(linie)
            if ok == 2 and linie !="Terminals":
                dictCfg["terminals"].append(linie)
            if ok == 3 and linie !="Productions":
                dictCfg["productions"].append(linie)

        linie = f.readline()

def verificare_fisier_CFG(dictCfg):
    ok=1
    for x in dictCfg["productions"]:
        x=x.split(" ::= ")
        y= x[1].split(" | ")
        b = x[0][1 : len(x[0]) - 1]

        if b not in dictCfg["variables"]:
            ok=0
        
        for z in y:
            z=z.split(" ")
            for a in z:
                if "<" in a or ">" in a:
                    c=a[1:len(a)-1]
                    if c not in dictCfg["variables"]:
                        ok=0

                else:
                    if a != '""':
                        p=a[1:len(a)-1]
                        if p not in dictCfg["terminals"]:
                            ok=0
                    else:
                        if '""' not in dictCfg["terminals"]:
                            ok=0
    return ok

def creare_CFG(dictCfg):
    dict2={}
    for x in dictCfg["productions"]:
        x=x.split("> ::= ")
        y = x[1].split(" | ")
        b = x[0][1:]
        dict2[b] = []
        l=[]
        for a in y:
            a=a[:len(a)-1]
            a=a[1:]
            l.append(a)
        dict2[b] = l
    dictCfg["productions"] = dict2


def verificare_comanda_prin_CFG(dictCfg, listaComenzi):
    for comanda in listaComenzi:
        if(len(comanda) > 1):
            if(comanda[1] not in dictCfg["productions"][comanda[0]]):
                print("REJECT!! Comanda `", comanda[0] , comanda[1], "` nu a fost definita corect")
                return 0
    return 1        


descriere_camere={}
descriere_camere["entranceHall"] = "Entrance Hall: The grand foyer of the Castle of Illusions"
descriere_camere["diningRoom"] = "Dining Room: A room with a large table filled with an everlasting feast."
descriere_camere["kitchen"] = "Kitchen: A room packed with peculiar ingredients."
descriere_camere["pantry"] = "Pantry: A storage area for the Kitchen."
descriere_camere["armoury"] = "Armoury: A chamber filled with antiquated weapons and armour."
descriere_camere["treasury"] = "Treasury: A glittering room overflowing with gold and gemstones."
descriere_camere["library"] = "Library: A vast repository of ancient and enchanted texts."
descriere_camere["throneRoom"] = "Throne Room: The command center of the castle."
descriere_camere["wizardsStudy"] = "Wizard's Study: A room teeming with mystical artifacts."
descriere_camere["secretExit"] = "Secret Exit: The hidden passage that leads out of the Castle of Illusions."

d={}
d["alfabet input"]=[]
d["alfabet lista"]=[]
d["stari LA"]=[]
d["tranzitii"]=[]
d["stare start"]=[]
d["stari finale"]=[]
listaComenzi=[]

dictCfg={}
dictCfg["variables"]=[]
dictCfg["terminals"]=[]
dictCfg["productions"]=[]


citire_date("input_joc.in")
citireComenzi("comenzi.in")         
citire_date_CFG("input_CFG.in")
creare_CFG(dictCfg)

if(verificare_stari(d) == 0 or verificare_input(d) == 0 or verificare_alfabet_lista(d) == 0  or verificare_numar_stari_start_final(d) == 0):
    print("REJECT. inputul pentru joc nu este corect. Te rugam verifica daca starile, alfabetul si tranzitiile au fost definite corect")
elif (verificare_comanda_prin_CFG(dictCfg, listaComenzi) == 0):
    print("REJECT. lista de comenzi data nu este valida. Nu se va accepta o comanda de forma `go invitation` sau alte asemenea")
elif(parcurgere_lista_comenzi(listaComenzi) == 0):
    print("REJECT. Din pacate, jucatorul nu a putut ajunge in exitRoom. Te rugam introdu alte comenzi!")
else:
    print("felicitari! Comenzile au fost corecte! Dupa o noapte nedormita, jucatorul a ajuns in Exit Room!! ")
