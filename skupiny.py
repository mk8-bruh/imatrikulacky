def n2a(n):
    d, m = divmod(n, 26)
    return '' if n < 0 else n2a(d - 1) + chr(m + 65)

class Student:
    def __init__(self, data):
        if not isinstance(data, str):
            raise TypeError(f"Student data must be a string (received: {type(data)})")

        s = data.strip().split()
        n = len(s)
        if n < 2:
            raise ValueError("Invalid student data string")
        s = [w[0].upper() + w[1:] for w in s]
        self.Class = s[-1]
        self.FirstName = s[0]
        if n > 2:
            self.LastName = s[-2]
        self.FullName = " ".join(s[:-1])
        self.Groups = []
     
    def __repr__(self):
    	return f"<[Student] Name: {self.FullName}, Class: {self.Class}, Groups: {[g.GetNamePath() for g in self.Groups]}>"
    def __str__(self):
    	return self.__repr__()

class Group:
    def __init__(self, name = "", subgroups = [], parent = None):
        if not isinstance(name, str):
            raise TypeError(f"Group name must be a string (received: {type(name)})")
        if not isinstance(subgroups, list):
            raise TypeError(f"Subgroup count must be a list or None (received: {type(subgroups)})")

        self.Name = name
        self.Subgroups = [Group(str(g), parent = self) for g in subgroups]
        self.SubgroupByStudent = dict()
        self.Parent = parent
        self.Students = []
        self.Classes = dict()
    def AddStudent(self, student):
        if not isinstance(student, Student):
            raise TypeError(f"Subject must be a Student object (received: {type(student)})")

        student.Groups.append(self)
        self.Students.append(student)
        if not student.Class in self.Classes:
            self.Classes[student.Class] = []
        self.Classes[student.Class].append(student)
        if len(self.Subgroups) > 0:
            s = Group.BestGroup(self.Subgroups, student)
            if s:
                s.AddStudent(student)
                self.SubgroupByStudent[student] = s
    
    def GetNamePath(self):
        return f"{self.Parent.GetNamePath()}/{self.Name}" if self.Parent else self.Name
    def GetStudentCount(self):
        return len(self.Students)
    def GetClassCount(self, className):
        return len(self.Classes.get(className, []))
    
    @staticmethod
    def BetterGroup(a, b, student):
        if a != None and not isinstance(a, Group):
            raise TypeError(f"Argument #1 must be a Group object (received: {type(a)})")
        if b != None and not isinstance(student, Student):
            raise TypeError(f"Argument must be a Student object (received: {type(b)})")
        if student == None or not isinstance(student, Student):
            raise TypeError(f"Subject must be a Student object (received: {type(student)})")

        return (not b) or (a.GetClassCount(student.Class) < b.GetClassCount(student.Class)) or (a.GetClassCount(student.Class) == b.GetClassCount(student.Class) and a.GetStudentCount() < b.GetStudentCount())
    @staticmethod
    def BestGroup(groups, student):
        best = None
        for group in groups:
            if Group.BetterGroup(group, best, student):
                best = group
        return best

    def __repr__(self):
    	return f"<[Group] Name: {self.Name}, Parent: {self.Parent.Name if self.Parent else 'None'}, Path: {self.GetNamePath()}, Subgroups: {[s.Name for s in self.Subgroups]}, Students: {[f'{s.FullName} ({s.Class}) - {self.SubgroupByStudent[s].Name}' for s in self.Students]}>"
    def __str__(self):
    	return self.__repr__()

groupCount = int(input("# of groups: "))
subgroupCount = int(input("# of groups: "))

students = []
groups = [Group(n2a(i), [str(j + 1) for j in range(subgroupCount)]) for i in range(groupCount)]
groupsByName = {g.Name.lower(): g for g in groups}

exit = False
while not exit:
    inp = input("> ").strip()
    if "#" in inp:
        exit = True
    elif "?" in inp:
        n = " ".join([w.lower() for w in inp.split() if w != "?"])
        matches = []
        for s in students:
            if n in s.FullName.lower():
                matches.append(s)
        print(f"{len(matches)} matches")
        for s in matches:
            print(f"    {s.FullName} ({s.Class}) - {s.Groups[1].GetNamePath()}")
    elif "*" in inp:
        g = " ".join([w.lower() for w in inp.split() if w != "*"])
        if g in groupsByName:
            gr = groupsByName[g]
            print(f"  {gr.Name}")
            for c in gr.Classes:
                print(f"    {c}")
                for s in gr.Classes[c]:
                    print(f"      {s.FullName} - {s.Groups[1].Name}")
        elif g == "":
            for g in groups:
                print(f"  {g.Name}")
                for c in g.Classes:
                    print(f"    {c}")
                    for s in g.Classes[c]:
                        print(f"      {s.FullName} - {s.Groups[1].Name}")
        else:
            print("  no groups found")
    elif "$" in inp:
        e = " ".join([w for w in inp.split() if w != "$"])
        try:
            print(f"  {eval(e)}")
        except Exception as e:
            print(f"  error: {e}")
    else:
        try:
            s = Student(inp)
            g = Group.BestGroup(groups, s)
            g.AddStudent(s)
            students.append(s)
            print(f"{', '.join([g.Name for g in s.Groups])}")
        except Exception as e:
            print(f"  error: {e}")