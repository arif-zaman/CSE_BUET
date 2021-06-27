length = 0

def printMatrix(P):
    for row in range(len(P)):
        for col in range(len(P[row])):
            print '%2d' % P[row][col], 
        print


def initialMatrix(file_name):
	global length
	with open(file_name) as fhandle:
		for i, l in enumerate(fhandle):
			pass

        length = i+1

        # Create Blank NxN Matrix
        P = [[0 for x in range(length)] for y in range(length)]
	
	with open(file_name) as fhandle:
		value = []
		for line in fhandle:
			words = line.split()
			for word in words:
				value.append(int(word))
        
        for i in xrange(length):
        	for j in xrange(length):
        		P[i][j] = value.pop(0)
	return P


def defaultGoal():
    P = [[0 for x in range(length)] for y in range(length)]
    count = 1
    for x in xrange(length):
        for y in xrange(length):
            P[x][y] = count
            count = count+1

    P[length-1][length-1] = 0
    
    return P


def customGoal(file_name):
    P = [[0 for x in range(length)] for y in range(length)]
    
    with open(file_name) as fhandle:
        value = []
        for line in fhandle:
            words = line.split()
            for word in words:
                value.append(int(word))
        
        for i in xrange(length):
            for j in xrange(length):
                P[i][j] = value.pop(0)
    return P


def goalMatrix(file_name):
    print "\nEnter :\n1 - Default Goal\n2 - Custom Goal\n"
    num = int(raw_input("Choice : "))
    print

    if num == 1:
        P = defaultGoal()
        return P
    if num == 2:
       P = customGoal(file_name)
       return P


def isSolvable(P):
    temp = P
    temp2 = []
    inversion = 0
    zero = 0
    for i in xrange(length):
        for j in xrange(length):
            temp2.append(temp[i][j])

    #print temp2
    zero = temp2.index(0) / length

    for i in xrange(length**2):
        for j in xrange(length**2):
            if i+j>length**2-1:
                break
            if temp2[i]>temp2[i+j]:
                if temp2[i+j]==0:
                    continue
                #print temp2[i],temp2[i+j]
                inversion += 1

    #print zero,inversion
    if length%2==0:
        if (inversion+zero)%2==0:
            return False
        else:
            return True
    else:
        if inversion%2==1:
            return False
        else:
            return True



def manhattan_Crude_Method(puzzle):
    row,col = puzzle.getPosition(0)
    return abs(length-1-row)+abs(length-1-col)


def manhattan(puzzle):
    pCost = 0
    for row in range(length):
        for col in range(length):
            val = puzzle.getValue(row, col) - 1
            if val < 0:
            	continue

            tRow = val / length
            tCol = val % length
            #print val,length,tRow,tCol
            pCost += abs(tRow - row) + abs(tCol - col)
            #print val,length,tRow,row,tCol,col,pCost

    #print pCost
    return pCost


def linearConflict(puzzle):
	pCost = 0
	pCost = manhattan(puzzle)
	N = length*length

	for i in xrange(N):
		for j in xrange(N):
			if i==j or i==0 or j==0:
				continue # Same Tile or Zero

			row_i,col_i = puzzle.getPosition(i)
			tRow_i = (i-1) / length
			tCol_i = (i-1) % length

			row_j,col_j = puzzle.getPosition(j)
			tRow_j = (j-1) / length
			tCol_j = (j-1) % length

			if (row_i==row_j and row_i==tRow_i and row_j==tRow_j and col_i>col_j and tCol_i<tCol_j) or (col_i==col_j and col_i==tCol_i and col_j==tCol_j and row_i>row_j and tRow_i<tRow_j):
				pCost = pCost+2
			
	return pCost


def index(item, seq):
    # Return Index of a Sequence
    if item in seq:
        return seq.index(item)
    else:
        return -1


class Board:
    def __init__(self,finish):
        self.hval = 0           # Heuristic Value
        self.depth = 0          # Search Depth of Current Instance
        self.parent = None      # Parent Node in Search Path
        self.pState = []        # Present State
        self.gState = finish    # Goal State

        for i in range(length):
            self.pState.append(self.gState[i][:])


    def __str__(self):
    	# Called by the str() built-in function and by the print statement
    	# to compute the "informal" string representation of an object.
        res = ''
        for row in range(length):
            res += ' '.join(map(str, self.pState[row]))
            res += '\r\n'
        return res


    def set(self, P):
        self.pState = P
    

    def clone(self):
        p = Solver(self.gState)
        for i in range(length):
            p.pState[i] = self.pState[i][:]
        return p


    def getPosition(self, value):
        if value < 0 or value > length**2-1:
            raise Exception("value out of range")

        for row in range(length):
            for col in range(length):
                if self.pState[row][col] == value:
                    return row, col


    def getValue(self, row, col):
        return self.pState[row][col]


    def setValue(self, row, col, value):
        self.pState[row][col] = value


    def swapPositon(self, positionA, positionB):
        temp = self.getValue(*positionA)
        self.setValue(positionA[0], positionA[1], self.getValue(*positionB))
        self.setValue(positionB[0], positionB[1], temp)


