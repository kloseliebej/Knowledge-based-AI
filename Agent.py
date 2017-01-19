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
from matplotlib.cbook import Null
import numpy
import sys

from PIL import Image
from multiprocessing import Queue



#from __builtin__ import True
class LabelSet:
    def __init__(self, val):
        self.parent = Null
        self.val = val
    
    def ChangeParent(self, newParent):
        self.parent = newParent

    def FindRoot(self):
        while self.parent != Null:
            self.val = self.parent.val
            self.parent = self.parent.parent
        return self.val
    
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
        
        
        
        is_result_graph = False
        #one row has same shape
        if self.SimilarGraph(figureA, figureB) and self.SimilarGraph(figureB, figureC) and self.SimilarGraph(figureD, figureE) and self.SimilarGraph(figureE, figureF) and self.SimilarGraph(figureG, figureH):
            print("one row same shape")
            is_result_graph = True
            result_graph = figureH
        #diagonal has same shape
        elif self.SimilarGraph(figureB, figureF) and self.SimilarGraph(figureF, figureG) and self.SimilarGraph(figureC, figureD) and self.SimilarGraph(figureD, figureH) and self.SimilarGraph(figureA, figureE):
            print('diagonal same shape')
            is_result_graph = True
            result_graph = figureE    
        # A OR B = C
        elif self.SimilarGraph(self.OrGraph(figureA, figureB), figureC ) and self.SimilarGraph(self.OrGraph(figureD, figureE), figureF ):
            print('OR')
            is_result_graph = True
            result_graph = self.OrGraph(figureG, figureH)
        # A AND B = C
        elif self.SimilarGraph(self.AndGraph(figureA, figureB), figureC ) and self.SimilarGraph(self.AndGraph(figureD, figureE), figureF ):
            print('AND')
            is_result_graph = True
            result_graph = self.AndGraph(figureG, figureH)
        # A XOR B = C
        elif self.SimilarGraph(self.XORGraph(figureA, figureB), figureC ) and self.SimilarGraph(self.XORGraph(figureD, figureE), figureF ):
            print('XOR')
            is_result_graph = True
            result_graph = self.XORGraph(figureG, figureH)
        #subtract
        elif self.SimilarGraph(AB, DE) and self.SimilarGraph(AB, GH) and self.SimilarGraph(BC,EF):
            #add EF to H
            is_result_graph = True
            result_graph = EF + figureH
            result_graph = self.OverflowGraph(result_graph)
            #self.outputFile(problem.name + "expect", result_graph)
            print("Similiar subtract")
            
        elif self.SimilarGraph(AB, BCflip) and self.SimilarGraph(DE, EFflip):
            print("Similar flip")
            is_result_graph = True
            result_graph = figureH + numpy.flipud(GH)
        
        # A+B+C == D+E+F
        elif self.SimilarGraph(self.OrGraph(self.OrGraph(figureA,figureB),figureC) ,self.OrGraph(self.OrGraph(figureD,figureE),figureF) ):
            print('A+B+C == D+E+F')
            possible_answers = []
            possible_answers_index = []
            points = []
            OrABC = self.OrGraph(self.OrGraph(figureA,figureB),figureC)
            for i in range(8):
                figureAns = Image.open(problem.figures[chr(ord('1')+i)].visualFilename).load()
                figureAns = self.ModifyMatrix(figureAns, size0, size1)
                if self.SimilarGraphStrict(self.OrGraph(self.OrGraph(figureG,figureH),figureAns), OrABC):
