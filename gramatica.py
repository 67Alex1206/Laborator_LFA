from collections import defaultdict
from settingsdfa import get_sections, clean_line
import random

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
                    if s=="Sub":
                        e=[]
                        v=line.split("->")[0]
                        e.append(v)
                        t=tuple(line.split("->")[1].split("|"))
                        e.append(t)
                        info.append(e)

                    elif s=="Sigma" or s=="Var":
                        info=l.strip().split(",")


            elif "End" in line:
                ok=0
        return info

def generate(d,Prop):


    ok=1
    while ok==1:
        ok=0
        p=list(Prop)
        x=0
        while x<len(p):
            if p[x] in d["Var"]:
                ok=1
                for s in d["Sub"]:
                    if s[0]==p[x]:
                        p[x]=random.choice(s[1])
                        Prop="".join(p)
                        print(Prop)

                        break
            x+=1
    return "".join(p)





def gramatica(file):
    sections = get_sections(file)
    print(sections)

    d = defaultdict(list)
    for s in sections:
        d[s] = get_data(file, s)
    print(d)

    Prop=""
    x=0
    while x< len(d["Var"]):
        if d["Var"][x][0]=="!":
            d["Var"][x]=d["Var"][x][1:]
            Prop=d["Var"][x]
        x+=1

    print(d)



    Prop=generate(d,Prop)
    print(Prop)




