
import sys
class Person:
    #BinaryHypergraphNode, I think
    def __init__(self, name):
        self.name = name
        self.parents = set()
        self.children = set()

    def add_parent(self, person):
        if len(self.parents) < 2:
            self.parents.add(person)
        else:
            print("too many parents")

    def add_child(self, child):
        self.children.add(child)

    def findRelationRecur(self, person1Name, person2Name):
        sumResult = 0
        if person1Name == self.name or person2Name == self.name:
            sumResult=1
        for child in self.children:
            result = child.findRelationRecur(person1Name, person2Name)
            sumResult += result[0]
            if (sumResult == 2):
                if (result[1] == None):
                    return (sumResult, self)
                else:
                    return (sumResult, result[1])
        else:
            return (sumResult, None)
        



class FamilyTree:
    def __init__(self):
        self.persons = set()
        self.orphan_siblings = {}
        self.ancestors = set()


    def printFamily(self):
        def printFamilyRecursive(person, level):
            print("  " * level + "|_" + person.name)
            # Print children
            for child in person.children:
                printFamilyRecursive(child, level + 1)

        for ancestor in self.ancestors:
            printFamilyRecursive(ancestor, 0)

    #returns None if not found, returns the person if found
    def is_person_in_family(self, name):
        for person in self.persons:
            if person.name == name:
                return person
        return None
    
    #returns the new person if not in tree, returns None if already in tree
    def add_person(self, name):
        if (not self.is_person_in_family(name)):
            person = Person(name)
            self.persons.add(person)
            self.ancestors.add(person)
            return person
        else:
            return None
    
    def add_or_find(self,name):
        person = self.is_person_in_family(name)
        if (person == None):
            person = self.add_person(name)
            if (person == None):
                print("Error in add_or_find")
        return person
        
    def add_parent_child(self, child, parent):
        child.add_parent(parent)
        parent.add_child(child)


    def add_relation(self, person1_name, person2_name, relation):
        person1 = self.add_or_find(person1_name)
        person2 = self.add_or_find(person2_name)
        if relation == "parent":
            self.add_parent_child(person1, person2)
            if (person1 in self.orphan_siblings):
                self.orphan_siblings[person1].parents = person1.parents
                del self.orphan_siblings[self.orphan_siblings[person1]]
                del self.orphan_siblings[person1]
                
        if relation == "child":
            self.add_parent_child(person2, person1)
        if relation == "sibling": #assumes siblings have same both parents
            person1.parents = person1.parents | person2.parents
            person2.parents = person1.parents | person2.parents

            for parent in person1.parents:
                self.add_parent_child(person1, parent)
                self.add_parent_child(person2, parent)
            if (len(person1.parents) == 0):
                self.orphan_siblings[person1] = person2
                self.orphan_siblings[person2] = person1
        
        print(self.ancestors)
        if (len(person1.parents) != 0):
            self.ancestors.discard(person1)
        if (len(person2.parents) != 0):
            self.ancestors.discard(person2)

    def findRelation(self, person1name, person2name):
        commonAncestors = set()
        for ancestor in self.ancestors:
            result = ancestor.findRelationRecur(person1name, person2name)
            if result[0] == 2:
                commonAncestors.add(result[1]) 
        if len(commonAncestors) != 0:
            sys.stdout.write(person1name + " and "+  person2name + " share most recent common ancestors: ")
            for ancestor in commonAncestors:
                sys.stdout.write(ancestor.name + ", ")
            sys.stdout.write("\n")
        else:
             sys.stdout.write(person1name + " and "+  person2name + " do not share a common ancestor" + "\n")


        
       

        

family = FamilyTree()
family.add_relation("Smriti", "Narayanan", "parent")
family.add_relation("Smriti", "Narayanan", "parent")
family.add_relation("Smriti", "Narayanan", "parent")
family.add_relation("Smriti", "Padma", "parent")
family.add_relation("Narayanan", "Vaidyanathan", "parent")
family.add_relation("Seetha", "Narayanan", "child")
family.add_relation("Narayanan", "Vijay", "sibling")
family.add_relation("Narayanan", "Sukanya", "sibling")
family.add_relation("Vijay", "Vedh", "child")
family.add_relation("Vijay", "Sanjana", "child")
family.add_relation("Sukanya", "Manas", "child")
family.add_relation("Manas", "Vijay2", "parent")
family.add_relation("Manas", "Varun", "sibling")


family.add_relation("Prabha", "Vishal", "child")
family.add_relation("Prabha", "Vidyuth", "child")
family.add_relation("Vidyuth", "Manavi", "sibling")
family.add_relation("Padma", "Akila", "parent")
family.add_relation("Padma", "Sivaraman", "parent")
family.add_relation("Padma", "Prabha", "sibling")

family.add_relation("Akila", "Subbupatti", "parent")
family.add_relation("Ambulu", "Doraiswami", "parent")
family.add_relation("Ambulu", "Akila", "sibling")

family.add_relation("Advika", "Vivin", "sibling")
family.add_relation("Advika", "Anand", "parent")
family.add_relation("Vivin", "Navina", "parent")
family.add_relation("Ambulu", "Anand", "child")
family.printFamily()

family.findRelation("Smriti", "Narayanan")
family.findRelation("Smriti", "Navina")
family.findRelation("Smriti", "Manas")
family.findRelation("Vedh", "Manavi")
family.findRelation("Vedh", "Vaidyanathan")
family.findRelation("Vijay2", "Smriti")
family.findRelation("Advika", "Smriti")
family.findRelation("Manas", "Varun")


             
        