#                     print(i+1)
#                     print(self.DifferenceGraph(self.OrGraph(self.OrGraph(figureG,figureH),figureAns), OrABC))
                    possible_answers.append(figureAns)
                    possible_answers_index.append(i)
                    points.append(0)
            if len(possible_answers) == 0:
                return -1        
            for i in range(len(possible_answers)):
                points[i] = self.DifferenceGraph(figureA, possible_answers[i]) + self.DifferenceGraph(figureE, possible_answers[i])
            minval = size0*size1+1000
            for i in range(len(possible_answers)):
                if points[i] < minval:
                    minval = points[i]
                    mini = possible_answers_index[i]
            return mini+1 
        
        # A+D+G == B+E+H
        elif self.SimilarGraph(self.OrGraph(self.OrGraph(figureA,figureD),figureG) ,self.OrGraph(self.OrGraph(figureB,figureE),figureH) ):
            print('A+D+G == B+E+H')
            possible_answers = []
            possible_answers_index = []
            points = []
            OrADG = self.OrGraph(self.OrGraph(figureA,figureD),figureG)
            for i in range(8):
                figureAns = Image.open(problem.figures[chr(ord('1')+i)].visualFilename).load()
                figureAns = self.ModifyMatrix(figureAns, size0, size1)
                if self.SimilarGraphStrict(self.OrGraph(self.OrGraph(figureC,figureF),figureAns), OrADG):
                    #print(i+1)
                    #print(self.DifferenceGraph(self.OrGraph(self.OrGraph(figureC,figureF),figureAns), OrADG))
                    possible_answers.append(figureAns)
                    possible_answers_index.append(i)
                    points.append(0)
            if len(possible_answers) == 0:
                return -1         
            for i in range(len(possible_answers)):
                points[i] = self.DifferenceGraph(figureG, possible_answers[i]) + self.DifferenceGraph(figureH, possible_answers[i])
            minval = size0*size1+1000
            for i in range(len(possible_answers)):
                if points[i] < minval:
                    minval = points[i]
                    mini = possible_answers_index[i]
            return mini+1 
        
        
        
        #A = B+C, including shift
        else:
            
            offset = self.ShiftAmount(figureB, figureA)
            figureB = numpy.roll(figureB, offset, axis = 0)
            offset = self.ShiftAmount(figureE, figureD)
            figureE = numpy.roll(figureE, offset, axis = 0)
            offset = self.ShiftAmount(figureH, figureG)
            figureH = numpy.roll(figureH, offset, axis = 0)
            
            AB = figureA - figureB
            DE = figureD - figureE
            GH = figureG - figureH
            
            offset = self.ShiftAmount(AB, figureC)
            AB = numpy.roll(AB, offset, axis = 0)
            offset = self.ShiftAmount(DE, figureF)
            DE = numpy.roll(DE, offset, axis = 0)
            
            if self.SimilarGraph(AB, figureC) and self.SimilarGraph(DE, figureF):
                print("A = B+C, shift")
                GH = self.CenterGraph(GH)
                #self.outputFile(problem.name + "GHcenter", GH)
                is_result_graph = True
                result_graph = GH

            else:
                
                figureBflip = numpy.fliplr(figureB)
                figureEflip = numpy.fliplr(figureE)
                figureHflip = numpy.fliplr(figureH) 
                
                offset = self.ShiftAmount(figureBflip, figureA)
                figureBflip = numpy.roll(figureBflip, offset, axis = 0)
                offset = self.ShiftAmount(figureEflip, figureD)
                figureEflip = numpy.roll(figureEflip, offset, axis = 0)
                offset = self.ShiftAmount(figureHflip, figureG)
                figureHflip = numpy.roll(figureHflip, offset, axis = 0)
                
                AB = figureA - figureBflip
                DE = figureD - figureEflip
                GH = figureG - figureHflip
                
                offset = self.ShiftAmount(figureC, AB)
                AB = numpy.roll(AB, offset, axis = 0)
                offset = self.ShiftAmount(figureF, DE)
                DE = numpy.roll(DE, offset, axis = 0)
                
                if self.SimilarGraph(AB, figureC) and self.SimilarGraph(DE, figureF):
                    print("flip add")
                    is_result_graph = True
                    result_graph = self.CenterGraph(GH)
                    
                    #self.outputFile(problem.name + "expect", result_graph)
                    
                else:
                    print('after flip add')
                    
                    objectsA = self.FindAllObjects(figureA)
                    objectsB = self.FindAllObjects(figureB)
                    objectsC = self.FindAllObjects(figureC)
                    objectsD = self.FindAllObjects(figureD)
                    objectsE = self.FindAllObjects(figureE)
                    objectsF = self.FindAllObjects(figureF)
                    objectsG = self.FindAllObjects(figureG)
                    objectsH = self.FindAllObjects(figureH)
                    
