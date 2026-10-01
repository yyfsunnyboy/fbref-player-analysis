import pygame
import random

# 初始化 Pygame
pygame.init()

# 定義顏色 (復古風格)
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)

# 設定遊戲視窗尺寸
width = 800
height = 600
dis = pygame.display.set_mode((width, height))
pygame.display.set_caption('Gemini 製作的復古貪食蛇')

# 設定遊戲時鐘
clock = pygame.time.Clock()
snake_block = 20
snake_speed = 15

# 設定字體 (像素風格)
font_style = pygame.font.SysFont("monospace", 35)
score_font = pygame.font.SysFont("monospace", 50)

def Your_score(score):
    value = font_style.render("Score: " + str(score), True, white)
    dis.blit(value, [10, 10])

def our_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(dis, white, [x[0], x[1], snake_block, snake_block])

def message(msg, color, y_displace=0):
    mesg = font_style.render(msg, True, color)
    # 將訊息置中
    msg_rect = mesg.get_rect(center=(width / 2, height / 2 + y_displace))
    dis.blit(mesg, msg_rect)

def gameLoop():
    game_over = False
    game_close = False

    # 蛇的初始位置
    x1 = width / 2
    y1 = height / 2

    # 蛇的移動
    x1_change = 0
    y1_change = 0

    # 蛇的身體和分數
    snake_List = []
    Length_of_snake = 1
    score = 0

    # 食物的位置
    foodx = round(random.randrange(0, width - snake_block) / 20.0) * 20.0
    foody = round(random.randrange(0, height - snake_block) / 20.0) * 20.0

    while not game_over:

        while game_close == True:
            dis.fill(black)
            # 結束畫面
            final_score_text = score_font.render("Your Score: " + str(score), True, red)
            score_rect = final_score_text.get_rect(center=(width / 2, height / 4))
            dis.blit(final_score_text, score_rect)
            
            message("按 C-重新開始 或 Q-離開", white, 100)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()
                if event.type == pygame.QUIT:
                    game_over = True
                    game_close = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = snake_block
                    x1_change = 0

        if x1 >= width or x1 < 0 or y1 >= height or y1 < 0:
            game_close = True
        x1 += x1_change
        y1 += y1_change
        dis.fill(black) # 黑色背景
        pygame.draw.rect(dis, red, [foodx, foody, snake_block, snake_block]) # 紅色食物
        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True

        our_snake(snake_block, snake_List)
        Your_score(score)

        pygame.display.update()

        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, width - snake_block) / 20.0) * 20.0
            foody = round(random.randrange(0, height - snake_block) / 20.0) * 20.0
            Length_of_snake += 1
            score += 10

        clock.tick(snake_speed)

    pygame.quit()
    quit()

gameLoop()