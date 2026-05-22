from collections import defaultdict
from settingsdfa import get_sections, clean_line





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
                    elif s=="Sigma":
                        info=l.strip().split(",")
                    elif s=="Gamma":
                        info=l.strip().split(",")
                    elif s=="InitStack":
                        info=l.strip().split(",")


            elif "End" in line:
                ok=0
        return info

def analyze_pda(init_state,final_states,d,W):

    for t in d["Delta"]:
        simbol_pop = t[2]
        simbol_push = t[4]

        if simbol_pop!="epsilon" and simbol_pop not in d["Gamma"]:
            return "Simbol stiva necunoscut"

        if simbol_push!="epsilon" and simbol_push not in d["Gamma"]:
            return "Simbol stiva necunoscut"


    if "InitStack" not in d.keys():
        stack=[]
    stack=list(d["InitStack"])
    topofstack="null"



    current_state=init_state
    st=list(map(str,list(W)))
    for i in st:
        t_found=False
        topofstack="null"
        if i not in d["Sigma"]:
            return "Simbol necunoscut"
        else:
            for t in d["Delta"]:
                if t[0]==current_state and t[1]==i:
                    if len(stack)>0:
                        topofstack=stack[-1]
                    if topofstack==t[2]: #ce simbol scot din stiva
                        stack.pop()
                        current_state=t[3] #starea in care ajung
                        t_found=True
                        if t[4]!="epsilon": #ce simbol scot din stiva
                            stack.append(t[4])
                        break
                    elif t[2]=="epsilon":
                        current_state=t[3]
                        t_found=True
                        if t[4]!="epsilon":
                            stack.append(t[4])
                        break
        if t_found==False:
            return False

    if current_state in final_states:
        return True
    return False



def pda(file):
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
            print(cuv, "=", analyze_pda(init_state, final_states, d, cuv))

    else:
        print("Nu exista stari finale")

