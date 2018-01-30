item00 = "-"
item01 = "-"
item02 = "-"
item10 = "-"
item11 = "-"
item12 = "-"
item20 = "-"
item21 = "-"
item22 = "-"
piece = "X"

def main():
    global piece
    while True:
        #draw the board
        #ask the user for a location
        #draw the piece at the location
        #check for winner
        #switch the piece
        drawBoard()
        location = input("Please enter a location: ")
        row = location[0]
        col = location[2]
        makeMove(row, col, piece)
        checkWinner()
        if checkWinner() == True:
            break
        if piece == "X":
            piece = "O"
        else:
            piece = "X"

def drawBoard():
    global item00
    global item01
    global item02
    global item10
    global item11
    global item12
    global item20
    global item21
    global item22
    global piece

    print(item00, item01, item02)
    print("")
    print(item10, item11, item12)
    print("")
    print(item20, item21, item22)

def makeMove(row, col, str):
    global item00
    global item01
    global item02
    global item10
    global item11
    global item12
    global item20
    global item21
    global item22
    global piece

    if row == "0" and col == "0":
        item00 = piece
    if row == "0" and col== "1":
        item01 = piece
    if row == "0" and col == "2":
        item02 = piece
    if row == "1" and col == "0":
        item10 = piece
    if row == "1" and col == "1":
        item11 = piece
    if row == "1" and col == "2":
        item12 = piece
    if row == "2" and col == "0":
        item20 = piece
    if row == "2" and col == "1":
        item21 = piece
    if row == "2" and col == "2":
        item22 = piece

def checkWinner():
    if item00 == "X" and item01 == "X" and item02== "X":
        drawBoard()
        print("Player X won the game!")
        return True
    if item00 == "O" and item01 == "O" and item02== "O":
        drawBoard()
        print("Player O won the game!")
        return True
    if item10 == "X" and item11 == "X" and item12== "X":
        drawBoard()
        print("Player X won the game!")
        return True
    if item10 == "O" and item11 == "O" and item12== "O":
        drawBoard()
        print("Player O won the game!")
        return True
    if item20 == "X" and item21 == "X" and item22== "X":
        drawBoard()
        print("Player X won the game!")
        return True
    if item20 == "O" and item21 == "O" and item22== "O":
        drawBoard()
        print("Player O won the game!")
        return True
    if item00 == "X" and item10 == "X" and item20== "X":
        drawBoard()
        print("Player X won the game!")
        return True
    if item00 == "O" and item10 == "O" and item20== "O":
        drawBoard()
        print("Player O won the game!")
        return True
    if item01 == "X" and item11 == "X" and item21== "X":
        drawBoard()
        print("Player X won the game!")
        return True
    if item01 == "O" and item11 == "O" and item21 == "O":
        drawBoard()
        print("Player O won the game!")
        return True
    if item02 == "X" and item12 == "X" and item22== "X":
        drawBoard()
        print("Player X won the game!")
        return True
    if item02 == "O" and item12 == "O" and item22== "O":
        drawBoard()
        print("Player O won the game!")
        return True
    if item00 == "X" and item11 == "X" and item22== "X":
        drawBoard()
        print("Player X won the game!")
        return True
    if item00 == "O" and item11 == "O" and item22== "O":
        drawBoard()
        print("Player O won the game!")
        return True
    if item02 == "X" and item11 == "X" and item20== "X":
        drawBoard()
        print("Player X won the game!")
        return True
    if item02 == "O" and item11 == "O" and item20== "O":
        drawBoard()
        print("Player O won the game!")
        return True
    else:
        return False

main()