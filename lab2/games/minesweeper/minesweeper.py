import random
import datetime

class MineSweeper:

    # static
    __COVERED_ZERO = -10
    __FLAG_MOD = 10
    __OPEN = -1
    __FLAG = -2
    __MINE = 9
    
    @classmethod
    def FLAG_MOD(cls) -> int:
        """Getter for the flag mod

        Returns:
            int: value of the flag mod
        """
        return cls.__FLAG_MOD


    @classmethod
    def OPEN(cls) -> int: 
        """Returns the value of a open space

        Returns:
            int: constant
        """
        return cls.__OPEN


    @classmethod
    def FLAG(cls) -> int:
        """Constant representing a flag

        Returns:
            int: value of constant representing a flag
        """
        return cls.__FLAG


    @classmethod
    def MINE(cls) -> int:
        """
        Returns:
            int: value of constant representing a mine
        """
        return cls.__MINE


    def getCols(self) -> int:
        """getter for the number of columns

        Returns:
            int: number of columns in __board
        """
        return len(self.__board[0])

    def getRows(self) -> int:
        """getter for the number of rows

        Returns:
            int: number of rows in __board
        """
        return len(self.__board)

    def getGameOver(self) -> int:
        """getter for the game over status

        Returns:
            int: non zero if game is over
        """
        return self.__gameOver
    
    def getScore(self) -> int:
        """getter for the score

        Returns:
            int: current score
        """
        return self.__score
    
    def time(self) -> int:
        """getter for the time

        Returns:
            int: time since game started
        """
        if self.__startTime <= 0:
            return abs(self.__startTime)
        
        return (datetime.datetime.now().timestamp() - self.__startTime)
    
    def getName(self) -> str:
        print("NAME NOT IMPLMENTED")
        pass

    def setName(self, name: str) -> None:
        print("NAME SET NOT IMPLMENTED")
        pass
    

    def __init__(self, rows: int, cols: int):
        """Create a populating MineSweeper board

        Args:
            rows (int): number of rows in the game
            cols (int): number of columns in the game
        """

        self.__gameOver: int = 0 # 1 = win, -1 = lose, 0 = keep going
        self.__score: int = 0
        self.__name: str = None
        self.__PERCENT_CHANCE_MINE: int = 20
        self.__numMines: int = 0 
        self.__startTime: int = 0
        self.__board: list[list[int]] = []
 
        emptyRow = [0 for i in range(cols)]
        for i in range(rows):
            self.__board.append(emptyRow.copy())

        self.__resetBoard()

    def __resetBoard(self):
        """Reset the board to a new game state
        """
        print(f"FLAG MOD: {MineSweeper.FLAG_MOD()}, OPEN: {MineSweeper.OPEN()}, FLAG: {MineSweeper.FLAG()}, MINE: {MineSweeper.MINE()}")

        #print(self.__board)
        self.__score = self.getRows() * self.getCols()
        # reset board to all zeros
        for row in range(self.getRows()):
            for col in range(self.getCols()):
                self.__board[row][col] = 0
        
        # place mines and calculate board spaces
        for row in range(self.getRows()):
            for col in range(self.getCols()):
                isMine = random.randint(0, 100) < self.__PERCENT_CHANCE_MINE
                if isMine:
                    print(f"Mine at {row}, {col}")
                    # is a mine 
                    self.__board[row][col] = -MineSweeper.MINE()
                    self.__numMines += 1
                    # decrement surrounding spaces
                    for r in range(row - 1, row + 2):
                        for c in range(col - 1, col + 2):
                            if r >= 0 and r < self.getRows() and c >= 0 and c < self.getCols():
                                if (self.__board[r][c] != -MineSweeper.MINE()):
                                    self.__board[r][c] -= 1
                            
        # set zeros to covered values
        for row in range(self.getRows()):
            for col in range(self.getCols()):
                if self.__board[row][col] == 0:
                    self.__board[row][col] = self.__COVERED_ZERO
        
        for row in self.__board:
            print(row)
        #print(self.__board)
    
    def pickSpace(self, row, col, toggleFlag = False) -> bool:
        """Picks a space and enforces rules of MineSweeper

        Args:
            row (_type_): row to select (start at zero)
            col (_type_): column to select (start at zero)
            toggleFlag (bool, optional): true to toggle flag placement. Defaults to False.

        Returns:
            bool: true if the move was valid, false otherwise 
        """
        print(f"Picking space {row}, {col}")
        if self.__gameOver:
            print("---Minesweeper.py - Pick space Game Over")
            return False
        
        if row < 0 or row >= self.getRows() or col < 0 or col >= self.getCols():
            print("---Minesweeper.py - pick space out of bounds")            
            return False
        
        # already picked
        if self.__board[row][col] >= 0:
            print("---Minesweeper.py - Pick space already picked")
            return False
        
        # toggle flag
        if toggleFlag:
            mod = -MineSweeper.FLAG_MOD()
            if self.__board[row][col] < 0:
                mod *= -1
            self.__board[row][col] += mod
            return True
        
        # flagged spaces cannot be picked (still handled on server)
        if self.__board[row][col] < -MineSweeper.FLAG_MOD():
            print("---Minesweeper.py - Pick space flagged")
            return False
        
        self.__uncoverSpace(row, col)
        self.__score -= 1
        if self.__board[row][col] == 0:
            # hit a zero uncover the spaces around it
            for r in range(row - 1, row + 2):
                for c in range(col - 1, col + 2):
                    self.pickSpace(r, c)

        elif self.__board[row][col] == MineSweeper.MINE():
            self.__gameOver = -1
            self.__startTime = -1*self.time()
        
        # winning!
        if self.__score == self.__numMines:
            self.__gameOver = 1
            self.__startTime = -1*self.time()
        return True 
    
    def __uncoverSpace(self, row, col):
        if self.__board[row][col] >= 0:
            return self.__board[row][col]
        
        # remove the flag
        if self.__board[row][col] < -MineSweeper.FLAG_MOD():
            self.__board[row][col] += MineSweeper.FLAG_MOD()
        
        # uncover the space
        if self.__board[row][col] < 0:
            self.__board[row][col] *= -1
        
        # set the zero properly
        if self.__board[row][col] == -MineSweeper.__COVERED_ZERO:
            self.__board[row][col] = 0
        
        return self.__board[row][col]

    def getSpace(self, row: int, col: int) -> int:
        """Get the status of a space

        Args:
            row (int): the row to query (starting at zero)
            col (int): the column to query (starting at zero)

        Returns:
            int: value at (row,col) if uncovered, OPEN if covered or invalid
        """
        # print constants for debugging
        print(f"Row {row}, Col {col} value: {self.__board[row][col]}")
        if (row < 0 or row >= self.getRows() or col < 0 or col >= self.getCols()):
            return MineSweeper.OPEN()

        if (self.__gameOver):
            print(f"=======Game Over at {row}, {col}")
            self.__uncoverSpace(row, col)
            return self.__board[row][col]

        if (self.__board[row][col] < -MineSweeper.FLAG_MOD()):
            print(f"=======Flagged space at {row}, {col}")
            return MineSweeper.FLAG()
        
        if (self.__board[row][col] < 0):
            return MineSweeper.OPEN()
        
        return self.__board[row][col]
    
    def startGame(self) -> None:
        """Starts the clock for the game
        """
        self.__startTime = datetime.datetime.now().timestamp()


                

if __name__ == "__main__":
    game = MineSweeper(5, 5)
