# Your Agent for solving Raven's Progressive Matrices. You MUST modify this file.
#
# You may also create and submit new files in addition to modifying this file.
#
# Make sure your file retains methods with the signatures:
# def __init__(self)
# def Solve(self,problem)
#
# These methods will be necessary for the project's main method to run.

# Install Pillow and uncomment this line to access image processing.
from PIL import Image
import numpy




class Agent:
    # The default constructor for your Agent. Make sure to execute any
    # processing necessary before your Agent starts solving problems here.
    #
    # Do not add any variables to this signature; they will not be used by
    # main().
    def __init__(self):
        self.problemNum = 0
        self.matchpair = []
        self.existingAnswers = 6
        self.possibleAnswers = [1,1,1,1,1,1]
        


    def objectRelation(self, object1, object2):
        relation = {}
        for attributeName in object1.attributes:
            if(attributeName == 'shape' and 'shape' in object2.attributes):
                if(object1.attributes['shape'] == object2.attributes['shape']):
                    relation['shape'] = 1
                else:
                    relation['shape'] = 0
            if(attributeName == 'fill' and 'fill' in object2.attributes):
                if(object1.attributes['fill'] == object2.attributes['fill']):
                    relation['fill'] = 1
                else:
                    relation['fill'] = 0
            if(attributeName == 'size' and 'size' in object2.attributes):
                if(object1.attributes['size'] == object2.attributes['size']):
                    relation['size'] = 1
                else:
                    relation['size'] = 0
            if(attributeName == 'angle' and 'angle' in object2.attributes):
                
                if(object1.attributes['angle'] == object2.attributes['angle']):
                    relation['angle'] = 1
                elif(object1.attributes['shape'] == 'pac-man' and object2.attributes['shape'] == 'pac-man'):
                    if((object1.attributes['angle'] == '45' and object2.attributes['angle'] == '135') or (object2.attributes['angle'] == '45' and object1.attributes['angle'] == '135')):
                        relation['angle'] = 'reflection'
                    elif((object1.attributes['angle'] == '315' and object2.attributes['angle'] == '225') or (object2.attributes['angle'] == '315' and object1.attributes['angle'] == '225')):
                        relation['angle'] = 'reflection'
                    elif((object1.attributes['angle'] == '180' and object2.attributes['angle'] == '0') or (object2.attributes['angle'] == '180' and object1.attributes['angle'] == '0')):
                        relation['angle'] = 'reflection'
                elif(object1.attributes['shape'] == 'right triangle' and object2.attributes['shape'] == 'right triangle'):
                    if((object1.attributes['angle'] == '270' and object2.attributes['angle'] == '0') or (object2.attributes['angle'] == '270' and object1.attributes['angle'] == '0')):
                        relation['angle'] = 'reflection'
                    elif((object1.attributes['angle'] == '180' and object2.attributes['angle'] == '90') or (object2.attributes['angle'] == '180' and object1.attributes['angle'] == '90')):
                        relation['angle'] = 'reflection'
                else: 
                    relation['angle'] = int(object2.attributes['angle'])-int(object1.attributes['angle'])
            if(attributeName == 'alignment' and 'alignment' in object2.attributes):
                ali1 = object1.attributes['alignment']
                ali2 = object2.attributes['alignment']
                #unchanged
                if(ali1 == ali2):
                    relation['alignment'] = 1
                #move left 
                elif((ali1 == 'bottom-right' and ali2 == 'bottom-left') or (ali1 == 'top-right' and ali2 == 'top-left')):
                    relation['alignment'] = 2
                #move right
                elif((ali1 == 'bottom-left' and ali2 == 'bottom-right') or (ali1 == 'top-left' and ali2 == 'top-right')):
                    relation['alignment'] = 3
                #move top
                elif((ali1 == 'bottom-right' and ali2 == 'top-right') or (ali1 == 'bottom-left' and ali2 == 'top-left')):
                    relation['alignment'] = 4
                #move down
                elif((ali1 == 'top-right' and ali2 == 'bottom-right') or (ali1 == 'top-left' and ali2 == 'bottom-left')):
                    relation['alignment'] = 5
                #move from bottom left to top right
                elif(ali1 == 'bottom-left' and ali2 == 'top-right'):
                    relation['alignment'] = 6
                #move from top left to bottom right
                elif(ali1 == 'top-left' and ali2 == 'bottom-right'):
                    relation['alignment'] = 7
                #move from top right to bottom left
                elif(ali1 == 'top-right' and ali2 == 'bottom-left'):
                    relation['alignment'] = 8
                #move from top left to bottom right
                elif(ali1 == 'top-left' and ali2 == 'bottom-right'):
                    relation['alignment'] = 9
                else:
                    relation['alignment'] = 10
        return relation
        

    
    def isEqualAttributes(self, attribute1, attribute2):
        if (len(attribute1) != len(attribute2)):
            return 0
        
        for attributeName in attribute1:
            if(attributeName not in attribute2):
                return 0
            else:
                if(attribute1[attributeName] != attribute2[attributeName]):
                    if(attributeName == "shape" or attributeName == "fill" or attributeName == "size" or attributeName == "angle" or attributeName == "alignment"):
                        return 0
                
        return 1


    def FindMatchedPair(self, figure1, figure2):
        pairRelation = []
        Relation = []
        pairnum = 0
        for objectName in figure1.objects:
            for objectName2 in figure2.objects:
                if( self.isEqualAttributes(figure1.objects[objectName].attributes, figure2.objects[objectName2].attributes) == 1):
                    pairnum = pairnum + 1
                    Relationtemp = figure1.objects[objectName].attributes
                    Relation.append(Relationtemp)
                    self.matchpair.append(objectName)
                    self.matchpair.append(objectName2)
        pairRelation.append(pairnum)   
        for i in range(len(Relation)):
            pairRelation.append(Relation[i])        
        return pairRelation
        
        
    def FindRelationsMultiObjects(self, figure1, figure2): 
        
        pairRelation = self.FindMatchedPair(figure1, figure2)
        if(len(figure1.objects) > len(figure2.objects)):
            
            pairRelation.append('delete')
            for objectName1 in figure1.objects:
                if(objectName1 not in self.matchpair):
                    pairRelation.append(figure1.objects[objectName1].attributes)
            pairRelation.append(len(figure1.objects)-len(figure2.objects))
            return pairRelation
        else:
            for objectName1 in figure1.objects:
                for objectName2 in figure2.objects:
                    if(objectName1 not in self.matchpair and objectName2 not in self.matchpair):
                        pairRelation.append(self.objectRelation(figure1.objects[objectName1], figure2.objects[objectName2]))
                        
            
        return pairRelation    
        

    def findAns(self):
        for index in range(len(self.possibleAnswers)):
            if self.possibleAnswers[index] == 1:
                return index+1


    
    def SolveHelper(self, bool_oneObject, problem, direction):
        if(bool_oneObject == 1):
            relationAB = {}
            for objectName in problem.figures['A'].objects:
                objecta = problem.figures['A'].objects[objectName]
            for objectName in problem.figures['B'].objects:
                objectb = problem.figures['B'].objects[objectName]
            for objectName in problem.figures['C'].objects:
                objectc = problem.figures['C'].objects[objectName]
            if (direction == 1):
                relationAB = self.objectRelation(objecta,objectb) 
            else:
                relationAB = self.objectRelation(objecta,objectc)   
