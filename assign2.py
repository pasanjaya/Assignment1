class Node:
    def __init__(self, name):
        self.coordname = name
        self.x1 = None
        self.y1 = None
        self.x2 = None
        self.y2 = None
        self.nfront = None
        self.nback = None
        self.nlyingOn = []


class bTree:
    def __init__(self):
        self.root = None
        self.front = []
        self.back = []
        self.on_line = []

    def insertRoot(self, coordData):
        if (self.root == None):
            newNode = Node(coordData)
            newNode.x1 = float(coordData[0][0])
            newNode.y1 = float(coordData[0][1])
            newNode.x2 = float(coordData[1][0])
            newNode.y2 = float(coordData[1][1])
            self.root = newNode
            # print(self.root.coordname)
        else:
            print(self.root)
    def checkingfb(self, rootcoordData, chkcoordData):

        ax = float(rootcoordData[0][0])
        ay = float(rootcoordData[0][1])
        bx = float(rootcoordData[1][0])
        by = float(rootcoordData[1][1])

        cx = float(chkcoordData[0][0])
        cy = float(chkcoordData[0][1])
        dx = float(chkcoordData[1][0])
        dy = float(chkcoordData[1][1])

        signOne = self.signchk((bx-ax)*(cy-ay)- (by-ay)*(cx-ax))
        signTwo = self.signchk((bx-ax)*(dy-ay)- (by-ay)*(dx-ax))

        # print(rootcoordData)
        # print(chkcoordData)

        # print(signOne)
        # print(signTwo)

        if (signOne == signTwo):
            if(signOne == 1):
                # print("front")
                #self.front.append(chkcoordData)
                return("front", chkcoordData)
            elif(signOne == -1):
                # print("back")
                #self.back.append(chkcoordData)
                return ("back", chkcoordData)
            else:
                # print("onLine")
                #self.on_line.append(chkcoordData)
                return("on_line", chkcoordData)
        else:
            # print("intersect")
            if(signOne + signTwo != 0):
                if(signOne == 1 or signTwo == 1):
                    #self.front.append(chkcoordData)
                    return ("front", chkcoordData)
                elif(signOne == -1 or signTwo == -1):
                    #self.back.append(chkcoordData)
                    return ("back", chkcoordData)
                else:
                    print("Error found")
            elif(signOne + signTwo == 0):
                # print("Serious case found")

                pt1 = rootcoordData[0]
                pt2 = rootcoordData[1]

                ptA = chkcoordData[0]
                ptB = chkcoordData[1]

                # print(pt1)
                # print(pt2)
                # print(ptA)
                # print(ptB)

                result = self.intersectLines(pt1, pt2, ptA, ptB)
                intersectX, intersectY = result
                intersectCoord = (round(intersectX,2),round(intersectY,2))
                # print(chkcoordData)
                # print(cx)
                # print(cy)
                # print("Specil: ",intersectCoord)
                newCoord1 = [chkcoordData[0], intersectCoord]
                newCoord2 = [intersectCoord, chkcoordData[1]]
                if(signOne == 1):
                    #self.front.append(newCoord1)
                    # print("f1")
                    return ["special",(("front", newCoord1),("back", newCoord2))]
                elif(signOne == -1):
                    #self.back.append(newCoord1)
                    # print("b1")
                    return ["special",(("front", newCoord2),("back", newCoord1))]
                # if(signTwo == 1):
                #     #self.front.append(newCoord2)
                #     print("f2")
                #     return ("front", newCoord2)
                # elif(signTwo == -1):
                #     #self.back.append(newCoord2)
                #     print("b2")
                #     return ("back", newCoord2)
                else:
                    print("serious intersect error")

                # print(newCoord1)
                # print(newCoord2)

            else:
                print("Error found while intersect")
        print(self.front)
        print(len(self.front))
        print(self.back)
        print(len(self.back))
        print(self.on_line)
        print(len(self.on_line))

    def signchk(self,value):
        #check positive or negetive or on line
        if(value>0):
            return 1 #if positive return 1
        elif(value<0):
            return -1 #if negetive return 1
        else:
            return 0 #if on line return 0


    def intersectLines(self, pt1, pt2, ptA, ptB):
        #   Solve using Cayley-Hamilton theorem
        #   [ dx1  -dx ][ r ] = [ x-x1 ]
        #   [ dy1  -dy ][ s ] = [ y-y1 ]
        #   X = A^(-1)B
        #   [ r ] = _1_  [  -dy   dx ] [ x-x1 ]
        #   [ s ] = DET  [ -dy1  dx1 ] [ y-y1 ]

        DET_TOLERANCE = 0.00000001

        # first line
        Ax, Ay = pt1
        Bx, By = pt2
        dx1 = Bx - Ax
        dy1 = By - Ay

        # second line
        Qx, Qy = ptA
        Px, Py = ptB
        dx = Px - Qx
        dy = Py - Qy

        DET = (-dx1 * dy + dy1 * dx)

        if math.fabs(DET) < DET_TOLERANCE: return (0, 0, 0, 0, 0)  # parallel line

        DETinv = 1.0 / DET

        r = DETinv * (-dy * (Qx - Ax) + dx * (Qy - Ay))

        s = DETinv * (-dy1 * (Qx - Ax) + dx1 * (Qy - Ay))

        xi = (Ax + r * dx1 + Qx + s * dx) / 2.0
        yi = (Ay + r * dy1 + Qy + s * dy) / 2.0
        return (xi, yi)


    def insertfbNode(self,rootcoordData, chkcoordData):
        if (self.root != None):
            temp = self.root
            while (True):
                print("checking coord: ", chkcoordData)
                position, coord = self.checkingfb(temp.coordname, chkcoordData)
                print("checking root: ", temp.coordname)
                print("found position: ", position)
                if (position == "front"):
                    if(temp.nfront == None):
                        newNode = Node(coord)
                        newNode.x1 = float(coord[0][0])
                        newNode.y1 = float(coord[0][1])
                        newNode.x2 = float(coord[1][0])
                        newNode.y2 = float(coord[1][1])
                        temp.nfront = newNode
                        print("root: ", temp.coordname)
                        print("front: ++++++++++++++++", temp.nfront.coordname)
                        return
                    else:
                        print("else")
                        temp = temp.nfront
                elif(position == "back"):
                    if (temp.nback == None):
                        newNode = Node(coord)
                        newNode.x1 = float(coord[0][0])
                        newNode.y1 = float(coord[0][1])
                        newNode.x2 = float(coord[1][0])
                        newNode.y2 = float(coord[1][1])
                        temp.nback = newNode
                        print("root: ", temp.coordname)
                        print("back:++++++++++++ ", temp.nback.coordname)
                        return
                    else:
                        print("else")
                        temp = temp.nback
                elif(position == "on_line"):
                    temp.nlyingOn.append(coord)
                    print("OnLine")
                    return

                elif (position == "special"):
                    ck = 0
                    if(coord[0][0] == "front"):
                        if (temp.nfront == None):
                            ncoord = coord[0][1]
                            newNode = Node(ncoord)
                            newNode.x1 = float(ncoord[0][0])
                            newNode.y1 = float(ncoord[0][1])
                            newNode.x2 = float(ncoord[1][0])
                            newNode.y2 = float(ncoord[1][1])
                            temp.nfront = newNode
                            ck +=1
                            print("root: ", temp.coordname)
                            print("front:++++++++++++++++ ", temp.nfront.coordname)

                        else:
                            print("XXXX")
                            print(temp.nfront.coordname)
                            #chkcoordData = coord[0][1]
                            temp = temp.nfront
                            continue
                    print("ck: ", coord[1][0])
                    if(coord[1][0] == "back"):
                        if (temp.nback == None):
                            ncoord = coord[1][1]
                            newNode = Node(ncoord)
                            newNode.x1 = float(ncoord[0][0])
                            newNode.y1 = float(ncoord[0][1])
                            newNode.x2 = float(ncoord[1][0])
                            newNode.y2 = float(ncoord[1][1])
                            temp.nback = newNode
                            ck +=1
                            print("root: ", temp.coordname)
                            print("back: +++++++++++++++++", temp.nback.coordname)

                        else:
                            print("else@@@")
                            # chkcoordData = coord[1][1]
                            temp = temp.nback
                            continue
                    if(ck==2):
                        print("****")
                        return
                    else:
                        print("!!!!!!")


    def frontMostLine(self):
        self.frontLine(self.root)

    def frontLine(self, curNode):
        if (curNode.nfront == None):
            print("Front Most Line: ", curNode.coordname)
        elif (curNode.nfront != None):
            self.frontLine(curNode.nfront)

    def back2front(self, curNode):
        if (curNode != None):
            self.back2front(curNode.nback)
            print(curNode.coordname)
            self.back2front(curNode.nfront)

    def frontBackNode(self,searchKey):
        node = self.traversal(searchKey)
        if(node != None):
            # print("#### ",node.coordname)
            if(node.nfront != None):
                print("Front line: ", node.nfront.coordname,"\n")
            elif(node.nfront == None):
                print("No front line(s) for: ",node.coordname,"\n")
            if (node.nback != None):
                print("Back line: ",node.nback.coordname,"\n")
            elif (node.nback == None):
                print("No back line(s) for: ", node.coordname,"\n")

            if (node.nlyingOn != []):
                print("On line: ",node.nlyingOn,"\n")
            elif (node.nlyingOn == []):
                print("No on line segments for: ", node.coordname,"\n")

            else:
                print("BLA BLA BLA")
        else:
            print("Searching Key is not Found, maybe it intersected by a line")
        #print(searchKey)

    def traversal(self,data):
        curNode = self.root
        while(curNode != None):
            # print(curNode.coordname)
            # print(data)
            if(curNode.coordname == data):
                print("Found")
                return curNode
            elif(curNode.coordname != data):
                position, coord = position, coord = self.checkingfb(curNode.coordname, data)
                if(position == "front"):
                    curNode = curNode.nfront
                    continue
                elif(position == "back"):
                    curNode = curNode.nback
                    continue
                elif(position == "special"):
                    if(coord[0][0] == "front"):
                        curNode = curNode.nfront
                        continue
                else:
                    print(position)
                    break