#                     self.outputFile(problem.name + "first objectA", objectsA[0])
#                     self.outputFile(problem.name + "first objectB", objectsB[0])
#                     self.outputFile(problem.name + "first objectC", objectsC[0])
#                     self.outputFile(problem.name + "first objectD", objectsD[0])
#                     self.outputFile(problem.name + "first objectE", objectsE[0])
#                     self.outputFile(problem.name + "first objectF", objectsF[0])
#                     self.outputFile(problem.name + "first objectG", objectsG[0])
#                     self.outputFile(problem.name + "first objectH", objectsH[0])
                    #print(len(objectsA) + len(objectsB) + len(objectsC))
                    if len(objectsA)== 0 or len(objectsB)== 0 or len(objectsC)== 0 or len(objectsD)== 0 or len(objectsE)== 0 or len(objectsF)== 0 or len(objectsG)== 0 or len(objectsH)== 0:
                        return -1
                    
                    if len(objectsA)-1 + len(objectsB)-1 + len(objectsC)-1 <= 10 :
                        print('length < 9')
                        #try to split figure into inner part and outer part
                        in_objectA = objectsA[0]
                        in_objectB = objectsB[0]
                        in_objectC = objectsC[0]
                        in_objectD = objectsD[0]
                        in_objectE = objectsE[0]
                        in_objectF = objectsF[0]
                        in_objectG = objectsG[0]
                        in_objectH = objectsH[0]
                        
                        out_objectA = figureA - in_objectA
                        out_objectB = figureB - in_objectB
                        out_objectC = figureC - in_objectC
                        out_objectD = figureD - in_objectD
                        out_objectE = figureE - in_objectE
                        out_objectF = figureF - in_objectF
                        out_objectG = figureG - in_objectG
                        out_objectH = figureH - in_objectH
                        
                        out_objectA_comp = self.GetBoundingBox(out_objectA)
                        out_objectB_comp = self.GetBoundingBox(out_objectB)
                        out_objectC_comp = self.GetBoundingBox(out_objectC)
                        out_objectD_comp = self.GetBoundingBox(out_objectD)
                        out_objectE_comp = self.GetBoundingBox(out_objectE)
                        out_objectF_comp = self.GetBoundingBox(out_objectF)
                        out_objectG_comp = self.GetBoundingBox(out_objectG)
                        out_objectH_comp = self.GetBoundingBox(out_objectH)
                        
                        
#                         self.outputFile(problem.name + 'out B', out_objectB)
#                         self.outputFile(problem.name + 'out F', out_objectF)
#                         self.outputFile(problem.name + 'out G', out_objectG)
                        
                        # inner pattern AFH (sub diagonal)
                        if self.SimilarGraphLoose(in_objectA, in_objectF) and self.SimilarGraphLoose(in_objectF, in_objectH) and self.SimilarGraphLoose(in_objectC, in_objectE) and self.SimilarGraphLoose(in_objectE, in_objectG) and self.SimilarGraphLoose(in_objectB, in_objectD):
                            # out pattern BFG (main diagonal) 
                            #print('sub and main')
                            line1 = self.SimilarGraphLoose(out_objectB_comp, out_objectF_comp) and self.SimilarGraphLoose(out_objectF_comp, out_objectG_comp)
                            line2 = self.SimilarGraphLoose(out_objectC_comp, out_objectD_comp) and self.SimilarGraphLoose(out_objectD_comp, out_objectH_comp)
                            line3 = self.SimilarGraphLoose(out_objectA_comp, out_objectE_comp)
                            
                            if line1 or line2 or line3:
                                print('sub and main')
#                                 for i in range(8):
#                                     figureAns = Image.open(problem.figures[chr(ord('1')+i)].visualFilename).load()
#                                     figureAns = self.ModifyMatrix(figureAns, size0, size1)
#                                     objectsAns = self.FindAllObjects(figureAns)
#                                     in_objectAns = objectsAns[0]
#                                     out_objectAns = figureAns - in_objectAns
#                                     out_objectAns = self.GetBoundingBox(out_objectAns)
#                                     if (self.SimilarGraphLoose(in_objectAns , in_objectB) or self.SimilarGraphLoose(in_objectAns , in_objectD)) and (self.SimilarGraphLoose(out_objectAns, out_objectA) or self.SimilarGraphLoose(out_objectAns, out_objectE)):
#                                         print("answer is " + str(i+1))
#                                         return i+1
                                is_result_graph = True
                                result_graph = in_objectB + out_objectE
                                #self.outputFile(problem.name + 'expect', result_graph)
                        # inner pattern BFG (main diagonal)
                            #out pattern sub diagonal
                        elif self.SimilarGraphLoose(in_objectB, in_objectF) and self.SimilarGraphLoose(in_objectF, in_objectG) and self.SimilarGraphLoose(in_objectC, in_objectD) and self.SimilarGraphLoose(in_objectD, in_objectH) and self.SimilarGraphLoose(in_objectA, in_objectE):
                            
                            line1 = self.SimilarGraphLoose(out_objectA_comp, out_objectF_comp) and self.SimilarGraphLoose(out_objectF_comp, out_objectH_comp)
                            line2 = self.SimilarGraphLoose(out_objectC_comp, out_objectE_comp) and self.SimilarGraphLoose(out_objectE_comp, out_objectG_comp)
                            line3 = self.SimilarGraphLoose(out_objectB_comp, out_objectD_comp)
                            if line1 or line2 or line3:
                                print('main and sub')
                                is_result_graph = True
                                result_graph = in_objectE + out_objectB
