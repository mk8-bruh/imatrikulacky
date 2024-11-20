from math import inf
from random import randint as rand

def parseName(str):
    if len(str.split()) == 1:
        n = str.strip()
        return n[0].upper() + n[1:].lower()
    else:
        n = str.split()
        f, l = n[0].strip(), n[-1].strip()
        return f[0].upper() + f[1:].lower() + " " + l[0].upper() + l[1:].lower()

classes = []
studentByClass = dict()
classByStudent = dict()

exit = False
currentClass = None
while not exit:
    inp = input(f"{currentClass}> " if currentClass else "$: ")
    if inp.strip() != "":
        if currentClass:
            n = parseName(inp)
            if not n in studentByClass[currentClass]:
                studentByClass[currentClass].append(n)
                classByStudent[n] = currentClass
        else:
            currentClass = inp.strip()
            if not currentClass in classes:
                classes.append(currentClass)
                studentByClass[currentClass] = []
    else:
        if currentClass:
            currentClass = None
        else:
            exit = True

ngroups = int(input("# of groups: "))
nsgroups = int(input("# of subgroups: "))
groups = [{"count": 0, "scounts": [0 for _ in range(nsgroups)]} for _ in range(ngroups)]
sgroupByStudent = {}

for id in classes:
    cl = studentByClass[id]
    for _ in range(len(cl)):
        g, c = None, inf
        for f in groups:
            if f["count"] < c:
                g, c = f, f["count"]
        s, v = None, inf
        for i in range(nsgroups):
            if g["scounts"][i] < v:
                s, v = i, g["scounts"][i]
        if not id in g:
            g[id] = []
        n = cl.pop(rand(0, len(cl) - 1))
        g[id].append(n)
        g["count"] += 1
        sgroupByStudent[n] = s
        g["scounts"][s] += 1

for i in range(ngroups):
    g = groups[i]
    print(f"group {i + 1} ({g["count"]})")
    for id in classes:
        if id in g:
            print(f"> {id}")
            for name in sorted(g[id]):
                print(f"  {name} ({sgroupByStudent[name] + 1})")
    print("----------")