#------------------------------------- main()--------------------------------------#
import ast, math

bt = bTree()
f = open("testCase.txt", "r")

while True:
    n = f.readline() # input()
    n = n.strip("\n")
    try:
        n = int(n.strip())
        if n < 0:
            print("Negetive numbers not allowed.\nTry again.")
            continue
        break
    except ValueError:
        print("Integer not found.\nTry again.")
# print(n)  # number of lines
while True:
    s = f.readline()
    s = s.strip("\n")# input()
    try:
        s = int(s.strip())
        if (s < 3 or s > n + 2):
            print("Input Error!.\nTry again.")
            continue
        break
    except ValueError:
        print("Integer not found.\nTry again.")
# print(s)  # starting line
f.close()
f = open("testCase.txt", "r")
fCoord = f.readlines()
# print(fCoord)
coordString = fCoord[s-1].strip()
if coordString:
    a = list(ast.literal_eval(coordString)) #make string to list of tuple
    bt.insertRoot(a)
coordList = []
for i in range(2, n + 2):
    if (i != s-1):
        coord = fCoord[i]
        coordString = coord.strip()
        if (coordString):
            #print(list(ast.literal_eval(coordString)))
            b = list(ast.literal_eval(coordString))
            #bt.checkingfb(a,b)
            coordList.append(b)
            #bt.insertfbNode(a,b)
#bt.insertfbNode()
while(coordList != []):
    b = coordList.pop(0)
    bt.insertfbNode(a,b)
    #print(coordList)
f.close()  # close file



print("#################################################################")
print("To find front most: Enter A")
print("Output from back to front: Enter B")
print("To find position of given node: Enter C")


inLine = input("On your Command: ")
while(inLine != "Q"):
    if(inLine == "A"):
        print()
        bt.frontMostLine()
        print()
    elif(inLine == "B"):
        print()
        print("- - - PRINTING ALL NODES FROM BACK TO FRONT - - -\n")
        bt.back2front(bt.root)
        print()
    elif(inLine == "C"):
        print()
        print("Ex:   [(4,6),(7,23)]")
        print()
        searchKey = input("What is your searching line?: ")
        searchKey = list(ast.literal_eval(searchKey))
        # searchKey = [(-4, -2), (-3.5, -0.33)] #testing
        bt.frontBackNode(searchKey)
        print()
    inLine = input("On your Command: ")
    
print("++++++++++++END++++++++++++++")