#                                 for i in range(8):
#                                     figureAns = Image.open(problem.figures[chr(ord('1')+i)].visualFilename).load()
#                                     figureAns = self.ModifyMatrix(figureAns, size0, size1)
#                                     objectsAns = self.FindAllObjects(figureAns)
#                                     in_objectAns = objectsAns[0]
#                                     out_objectAns = figureAns - in_objectAns
#                                     out_objectAns = self.GetBoundingBox(out_objectAns)
#                                     if (self.SimilarGraphLoose(in_objectAns , in_objectA) or self.SimilarGraphLoose(in_objectAns , in_objectE)) and (self.SimilarGraphLoose(out_objectAns, out_objectB) or self.SimilarGraphLoose(out_objectAns, out_objectD)):
#                                         return i+1
 
                    elif self.HaveSimilarObj(objectsA) and self.HaveSimilarObj(objectsB) and self.HaveSimilarObj(objectsC) and self.HaveSimilarObj(objectsD) and self.HaveSimilarObj(objectsE) and self.HaveSimilarObj(objectsF) and self.HaveSimilarObj(objectsG) and self.HaveSimilarObj(objectsH):
                        if len(objectsA)-1 > 2 and len(objectsB)-1 > 2 and len(objectsC)-1 > 2 and len(objectsD)-1 > 2 and len(objectsE)-1 > 2 and len(objectsF)-1 > 2 and len(objectsG)-1 > 2 and len(objectsH)-1 > 2:
                            if len(objectsA) + len(objectsB) + len(objectsC) == len(objectsD) + len(objectsE) + len(objectsF):
                                print("have same objects in one figure, 3, 4, 5")
                                #pattern 1 (answer has similar pattern = B or D, answer has size = A, E)
                                if self.SimilarGraphLoose(objectsC[1], objectsE[1]) and self.SimilarGraphLoose(objectsE[1], objectsG[1]) and self.SimilarGraphLoose(objectsA[1], objectsF[1]) and self.SimilarGraphLoose(objectsF[1], objectsH[1]) and self.SimilarGraphLoose(objectsD[1], objectsB[1]):  
                                    for i in range(8):
                                        figureAns = Image.open(problem.figures[chr(ord('1')+i)].visualFilename).load()
                                        figureAns = self.ModifyMatrix(figureAns, size0, size1)
                                        objectsAns = self.FindAllObjects(figureAns)
                                        if (self.SimilarGraphLoose(objectsAns[1] , objectsB[1]) or self.SimilarGraphLoose(objectsAns[1] , objectsD[1])) and len(objectsAns) + len(objectsG) + len(objectsH) == len(objectsA) + len(objectsB) + len(objectsC):
                                            return i+1
                                    
        
                                #pattern 2
                                elif self.SimilarGraphLoose(objectsC[1], objectsD[1]) and self.SimilarGraphLoose(objectsD[1], objectsH[1]) and self.SimilarGraphLoose(objectsB[1], objectsF[1]) and self.SimilarGraphLoose(objectsF[1], objectsG[1]) and self.SimilarGraphLoose(objectsA[1], objectsE[1]): 
                                    for i in range(8):
                                        figureAns = Image.open(problem.figures[chr(ord('1')+i)].visualFilename).load()
                                        figureAns = self.ModifyMatrix(figureAns, size0, size1)
                                        objectsAns = self.FindAllObjects(figureAns)
                                        if (self.SimilarGraphLoose(objectsAns[1] , objectsA[1]) or self.SimilarGraphLoose(objectsAns[1] , objectsE[1])) and len(objectsAns) + len(objectsG) + len(objectsH) == len(objectsA) + len(objectsB) + len(objectsC):
                                            return i+1
            
            
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
        
    
            
    def SimilarGraphStrict(self, graph1, graph2):
        threshold = graph1.size*0.023
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
        
    def SimilarGraphLoose(self, graph1, graph2):
        threshold = graph1.size*0.15
        diff_val = 0
        diff_graph = numpy.zeros((min(graph1.shape[0], graph2.shape[0]), min(graph1.shape[1], graph2.shape[1])))
        for i in range(min(graph1.shape[0], graph2.shape[0])):
            for j in range(min(graph1.shape[1], graph2.shape[1])):
                if graph1[i,j] != graph2[i,j]:
                    diff_val += 1
                    diff_graph[i,j] = 1
        #self.outputFile('D12 figureC difference', diff_graph)
        if diff_val > threshold:
