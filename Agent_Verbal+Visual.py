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
import sys
#from __builtin__ import True




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
        self.existingAnswers3x3 = 8
        self.possibleAnswers3x3 = [1,1,1,1,1,1,1,1]
        


    def objectRelation(self, object1, object2):
        relation = {}
        sizemap = {'very small': 0, 'small': 1, 'medium':2, 'large':3, 'very large': 4, 'huge': 5}
        for attributeName in object1.attributes:
            if attributeName == 'shape' and 'shape' in object2.attributes:
                if object1.attributes['shape'] == object2.attributes['shape']:
                    relation['shape'] = 1
                else:
                    relation['shape'] = 0
            if attributeName == 'fill' and 'fill' in object2.attributes:
                if object1.attributes['fill'] == object2.attributes['fill']:
                    relation['fill'] = 1
                else:
                    relation['fill'] = 0
            if attributeName == 'size' and 'size' in object2.attributes:
                if object1.attributes['size'] == object2.attributes['size']:
                    relation['size'] = 1
                else:
                    size1 = sizemap[object1.attributes['size']]
                    size2 = sizemap[object2.attributes['size']]
                    relation['size'] = 0 if size1 < size2 else -1

            if attributeName == 'angle' and 'angle' in object2.attributes:
                
                if object1.attributes['angle'] == object2.attributes['angle']:
                    relation['angle'] = 1
                elif object1.attributes['shape'] == 'pac-man' and object2.attributes['shape'] == 'pac-man':
                    if (object1.attributes['angle'] == '45' and object2.attributes['angle'] == '135') or (object2.attributes['angle'] == '45' and object1.attributes['angle'] == '135'):
                        relation['angle'] = 'reflection'
                    elif (object1.attributes['angle'] == '315' and object2.attributes['angle'] == '225') or (object2.attributes['angle'] == '315' and object1.attributes['angle'] == '225'):
                        relation['angle'] = 'reflection'
                    elif (object1.attributes['angle'] == '180' and object2.attributes['angle'] == '0') or (object2.attributes['angle'] == '180' and object1.attributes['angle'] == '0'):
                        relation['angle'] = 'reflection'
                elif object1.attributes['shape'] == 'right triangle' and object2.attributes['shape'] == 'right triangle':
                    if (object1.attributes['angle'] == '270' and object2.attributes['angle'] == '0') or (object2.attributes['angle'] == '270' and object1.attributes['angle'] == '0'):
                        relation['angle'] = 'reflection'
                    elif (object1.attributes['angle'] == '180' and object2.attributes['angle'] == '90') or (object2.attributes['angle'] == '180' and object1.attributes['angle'] == '90'):
                        relation['angle'] = 'reflection'
                else: 
                    relation['angle'] = int(object2.attributes['angle'])-int(object1.attributes['angle'])
            if attributeName == 'alignment' and 'alignment' in object2.attributes:
                ali1 = object1.attributes['alignment']
                ali2 = object2.attributes['alignment']
                #unchanged
                if ali1 == ali2:
                    relation['alignment'] = 1
                #move left 
                elif (ali1 == 'bottom-right' and ali2 == 'bottom-left') or (ali1 == 'top-right' and ali2 == 'top-left'):
                    relation['alignment'] = 2
                #move right
                elif (ali1 == 'bottom-left' and ali2 == 'bottom-right') or (ali1 == 'top-left' and ali2 == 'top-right'):
                    relation['alignment'] = 3
                #move top
                elif (ali1 == 'bottom-right' and ali2 == 'top-right') or (ali1 == 'bottom-left' and ali2 == 'top-left'):
                    relation['alignment'] = 4
                #move down
                elif (ali1 == 'top-right' and ali2 == 'bottom-right') or (ali1 == 'top-left' and ali2 == 'bottom-left'):
                    relation['alignment'] = 5
                #move from bottom left to top right
                elif ali1 == 'bottom-left' and ali2 == 'top-right':
                    relation['alignment'] = 6
                #move from top left to bottom right
                elif ali1 == 'top-left' and ali2 == 'bottom-right':
                    relation['alignment'] = 7
                #move from top right to bottom left
                elif ali1 == 'top-right' and ali2 == 'bottom-left':
                    relation['alignment'] = 8
                #move from top left to bottom right
                elif ali1 == 'top-left' and ali2 == 'bottom-right':
                    relation['alignment'] = 9
                else:
                    relation['alignment'] = 10
                    
            if attributeName == 'width' and 'width' in object2.attributes:
                if(object1.attributes['width'] == object2.attributes['width']):
                    relation['width'] = 1
                else:
                    width1 = sizemap[object1.attributes['width']]
                    width2 = sizemap[object2.attributes['width']]
                    relation['width'] = -1 if width1 < width2 else 0 

            if attributeName == 'height' and 'height' in object2.attributes:
                if object1.attributes['height'] == object2.attributes['height']:
                    relation['height'] = 1
                else:
                    height1 = sizemap[object1.attributes['height']]
                    height2 = sizemap[object2.attributes['height']]
                    relation['height'] = -1 if height1 < heigh2 else 0

            if attributeName == 'alignmentx' and 'alignmentx' in object2.attributes: 
                a1 = object1.attributes['alignmentx']
                a2 = object2.attributes['alignmentx']
                if a1 == a2:
                    relation['alignmentx'] = 'NotMove'
                elif (a1-a2) == -2:
                    relation['alignmentx'] = 'MoveD2'
                elif (a1-a2) == -1:
                    relation['alignmentx'] = 'MoveD1' 
                elif (a1-a2) == 1:
                    relation['alignmentx'] = 'MoveU1'
                elif (a1-a2) == 2:  
                    relation['alignmentx'] = 'MoveU2'
            if attributeName == 'alignmenty' and 'alignmenty' in object2.attributes: 
                a1 = object1.attributes['alignmenty']
                a2 = object2.attributes['alignmenty']
                if a1 == a2:
                    relation['alignmenty'] = 'NotMove'
                elif (a1-a2) == -2:
                    relation['alignmenty'] = 'MoveR2'
                elif (a1-a2) == -1:
                    relation['alignmenty'] = 'MoveR1' 
                elif (a1-a2) == 1:
                    relation['alignmenty'] = 'MoveL1'
                elif (a1-a2) == 2:  
                    relation['alignmenty'] = 'MoveL2'        
                
        return relation
        

    
    def isEqualAttributes(self, attribute1, attribute2):
        if len(attribute1) != len(attribute2):
            return 0
        
        for attributeName in attribute1:
            if attributeName not in attribute2:
                return 0
            else:
                if attribute1[attributeName] != attribute2[attributeName]:
                    if attributeName == "shape" or attributeName == "fill" or attributeName == "size" or attributeName == "angle" or attributeName == "alignment" or attributeName == "width" or attributeName == "height" or attributeName == "alignmentx" or attributeName == "alignmenty":
                        return 0
                
        return 1
    
    def isSimilarAttributes(self, attribute1, attribute2):
        if len(attribute1) != len(attribute2):
            return 0
        if 'width' in attribute1 and 'height' in attribute1 and 'width' in attribute2:
            if (attribute1['shape'] == attribute2['shape']) and (attribute1['fill'] == attribute2['fill']):
                return 1
            else:
                return 0
        elif (attribute1['shape'] == attribute2['shape']) and (attribute1['fill'] == attribute2['fill']):
            return 1
        else:
            return 0
        


    def FindMatchedPair(self, figure1, figure2):
        pairRelation = []
        Relation = []
        pairnum = 0
        for objectName in figure1.objects:
            for objectName2 in figure2.objects:
                if self.isEqualAttributes(figure1.objects[objectName].attributes, figure2.objects[objectName2].attributes) == 1:
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
        if len(figure1.objects) > len(figure2.objects):
            
            pairRelation.append('delete')
            for objectName1 in figure1.objects:
                if objectName1 not in self.matchpair:
                    pairRelation.append(figure1.objects[objectName1].attributes)
            pairRelation.append(len(figure1.objects)-len(figure2.objects))
            return pairRelation
        else:
            for objectName1 in figure1.objects:
                for objectName2 in figure2.objects:
                    if objectName1 not in self.matchpair and objectName2 not in self.matchpair:
                        pairRelation.append(self.objectRelation(figure1.objects[objectName1], figure2.objects[objectName2]))
                        
            
        return pairRelation    
        

    def findAns(self):
        for index in range(len(self.possibleAnswers)):
            if self.possibleAnswers[index] == 1:
                return index+1


    
    def SolveHelper(self, bool_oneObject, problem, direction):
        if bool_oneObject == 1:
            relationAB = {}
            for objectName in problem.figures['A'].objects:
                objecta = problem.figures['A'].objects[objectName]
            for objectName in problem.figures['B'].objects:
                objectb = problem.figures['B'].objects[objectName]
            for objectName in problem.figures['C'].objects:
                objectc = problem.figures['C'].objects[objectName]
            if direction == 1:
                relationAB = self.objectRelation(objecta,objectb) 
            else:
                relationAB = self.objectRelation(objecta,objectc)   

            for index in range(1,7):
                relationAns = {}
                for objectName in problem.figures[str(index)].objects:
                    objectAns = problem.figures[str(index)].objects[objectName]
                if direction == 1:
                    relationAns = self.objectRelation(objectc,objectAns)     
                else:
                    relationAns = self.objectRelation(objectb,objectAns) 
                attributes = ['shape', 'size', 'fill', 'angle', 'alignment']
                for attribute in attributes:
                    if attribute in relationAns and attribute not in relationAB or relationAns[attribute] != relationAB[attribute]:
                        self.existingAnswers -= 1
                        self.possibleAnswers[index-1] = 0
                        if self.existingAnswers == 1:
                            return self.findAns()
                        break

        else:
            MultiRelationAB = self.FindRelationsMultiObjects(problem.figures['A'],problem.figures['B'])
            unchangeObjNum = MultiRelationAB[0]
            MultiRelationAB_length = len(MultiRelationAB)
            
            for index in range(1,7):
                self.matchpair = []
                CurrentRelation = self.FindRelationsMultiObjects(problem.figures['C'],problem.figures[str(index)])  
                currentUnchangeObjNum = CurrentRelation[0]  

                #all objects unchanged
                if MultiRelationAB_length == (unchangeObjNum+1):
                    if unchangeObjNum == CurrentRelation[0]:
                        correctnum = 0
                        for i in range(unchangeObjNum):
                            if self.isEqualAttributes(MultiRelationAB[i+1], CurrentRelation[i+1]): 
                                correctnum = correctnum + 1
                        if correctnum == unchangeObjNum:
                            return index
                #some objects change
                
                else:
                    #some objects deleted
                    if "delete" in MultiRelationAB:
                        deletenum = MultiRelationAB[MultiRelationAB_length-1]
                        if "delete" in CurrentRelation and deletenum == CurrentRelation[len(CurrentRelation)-1]:
                                equal = 0
                                for dele in range(deletenum):
                                    attribute_delete = MultiRelationAB[MultiRelationAB_length-dele-2]
                                    for same in range(CurrentRelation[0]):
                                        attribute_same = CurrentRelation[same+1]
                                        if self.isEqualAttributes(attribute_delete, attribute_same):
                                            equal = 1
                                if equal == 0: 
                                    return index
                    #no objects delete
                    else:
                        changeRelationNum = MultiRelationAB_length - unchangeObjNum - 1
                        if len(CurrentRelation) >= (changeRelationNum+currentUnchangeObjNum+1) and "delete" not in CurrentRelation:
                            correctnum2 = 0
                            for i in range(changeRelationNum):
                                if self.isEqualAttributes(MultiRelationAB[i+unchangeObjNum+1], CurrentRelation[i+currentUnchangeObjNum+1]):
                                    correctnum2 = correctnum2 + 1
                            if correctnum2 == changeRelationNum:
                                return index
                            
        return -1
    
    
    def DeleteAnswers3x3(self, length):
        answer_length = 0
        if length[0] == 1 and length[1] == 2 and length[2] == 3 and length[3] == 2 and length[4] == 4 and length[5] == 6 and length[6] == 3 and length[7] == 6:
            answer_length = 9
        elif (length[0] == length[1] == length[2]) and (length[3] == length[4] == length[5]):
            answer_length = length[6]
        elif ((length[1] - length[0]) == (length[2] - length[1])) and ((length[4] - length[3]) == (length[5] - length[4])):
            answer_length = length[7] + (length[7] - length[6])
        elif length[2] == length[5] == length[6] == length[7]:
            answer_length = length[2]
        elif (length[2] == length[1]) and (length[5] == length[4]):
            answer_length = length[7]
        #print(answer_length)
        for i in range(8,16):
            if length[i] != answer_length:
                self.existingAnswers3x3 -= 1
                self.possibleAnswers3x3[i - 8] = 0
            
    
    
    def SolveChangeN3x3(self,problem):
        relationAB = self.FindRelationsMultiObjectsAddition(problem.figures['A'], problem.figures['B'])   
        relationDE = self.FindRelationsMultiObjectsAddition(problem.figures['D'], problem.figures['E'])
        relationGH = self.FindRelationsMultiObjectsAddition(problem.figures['G'], problem.figures['H'])
        relationBC = self.FindRelationsMultiObjectsAddition(problem.figures['B'], problem.figures['C'])
        relationEF = self.FindRelationsMultiObjectsAddition(problem.figures['E'], problem.figures['F'])
        
        relationSet = [relationAB, relationDE, relationGH, relationBC, relationEF]
        
        Scores = [0,0,0,0,0,0,0,0]
        for i in range(8):
            if self.possibleAnswers3x3[i] == 1:
                #generate relation
                relationAns = self.FindRelationsMultiObjectsAddition(problem.figures['H'], problem.figures[str(i+1)])
                #evaluate
                Scores[i] = self.Evaluate3x3Addition(relationAns,relationSet)
            else:
                Scores[i] = -1
        return self.PickHighestScore(Scores)
            
    def SolveRec(self, problem):
        for FigureName in problem.figures:
            thisFigure = problem.figures[FigureName]
            for ObjectName in thisFigure.objects:
                thisObject = thisFigure.objects[ObjectName]
                if thisObject.attributes['shape'] == 'square':
                    thisObject.attributes['shape'] = 'rectangle'
                    thisObject.attributes['width'] = thisObject.attributes['size']
                    thisObject.attributes['height'] = thisObject.attributes['size']
                    del thisObject.attributes['size']
        return self.SolveChangeN3x3(problem)            
        
    def SolveAlign(self, problem):
        #choose a center object
        
        center_object = problem.figures['A'].objects['a']
        center_shape = center_object.attributes['shape']

        if 'angle' in center_object.attributes:
            center_angle = center_object.attributes['angle']
        
        skip = []
        for i in range(8):
            if self.possibleAnswers3x3[i] == 0:
                skip.append(str(i+1))
       
        
        for FigureName in problem.figures:
            thisFigure = problem.figures[FigureName]
            if FigureName in skip:
                continue
            
            for ObjectName in thisFigure.objects:
                thisObject = thisFigure.objects[ObjectName]
                if 'angle' in thisObject.attributes:
                    if thisObject.attributes['angle'] == center_angle:
                        center = thisObject
                    else:
                        move = thisObject
                else:
                    if thisObject.attributes['shape'] == center_shape:
                        center = thisObject
                    else:
                        move = thisObject
                
            if 'left-of' in move.attributes and 'above' in move.attributes:
                move.attributes['alignmentx'] = 0
                move.attributes['alignmenty'] = 0
                del move.attributes['left-of']
                del move.attributes['above']
            elif 'left-of' in move.attributes and 'above' in center.attributes:
                move.attributes['alignmentx'] = 2
                move.attributes['alignmenty'] = 0
                del move.attributes['left-of']
                del center.attributes['above']
            elif 'left-of' in move.attributes and 'above' not in center.attributes:
                move.attributes['alignmentx'] = 1
                move.attributes['alignmenty'] = 0
                del move.attributes['left-of']
            elif 'left-of' in center.attributes and 'above' in move.attributes:
                move.attributes['alignmentx'] = 0
                move.attributes['alignmenty'] = 2
                del move.attributes['above']
                del center.attributes['left-of']
            elif 'left-of' not in move.attributes and 'above' in move.attributes:
                move.attributes['alignmentx'] = 0
                move.attributes['alignmenty'] = 1
                del move.attributes['above']
            elif 'left-of' in center.attributes and 'above' in center.attributes:
                move.attributes['alignmentx'] = 2
                move.attributes['alignmenty'] = 2
                del center.attributes['left-of']
                del center.attributes['above']
            elif 'left-of' not in move.attributes and 'above' in center.attributes:
                move.attributes['alignmentx'] = 2
                move.attributes['alignmenty'] = 1
                del center.attributes['above']
            elif 'left-of' in center.attributes and 'left-of' not in move.attributes:
                move.attributes['alignmentx'] = 1
                move.attributes['alignmenty'] = 2
                del center.attributes['left-of']
            else:
                move.attributes['alignmentx'] = 1
                move.attributes['alignmenty'] = 1
                if 'overlaps' in move.attributes:
                    del move.attributes['overlaps']
                elif 'overlaps' in center.attributes:
                    del center.attributes['overlaps']
                       
        return self.SolveChangeN3x3(problem)
        
    
    def FindRelationsMultiObjectsAddition(self,figure1,figure2):
        Relation = {}
        #unchanged part, addition part, and delete part
        unchange = 0
        delete = 0
        modify = 0
        matched = {}
        Relation['relation'] = []
        for objectName1 in figure1.objects:
            find = False
            findsimilar = False
            obj1 = figure1.objects[objectName1]
            for objectName2 in figure2.objects:
                obj2 = figure2.objects[objectName2]
                if self.isEqualAttributes(obj1.attributes, obj2.attributes):
                    unchange += 1
                    matched[objectName2] = 'matched'
                    find = True
                    break
            if not find:
                for objectName2 in figure2.objects:
                    obj2 = figure2.objects[objectName2]
                    if objectName2 not in matched:
                        if self.isSimilarAttributes(obj1.attributes, obj2.attributes):
                            Relation['relation'].append(self.objectRelation(obj1, obj2))
                            findsimilar = True
                            break
                if not findsimilar:
                    delete += 1   
        add = len(figure2.objects) - unchange
        Relation['unchange'] = unchange
        Relation['delete'] = delete
        Relation['add'] = add
        
        #modify part
        count = 0
        firstObj = {}
        modify1 = 0
        modify2= 0
        left_1 = 0
        above_1 = 0
        left_2 = 0
        above_2 = 0
        over_1 = 0
        over_2 = 0
        for objectName1 in figure1.objects:
            count += 1
            obj1 = figure1.objects[objectName1]
            if 'left-of' in obj1.attributes:
                left_1 += len(obj1.attributes['left-of'].split(","))
            if 'above' in obj1.attributes:
                above_1 += len(obj1.attributes['above'].split(","))
            if 'overlaps' in obj1.attributes:
                over_1 += len(obj1.attributes['overlaps'].split(","))
            if(count == 1):
                firstObj['shape'] = obj1.attributes['shape']
                if 'height' in obj1.attributes and 'width' in obj1.attributes:
                    firstObj['width'] = obj1.attributes['width']
                    firstObj['height'] = obj1.attributes['height']
                else:
                    firstObj['size'] = obj1.attributes['size']
                firstObj['fill'] = obj1.attributes['fill']
                modify1 += 1
            else:
                if 'height' in firstObj:
                    if obj1.attributes['shape'] == firstObj['shape'] and obj1.attributes['width'] == firstObj['width'] and obj1.attributes['height'] == firstObj['height'] and obj1.attributes['fill'] == firstObj['fill']:
                        modify1 += 1
                else:
                    if obj1.attributes['shape'] == firstObj['shape'] and obj1.attributes['size'] == firstObj['size'] and obj1.attributes['fill'] == firstObj['fill']:
                        modify1 += 1
        if 'shape' not in firstObj:
            modify = 0
        else:
            for objectName2 in figure2.objects:
                obj = figure2.objects[objectName2]
                if 'left-of' in obj.attributes:
                    left_2 += len(obj.attributes['left-of'].split(","))
                if 'above' in obj.attributes:
                    above_2 += len(obj.attributes['above'].split(","))
                if 'overlaps' in obj.attributes:
                    over_2 += len(obj.attributes['overlaps'].split(","))
                if 'height' in firstObj:
                    if obj.attributes['shape'] == firstObj['shape'] and obj.attributes['width'] == firstObj['width'] and obj.attributes['height'] == firstObj['height'] and obj.attributes['fill'] == firstObj['fill']:
                        modify2 += 1
                else:
                    if obj.attributes['shape'] == firstObj['shape'] and obj.attributes['size'] == firstObj['size'] and obj.attributes['fill'] == firstObj['fill']:
                        modify2 += 1
            if modify2 > modify1:
                modify = modify1
        Relation['modify'] = modify
        if left_2 > left_1 and over_2 > over_1:
            Relation['modify-type'] = 'left-overlaps'
            Relation['modify-num'] = left_2 - left_1
        elif left_2 > left_1 and above_2 > above_1:
            Relation['modify-type'] = "left-above"
            Relation['modify-num'] = left_2 - left_1 + above_2 - above_1
        elif left_2 > left_1:
            Relation['modify-type'] = 'right'
            Relation['modify-num'] = left_2 - left_1
        else:
            Relation['modify-type'] = "unknown"
        
        return Relation
        
    def Evaluate3x3Addition(self,relationAns,relationSet):
        score = 0
        if relationSet[0]['modify'] != 0:
            div1 = relationSet[3]['modify']/relationSet[0]['modify']
        else:
            div1 = 0
        if relationSet[1]['modify'] != 0:    
            div2 = relationSet[4]['modify']/relationSet[1]['modify']
        else:
            div2 = 0
        
        sub1 = relationSet[3]['modify']-relationSet[0]['modify']
        sub2 = relationSet[4]['modify']-relationSet[1]['modify']
        if (div1 == div2) and (div1 >= 1):
            if relationAns['modify'] == (relationSet[2]['modify'] * div1):
                score += 5
            else:
                score -= 1
        elif (sub1 == sub2) and (sub1 >= 1):
            if relationAns['modify'] == (relationSet[2]['modify'] + sub1):
                score += 5
            else:
                score -= 1
                
        uc0 = relationSet[0]['unchange']
        uc1 = relationSet[1]['unchange']
        uc2 = relationSet[2]['unchange']
        uc3 = relationSet[3]['unchange']
        uc4 = relationSet[4]['unchange']
        ad0 = relationSet[0]['add']
        ad1 = relationSet[1]['add']
        ad2 = relationSet[2]['add']
        ad3 = relationSet[3]['add']
        ad4 = relationSet[4]['add']
        dl0 = relationSet[0]['delete']
        dl1 = relationSet[1]['delete']
        dl2 = relationSet[2]['delete']
        dl3 = relationSet[3]['delete']
        dl4 = relationSet[4]['delete']
        
        if uc0 == uc3 and uc1 == uc4:
            expected_unchange = uc2
        elif uc3-uc0 == uc4-uc1:
            expected_unchange = uc2 + uc3 - uc0
        elif uc0 != 0 and uc1 != 0 and uc3/uc0 == uc4/uc1:
            expected_unchange = uc2*uc3/uc0
        else:
            expected_unchange = -1
            
        if ad0 == ad3 and ad1 == ad4:
            expected_add = ad2
        elif ad3-ad0 == ad4-ad1:
            expected_add = ad2 + ad3 - ad0
        elif ad0 != 0 and ad1 != 0 and ad3/ad0 == ad4/ad1:
            expected_add = ad2*ad3/ad0
        else:
            expected_add = -1
            
        if dl0 == dl3 and dl1 == dl4:
            expected_delete = dl2
        elif dl3-dl0 == dl4-dl1:
            expected_delete = dl2 + dl3 - dl0
        elif dl0 != 0 and dl1 != 0 and dl3/dl0 == dl4/dl1:
            expected_delete = dl2*dl3/dl0
        else:
            expected_delete = -1
            
        for i in range(5):
            if 'relation' in relationSet[i] and 'relation' in relationAns: 
                if relationSet[i]['relation'] == relationAns['relation']:
                    score += 5
                else:
                    score -= 1
            if expected_add >= 0:
                if relationAns['add'] == expected_add:
                    score += 5
                else: 
                    score -= 3
           
            if expected_delete >= 0: 
                if relationAns['delete'] == expected_delete:
                    score += 5
                else:
                    score -= 3
            
            if expected_unchange >= 0: 
                if relationAns['unchange'] == expected_unchange:
                    score += 5
                else:
                    score -= 3

        
        count = [0,0,0,0]
        for i in range(5):
            if relationSet[i]['modify-type'] == 'right':
                count[2] += 1
            elif relationSet[i]['modify-type'] == 'left-above':
                count[0] += 1
            elif relationSet[i]['modify-type'] == 'left-overlaps':
                count[1] += 1
            elif relationSet[i]['modify-type'] == 'unknown':
                count[3] += 1
        maxcount = 0
        maxindex = 0
        for i in range(4):
            if count[i] > maxcount:
                maxcount = count[i]
                maxindex = i 
        if maxindex == 0 and count[2] > 0:
            modifytype = 'right'
        elif maxindex == 0:
            modifytype = 'left-above'    
        elif maxindex == 1:
            modifytype = 'left-overlaps'
        elif maxindex == 2:
            modifytype = 'right'
        elif maxindex == 3:
            modifytype = 'unknown'
            
            
        if relationAns['modify-type'] != modifytype:
            score -= 1
        elif relationAns['modify-type'] == 'left-above' or relationAns['modify-type'] == 'left-overlaps':
            modifynum1 = relationSet[3]['modify-num']/relationSet[0]['modify-num']
            modifynum2 = relationSet[4]['modify-num']/relationSet[1]['modify-num']
            if modifynum1 == modifynum2 and modifynum1 >= 1:
                errorfactor = relationSet[2]['modify-num']/5
                if relationAns['modify-num'] >= (relationSet[2]['modify-num'] * modifynum1 - errorfactor) and relationAns['modify-num'] <= (relationSet[2]['modify-num'] * modifynum1):
                    score += 5
                else:
                    score -= 1
        
            
        return score
                
    def SolveVisual(self,problem):
        size0 = Image.open(problem.figures['A'].visualFilename).size[0]
        size1 = Image.open(problem.figures['A'].visualFilename).size[1]
        figureA = Image.open(problem.figures['A'].visualFilename).load()
        figureB = Image.open(problem.figures['B'].visualFilename).load()
        figureC = Image.open(problem.figures['C'].visualFilename).load()
        figureD = Image.open(problem.figures['D'].visualFilename).load()
        figureE = Image.open(problem.figures['E'].visualFilename).load()
        figureF = Image.open(problem.figures['F'].visualFilename).load()
        figureG = Image.open(problem.figures['G'].visualFilename).load()
        figureH = Image.open(problem.figures['H'].visualFilename).load()
        
        figureA = self.ModifyMatrix(figureA, size0, size1)
        figureB = self.ModifyMatrix(figureB, size0, size1)
        figureC = self.ModifyMatrix(figureC, size0, size1)
        figureD = self.ModifyMatrix(figureD, size0, size1)
        figureE = self.ModifyMatrix(figureE, size0, size1)
        figureF = self.ModifyMatrix(figureF, size0, size1)
        figureG = self.ModifyMatrix(figureG, size0, size1)
        figureH = self.ModifyMatrix(figureH, size0, size1)
                   
        AB = figureB - figureA
        DE = figureE - figureD
        GH = figureH - figureG
        BC = figureC - figureB
        EF = figureF - figureE
        
        #flip
        BCflip = numpy.flipud(BC)
        EFflip = numpy.flipud(EF)

        #numpy.savetxt('AB.txt', AB, fmt = '%i', header = problem.name)
        X_c = self.FindWhiteLineX(figureC)
        X_f = self.FindWhiteLineX(figureF)
        Y_g = self.FindWhiteLineY(figureG)
        Y_h = self.FindWhiteLineY(figureH)

        
        is_result_graph = False
        if self.SimilarGraph(AB, DE) and self.SimilarGraph(AB, GH) and self.SimilarGraph(BC,EF):
            #add EF to H
            is_result_graph = True
            result_graph = EF + figureH
            result_graph = self.OverflowGraph(result_graph)
            #self.outputFile(problem.name + "expect", result_graph)
            print("Similiar")
            
        elif self.SimilarGraph(AB, BCflip) and self.SimilarGraph(DE, EFflip):
            print("Similar flip")
            is_result_graph = True
            result_graph = figureH + numpy.flipud(GH)
            
        if is_result_graph:    
            similar_graphs = [0,0,0,0,0,0,0,0]
            minval = size0*size1+1000
            for i in range(8):
                if self.possibleAnswers3x3[i]:
                    figureAns = Image.open(problem.figures[chr(ord('1')+i)].visualFilename).load()
                    figureAns = self.ModifyMatrix(figureAns, size0, size1)
                    similar_graphs[i] = self.DifferenceGraph(figureAns, result_graph)
                else:
                    similar_graphs[i] = minval
            
            mini = 0
            for i in range(8):
                if similar_graphs[i] < minval:
                    minval = similar_graphs[i]
                    mini = i+1
            return mini  
        
             
        
        return -1
    def FindWhiteLineY(self, graph):
        y = []
        for j in range(graph.shape[1]):
            havespot = False
            for i in range(graph.shape[0]):
                if graph[i,j] == 1:
                    havespot = True
            if havespot == False and j > 25 and j < 160:
                y.append(j)
        return y
    
    def FindWhiteLineX(self, graph):
        x = []
        for i in range(graph.shape[0]):
            havespot = False
            for j in range(graph.shape[1]):
                if graph[i,j] == 1:
                    havespot = True
            if havespot == False and i > 25 and i < 160:
                x.append(i)
        return x   
    
    def SimilarList(self, list1, list2):
        if len(list1) == len(list2) == 0:
            return False
        threshold = (len(list1)+len(list2))/2*0.95
        max1 = max(list1)
        max2 = max(list2)
        similar = 0
        
        if max1 > max2:
            big_list = [0] * (max1+1)
            maxtotal = max1
        else:
            big_list = [0] * (max2+1) 
            maxtotal = max2 
        for i in range(len(list1)):
            big_list[list1[i]] += 1   
        for i in range(len(list2)):
            big_list[list2[i]] += 1  
        for i in range(maxtotal):
            if big_list[i] == 2:
                similar += 1
        if similar > threshold:
            return True
        else:
            return False
        
    def SimilarValList(self, list1, list2):
        max1 = max(list1)
        max2 = max(list2)
        similar = 0
        if max1 > max2:
            big_list = [0] * (max1+1)
            maxtotal = max1
        else:
            big_list = [0] * (max2+1) 
            maxtotal = max2 
        for i in range(len(list1)):
            big_list[list1[i]] += 1   
        for i in range(len(list2)):
            big_list[list2[i]] += 1  
        for i in range(maxtotal):
            if big_list[i] == 2:
                similar += 1
        return similar
          
    def SimilarGraph(self, graph1, graph2):
        threshold = graph1.size*0.03
        diff = graph2 - graph1
        diff_val = 0
        for i in range(graph1.shape[0]):
            for j in range(graph1.shape[1]):
                if diff[i,j] != 0:
                    diff_val += 1
        if diff_val > threshold:
            return False
        else:
            return True
        
    def DifferenceGraph(self, graph1, graph2):
        diff = graph2 - graph1
        diff_val = 0
        for i in range(graph1.shape[0]):
            for j in range(graph1.shape[1]):
                if diff[i,j] != 0:
                    diff_val += 1
        return diff_val
    

    def OverflowGraph(self,graph):
        for i in range(graph.shape[0]):
            for j in range(graph.shape[1]):
                if graph[i,j] > 1:
                    graph[i,j] = 1
        return graph
    def outputFile(self, problemName, matrix):
        f=open(problemName, "w")
        
        for i in range(matrix.shape[0]):
            for j in range(matrix.shape[1]):
                if matrix[j,i] > 0:
                    f.write('x')
                else:
                    f.write(' ')
            f.write("\n")
        f.close()
    
    def ModifyMatrix(self,matrix,size0,size1):
        newMatrix = numpy.zeros((size0,size1))
        for i in range(size0):
            for j in range(size1):
                if matrix[i,j][1] == 0:
                    newMatrix[i,j] = 1
                else:
                    newMatrix[i,j] = 0
        return newMatrix
                 
    def SolveHelper3x3(self,problem):
        Objectslen = []
        for i in range(16):
            Objectslen.append(0)
        problemHasRec = 0
        problemHasLeft = 0
        problemHasAbove = 0
        problemHasOver = 0
        for i in range(8):
            Objectslen[i] = len(problem.figures[chr(ord('A')+i)].objects)
            for ObjectName in problem.figures[chr(ord('A')+i)].objects:
                thisObject = problem.figures[chr(ord('A')+i)].objects[ObjectName]
                if(thisObject.attributes['shape'] == 'rectangle'):
                    problemHasRec = 1
                if 'left-of' in thisObject.attributes:
                    problemHasLeft = 1
                if 'above' in thisObject.attributes:
                    problemHasAbove = 1
                if 'overlaps' in thisObject.attributes:
                    problemHasOver = 1
        for i in range(8,16):
            Objectslen[i] = len(problem.figures[chr(ord('1')+i-8)].objects)
        
        #self.DeleteAnswers3x3(Objectslen)
        
        if self.existingAnswers3x3 == 1:
            for i in range(8):
                if self.possibleAnswers3x3[i]:
                    return i+1
        
        if Objectslen[0] == Objectslen[1] == Objectslen[2]:#N unchange
            if Objectslen[0] > 2:
                return -1
            elif problemHasRec:
                return self.SolveRec(problem)
            elif problemHasLeft and (problemHasAbove or problemHasOver):
                return self.SolveAlign(problem)
            
            else:
                return self.SolveChangeN3x3(problem)
                
        else:
            return self.SolveChangeN3x3(problem)
        
        return -1
                
    def PickHighestScore(self,scores):
        maxnum = 0
        for i in range(8):
            if(scores[i] > maxnum):
                maxi = i
                maxnum = scores[i]
        if maxnum > 0:
            find_another = False
            for i in range(8):
                if scores[i] == maxnum and maxi != i:
                    find_another = True
            
            if not find_another and maxnum > 42: 
                return maxi + 1
            else:
                return -1
        else:
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
        Objectslen = []
        self.__init__()
            
        if problem.problemType == "2x2":
            bool_oneObject = 1
            for figureName in problem.figures:
                thisFigure = problem.figures[figureName]
                Objectslen.append(len(thisFigure.objects))
                

            for x in Objectslen:
                if(Objectslen[x] != 1):
                    bool_oneObject = 0
            
            firstresult = self.SolveHelper(bool_oneObject, problem, 1)
            if firstresult == -1:
                return self.SolveHelper(bool_oneObject, problem, 2)
            else:
                return firstresult
        else:
            result3x3 = self.SolveHelper3x3(problem)
                
            if result3x3 == -1:
                return self.SolveVisual(problem) 
            else:
                return result3x3       
        return -1;
        
                    



