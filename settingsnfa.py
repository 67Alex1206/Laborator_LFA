from settingsdfa import get_data, get_sections
from collections import defaultdict

def epsilon(x,d):
    current_states=x.copy()
    ok=1
    while ok==1: #verific daca s-a adaugat ceva data trecuta
        tba_states=set()
        ok=0
        for t in d["Delta"]:
            if t[0] in current_states and t[1]=="e": #daca starea curenta are tranzitie cu epsilon
                if t[2] not in current_states: #daca rezultatul tranzitiei nu e deja stare curenta
                    tba_states.add(t[2]) #adaug rezultatul la stari curente
                    ok=1
        current_states=current_states.union(tba_states)
    return current_states




def analyze_nfa(init_state,final_states,d,W):
    current_states=set()
    current_states.add(init_state)

    current_states=epsilon(current_states,d) # iau toate tranzitiile cu epsilon care pleaca din starea initiala si merg pe ele

    st = list(map(str, list(W)))
    for i in st:
        if i not in d["Sigma"]:
            return "Simbol necunoscut"
        else:
            tba_states=set()
            for t in d["Delta"]:
                if t[0] in current_states and t[1]==i:
                    tba_states.add(t[2])



        current_states=tba_states

        current_states = epsilon(current_states, d) # verific daca starile curente au tranzitii epsilon si merg pe ele

        print(current_states)

    for j in current_states:
        if j in final_states:
            return True
    return False


def nfa(file):
    sections = get_sections(file)
    print(sections)

    d = defaultdict(list)
    for s in sections:
        d[s] = get_data(file, s)
    print(d)
    final_states = []
    ex = 0
    for x in d["States"]:
        if x[0] == 1:
            final_states.append(x[1])
            ex = 1
    if ex==1:
        init_state = d["States"][0][1]
        W = input().split(" ")
        for cuv in W:
            print(cuv, "=", analyze_nfa(init_state, final_states, d, cuv))
    else:
        print("Nu exista stari finale")

