from collections import defaultdict
from settingsdfa import get_sections, clean_line
from os import system





def get_data(x,s):
    with open(x) as f:
        info=[]
        lines = f.readlines()
        ok=0
        for line in lines:
            line=clean_line(line)
            sect="".join(list(line[1:len(line)-1]))
            if  sect == s:
                ok=1
            elif ok==1 and "End" not in line:
                l=line
                if len(l)>=1:
                    if s=="States":
                        if list(l)[0]=="*":
                            tup=tuple([1,"".join(list(l)[1:])])
                        else:
                            tup=tuple([0,l])
                        l=tup
                        info.append(l)
                    elif s=="Delta":
                        tup=tuple(l.strip().split(","))
                        l=tup
                        info.append(l)
                    elif s=="Sigma" or s=="Gamma":
                        info=l.strip().split(",")
                    elif s=="InitStack":
                        info=list(l)


            elif "End" in line:
                ok=0
        return info

def analyze_pda(init_state,final_states,d):

    if "InitStack" not in d.keys():
        stack=[]
    stack=list(d["InitStack"])
    topofstack="null"



    current_state=init_state
    ok=1
    while ok==1:
        t_found = False
        topofstack = "null"
        s=0
        system('cls')
        print("-" * 20)
        print("Te afli in:", current_state)
        print("Ce vrei sa faci mai departe?")
        print("W->Sus")
        print("A->Stanga")
        print("S->Jos")
        print("D->Dreapta")
        print("P->Cauta iteme")
        print("E->Interactioneaza")



        i=input("Simbol: ")
        i=i.lower()
        if i not in d["Sigma"]:
            s=1
        while s==1:
            system('cls')
            print("-" * 20)
            print("Te afli in:", current_state)
            print("Ce vrei sa faci mai departe?")
            print("W->Sus")
            print("A->Stanga")
            print("S->Jos")
            print("D->Dreapta")
            print("P->Cauta iteme")
            print("E->Interactioneaza")
            i=input("Introdu un simbol valid: ")
            i=i.lower()

            if i not in d["Sigma"]:
                s=1
            else:
                s=0

        intamplat=0
        for t in d["Delta"]:
            if t[0] == current_state and t[1] == i:
                if len(stack) > 0:
                    topofstack = stack[-1]
                if topofstack == t[2]: #ce simbol scot din stiva
                    stack.pop()
                    if(current_state!=t[3]):
                        intamplat=1
                    current_state = t[3] #starea in care ajung
                    t_found = True
                    if t[4] != "epsilon": #ce pun in stiva
                        if t[4]!=t[2]:
                            print("Ai gasit:", t[4])
                            system('pause')
                            intamplat=1

                        stack.append(t[4])

                    break
                elif t[2] == "epsilon":
                    if(current_state!=t[3]):
                        intamplat = 1
                    current_state = t[3]
                    t_found = True
                    if t[4] != "epsilon":
                        stack.append(t[4])
                        if t[4] != t[2]:
                            print("Ai gasit:", t[4])
                            system('pause')
                            intamplat = 1
                    break
        if intamplat == 0:
            print("Nu s-a intamplat nimic")
            system('pause')
        if current_state in final_states:
            print("Ai castigat")
            ok=0




def joc(file):
    sections = get_sections(file)

    d = defaultdict(list)
    for s in sections:
        d[s] = get_data(file, s)
    final_states = []
    for x in d["States"]:
        if x[0] == 1:
            final_states.append(x[1])

    init_state = d["States"][0][1]
    analyze_pda(init_state, final_states, d)


file="harta_joc.in"
joc(file)