#             print("relationAB")
#             print(relationAB)
            for index in range(1,7):
                relationAns = {}
                for objectName in problem.figures[str(index)].objects:
                    objectAns = problem.figures[str(index)].objects[objectName]
                if (direction == 1):
                    relationAns = self.objectRelation(objectc,objectAns)     
                else:
                    relationAns = self.objectRelation(objectb,objectAns) 
#                 print("relationAns")
#                 print(relationAns)

                if relationAns['shape'] != relationAB['shape']:
                    self.existingAnswers = self.existingAnswers - 1
                    self.possibleAnswers[index-1] = 0
                    if self.existingAnswers == 1:
                        return self.findAns()
                else:
                    if 'size' in relationAns and 'size' in relationAB and relationAns['size'] != relationAB['size']:
                        self.existingAnswers = self.existingAnswers - 1
                        self.possibleAnswers[index-1] = 0
                        if self.existingAnswers == 1:
                            return self.findAns()   
                    else:
                        if 'fill' in relationAns and 'fill' in relationAB and relationAns['fill'] != relationAB['fill']:
                            self.existingAnswers = self.existingAnswers - 1
                            self.possibleAnswers[index-1] = 0
                            if self.existingAnswers == 1:
                                return self.findAns() 
                        else:
                            if 'angle' in relationAB:
                                if 'angle' not in relationAns:
                                    self.existingAnswers = self.existingAnswers - 1
                                    self.possibleAnswers[index-1] = 0
                                    if self.existingAnswers == 1:
                                        return self.findAns() 
                                else: 
                                    if relationAB['angle'] == 1 and relationAns['angle'] != 1:
                                        self.existingAnswers = self.existingAnswers - 1
                                        self.possibleAnswers[index-1] = 0
                                        if self.existingAnswers == 1:
                                            return self.findAns() 
                                    elif relationAB['angle'] == 'reflection':
                                        if(relationAns['angle'] != 'reflection'):
                                            self.existingAnswers = self.existingAnswers - 1
                                            self.possibleAnswers[index-1] = 0
                                            if self.existingAnswers == 1:
                                                return self.findAns()
                                    else:
                                        #if relationAB['angle'] >= 180  or relationAB['angle'] <= -180:
                                        if relationAB['angle'] != relationAns['angle']:
                                            self.existingAnswers = self.existingAnswers - 1
                                            self.possibleAnswers[index-1] = 0
                                            if self.existingAnswers == 1:
                                                return self.findAns() 
