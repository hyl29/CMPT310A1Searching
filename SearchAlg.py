# SearchAlg.py
#
# Sept30 2018

import heapq
import math

# Variable Settings
testCase = 'filepathhere'


# -------------------------------------------------------------------
def readDataFile(inputFile):
    """
        This function opens the file, read its content in to a list,
        close the file and return a data list.

        :param inputFile: the input file name
        :return dataList: a list holding the content of the data file
    """
    dataFile = open(inputFile, "r")

    # Read file content into a list
    dataList = list(dataFile)

    # Close file
    dataFile.close()
    return dataList


# -------------------------------------------------------------------
def makeGridList(dataList):
    """
        This function turns a string list of unwanted symbols into a integer list

        :param dataList: the header input list including "[","]"," "
        :return: a list of grid positions
    """
    # Deleting the unwanted symbols while keeping the numbers ( string type )
    info = dataList.replace("[", "").replace("]", "").replace("  ", ",")

    # For loop to check multiple digits numbers
    stringList = []
    word = ""
    for i in range(0, len(info)):
        if info[i].isdigit():
            word = word + info[i]
        else:
            stringList.append(word)
            word = ""

    # Mapping to convert string type list to integer list type
    intList = list(map(int, stringList))
    return intList


# -------------------------------------------------------------------
def gridPositionList(dataList, gridSize):
    """
        This function fixes the formatting problem like the previous function

        :param dataList: the body input list including "[","]"," "
        :param gridSize: the size of the grid
        :return: a list of grid positions
    """
    newGridList = []
    for i in range(2, gridSize + 2):
        string = dataList[i].replace("[", "").replace("]", "").strip(" ")
        intList = [int(s) for s in string.split(" ")]
        newGridList.append(intList)
    return newGridList


# -------------------------------------------------------------------
def checkMove(currentX, currentY, newX, newY, gridSize, gridList):
    """
        This function checks for an impassible cliff and boundary

        :param currentX: current position x
        :param currentY: current position y
        :param newX: new position x
        :param newY: new position y
        :param gridSize: N * N matrix boundary
        :param gridList: Actual coordinates of the grid
        :return: True for valid move, False for invalid move
    """
    if (newX < 0 or newY < 0):
        return False
    elif (newX >= gridSize or newY >= gridSize):
        return False
    else:
        currentElevation = gridList[currentY][currentX]
        # print("cur x = ", currentX)
        # print("cur y = ", currentY)
        # print("cur value is ", currentElevation)

        newElevation = gridList[newY][newX]
        # print("new x = ", newX)
        # print("new y = ", newY)
        # print("new value is ", newElevation)
        if (abs(currentElevation - newElevation) <= 4):
            return True
        else:
            return False


# -------------------------------------------------------------------
def calculateCost(currentX, currentY, newX, newY, gridList):
    """
        Calculating the cost of the next position
        :param currentX: current position x
        :param currentY: current position y
        :param newX: new position x
        :param newY: new position y
        :param gridList: Actual coordinates of the grid
        :return: the cost of making the new move
    """
    currentElevation = gridList[currentY][currentX]
    newElevation = gridList[newY][newX]

    cost = 1 + abs(currentElevation - newElevation)
    return cost


# -------------------------------------------------------------------
def calculateCostAStar(currentX, currentY, newX, newY, gridList, targetPosition):
    """
        Calculating the cost of the next position
        :param currentX: current position x
        :param currentY: current position y
        :param newX: new position x
        :param newY: new position y
        :param gridList: Actual coordinates of the grid
        :param targetPosition: the target position of the grid
        :return: the cost combining cost so far and heuristic function
    """
    currentElevation = gridList[currentY][currentX]
    newElevation = gridList[newY][newX]
    targetX = int(targetPosition.split(",")[0])
    targetY = int(targetPosition.split(",")[1])

    # Regular cost so far
    cost = 1 + abs(currentElevation - newElevation)

    # Heuristic Function using Euclidean Distance ( Pythagorean Theorem )
    heuristic = math.sqrt((targetX-currentX)**2 + (targetY-currentY)**2)

    costAStar = cost + heuristic
    return costAStar


# ------------------------------------------------ Main ------------------------------------------------ #
# Read data from file
dataList = readDataFile(testCase)

# Obtaining grid size of N x N
gridSize = int(dataList[0])

# Initial and target position of X and Y (both int and string version for debugging)
gridList = makeGridList(dataList[1])
initialPosX = gridList[0]
initialPosY = gridList[1]
targetPosX = gridList[2]
targetPosY = gridList[3]
targetPosition = str(targetPosX) + "," + str(targetPosY)

