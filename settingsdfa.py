from collections import defaultdict
def clean_line(line):
    return line.split('#')[0].strip()
def get_sections(x):
    with open(x) as f:
        lines = f.readlines()
        sections = []
        ok = 0
        for line in lines:
            line=clean_line(line)
            if "[" in line and "]" in line and "End" not in line and ok==0:
                ok=1
                sections.append("".join(list(line[1:len(line)-1])))
            if "[" in line and "]" in line and "End" in line and ok==1:
                ok=0
    return sections


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


            elif "End" in line:
                ok=0
        return info



def analyze_dfa(init_state,final_states,d,W):
    current_state=init_state
    st=list(map(str,list(W)))
    for i in st:
        t_found=False
        if i not in d["Sigma"]:
            return "Simbol necunoscut"
        else:
            for t in d["Delta"]:
                if t[0]==current_state and t[1]==i:
                    current_state=t[2]
                    t_found=True
                    break
        if t_found==False:
            return False
    if current_state in final_states:
        print(current_state)
        return True
    print(current_state)
    return False







def dfa(file):
    sections = get_sections(file)
    print(sections)

    d = defaultdict(list)
    for s in sections:
        d[s] = get_data(file, s)
    print(d)
    final_states = []
    ex=0
    for x in d["States"]:
        if x[0] == 1:
            final_states.append(x[1])
            ex=1
    if ex==1:
        init_state = d["States"][0][1]
        W = input().split(" ")
        for cuv in W:
            print(cuv, "=", analyze_dfa(init_state, final_states, d, cuv))
    else:
        print("Nu exista stari finale")

