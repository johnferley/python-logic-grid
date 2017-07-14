no_of_properties = 5
no_of_combinations = 5
no_of_rules = 15
properties = [["Red", "Green", "Yellow", "Blue", "White"], ["Dogs", "Cats", "Fish", "Birds", "Horses"], ["Tea", "Water", "Beer", "Milk", "Coffee"], ["Brit", "Swede", "Dane", "Norwegian", "German"], ["Pall Mall", "Dunhill", "Blend", "Bluemaster", "Prince"]]
relations = ["Left", "Right", "Has", "Neighbor", "At"]
locations = ["1", "2", "3", "4", "5"]

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
    def __init__(self, p1, r, p2, grid):
        self.p1 = p1
        self.p2 = p2
        self.r = r
        self.grid = grid
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
                        self.grid.values[p1_cell[0]][p1_cell[1]] = ""
                for p2_cell in p2_cells:
                    ok = False
                    for p1_cell in p1_cells:
                        if p2_cell[1] == p1_cell[1] + 1:
                            ok = True
                            break
                    if not ok:
                        self.grid.values[p2_cell[0]][p2_cell[1]] = ""
            elif self.r == "Right":
                for p1_cell in p1_cells:
                    ok = False
                    for p2_cell in p2_cells:
                        if p1_cell[1] == p2_cell[1] + 1:
                            ok = True
                            break
                    if not ok:
                        self.grid.values[p1_cell[0]][p1_cell[1]] = ""
                for p2_cell in p2_cells:
                    ok = False
                    for p1_cell in p1_cells:
                        if p2_cell[1] == p1_cell[1] - 1:
                            ok = True
                            break
                    if not ok:
                        self.grid.values[p2_cell[0]][p2_cell[1]] = ""
            elif self.r == "Has":
                for p1_cell in p1_cells:
                    ok = False
                    for p2_cell in p2_cells:
                        if p2_cell[1] == p1_cell[1]:
                            ok = True
                            break
                    if not ok:
                        self.grid.values[p1_cell[0]][p1_cell[1]] = ""
                for p2_cell in p2_cells:
                    ok = False
                    for p1_cell in p1_cells:
                        if p1_cell[1] == p2_cell[1]:
                            ok = True
                            break
                    if not ok:
                        self.grid.values[p2_cell[0]][p2_cell[1]] = ""
            elif self.r == "Neighbor":
                for p1_cell in p1_cells:
                    ok = False
                    for p2_cell in p2_cells:
                        if p1_cell[1] == p2_cell[1] - 1 or p1_cell[1] == p2_cell[1] + 1:
                            ok = True
                            break
                    if not ok:
                        self.grid.values[p1_cell[0]][p1_cell[1]] = ""
                for p2_cell in p2_cells:
                    ok = False
                    for p1_cell in p1_cells:
                        if p2_cell[1] == p1_cell[1] - 1 or p2_cell[1] == p1_cell[1] + 1:
                            ok = True
                            break
                    if not ok:
                        self.grid.values[p2_cell[0]][p2_cell[1]] = ""
        else:
            for row in range(0, len(self.grid.values)):
                for col in range(0, no_of_combinations):
                    test = self.grid.values[row][col]
                    ok = False
                    for property in properties:
                        if test in property and self.p1 in property:
                            ok = True
                    if ok:
                        if self.grid.values[row][col] != self.p1 and str(col + 1) == self.p2:
                            self.grid.values[row][col] = ""
                        elif self.grid.values[row][col] == self.p1 and str(col + 1) != self.p2:
                            self.grid.values[row][col] = ""

class Grid():
    def __init__(self):
        self.values = []
        self.rules = []
        for property in properties:
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
        for i in range(0, no_of_properties):
            output += "+"
            output += "-" * l
        output += "+"
        output += "\n"
        for loc in locations:
            output += "|"
            output += "{message: <{fill}}".format(message=str(loc), fill=str(l))
        output += "|"
        output += "\n"
        for i in range(0, no_of_properties):
            output += "+"
            output += "-" * l
        output += "+"
        output += "\n"
        for row in self.values:
            for col in row:
                output += "|"
                output += "{message: <{fill}}".format(message=col, fill=str(l))
            output += "|"
            output += "\n"
            if self.values.index(row) % no_of_properties == 4:
                for i in range(0, no_of_properties):
                    output += "+"
                    output += "-" * l
                output += "+"
                output += "\n"
        return output.rstrip()
    def add_rule(self, p1, r, p2):
        if r == "At":
            if search(p1, properties) and search(p2, locations) and search(r, relations):
                self.rules.append(Rule(p1, r, p2, self))
            else:
                print("Invalid properties:",p1,r,p2)
        else:
            if search(p1, properties) and search(p2, properties) and search(r, relations):
                self.rules.append(Rule(p1, r, p2, self))
            else:
                print("Invalid properties:",p1,r,p2)
    def find_property(self, p):
        results = []
        if not search(p, properties):
            print("Invalid property:", p)
        else:
            for row in range(0, len(self.values)):
                for col in range(0, no_of_properties):
                    if self.values[row][col] == p:
                        results.append([row,col])
        return results
    def validate(self):
        for rule in self.rules:
            rule.validate()
        counter = 0
        for row in range(0, len(self.values)):
            if self.values[row].count("") == len(self.values[row]) - 1:
                for property in self.values[row]:
                    if property != "":
                        p = property
                        i = self.values[row].index(p)
                        break
                for row2 in range(0, len(self.values)):
                    for col in range(0, no_of_properties):
                        if col == i:
                            if self.values[row2][col] != "" and self.values[row2][col] != p:
                                ok = False
                                for property in properties:
                                    if self.values[row2][col] in property and p in property:
                                        ok = True
                                if ok:
                                    counter += 1
                                    self.values[row2][col] = ""
        for prop in range(0, no_of_properties):
            for col in range(0, no_of_properties):
                n = 0
                for row in range(0 + (prop * no_of_combinations), no_of_combinations + (prop * no_of_combinations)):
                    if self.values[row][col] != "":
                        n += 1
                        i = row
                        j = col
                        if n > 1:
                            break
                if n == 1:
                    for col2 in range(0, no_of_properties):
                        if col2 != j and self.values[i][col2] != "":
                            counter += 1
                            self.values[i][col2] = ""

        if counter > 0:
            self.validate()

class Main():
    def __init__(self):
        puzzle = Grid()
        puzzle.add_rule("Brit", "Has", "Red")
        puzzle.add_rule("Swede", "Has", "Dogs")
        puzzle.add_rule("Dane", "Has", "Tea")
        puzzle.add_rule("Green", "Left", "White")
        puzzle.add_rule("Green", "Has", "Coffee")
        puzzle.add_rule("Pall Mall", "Has", "Birds")
        puzzle.add_rule("Yellow", "Has", "Dunhill")
        puzzle.add_rule("Milk", "At", "3")
        puzzle.add_rule("Norwegian", "At", "1")
        puzzle.add_rule("Blend", "Neighbor", "Cats")
        puzzle.add_rule("Dunhill", "Neighbor", "Horses")
        puzzle.add_rule("Bluemaster", "Has", "Beer")
        puzzle.add_rule("German", "Has", "Prince")
        puzzle.add_rule("Norwegian", "Neighbor", "Blue")
        puzzle.add_rule("Blend", "Neighbor", "Water")
        puzzle.validate()
        print(puzzle)

Main()