#             print('diff_val is ' + str(diff_val))
#             print('threshold is' + str(threshold))
#             print('size is ' + str(graph1.size))
#             print('width is ' + str(graph1.shape[0]))
            return False
        else:
            return True   
    
    def FillGraph(self, graph):
        center = (graph.shape[0] /2, graph.shape[1] /2)
        visit = numpy.zeros((graph.shape[0], graph.shape[1]))
        visit[center[0], center[1]] = 1
        q = queue.Queue()
        q.put(center)
        while not q.empty():
            point = q.get()
            graph[point[0], point[1]] = 1
            try:
                if graph[point[0]+1, point[1]] == 0 and visit[point[0]+1, point[1]] == 0:
                    q.put((point[0]+1, point[1]))
                    visit[point[0]+1, point[1]] = 1
                if graph[point[0]-1, point[1]] == 0 and visit[point[0]-1, point[1]] == 0:
                    q.put((point[0]-1, point[1]))
                    visit[point[0]-1, point[1]] = 1
                if graph[point[0], point[1]+1] == 0 and visit[point[0], point[1]+1] == 0:
                    q.put((point[0], point[1]+1))
                    visit[point[0], point[1]+1] = 1
                if graph[point[0], point[1]-1] == 0 and visit[point[0], point[1]-1] == 0:
                    q.put((point[0], point[1]-1))
                    visit[point[0], point[1]-1] = 1
            except LookupError:
                break
        
            
    
    def GetBoundingBox(self, graph):
        min_x = 183
        min_y = 183
        max_x = 0
        max_y = 0
        for i in range(graph.shape[0]):
            for j in range(graph.shape[1]):
                if graph[i,j] == 0:
                    continue
                if i < min_y :
                    min_y = i
                if j < min_x :
                    min_x = j
                if i > max_y :
                    max_y = i
                if j > max_x :
                    max_x = j
        if min_x == 183 and min_y == 183 and max_x == 0 and max_y == 0:
            newgraph = numpy.zeros((graph.shape[0], graph.shape[1]))
        else:
            newgraph = self.CopyGraph(graph, min_x, min_y, max_x, max_y)
        return newgraph            
                    
            
            
    def DifferenceGraph(self, graph1, graph2):
        diff = graph2 - graph1
        diff_val = 0
        for i in range(graph1.shape[0]):
            for j in range(graph1.shape[1]):
                if diff[i,j] != 0:
                    diff_val += 1
        return diff_val
        
    
    def OrGraph(self, graph1, graph2):
        newGraph = numpy.zeros((graph1.shape[0],graph1.shape[1]))
        for i in range(graph1.shape[0]):
            for j in range(graph1.shape[1]):
                if(graph1[i,j] == 0 and graph2[i,j] == 0):
                    newGraph[i,j] = 0
                else:
                    newGraph[i,j] = 1
        return newGraph
    
    def AndGraph(self, graph1, graph2):
        newGraph = numpy.zeros((graph1.shape[0],graph1.shape[1]))
        for i in range(graph1.shape[0]):
            for j in range(graph1.shape[1]):
                if(graph1[i,j] == 1 and graph2[i,j] == 1):
                    newGraph[i,j] = 1
                else:
                    newGraph[i,j] = 0
        return newGraph    
        
    def XORGraph(self, graph1, graph2):
        newGraph = numpy.zeros((graph1.shape[0],graph1.shape[1]))
        for i in range(graph1.shape[0]):
            for j in range(graph1.shape[1]):
                if(graph1[i,j] == 1 and graph2[i,j] == 1):
                    newGraph[i,j] = 0
                elif graph1[i,j] == 0 and graph2[i,j] == 0:
                    newGraph[i,j] = 0
                else:
                    newGraph[i,j] = 1
        return newGraph   
    
         
     
    def ShiftAmount(self, graph1, graph2):
        first1 = 0
        first2 = 0
        for i in range(graph1.shape[0]):
            havespot = False
            for j in range(graph1.shape[1]):
                if graph1[i,j] == 1:
                    first1 = i
                    havespot = True
            if havespot:
                break        
        for i in range(graph2.shape[0]):
            havespot = False
            for j in range(graph2.shape[1]):
                if graph2[i,j] == 1:
                    first2 = i
                    havespot = True
            if havespot:
                break  

        return first2-first1 
    
    
    def CenterGraph(self, graph):
        centerx = graph.shape[0]/2
        sumx = 0
        count = 0
        for i in range(graph.shape[0]):
            for j in range(graph.shape[1]) :
                if graph[i,j] == 1:
                    sumx += i
                    count += 1
        averagex = sumx / count
        graph = numpy.roll(graph, centerx - averagex ,axis = 0)
        return graph
                    
    def FindAllObjects(self, graph): 
        #newGraph = numpy.zeros((graph.shape[0],graph.shape[1])) 
        newGraph = self.CopyGraph(graph, 0, 0, graph.shape[0]-1, graph.shape[1]-1)
        ListOfLabels = []
        ListOfLabels.append(0)
        labelIndex = 1
        for j in range(newGraph.shape[0]):
            for i in range(newGraph.shape[1]):
                if j == 0:
                    above = 0
                else:
                    above = newGraph[i-1,j]
                if i == 0:
                    left = 0
                else:  
                    left = newGraph[i, j-1]
                if newGraph[i,j] == 1:
                    if left == 0 and above == 0:
                        newGraph[i,j] = labelIndex
                        newLabel = LabelSet(labelIndex)
                        ListOfLabels.append(newLabel)
                        labelIndex += 1
                    elif left >= 1 and above == 0:
                        newGraph[i,j] = left
                    elif left == 0 and above >= 1:
                        newGraph[i,j] = above
                    elif left >= 1 and above >= 1:
                        newGraph[i,j] = min(left,above)
                        
                        if left != above:
                            ListOfLabels[int(max(left,above))].ChangeParent(ListOfLabels[int(min(left,above))])
        
        objects = []
        for j in range(newGraph.shape[0]):
            for i in range(newGraph.shape[1]):
                if newGraph[i,j] <= 0:
                    continue
                root = ListOfLabels[int(newGraph[i,j])].FindRoot()
                newGraph[i,j] = root
                if root not in objects:
                    objects.append(root) 
        if len(objects) == 0:
            return objects
                
                    
        sumx = [0] * len(objects)
        sumy = [0] * len(objects)
        maxx = [0] * len(objects)
        maxy = [0] * len(objects)
        minx = [200] * len(objects)
        miny = [200] * len(objects)
        count = [0] * len(objects)        
        for j in range(newGraph.shape[0]):
            for i in range(newGraph.shape[1]):
                for obj in range(len(objects)):
                    if newGraph[i,j] == objects[obj]:
                        sumx[obj] += j
                        sumy[obj] += i
                        if j >= maxx[obj]:
                            maxx[obj] = j
                        if i >= maxy[obj]:
                            maxy[obj] = i
                        if j <= minx[obj]:
                            minx[obj] = j
                        if i <= miny[obj]:
                            miny[obj] = i
                        count[obj] += 1
                        break
        
        object_graphs = []
        maxcount = 0
        maxi = 0
        
        for i in range(len(objects)):
            if count[i] <= 3:
                continue
