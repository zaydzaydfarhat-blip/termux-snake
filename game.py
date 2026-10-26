
import curses
import random

def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(False)
    stdscr.keypad(True)
    curses.use_default_colors()

    height, width = stdscr.getmaxyx()
    if height < 10 or width < 20:
        stdscr.addstr(0, 0, "Make your terminal bigger!")
        stdscr.getch()
        return

    snake = [(height // 2, width // 2)]
    direction = (0, 1)
    food = (height // 2, width // 2 + 5)
    score = 0

    stdscr.timeout(120)

    while True:
        stdscr.erase()
        stdscr.border()

        stdscr.addstr(0, 2, f" SNAKE | Score: {score} ")
        for y, x in snake:
            stdscr.addch(y, x, "O")
        stdscr.addch(food[0], food[1], "*")
        stdscr.addstr(height - 1, 2, "Arrows/WASD move | Q quits")
        stdscr.refresh()

        key = stdscr.getch()
        directions = {
            curses.KEY_UP: (-1, 0), ord("w"): (-1, 0),
            curses.KEY_DOWN: (1, 0), ord("s"): (1, 0),
            curses.KEY_LEFT: (0, -1), ord("a"): (0, -1),
            curses.KEY_RIGHT: (0, 1), ord("d"): (0, 1),
        }

        if key in (ord("q"), ord("Q")):
            break

        new_direction = directions.get(key)
        if new_direction and new_direction != (-direction[0], -direction[1]):
            direction = new_direction

        y = snake[0][0] + direction[0]
        x = snake[0][1] + direction[1]
        head = (y, x)

        if y <= 0 or y >= height - 1 or x <= 0 or x >= width - 1:
            break

        eating = head == food
        body = snake if eating else snake[:-1]
        if head in body:
            break

        snake.insert(0, head)

        if eating:
            score += 1
            while True:
                food = (
                    random.randint(1, height - 2),
                    random.randint(1, width - 2)
                )
                if food not in snake:
                    break
        else:
            snake.pop()

    stdscr.nodelay(False)
    stdscr.addstr(height // 2, 2, f"Game Over! Score: {score}")
    stdscr.addstr(height // 2 + 1, 2, "Press any key to exit.")
    stdscr.getch()

curses.wrapper(main)
