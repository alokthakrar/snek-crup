import curses
from typing import Optional


class SnakeGame:
    def __init__(self, width: int, height: int):
        """
        Game should be initialized according to width
        and height. The game is played using wasd keys.

        The initial state should be:
        - Snake of length 3
        - Snake moving right
        - Snake in the center
        """
        self.width = width
        self.height = height

        # Initialize snake in center, length 3, moving right
        center_x = width // 2
        center_y = height // 2
        self.snake = [(center_x, center_y), (center_x - 1, center_y), (center_x - 2, center_y)]

        # Direction: (dx, dy) - initially moving right
        self.direction = (1, 0)
        self.next_direction = (1, 0)

        self.game_over = False

    def grid(self) -> list[list[str]]:
        """
        Handles the display of the grid
        Should return a 2D list of characters
        """
        # Create empty grid
        grid = [[' ' for _ in range(self.width)] for _ in range(self.height)]

        # Draw walls
        for x in range(self.width):
            grid[0][x] = '#'
            grid[self.height - 1][x] = '#'
        for y in range(self.height):
            grid[y][0] = '#'
            grid[y][self.width - 1] = '#'

        # Draw snake
        for i, (x, y) in enumerate(self.snake):
            if i == 0:
                grid[y][x] = 'O'  # Head
            else:
                grid[y][x] = 'o'  # Body

        return grid

    def set_direction(self, key_input: Optional[str]):
        """
        Set the direction.
        Assume input will either be w, a, s, d, or None
        """
        if key_input is None:
            return

        # Map keys to directions and prevent 180-degree turns
        direction_map = {
            'w': (0, -1),  # Up
            's': (0, 1),   # Down
            'a': (-1, 0),  # Left
            'd': (1, 0)    # Right
        }

        if key_input in direction_map:
            new_dir = direction_map[key_input]
            # Prevent moving in opposite direction
            if (new_dir[0] + self.direction[0] != 0 or
                new_dir[1] + self.direction[1] != 0):
                self.next_direction = new_dir

    def do_step(self) -> bool:
        """
        Performs a single step during 1 tick
        Return False if the game should end
        """
        if self.game_over:
            return False

        # Update direction
        self.direction = self.next_direction

        # Calculate new head position
        head_x, head_y = self.snake[0]
        new_head = (head_x + self.direction[0], head_y + self.direction[1])

        # Check wall collision
        if (new_head[0] <= 0 or new_head[0] >= self.width - 1 or
            new_head[1] <= 0 or new_head[1] >= self.height - 1):
            self.game_over = True
            return False

        # Check self collision
        if new_head in self.snake:
            self.game_over = True
            return False

        # Move snake (add new head, remove tail)
        self.snake.insert(0, new_head)
        self.snake.pop()

        return True


def game_loop(stdscr):
    """
    Main game loop that manages game setup and execution.
    """
    game = SnakeGame(25, 15)

    # Game setup
    curses.curs_set(0)
    stdscr.nodelay(1)
    stdscr.timeout(400)

    # Game loop
    while True:
        key = stdscr.getch()
        key = chr(key) if 0 <= key < 256 else None

        game.set_direction(key)
        if not game.do_step():
            print("Game over!")
            return

        stdscr.clear()

        # Draw grid
        for y, row in enumerate(game.grid()):
            for x, char in enumerate(row):
                stdscr.addch(y, x, ord(str(char)))

        # Refresh screen
        stdscr.refresh()


if __name__ == "__main__":
    curses.wrapper(game_loop)
