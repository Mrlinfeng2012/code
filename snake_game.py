import pygame
import random
import sys

# 初始化pygame
pygame.init()

# 游戏常量
WIDTH, HEIGHT = 600, 600
GRID_SIZE = 20
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE
FPS = 10

# 颜色定义
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# 方向
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# 初始化屏幕
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("贪吃蛇游戏")
clock = pygame.time.Clock()

class Snake:
    def __init__(self):
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = RIGHT
        self.next_direction = RIGHT
        self.grow = False
        
    def get_head_position(self):
        return self.positions[0]
    
    def update(self):
        # 更新方向
        self.direction = self.next_direction
        
        # 获取头部位置
        head = self.get_head_position()
        
        # 计算新的头部位置
        new_x = (head[0] + self.direction[0]) % GRID_WIDTH
        new_y = (head[1] + self.direction[1]) % GRID_HEIGHT
        new_head = (new_x, new_y)
        
        # 检查是否撞到自己
        if new_head in self.positions[1:]:
            return False  # 游戏结束
        
        # 添加新的头部
        self.positions.insert(0, new_head)
        
        # 如果不需要增长，则移除尾部
        if not self.grow:
            self.positions.pop()
        else:
            self.grow = False
            
        return True  # 游戏继续
    
    def change_direction(self, direction):
        # 防止直接反向移动
        if (direction[0] * -1, direction[1] * -1) != self.direction:
            self.next_direction = direction
    
    def grow_snake(self):
        self.grow = True
    
    def draw(self, surface):
        for i, p in enumerate(self.positions):
            color = GREEN if i == 0 else BLUE  # 头部绿色，身体蓝色
            rect = pygame.Rect((p[0] * GRID_SIZE, p[1] * GRID_SIZE), (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, color, rect)
            pygame.draw.rect(surface, BLACK, rect, 1)  # 边框

class Food:
    def __init__(self, snake_positions):
        self.position = self.randomize_position(snake_positions)
        
    def randomize_position(self, snake_positions):
        while True:
            position = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
            if position not in snake_positions:
                return position
    
    def draw(self, surface):
        rect = pygame.Rect((self.position[0] * GRID_SIZE, self.position[1] * GRID_SIZE), (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, RED, rect)
        pygame.draw.rect(surface, BLACK, rect, 1)  # 边框

def draw_grid(surface):
    for y in range(0, HEIGHT, GRID_SIZE):
        for x in range(0, WIDTH, GRID_SIZE):
            rect = pygame.Rect((x, y), (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, BLACK, rect, 1)

def main():
    snake = Snake()
    food = Food(snake.positions)
    score = 0
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    snake.change_direction(UP)
                elif event.key == pygame.K_DOWN:
                    snake.change_direction(DOWN)
                elif event.key == pygame.K_LEFT:
                    snake.change_direction(LEFT)
                elif event.key == pygame.K_RIGHT:
                    snake.change_direction(RIGHT)
        
        # 更新蛇的位置
        if not snake.update():
            # 游戏结束
            font = pygame.font.SysFont('Arial', 36)
            game_over_text = font.render(f'游戏结束! 得分: {score}', True, WHITE)
            screen.blit(game_over_text, (WIDTH // 2 - 150, HEIGHT // 2 - 18))
            pygame.display.update()
            pygame.time.wait(2000)
            return
        
        # 检查是否吃到食物
        if snake.get_head_position() == food.position:
            snake.grow_snake()
            food = Food(snake.positions)
            score += 1
        
        # 绘制
        screen.fill(BLACK)
        draw_grid(screen)
        snake.draw(screen)
        food.draw(screen)
        
        # 显示分数
        font = pygame.font.SysFont('Arial', 24)
        score_text = font.render(f'得分: {score}', True, WHITE)
        screen.blit(score_text, (5, 5))
        
        pygame.display.update()
        clock.tick(FPS)

if __name__ == "__main__":
    while True:
        main()
        
        # 显示重新开始提示
        screen.fill(BLACK)
        font = pygame.font.SysFont('Arial', 36)
        restart_text = font.render('按任意键重新开始', True, WHITE)
        screen.blit(restart_text, (WIDTH // 2 - 150, HEIGHT // 2 - 18))
        pygame.display.update()
        
        # 等待用户按键
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    waiting = False