#                                         else:
#                                             if relationAB['angle'] != -relationAns['angle']:
#                                                 self.existingAnswers = self.existingAnswers - 1
#                                                 self.possibleAnswers[index-1] = 0
#                                                 if self.existingAnswers == 1:
#                                                     return self.findAns()


                            if 'alignment' in relationAB:
                                if 'alignment' not in relationAns:
                                    self.existingAnswers = self.existingAnswers - 1
                                    self.possibleAnswers[index-1] = 0
                                    if self.existingAnswers == 1:
                                        return self.findAns()
                                    
                                else:
                                    if relationAB['alignment'] != relationAns['alignment']:
                                        self.existingAnswers = self.existingAnswers - 1
                                        self.possibleAnswers[index-1] = 0
                                        if self.existingAnswers == 1:
                                            return self.findAns() 
#                                     elif relationAB['alignment'] == 2 and relationAns['alignment'] != 3:
#                                         self.existingAnswers = self.existingAnswers - 1
#                                         self.possibleAnswers[index-1] = 0
#                                         if self.existingAnswers == 1:
#                                             return self.findAns() 
#                                     elif relationAB['alignment'] == 3 and relationAns['alignment'] != 2:
#                                         self.existingAnswers = self.existingAnswers - 1
#                                         self.possibleAnswers[index-1] = 0
#                                         if self.existingAnswers == 1:
#                                             return self.findAns()
#                                     elif relationAB['alignment'] == 4 and relationAns['alignment'] != 5:
#                                         self.existingAnswers = self.existingAnswers - 1
#                                         self.possibleAnswers[index-1] = 0
#                                         if self.existingAnswers == 1:
#                                             return self.findAns()   
#                                     elif relationAB['alignment'] == 5 and relationAns['alignment'] != 4:
#                                         self.existingAnswers = self.existingAnswers - 1
#                                         self.possibleAnswers[index-1] = 0
#                                         if self.existingAnswers == 1:
#                                             return self.findAns()


        else:
            MultiRelationAB = self.FindRelationsMultiObjects(problem.figures['A'],problem.figures['B'])
            unchangeObjNum = MultiRelationAB[0]
            MultiRelationAB_length = len(MultiRelationAB)
            
            print ("MR")
            print (MultiRelationAB)
            for index in range(1,7):
                self.matchpair = []
                CurrentRelation = self.FindRelationsMultiObjects(problem.figures['C'],problem.figures[str(index)])  
                currentUnchangeObjNum = CurrentRelation[0]  
                print ("CR")
                print (CurrentRelation)
                #all objects unchanged
                if(MultiRelationAB_length == (unchangeObjNum+1)):
                    if unchangeObjNum == CurrentRelation[0]:
                        correctnum = 0
                        for i in range(unchangeObjNum):
                            if(self.isEqualAttributes(MultiRelationAB[i+1], CurrentRelation[i+1])): 
                                correctnum = correctnum + 1
                        if(correctnum == unchangeObjNum):
                            return index
                #some objects change
                
                else:
                    #some objects deleted
                    if("delete" in MultiRelationAB):
                        deletenum = MultiRelationAB[MultiRelationAB_length-1]
                        if("delete" in CurrentRelation and deletenum == CurrentRelation[len(CurrentRelation)-1]):
                                equal = 0
                                for dele in range(deletenum):
                                    attribute_delete = MultiRelationAB[MultiRelationAB_length-dele-2]
                                    for same in range(CurrentRelation[0]):
                                        attribute_same = CurrentRelation[same+1]
                                        if(self.isEqualAttributes(attribute_delete, attribute_same)):
                                            equal = 1
                                if(equal == 0): 
                                    return index
                    #no objects delete
                    else:
                        changeRelationNum = MultiRelationAB_length - unchangeObjNum - 1
                        if(len(CurrentRelation) >= (changeRelationNum+currentUnchangeObjNum+1) and "delete" not in CurrentRelation):
                            correctnum2 = 0
                            for i in range(changeRelationNum):
                                if(self.isEqualAttributes(MultiRelationAB[i+unchangeObjNum+1], CurrentRelation[i+currentUnchangeObjNum+1])):
                                    correctnum2 = correctnum2 + 1
                            if(correctnum2 == changeRelationNum):
                                return index
                            
        return -1
    # The primary method for solving incoming Raven's Progressive Matrices.
    # For each problem, your Agent's Solve() method will be called. At the
    # conclusion of Solve(), your Agent should return an int representing its
    # answer to the question: 1, 2, 3, 4, 5, or 6. Strings of these ints 
    # are also the Names of the individual RavensFigures, obtained through
    # RavensFigure.getName(). Return a negative number to skip a problem.
    #
    # Make sure to return your answer *as an integer* at the end of Solve().
    # Returning your answer as a string may cause your program to crash.
    def Solve(self,problem):
    
#         if (problem.name == 'Basic Problem B-01' or problem.name == 'Basic Problem B-02' or problem.name == 'Basic Problem B-03' or problem.name == 'Basic Problem B-04'):
#             return -1
#         if(problem.name!='Basic Problem B-04'):
#             return -1;
#         if (problem.problemSetName == 'Basic Problems B' or problem.problemSetName == 'Basic Problems C'):
#             return -1
        print (problem.name)
        Objectslen = []
        bool_oneObject = 1

        self.__init__()
        for figureName in problem.figures:
            thisFigure = problem.figures[figureName]
            Objectslen.append(len(thisFigure.objects))

        for x in Objectslen:
            if(Objectslen[x] != 1):
                bool_oneObject = 0

        firstresult = self.SolveHelper(bool_oneObject, problem, 1)
        if ( firstresult == -1):
            return self.SolveHelper(bool_oneObject, problem, 2)
        else:
            return firstresult
        
        
                    



