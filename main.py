
import pygame
import random
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (192, 192, 192)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
CELL_SIZE = 30
MARGIN = 2
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

# I declared all constants(global variables to avoid hardcoding)
BEGINNER_MINES = 10
AMATEUR_MINES = 40
PROFESSIONAL_MINES = 99

class Minesweeper:
    """
    Minesweeper game class

    Attributes:
        width (int): Width of the board
        height (int): Height of the board
        num_mines (int): Number of mines on the board
        board (list): 2D list of strings representing the board
        mines (set): Set of tuples representing the coordinates of the mines
        game_over (bool): Whether the game is over
    """
    def __init__(self, width, height, num_mines):
        """
        Constructor for the Minesweeper class
        """
        self.width = width
        self.height = height
        self.num_mines = num_mines
        self.board = [[' ' for _ in range(self.width)] for _ in range(self.
                                                                      height)]
        self.mines = set()
        self.game_over = False

    def place_mines(self, first_move):
        """
        Place mines on the board
        """
        available_cells = [(x, y) for x in range(self.width) for y in range
        (self.height)]
        available_cells.remove(first_move)

        for _ in range(self.num_mines):
            """
            Randomly choose a cell from the available cells and add it to the
            mines set"""
            mine = random.choice(available_cells)
            self.mines.add(mine)
            available_cells.remove(mine)

    def count_adjacent_mines(self, x, y):
        """
        Count the number of mines adjacent to the cell at (x, y)
       Attributes:
            x (int): x coordinate of the cell
            y (int): y coordinate of the cell
        Returns:
            int: Number of mines adjacent to the cell at (x, y)
            >>> minesweeper = Minesweeper(3, 3, 0)
            >>> minesweeper.count_adjacent_mines(1, 1)
            0

        """
        count = 0
        for dx in [-1, 0, 1]:
            """
            Check all 8 adjacent cells for mines
            """
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.width and 0 <= ny < self.height and (nx, ny) \
                        in self.mines:
                    count += 1
        return count

    def expand_empty_cells(self, x, y):
        """
        Expand all adjacent empty cells

       Attributes:
            x (int): x coordinate of the cell
            y (int): y coordinate of the cell
    Returns:
            None

        """
        stack = [(x, y)]
        while stack:
            cx, cy = stack.pop()
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    nx, ny = cx + dx, cy + dy
                    if 0 <= nx < self.width and 0 <= ny < self.height and \
                            self.board[ny][nx] == ' ':
                        self.board[ny][nx] = str(self.count_adjacent_mines
                                                 (nx, ny))
                        if self.board[ny][nx] == '0':
                            stack.append((nx, ny))

    def make_move(self, x, y):
        """
        Make a move on the board

       Attributes:
            x (int): x coordinate of the cell
            y (int): y coordinate of the cell

        Returns:
            None

        """
        if self.game_over:
            print("Game over. Start a new game.Close the window and run the "
                  "program again.")
            return

        if (x, y) in self.mines:
            self.game_over = True
            self.board[y][x] = '*'
            self.print_board()
            print("You lose! Stepped on a mine.")
            return

        if self.board[y][x] != ' ':
            return

        self.board[y][x] = str(self.count_adjacent_mines(x, y))
        if self.board[y][x] == '0':
            self.expand_empty_cells(x, y)

        if self.check_win():
            print("HOORAH! You won!")
            self.game_over = True

    def check_win(self):
        """
        Check if the player has won the game
        Attributes: None
        Returns:
            bool: True if the player has won, False otherwise

        """
        for y in range(self.height):
            for x in range(self.width):
                if self.board[y][x] == ' ' and (x, y) not in self.mines:
                    return False
        return True

    def print_board(self):
        for row in self.board:
            print(' '.join(row))

    def draw_board(self, surface):
        surface.fill(WHITE)
        for y in range(self.height):
            for x in range(self.width):
                rect = pygame.Rect(
                    x * CELL_SIZE + MARGIN,
                    y * CELL_SIZE + MARGIN,
                    CELL_SIZE - 2 * MARGIN,
                    CELL_SIZE - 2 * MARGIN
                )
                pygame.draw.rect(surface, GRAY, rect)
                pygame.draw.rect(surface, BLACK, rect, 1)

                if self.board[y][x].isdigit():
                    font = pygame.font.Font(None, 24)
                    text = font.render(self.board[y][x], True, BLUE)
                    text_rect = text.get_rect(center=rect.center)
                    surface.blit(text, text_rect)
                elif self.board[y][x] == '*':
                    pygame.draw.circle(surface, RED, rect.center, CELL_SIZE
                                       // 4)

    def handle_mouse_click(self, x, y):
        """
        Handle mouse click events
            Attributes:
            x (int): x coordinate of the mouse click
            y (int): y coordinate of the mouse click
        Returns:
            None

        """
        if self.game_over:
            print("Game over. Start a new game.")
            return

        cell_x = x // CELL_SIZE
        cell_y = y // CELL_SIZE
        self.make_move(cell_x, cell_y)


def play_game(width, height, num_mines):
    """"
    Play a game of minesweeper
    Attributes:
        width (int): Width of the board
        height (int): Height of the board
        num_mines (int): Number of mines on the board
    Returns:
        None

        """
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Minesweeper")

    game = Minesweeper(width, height, num_mines)

    first_move = (random.randint(1, game.width - 2), random.randint(1,
                                                            game.height - 2))
    game.place_mines(first_move)

    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    game.handle_mouse_click(*event.pos)

        game.draw_board(screen)
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()


def choose_difficulty():
    """
    Choose difficulty level
    Returns:
        None

    """
    print("Choose difficulty level:")
    print("1. Beginner (9x9 field with 10 mines)")
    print("2. Amateur (16x16 field with 40 mines)")
    print("3. Professional (16x30 field with 99 mines)")
    print("4. Special (custom field size and number of mines)")

    choice = input("Enter your choice (1-4): ")
    if choice == '1':
        play_game(9, 9, 10)
    elif choice == '2':
        play_game(16, 16, 40)
    elif choice == '3':
        play_game(16, 30, 99)
    elif choice == '4':
        width = int(input("Enter the width of the field: "))
        height = int(input("Enter the height of the field: "))
        num_mines = int(input("Enter the number of mines: "))
        play_game(width, height, num_mines)
    else:
        print("Invalid choice. Please try again.")

choose_difficulty()