class Solver(Board):
    def __init__(self, finish):
        Board.__init__(self,finish)
        self.gState = finish


    def legalMoves(self):
        """Returns list of tuples with which the free space may
        be swapPositonped"""
        # get row and column of the empty piece
        row, col = self.getPosition(0)
        free = []
        
        # getPosition which pieces can move there
        if row > 0:
            free.append((row - 1, col))
        if col > 0:
            free.append((row, col - 1))
        if row < length-1:
            free.append((row + 1, col))
        if col < length-1:
            free.append((row, col + 1))

        return free


    def generateLegalMoves(self):
        free = self.legalMoves()
        zero = self.getPosition(0)

        def swapPositonAndClone(a, b):
            p = self.clone()
            p.swapPositon(a,b)
            p.depth = self.depth + 1
            p.parent = self
            return p

        return map(lambda pair: swapPositonAndClone(zero, pair), free)


    def buildPath(self, path):
        if self.parent == None:
            return path
        else:
            path.append(self)
            return self.parent.buildPath(path)


    def solve(self, h):
        # Performs A* search for goal state.
        # h(puzzle) - heuristic function, returns an integer

        def isGoal(puzzle):
            return puzzle.pState == self.gState

        openBrunch = [self]
        closedBrunch = []
        moveCount = 0

        while len(openBrunch) > 0:
            x = openBrunch.pop(0)
            moveCount += 1
            n = 100
            z = moveCount % n
            if z==0:
            	print "Searching node %d" % moveCount
            	n = n*2

            if (isGoal(x)):
                if len(closedBrunch) > 0:
                    return x.buildPath([]), moveCount
                else:
                    return [x], moveCount

            moveList = x.generateLegalMoves()
            ob_Index = cb_Index = -1
            for move in moveList:
                # Have We Already Seen This Node?
                ob_Index = index(move, openBrunch) # ob - Open Brunch
                cb_Index = index(move, closedBrunch) # cb - Closed Brunch

                hval = h(move)
                fval = hval + move.depth

                # Yet to Visit 
                if cb_Index == -1 and ob_Index == -1:
                    move.hval = hval
                    openBrunch.append(move)

                # Visiting Current Loop
                elif ob_Index > -1:
                    copy = openBrunch[ob_Index]
                    if fval < copy.hval + copy.depth:
                        # copy move's values over existing
                        copy.hval = hval
                        copy.parent = move.parent
                        copy.depth = move.depth

                # Compare Previously Visited Option
                elif cb_Index > -1:
                    copy = closedBrunch[cb_Index]
                    if fval < copy.hval + copy.depth:
                        move.hval = hval
                        closedBrunch.remove(copy)
                        openBrunch.append(move)

            closedBrunch.append(x)
            # sort by fval
            openBrunch = sorted(openBrunch, key=lambda p: p.hval + p.depth)

        # if finished state not found, return failure
        return [], 0


def main():
    initial_State = initialMatrix("initial.txt")
    goal_State = goalMatrix("goal.txt")

    print "Initial State :\n"
    printMatrix(initial_State)
    print "\nGoal State :\n"
    printMatrix(goal_State)

    if isSolvable(initial_State):
    	print "\nUsing Mathatton Distance :"
        print "\nSolution Path : \n"
        puzzle = Solver(goal_State)
        puzzle.set(initial_State)
        print puzzle

        path, count = puzzle.solve(manhattan)
        path.reverse()
        for i in path:
            print i

        print "Total States Explored : %d" % count
        print "Minimum Moves Need to Solve This Puzzle : %d" % len(path)

        print "\nUsing Linear Conflict :"
        print "\nSolution Path : \n"
        puzzle = Solver(goal_State)
        puzzle.set(initial_State)
        print puzzle

        path, count = puzzle.solve(linearConflict)
        path.reverse()
        for i in path:
            print i

        print "Total States Explored : %d" % count
        print "Minimum Moves Need to Solve This Puzzle : %d" % len(path)

        exit()

    print "\nUnsolvable Puzzle!!"


if __name__ == "__main__":
	main()