# Fix the formatting of the remaining lists
gridList = gridPositionList(dataList, gridSize)

# -------------------------------------- Part 1: Best-First Search -------------------------------------- #
# Counter for total number of nodes expanded
bestFirstTotal = 0

# Priority queue using Python's heap library
bestFirstPQ = []
initialPosition = str(initialPosX) + "," + str(initialPosY)
visitedList = []
parentList = []

# Inserting initial position
heapq.heappush(bestFirstPQ, (0, initialPosition))
# List to store all the nodes found
visitedList.append(initialPosition)
# parentList is the map backtracking array
parentList.append(initialPosition)

# -------------------------------- Main Algorithm for Best-First Search ----------------------------------#
while (len(bestFirstPQ) != 0):
    # Data for current node
    currentNode = heapq.heappop(bestFirstPQ)    # type = tuple
    bestFirstTotal += 1
    currentCost = currentNode[0]                # type = int
    currentPos = currentNode[1]                 # type = str
    currentX = int(currentPos.split(",")[0])    # type = int
    currentY = int(currentPos.split(",")[1])    # type = int

    # Check whether if we have arrived our target position
    if (currentPos == targetPosition):
        break
    # Check 4 available directions
    else:
        # UP
        checkUp = checkMove(currentX, currentY, currentX, currentY - 1, gridSize, gridList)
        nextPos = str(currentX) + "," + str(currentY - 1)
        if (checkUp and nextPos not in visitedList):
            nextCost = calculateCost(currentX, currentY, currentX, currentY - 1, gridList)
            visitedList.append(nextPos)
            parentList.append(currentPos)
            heapq.heappush(bestFirstPQ, (nextCost, nextPos))

        # DOWN
        checkDown = checkMove(currentX, currentY, currentX, currentY + 1, gridSize, gridList)
        nextPos = str(currentX) + "," + str(currentY + 1)
        if (checkDown and nextPos not in visitedList):
            nextCost = calculateCost(currentX, currentY, currentX, currentY + 1, gridList)
            visitedList.append(nextPos)
            parentList.append(currentPos)
            heapq.heappush(bestFirstPQ, (nextCost, nextPos))

        # LEFT
        checkLeft = checkMove(currentX, currentY, currentX - 1, currentY, gridSize, gridList)
        nextPos = str(currentX - 1) + "," + str(currentY)
        if (checkLeft and nextPos not in visitedList):
            nextCost = calculateCost(currentX, currentY, currentX - 1, currentY, gridList)
            visitedList.append(nextPos)
            parentList.append(currentPos)
            heapq.heappush(bestFirstPQ, (nextCost, nextPos))

        # RIGHT
        checkRight = checkMove(currentX, currentY, currentX + 1, currentY, gridSize, gridList)
        nextPos = str(currentX + 1) + "," + str(currentY)
        if (checkRight and nextPos not in visitedList):
            nextCost = calculateCost(currentX, currentY, currentX + 1, currentY, gridList)
            visitedList.append(nextPos)
            parentList.append(currentPos)
            heapq.heappush(bestFirstPQ, (nextCost, nextPos))

# ------------------------------ Part 1: Backtracking to find the path ---------------------------------- #
backTrackingList = []

currentBackTrack = targetPosition
backTrackingList.append(currentBackTrack)

# Using parentList as a dictionary
while(currentBackTrack != initialPosition):
    index = visitedList.index(currentBackTrack)

    # Go to parentList[index] to find the parent of visitedList[index]
    currentBackTrack = parentList[index]
    backTrackingList.append(currentBackTrack)

totalPathLength = len(backTrackingList)
totalPathCost = 0

# Calculating the total cost of the path
for i in range(0,totalPathLength-1):
    current = backTrackingList[i]
    next = backTrackingList[i+1]
    currentX = int(current.split(",")[0])
    currentY = int(current.split(",")[1])
    newX = int(next.split(",")[0])
    newY = int(next.split(",")[1])

    nextCost = calculateCost(currentX, currentY, newX, newY, gridList)
    totalPathCost = totalPathCost + nextCost


# Reversing the backTracking Array because it starts with target position
reversedList = backTrackingList[::-1]

# ------------------------------------------- Part 1: Results ------------------------------------------- #
print("Results of Best-First Search Algorithm")
print("The total number of nodes expanded: ", bestFirstTotal)
print("The total number of nodes found: ", len(visitedList))
print("The cost of the path: ", totalPathCost)
print("The length of the path: ", totalPathLength)
print("The path found: ", reversedList)
print("-------------------------------------------------------------------------------------------------")


# ------------------------------------------ Part 2: A* Search ------------------------------------------ #
# Counter for total number of nodes expanded
aStarTotal = 0