#             centerx = sumx[i]/count[i]
#             centery = sumy[i]/count[i]
#             maxwidth = maxx[i] - minx[i]
#             maxheight = maxy[i] - miny[i]
#             maxlen = max(maxwidth, maxheight)
            if count[i] > maxcount:
                maxcount = count[i]
                object_graph = self.CopyGraph(newGraph, minx[i], miny[i], maxx[i], maxy[i])
                object_graph = self.EliminateGraph(object_graph, objects[i])
                object_graphs.insert(0, object_graph)
                maxi = i
            else:
                object_graph = self.CopyGraph(newGraph, minx[i], miny[i], maxx[i], maxy[i])
                object_graph = self.EliminateGraph(object_graph, objects[i])
                object_graphs.append(object_graph)   
                
        center_graph = numpy.zeros((newGraph.shape[0], newGraph.shape[1]))
        for i in range (newGraph.shape[0]):
            for j in range (newGraph.shape[1]):
                if newGraph[i,j] == objects[maxi]:
                    center_graph[i,j] = 1
        
        if count[maxi] > 500 and count[maxi] < 1300 and (sumx[maxi]/count[maxi]) < 101 and (sumx[maxi]/count[maxi]) > 85 and (sumy[maxi]/count[maxi]) < 101 and (sumy[maxi]/count[maxi]) > 85:
            self.FillGraph(center_graph)
        object_graphs.insert(0, center_graph)
        return object_graphs
                                
    def HaveSimilarObj(self, ListOfGraph): 
        HaveSimilarObj = True
        for i in range (1, len(ListOfGraph)-1):
            graph1 = ListOfGraph[i]
            graph2 = ListOfGraph[i+1]
            #self.outputFile('D12 graph1 + ' + str(i), graph1)
            #self.outputFile('D12 graph2 + ' + str(i), graph2)
            #print(graph1.size)
            #print(graph2.size)
            if abs(graph1.size - graph2.size) >= 100:
                #print("here1")
                HaveSimilarObj = False
                break
            if not self.SimilarGraphLoose(graph1, graph2):
                #print('here2')
                HaveSimilarObj = False
                break
        
        
        return HaveSimilarObj
                    
                
        
                        
    def OverflowGraph(self,graph):
        for i in range(graph.shape[0]):
            for j in range(graph.shape[1]):
                if graph[i,j] > 1:
                    graph[i,j] = 1
        return graph
    
    def CopyGraph(self, graph, minx, miny, maxx, maxy):
        newgraph = numpy.zeros((maxy-miny+1, maxx-minx+1))
        for i in range(miny, maxy+1):
            for j in range(minx, maxx+1):
                newgraph[i-miny,j-minx] = graph[i,j]
        return newgraph
                
    
    def EliminateGraph(self, graph, item):
        #self.outputFileNumerical("eliminate before", graph)
        for i in range(graph.shape[0]):
            for j in range(graph.shape[1]):
                if graph[i,j] != item:
                    graph[i,j] = 0
                elif graph[i,j] == item:
                    graph[i,j] = 1
        #self.outputFileNumerical('eliminate after', graph)
        return graph
    
    def outputFile(self, problemName, matrix):
        f=open(problemName, "w")
        
        for i in range(matrix.shape[1]):
            for j in range(matrix.shape[0]):
                if matrix[j,i] > 0:
                    f.write('x')
                else:
                    f.write(' ')
            f.write("\n")
        f.close()
        
    def outputFileNumerical(self, problemName, matrix):
        f=open(problemName, "w")
        
        for i in range(matrix.shape[1]):
            for j in range(matrix.shape[0]):
                if matrix[j,i] > 0:
                    f.write(str(int(matrix[j,i])) + ' ')
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
            
            if (not find_another) and (maxnum > 42): 
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
    
#         if (problem.name == 'Basic Problem B-01' or problem.name == 'Basic Problem B-02' or problem.name == 'Basic Problem B-03' or problem.name == 'Basic Problem B-04'):
#             return -1
#         if(problem.name !='Basic Problem C-08'):
#             return -1;
#         if (problem.problemSetName == 'Challenge Problems B' or problem.problemSetName == 'Challenge Problems C'):
#             return -1
        print (problem.name)
        
        self.__init__()
        if(problem.problemType == '3x3'):
            #if  problem.name == 'Basic Problem D-07' or problem.name == 'Basic Problem D-08' or problem.name == 'Basic Problem D-12':
            #if problem.problemSetName == 'Challenge Problems E' :
            return self.SolveVisual(problem) 
        return -1
       
        
        
                    



