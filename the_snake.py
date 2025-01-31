from random import randint

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GS = GRID_SIZE
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)
SN_COLOR = SNAKE_COLOR

# Скорость движения змейки:
SPEED = 10

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """Базовый класс игровых объектов"""

    def __init__(self, position=(0, 0), body_color=(255, 255, 255)):
        self.body_color = body_color
        self.position = position

    def draw(self):
        """Отрисовка"""
        pass

    def get_position(self):
        """Геттер для координат объекта"""
        return self.position


class Snake(GameObject):
    """Класс змейка"""

    def __init__(self, position=None, body_color=None):
        if position is None and body_color is None:
            super().__init__((SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), SN_COLOR)
        else:
            super().__init__(position, body_color)
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None
        self.last = self.positions[-1]

    def update_direction(self):
        """Обновление направления движения"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def draw(self):
        """Отрисовка"""
        for position in self.positions[:-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        """Получение позиции головы змейки"""
        return self.positions[0]

    def reset(self):
        """Сброс змейки в начальное состояние"""
        self.__init__()

    def move(self):
        """Передвижение"""
        # HEAD
        # Up DOWN
        if self.direction == UP:
            if self.get_head_position()[1] - GS >= 0:
                newpos = (self.positions[0][0], self.positions[0][1] - GS)
                self.positions.insert(0, newpos)
            else:
                self.positions.insert(0, (self.positions[0][0], SCREEN_HEIGHT))
        elif self.direction == DOWN:
            if self.get_head_position()[1] + GS < SCREEN_HEIGHT:
                newpos = (self.positions[0][0], self.positions[0][1] + GS)
                self.positions.insert(0, newpos)
            else:
                self.positions.insert(0, (self.positions[0][0], 0))

        # Left Right
        if self.direction == LEFT:
            if self.get_head_position()[0] - GS >= 0:
                newpos = (self.positions[0][0] - GS, self.positions[0][1])
                self.positions.insert(0, newpos)
            else:
                self.positions.insert(0, (SCREEN_WIDTH, self.positions[0][1]))
        elif self.direction == RIGHT:
            if self.get_head_position()[0] + GS < SCREEN_WIDTH:
                newpos = (self.positions[0][0] + GS, self.positions[0][1])
                self.positions.insert(0, newpos)
            else:
                self.positions.insert(0, (0, self.positions[0][1]))

        # Teil
        if len(self.positions) - 1 == self.length:
            self.last = self.positions[-1]
            self.positions.pop()


class Apple(GameObject):
    """Класс яблоко"""

    def __init__(self, position=None, body_color=None):
        if position is None and body_color is None:
            super().__init__(self.randomize_position(), APPLE_COLOR)
        else:
            super().__init__(position, body_color)

    def randomize_position(self):
        """Рандомная позиция"""
        pos1 = randint(0, GRID_WIDTH - 1) * GRID_SIZE
        pos2 = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        return pos1, pos2

    def draw(self):
        """Отрисовка"""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def move(self):
        """Перемещение яблока на новое место"""
        self.position = self.randomize_position()


def handle_keys(game_object):
    """Функция обработки действий пользователя"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Главная функция игры"""
    # Инициализация PyGame:
    pygame.init()

    snake = Snake()
    apple = Apple()

    while True:
        handle_keys(snake)
        snake.update_direction()
        snake.move()

        # Коллизия
        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()
        if apple.get_position() == snake.get_head_position():
            snake.length += 1
            while apple.get_position() == snake.get_head_position():
                apple.move()

        snake.draw()
        apple.draw()

        pygame.display.update()
        clock.tick(SPEED)


if __name__ == '__main__':
    main()