# Priority queue using Python's heap library
aStarPQ = []

initialPositionStar = str(initialPosX) + "," + str(initialPosY)
visitedListAStar = []
parentListAStar = []

# Inserting initial position
heapq.heappush(aStarPQ, (0, initialPositionStar))
# List to store all the nodes found
visitedListAStar.append(initialPositionStar)
# parentList is the map backtracking array
parentListAStar.append(initialPositionStar)

# ---------------------------------- Main Algorithm for A-Star Search ----------------------------------- #
while (len(aStarPQ) != 0):
    # Data for current node
    currentNode = heapq.heappop(aStarPQ)      # type = tuple
    aStarTotal += 1
    currentCost = currentNode[0]              # type = int
    currentPos = currentNode[1]               # type = str
    currentX = int(currentPos.split(",")[0])  # type = int
    currentY = int(currentPos.split(",")[1])  # type = int

    # Check whether if we have arrived our target position
    if (currentPos == targetPosition):
        break
    # Check 4 available directions
    else:
        # UP
        checkUp = checkMove(currentX, currentY, currentX, currentY - 1, gridSize, gridList)
        nextPos = str(currentX) + "," + str(currentY - 1)
        if (checkUp and nextPos not in visitedListAStar):
            nextCost = calculateCostAStar(currentX, currentY, currentX, currentY - 1, gridList, targetPosition)
            visitedListAStar.append(nextPos)
            parentListAStar.append(currentPos)
            heapq.heappush(aStarPQ, (nextCost, nextPos))

        # DOWN
        checkDown = checkMove(currentX, currentY, currentX, currentY + 1, gridSize, gridList)
        nextPos = str(currentX) + "," + str(currentY + 1)
        if (checkDown and nextPos not in visitedListAStar):
            nextCost = calculateCostAStar(currentX, currentY, currentX, currentY + 1, gridList, targetPosition)
            visitedListAStar.append(nextPos)
            parentListAStar.append(currentPos)
            heapq.heappush(aStarPQ, (nextCost, nextPos))

        # LEFT
        checkLeft = checkMove(currentX, currentY, currentX - 1, currentY, gridSize, gridList)
        nextPos = str(currentX - 1) + "," + str(currentY)
        if (checkLeft and nextPos not in visitedListAStar):
            nextCost = calculateCostAStar(currentX, currentY, currentX - 1, currentY, gridList, targetPosition)
            visitedListAStar.append(nextPos)
            parentListAStar.append(currentPos)
            heapq.heappush(aStarPQ, (nextCost, nextPos))

        # RIGHT
        checkRight = checkMove(currentX, currentY, currentX + 1, currentY, gridSize, gridList)
        nextPos = str(currentX + 1) + "," + str(currentY)
        if (checkRight and nextPos not in visitedListAStar):
            nextCost = calculateCostAStar(currentX, currentY, currentX + 1, currentY, gridList, targetPosition)
            visitedListAStar.append(nextPos)
            parentListAStar.append(currentPos)
            heapq.heappush(aStarPQ, (nextCost, nextPos))

# ------------------------------ Part 2: Backtracking to find the path ---------------------------------- #
backTrackingListStar = []

currentBackTrackStar = targetPosition
backTrackingListStar.append(currentBackTrackStar)

# Using parentList as a dictionary
while(currentBackTrackStar != initialPositionStar):
    index = visitedListAStar.index(currentBackTrackStar)

    # Go to parentList[index] to find the parent of visitedList[index]
    currentBackTrackStar = parentListAStar[index]
    backTrackingListStar.append(currentBackTrackStar)

totalPathLengthStar = len(backTrackingListStar)
totalPathCostStar = 0

# Calculating the total cost of the path
for i in range(0,totalPathLengthStar-1):
    current = backTrackingListStar[i]
    next = backTrackingListStar[i+1]
    currentX = int(current.split(",")[0])
    currentY = int(current.split(",")[1])
    newX = int(next.split(",")[0])
    newY = int(next.split(",")[1])

    nextCost = calculateCost(currentX, currentY, newX, newY, gridList)
    totalPathCostStar = totalPathCostStar + nextCost


# Reversing the backTracking Array because it starts with target position
reversedListStar = backTrackingListStar[::-1]

# ------------------------------------------- Part 2: Results ------------------------------------------- #
print("Results of A-Star Search Algorithm")
print("The total number of nodes expanded: ", aStarTotal)
print("The total number of nodes found: ", len(visitedListAStar))
print("The cost of the path: ", totalPathCostStar)
print("The length of the path: ", totalPathLengthStar)
print("The path found: ", reversedListStar)
print("-------------------------------------------------------------------------------------------------")
