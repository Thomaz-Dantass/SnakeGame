import sys
import pygame
import random

# Definir constantes para as direções da cobra
LEFT = (-1, 0)
RIGHT = (1, 0)
UP = (0, -1)
DOWN = (0, 1)

pygame.init()

# Definir as dimensões da janela do jogo
WINDOW_WIDTH = 500
WINDOW_HEIGHT = 500
BLOCK_SIZE = 10

# Criar a janela do jogo
surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Jogo da cobrinha')

class Snake:
    def __init__(self):
        self.snake_body = [(100, 100), (90, 100), (80, 100)]
        self.direction = RIGHT
    
    def move_snake(self):
        new_head = (self.snake_body[0][0] + self.direction[0] * BLOCK_SIZE,
                    self.snake_body[0][1] + self.direction[1] * BLOCK_SIZE)
        self.snake_body.insert(0, new_head)
        self.snake_body.pop()
    
    def is_collision(self):
        head = self.snake_body[0]
        return (head[0] in (0, WINDOW_WIDTH - BLOCK_SIZE) or
                head[1] in (0, WINDOW_HEIGHT - BLOCK_SIZE) or
                head in self.snake_body[1:])
    
    def hit_self(self):
        return any(self.snake_body.count(block) > 1 for block in self.snake_body)
    
    def get_head_position(self):
        return self.snake_body[0]


class Food:
    def __init__(self):
        self.position = (0, 0)
        self.spawn_food()
    
    def spawn_food(self, snake_body=None):
        if snake_body is None:
            snake_body = []
        while True:
            x = random.randrange(BLOCK_SIZE, WINDOW_WIDTH - BLOCK_SIZE, BLOCK_SIZE)
            y = random.randrange(BLOCK_SIZE, WINDOW_HEIGHT - BLOCK_SIZE, BLOCK_SIZE)
            if (x, y) not in snake_body:
                break
        self.position = (x, y)

def main():
    clock = pygame.time.Clock()
    score_font = pygame.font.SysFont('comicsansms', 30)
    
    # Criar a cobra e a maçã
    snake = Snake()
    food = Food()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and snake.direction != RIGHT:
                    snake.direction = LEFT
                elif event.key == pygame.K_RIGHT and snake.direction != LEFT:
                    snake.direction = RIGHT
                elif event.key == pygame.K_UP and snake.direction != DOWN:
                    snake.direction = UP
                elif event.key == pygame.K_DOWN and snake.direction != UP:
                    snake.direction = DOWN
        
        # Atualizar a posição da cobra e verificar colisões
        snake.move_snake()
        if snake.is_collision() or snake.hit_self():
            pygame.quit()
            sys.exit()
        
        # Verificar se a cobra comeu a maçã
        if snake.get_head_position() == food.position:
            snake.snake_body.append(food.position)
            food.spawn_food(snake.snake_body)
        
        # Desenhar a cobra e a maçã na tela
        surface.fill((0, 0, 0))
        for block in snake.snake_body:
            pygame.draw.rect(surface, (255, 255, 255), (block[0], block[1], BLOCK_SIZE, BLOCK_SIZE))
        pygame.draw.rect(surface, (255, 0, 0), (food.position[0], food.position[1], BLOCK_SIZE, BLOCK_SIZE))
        
        # Mostrar a pontuação na tela
        score_text = score_font.render('pontuação: {}'.format(len(snake.snake_body) - 3), True, (255, 255, 255))
        surface.blit(score_text, (WINDOW_WIDTH - score_text.get_width() - 10, 10))
        
        # Atualizar a tela
        pygame.display.update()
        
        # Definir a taxa de atualização do jogo
        clock.tick(10)

if __name__ == '__main__':
    main()