import curses
import random
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

        # snake starts in center, length 3
        center_x = width // 2
        center_y = height // 2
        self.snake = [(center_x, center_y), (center_x - 1, center_y), (center_x - 2, center_y)]

        # moving right initially
        self.direction = (1, 0)
        self.next_direction = (1, 0)

        self.game_over = False
        self.score = 0
        self.food = self._spawn_food()

    def grid(self) -> list[list[str]]:
        """
        Handles the display of the grid
        Should return a 2D list of characters
        """
        # make empty grid
        grid = [[' ' for _ in range(self.width)] for _ in range(self.height)]

        # walls
        for x in range(self.width):
            grid[0][x] = '#'
            grid[self.height - 1][x] = '#'
        for y in range(self.height):
            grid[y][0] = '#'
            grid[y][self.width - 1] = '#'

        # draw snake
        for i, (x, y) in enumerate(self.snake):
            if i == 0:
                grid[y][x] = 'O'
            else:
                grid[y][x] = 'o'

        # food
        if self.food:
            grid[self.food[1]][self.food[0]] = '*'

        return grid

    def set_direction(self, key_input: Optional[str]):
        """
        Set the direction.
        Assume input will either be w, a, s, d, or None
        """
        if key_input is None:
            return

        # map wasd to directions
        direction_map = {
            'w': (0, -1),
            's': (0, 1),
            'a': (-1, 0),
            'd': (1, 0)
        }

        if key_input in direction_map:
            new_dir = direction_map[key_input]
            # dont let snake reverse into itself
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

        self.direction = self.next_direction

        # move head
        head_x, head_y = self.snake[0]
        new_head = (head_x + self.direction[0], head_y + self.direction[1])

        # hit wall
        if (new_head[0] <= 0 or new_head[0] >= self.width - 1 or
            new_head[1] <= 0 or new_head[1] >= self.height - 1):
            self.game_over = True
            return False

        # hit self
        if new_head in self.snake:
            self.game_over = True
            return False

        self.snake.insert(0, new_head)

        # check if ate food
        if new_head == self.food:
            self.score += 1
            self.food = self._spawn_food()
        else:
            self.snake.pop()

        return True

    def _spawn_food(self) -> tuple[int, int]:
        """spawn food randomly"""
        while True:
            x = random.randint(1, self.width - 2)
            y = random.randint(1, self.height - 2)
            if (x, y) not in self.snake:
                return (x, y)


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
            stdscr.clear()
            stdscr.addstr(0, 0, f"game over - score: {game.score}")
            stdscr.addstr(1, 0, "press any key")
            stdscr.refresh()
            stdscr.nodelay(0)
            stdscr.getch()
            return

        stdscr.clear()

        # draw grid
        for y, row in enumerate(game.grid()):
            for x, char in enumerate(row):
                stdscr.addch(y, x, ord(str(char)))

        # show score
        stdscr.addstr(16, 0, f"score: {game.score} | wasd | length: {len(game.snake)}")

        stdscr.refresh()


if __name__ == "__main__":
    curses.wrapper(game_loop)
