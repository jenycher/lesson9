import pygame
import random

pygame.init()

# Размеры окна и блоков
WIDTH, HEIGHT = 600, 600  # Увеличено по ширине для отображения информации
GAME_WIDTH = 300
BLOCK_SIZE = 30
COLUMNS = GAME_WIDTH // BLOCK_SIZE
ROWS = HEIGHT // BLOCK_SIZE

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (169, 169, 169)
COLORS = [
    (0, 255, 255),
    (0, 0, 255),
    (255, 165, 0),
    (255, 255, 0),
    (0, 255, 0),
    (128, 0, 128),
    (255, 0, 0)
]

# Фигуры Тетриса
SHAPES = [
    [[1, 1, 1, 1]],
    [[1, 1], [1, 1]],
    [[0, 1, 0], [1, 1, 1]],
    [[1, 1, 0], [0, 1, 1]],
    [[0, 1, 1], [1, 1, 0]],
    [[1, 1, 1], [0, 0, 1]],
    [[1, 1, 1], [1, 0, 0]]
]


class Tetris:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Tetris')
        self.clock = pygame.time.Clock()
        self.board = [[0 for _ in range(COLUMNS)] for _ in range(ROWS)]
        self.current_shape = self.new_shape()
        self.next_shape = self.new_shape()
        self.score = 0
        self.paused = False
        self.game_over_flag = False
        self.speed = 500  # начальная скорость падения фигуры (в миллисекундах)
        self.last_fall_time = pygame.time.get_ticks()

    def new_shape(self):
        return {
            'shape': random.choice(SHAPES),
            'color': random.choice(COLORS),
            'x': COLUMNS // 2 - 2,
            'y': 0
        }

    def rotate_shape(self, shape):
        return [list(row) for row in zip(*shape[::-1])]

    def valid_move(self, shape, offset_x, offset_y):
        for y, row in enumerate(shape['shape']):
            for x, cell in enumerate(row):
                if cell:
                    new_x = shape['x'] + x + offset_x
                    new_y = shape['y'] + y + offset_y
                    if new_x < 0 or new_x >= COLUMNS or new_y >= ROWS or new_y < 0 or self.board[new_y][new_x]:
                        return False
        return True

    def place_shape(self, shape):
        for y, row in enumerate(shape['shape']):
            for x, cell in enumerate(row):
                if cell:
                    self.board[shape['y'] + y][shape['x'] + x] = shape['color']
        self.clear_lines()
        self.current_shape = self.next_shape
        self.next_shape = self.new_shape()
        if not self.valid_move(self.current_shape, 0, 0):
            self.game_over()

    def clear_lines(self):
        lines_cleared = 0
        for y in range(ROWS):
            if all(self.board[y]):
                del self.board[y]
                self.board.insert(0, [0 for _ in range(COLUMNS)])
                lines_cleared += 1
        self.score += lines_cleared * 10

    def game_over(self):
        self.game_over_flag = True

    def draw_board(self):
        self.screen.fill(BLACK)
        # Отображение игровой доски
        for y, row in enumerate(self.board):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(self.screen, cell, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

        # Отображение текущей фигуры
        for y, row in enumerate(self.current_shape['shape']):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(self.screen, self.current_shape['color'], (
                        (self.current_shape['x'] + x) * BLOCK_SIZE,
                        (self.current_shape['y'] + y) * BLOCK_SIZE,
                        BLOCK_SIZE, BLOCK_SIZE))

        # Отображение сетки
        self.draw_grid()

        # Отображение информации
        self.draw_info()

        if self.game_over_flag:
            self.draw_game_over()

        pygame.display.flip()

    def draw_grid(self):
        for x in range(COLUMNS+1):
            pygame.draw.line(self.screen, GRAY, (x * BLOCK_SIZE, 0), (x * BLOCK_SIZE, HEIGHT))
        for y in range(ROWS):
            pygame.draw.line(self.screen, GRAY, (0, y * BLOCK_SIZE), (GAME_WIDTH, y * BLOCK_SIZE))

    def draw_info(self):
        font = pygame.font.SysFont('Arial', 20)
        score_text = font.render(f'Баллы: {self.score}', True, WHITE)
        pause_text = font.render('Пауза: Пробел', True, WHITE)
        exit_text = font.render('Выход: Esc', True, WHITE)

        self.screen.blit(score_text, (GAME_WIDTH + 100, 20))
        self.screen.blit(pause_text, (GAME_WIDTH + 100, 60))
        self.screen.blit(exit_text, (GAME_WIDTH + 100, 100))

        if self.paused:
            pause_label = font.render('Пауза', True, GRAY)
            self.screen.blit(pause_label, (GAME_WIDTH // 2 - 30, HEIGHT // 2 - 20))

    def draw_game_over(self):
        font = pygame.font.SysFont('Arial', 30)
        game_over_text = font.render(f'Игра окончена! Ваш балл: {self.score}', True, WHITE)
        restart_text = font.render('Нажмите Esc для начала игры сначала', True, WHITE)

        self.screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 50))
        self.screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2))

    def run(self):
        # Начальное сообщение
        self.screen.fill(BLACK)
        font = pygame.font.SysFont('Arial', 30)
        start_text = font.render('Игра Тетрис', True, WHITE)
        continue_text = font.render('Нажмите любую клавишу для продолжения', True, WHITE)
        self.screen.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, HEIGHT // 2 - 50))
        self.screen.blit(continue_text, (WIDTH // 2 - continue_text.get_width() // 2, HEIGHT // 2))
        pygame.display.flip()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    waiting = False

        while True:
            self.clock.tick(30)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        if self.game_over_flag:
                            self.reset_game()
                        else:
                            pygame.quit()
                            exit()
                    if event.key == pygame.K_SPACE and not self.game_over_flag:
                        self.paused = not self.paused
                    if not self.paused and not self.game_over_flag:
                        if event.key == pygame.K_LEFT and self.valid_move(self.current_shape, -1, 0):
                            self.current_shape['x'] -= 1
                        if event.key == pygame.K_RIGHT and self.valid_move(self.current_shape, 1, 0):
                            self.current_shape['x'] += 1
                        if event.key == pygame.K_DOWN and self.valid_move(self.current_shape, 0, 1):
                            self.current_shape['y'] += 1
                        if event.key == pygame.K_UP:
                            rotated_shape = self.rotate_shape(self.current_shape['shape'])
                            if self.valid_move({'shape': rotated_shape, 'x': self.current_shape['x'],
                                                'y': self.current_shape['y']}, 0, 0):
                                self.current_shape['shape'] = rotated_shape

            if not self.paused and not self.game_over_flag:
                current_time = pygame.time.get_ticks()
                if current_time - self.last_fall_time > self.speed:
                    if self.valid_move(self.current_shape, 0, 1):
                        self.current_shape['y'] += 1
                    else:
                        self.place_shape(self.current_shape)
                    self.last_fall_time = current_time

            self.draw_board()

    def reset_game(self):
        self.board = [[0 for _ in range(COLUMNS)] for _ in range(ROWS)]
        self.current_shape = self.new_shape()
        self.next_shape = self.new_shape()
        self.score = 0
        self.paused = False
        self.game_over_flag = False
        self.speed = 500
        self.last_fall_time = pygame.time.get_ticks()


if __name__ == "__main__":
    game = Tetris()
    game.run()