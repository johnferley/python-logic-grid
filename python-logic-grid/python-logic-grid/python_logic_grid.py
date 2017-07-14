def search(p, ps):
    return any(p in search for search in ps)

class Node():
    def __init__(self, action):
        children = []
    def up(self):
        pass
    def down(self, target):
        pass

class Rule():
    def __init__(self, p1, r, p2, grid, text):
        self.p1 = p1
        self.p2 = p2
        self.r = r
        self.grid = grid
        self.text = text
    def __str__(self):
        output = self.text.format(self.p1, self.r, self.p2)
        return output
    def validate(self):
        if self.r != "At":
            p1_cells = self.grid.find_property(self.p1)
            p2_cells = self.grid.find_property(self.p2)
            if self.r == "Left":
                for p1_cell in p1_cells:
                    ok = False
                    for p2_cell in p2_cells:
                        if p1_cell[1] == p2_cell[1] - 1:
                            ok = True
                            break
                    if not ok:
                        print("[",p1_cell[0],",",p1_cell[1],"] =", self.grid.values[p1_cell[0]][p1_cell[1]], " removed",str(self))
                        self.grid.values[p1_cell[0]][p1_cell[1]] = ""
                for p2_cell in p2_cells:
                    ok = False
                    for p1_cell in p1_cells:
                        if p2_cell[1] == p1_cell[1] + 1:
                            ok = True
                            break
                    if not ok:
                        print("[",p2_cell[0],",",p2_cell[1],"] =", self.grid.values[p2_cell[0]][p2_cell[1]], " removed",str(self))
                        self.grid.values[p2_cell[0]][p2_cell[1]] = ""
            elif self.r == "Right":
                for p1_cell in p1_cells:
                    ok = False
                    for p2_cell in p2_cells:
                        if p1_cell[1] == p2_cell[1] + 1:
                            ok = True
                            break
                    if not ok:
                        print("[",p1_cell[0],",",p1_cell[1],"] =", self.grid.values[p1_cell[0]][p1_cell[1]], " removed",str(self))
                        self.grid.values[p1_cell[0]][p1_cell[1]] = ""
                for p2_cell in p2_cells:
                    ok = False
                    for p1_cell in p1_cells:
                        if p2_cell[1] == p1_cell[1] - 1:
                            ok = True
                            break
                    if not ok:
                        print("[",p2_cell[0],",",p2_cell[1],"] =", self.grid.values[p2_cell[0]][p2_cell[1]], " removed",str(self))
                        self.grid.values[p2_cell[0]][p2_cell[1]] = ""
            elif self.r == "Has":
                for p1_cell in p1_cells:
                    ok = False
                    for p2_cell in p2_cells:
                        if p2_cell[1] == p1_cell[1]:
                            ok = True
                            break
                    if not ok:
                        print("[",p1_cell[0],",",p1_cell[1],"] =", self.grid.values[p1_cell[0]][p1_cell[1]], " removed",str(self))
                        self.grid.values[p1_cell[0]][p1_cell[1]] = ""
                for p2_cell in p2_cells:
                    ok = False
                    for p1_cell in p1_cells:
                        if p1_cell[1] == p2_cell[1]:
                            ok = True
                            break
                    if not ok:
                        print("[",p2_cell[0],",",p2_cell[1],"] =", self.grid.values[p2_cell[0]][p2_cell[1]], " removed",str(self))
                        self.grid.values[p2_cell[0]][p2_cell[1]] = ""
            elif self.r == "Neighbor":
                for p1_cell in p1_cells:
                    ok = False
                    for p2_cell in p2_cells:
                        if p1_cell[1] == p2_cell[1] - 1 or p1_cell[1] == p2_cell[1] + 1:
                            ok = True
                            break
                    if not ok:
                        print("[",p1_cell[0],",",p1_cell[1],"] =", self.grid.values[p1_cell[0]][p1_cell[1]], " removed",str(self))
                        self.grid.values[p1_cell[0]][p1_cell[1]] = ""
                for p2_cell in p2_cells:
                    ok = False
                    for p1_cell in p1_cells:
                        if p2_cell[1] == p1_cell[1] - 1 or p2_cell[1] == p1_cell[1] + 1:
                            ok = True
                            break
                    if not ok:
                        print("[",p2_cell[0],",",p2_cell[1],"] =", self.grid.values[p2_cell[0]][p2_cell[1]], " removed",str(self))
                        self.grid.values[p2_cell[0]][p2_cell[1]] = ""
        else:
            for row in range(0, len(self.grid.values)):
                for col in range(0, self.grid.no_of_properties):
                    test = self.grid.values[row][col]
                    ok = False
                    for property in self.grid.properties:
                        if test in property and self.p1 in property:
                            ok = True
                    if ok:
                        if self.grid.values[row][col] != self.p1 and str(col + 1) == self.p2:
                            print("[",row,",",col,"] =", self.grid.values[row][col], " removed",str(self))
                            self.grid.values[row][col] = ""
                        elif self.grid.values[row][col] == self.p1 and str(col + 1) != self.p2:
                            print("[",row,",",col,"] =", self.grid.values[row][col], " removed",str(self))
                            self.grid.values[row][col] = ""

