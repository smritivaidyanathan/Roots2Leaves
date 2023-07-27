
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
        generationalGap = sys.maxsize
        #print(self.name)

        foundSelf = False

        if person1Name == self.name or person2Name == self.name:
            sumResult=1
            foundSelf = True
            #print("This is " + self.name)

        for child in self.children:
            #print("looking in " + self.name + "'s child named " + child.name)
            result = child.findRelationRecur(person1Name, person2Name)
            sumResult += result[0]

            if (sumResult == 2):
                #print("success")
                if (result[1] == None):
                    #print("Common ancestor found: " + self.name + " in "  + self.name + "'s child named " + child.name)
                    #print("final generational gap = " + str(min(result[2], generationalGap) + 1))
                    #print(abs(generationalGap - result[2]))
                    return (sumResult, self, min(result[2], generationalGap) + 1, abs(generationalGap - result[2]))
                    
                else:
                    #print("Going back up the tree from the common ancestor found: " + result[1].name + "in "  + self.name + "'s child named " + child.name)
                    return (sumResult, result[1], result[2], 0)
            if (result[0] == 1):
                #print("found one of them in "  + self.name + "'s child named " + child.name)
                generationalGap = min(result[2], generationalGap)
                #print(abs(generationalGap - result[2]), 0)
            

        if (sumResult == 1 and len(self.children) !=0):
            if (foundSelf):
                return (sumResult, None, 0, 0)
            #print("going up after having found only one in list of children in " +  self.name)
            #print("adding to generationalgap :" + str(generationalGap + 1))
            return (sumResult, None, generationalGap + 1, 0)
        else:
            #if (sumResult == 1):
                #print("Once  again, This is " + self.name)
            #else:
                #print("found no one in " + self.name)
            return (sumResult, None, 0, 0)
        

    
        



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

    def findRecentCommonAncestors(self, person1name, person2name):
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

    def findRelation(self, person1name, person2name):
        commonAncestors = set()
        related = False
        resultgeneration = 0
        for ancestor in self.ancestors:
            result = ancestor.findRelationRecur(person1name, person2name)
            if result[0] == 2:
                related = True
                resultgeneration = result
                if person1name == result[1].name or person2name == result[1].name:
                    print(person1name + " and " + person2name + " lie in a direct line of descent")
                    print(person1name + " and " + person2name + " have " + str(result[2]) + " generations between them.\n")
                    return
        if related:
            print(person1name + " and "+  person2name + " share a recent common ancestor")
            print(person1name + " and " + person2name + " have " + str(resultgeneration[2]) + " generations between them and the most recent common ancestor.")
            print(person1name + " and " + person2name + " have " + str(resultgeneration[3]) + " generations between them\n")
        else:
            print(person1name + " and "+  person2name + " are not related\n")

       

        
       

        

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

# family.findRecentCommonAncestors("Smriti", "Narayanan")
# family.findRecentCommonAncestors("Smriti", "Navina")
# family.findRecentCommonAncestors("Smriti", "Manas")
# family.findRecentCommonAncestors("Vedh", "Manavi")
# family.findRecentCommonAncestors("Vedh", "Vaidyanathan")
# family.findRecentCommonAncestors("Vijay2", "Smriti")
# family.findRecentCommonAncestors("Advika", "Smriti")
# family.findRecentCommonAncestors("Manas", "Varun")
# family.findRecentCommonAncestors("Smriti", "Vijay")

print("\n")

family.findRelation("Smriti", "Narayanan")
family.findRelation("Smriti", "Navina")
family.findRelation("Smriti", "Manas")
family.findRelation("Smriti", "Vijay")
family.findRelation("Smriti", "Ambulu")
family.findRelation("Vedh", "Manavi")
family.findRelation("Vedh", "Vaidyanathan")
family.findRelation("Vijay2", "Smriti")
family.findRelation("Advika", "Smriti")
family.findRelation("Manas", "Varun")



             
        