class Grid():
    def __init__(self):
        self.values = []
        self.rules = []
        self.properties = [["Red", "Green", "Yellow", "Blue", "White"], ["Dogs", "Cats", "Fish", "Birds", "Horses"], ["Tea", "Water", "Beer", "Milk", "Coffee"], ["Brit", "Swede", "Dane", "Norwegian", "German"], ["Pall Mall", "Dunhill", "Blend", "Bluemaster", "Prince"]]
        self.RELATIONS = ["Left", "Right", "Has", "Neighbor", "At"]
        self.locations = ["1", "2", "3", "4", "5"]
        self.no_of_properties = len(self.properties)
        self.no_of_combinations = len(self.properties[0])
        for property in self.properties:
            for each in property:
                temp = [each, each, each, each, each]
                self.values.append(temp)
    def __str__(self):
        l = 0
        output = ""
        for row in self.values:
            for col in row:
                if len(col) > l:
                    l = len(col)
        for i in range(0, self.no_of_properties):
            output += "+"
            output += "-" * l
        output += "+"
        output += "\n"
        for loc in self.locations:
            output += "|"
            output += "{message: <{fill}}".format(message=str(loc), fill=str(l))
        output += "|"
        output += "\n"
        for i in range(0, self.no_of_properties):
            output += "+"
            output += "-" * l
        output += "+"
        output += "\n"
        for row in range(0, len(self.values)):
            for col in self.values[row]:
                output += "|"
                output += "{message: <{fill}}".format(message=col, fill=str(l))
            output += "|"
            output += "\n"
            if row % self.no_of_properties == 4:
                for i in range(0, self.no_of_properties):
                    output += "+"
                    output += "-" * l
                output += "+"
                output += "\n"
        return output.rstrip()
    def add_rule(self, p1, r, p2, text):
        if r == "At":
            if search(p1, self.properties) and search(p2, self.locations) and search(r, self.RELATIONS):
                self.rules.append(Rule(p1, r, p2, self, text))
            else:
                print("Invalid properties:",p1,r,p2)
        else:
            if search(p1, self.properties) and search(p2, self.properties) and search(r, self.RELATIONS):
                self.rules.append(Rule(p1, r, p2, self, text))
            else:
                print("Invalid properties:",p1,r,p2)
    def add_property(self):
        pass
    def add_location(self):
        pass
    def find_property(self, p):
        results = []
        if not search(p, self.properties):
            print("Invalid property:", p)
        else:
            for row in range(0, len(self.values)):
                for col in range(0, self.no_of_properties):
                    if self.values[row][col] == p:
                        results.append([row,col])
        return results
    def validate(self):
        for rule in self.rules:
            rule.validate()
        counter = 0
        #for row in range(0, len(self.values)):
        #    if self.values[row].count("") == len(self.values[row]) - 1:
        #        for property in self.values[row]:
        #            if property != "":
        #                p = property
        #                i = self.values[row].index(p)
        #                break
        #        for row2 in range(0, len(self.values)):
        #            for col in range(0, self.no_of_properties):
        #                if col == i:
        #                    if self.values[row2][col] != "" and self.values[row2][col] != p:
        #                        ok = False
        #                        for property in self.properties:
        #                            if self.values[row2][col] in property and p in property:
        #                                ok = True
        #                        if ok:
        #                            counter += 1
        #                            self.values[row2][col] = ""
        for prop in range(0, self.no_of_properties):
            for row in range(0 + (prop * self.no_of_combinations), self.no_of_combinations + (prop * self.no_of_combinations)):
                if self.values[row].count("") == len(self.values[row]) - 1:
                    for property in self.values[row]:
                        if property != "":
                            i = row
                            j = self.values[row].index(property)
                            break
                    for row2 in range(0 + (prop * self.no_of_combinations), self.no_of_combinations + (prop * self.no_of_combinations)):
                        if self.values[row2][j] != "" and row2 != i:
                            print("[",row2,",",j,"] =", self.values[row2][j], " removed")
                            counter += 1
                            self.values[row2][j] = ""
            for col in range(0, self.no_of_properties):
                n = 0
                for row in range(0 + (prop * self.no_of_combinations), self.no_of_combinations + (prop * self.no_of_combinations)):
                    if self.values[row][col] != "":
                        n += 1
                        i = row
                        j = col
                        if n == 1:
                            break
                if n == 1:
                    for col2 in range(0, self.no_of_properties):
                        if col2 != j and self.values[i][col2] != "":
                            print("[",i,",",col2,"] =", self.values[i][col2], " removed")
                            counter += 1
                            self.values[i][col2] = ""

        if counter > 0:
            self.validate()

class Main():
    def __init__(self):
        puzzle = Grid()
        puzzle.add_rule("Brit", "Has", "Red","The {0} lives in the {2} house")
        puzzle.add_rule("Swede", "Has", "Dogs","The {0} keeps {2} as pets")
        puzzle.add_rule("Dane", "Has", "Tea", "The {0} drinks {2}")
        puzzle.add_rule("Green", "Left", "White", "The {0} house is on the {1} of the {2} house")
        puzzle.add_rule("Green", "Has", "Coffee", "The {0} homeowner drinks {2}")
        puzzle.add_rule("Pall Mall", "Has", "Birds", "The person who smokes {0} rears {2}")
        puzzle.add_rule("Yellow", "Has", "Dunhill", "The owber if the {0} house smokes {2}")
        puzzle.add_rule("Milk", "At", "3", "The man living in the center house drinks {0}")
        puzzle.add_rule("Norwegian", "At", "1", "The {0} lives in the first house")
        puzzle.add_rule("Blend", "Neighbor", "Cats", "The man who smokes {0} lives next to the one who keeps {2}")
        puzzle.add_rule("Dunhill", "Neighbor", "Horses", "The man who keeps the {2} lives next to the man who smokes {0}")
        puzzle.add_rule("Bluemaster", "Has", "Beer", "The owner who smokes {0} drinks {2}")
        puzzle.add_rule("German", "Has", "Prince", "The {0} smokes {2}")
        puzzle.add_rule("Norwegian", "Neighbor", "Blue", "The {0} lives next to the {2} house")
        puzzle.add_rule("Blend", "Neighbor", "Water", "The man who smokes {0} has a neighbor who drinks {2}")
        puzzle.validate()
        print(puzzle)

Main()
