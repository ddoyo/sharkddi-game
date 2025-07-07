import random
from time import sleep

import pygame
from pygame.locals import*


BGWIDTH = 1000
BGHEIGHT = 650

BLACK = (0,0,0)
WHITHE = (255,255,255)
YELLOW = (250,250,50)
RED = (250,50,50)

FPS = 60


# 상어설정
class Sharkddi(pygame.sprite.Sprite):
    def __init__(self):
        super(Sharkddi, self).__init__()
        self.image = pygame.image.load('sharkddi.png')
        self.rect = self.image.get_rect()
        self.rect.x = int(BGWIDTH/2)
        self.rect.y = BGHEIGHT - self.rect.height
        self.dx = 0
        self.dy = 0

    def update(self):
        self.rect.x += self.dx
        self.rect.y += self.dy

        if self.rect.x < 0 or self.rect.x + self.rect.width > BGWIDTH:
            self.rect.x -= self.dx

        if self.rect.y < 0 or self.rect.y + self.rect.height > BGHEIGHT:
            self.rect.y -= self.dy

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def collide(self, sprites):
        for sprite in sprites:
            if pygame.sprite.collide_rect(self, sprite):
                return sprite

# 물방울 설정
class Space(pygame.sprite.Sprite):
    def __init__(self, xpos, ypos, speed):
        super(Space, self).__init__()
        self.image = pygame.image.load('space.png')
        self.rect = self.image.get_rect()
        self.rect.x = xpos
        self.rect.y = ypos
        self.speed = speed

    def update(self):
        self.rect.y -= self.speed
        if self.rect.y + self.rect.height < 0:
            self.kill()

    def collide(self, sprites):
        for sprite in sprites:
            if pygame.sprite.collide_rect(self, sprite):
                return sprite
            
# 물고기 설정
class Fish(pygame.sprite.Sprite):
    def __init__(self, xpos, ypos, speed):
        super(Fish, self).__init__()
        fish_images = ('fish1.png','fish2.png','fish3.png','fish4.png','fish5.png',
                       'fish6.png','fish7.png','fish8.png','fish9.png')
        self.image = pygame.image.load(random.choice(fish_images))
        self.rect = self.image.get_rect()
        self.rect.x = xpos
        self.rect.y = ypos
        self.speed = speed

    def update(self):
        self.rect.y += self.speed

    def out_of_screen(self):
        if self.rect.y > BGHEIGHT:
            return True

# 쓰레기 설정
class Trash(pygame.sprite.Sprite):
    def __init__(self, xpos, ypos, speed):
        super(Trash, self).__init__()
        trash_images = ('trash1.png','trash2.png','trash3.png','trash4.png',
                        'trash5.png','trash6.png','trash7.png','trash8.png')
        self.image = pygame.image.load(random.choice(trash_images))
        self.rect = self.image.get_rect()
        self.rect.x = xpos
        self.rect.y = ypos
        self.speed = speed

    def update(self):
        self.rect.y += self.speed

    def out_of_screen(self):
        if self.rect.y > BGHEIGHT:
            return True


# 글씨 설정
def draw_text(text, font, surface, x, y, main_color):
    text_obj = font.render(text, True, main_color)
    text_rect = text_obj.get_rect()
    text_rect.centerx = x
    text_rect.centery = y
    surface.blit(text_obj, text_rect)

# 닿았을 때 100점 이미지 설정
def occur_yummy(surface, x, y):
    yummy_image = pygame.image.load('100.png')
    yummy_rect = yummy_image.get_rect()
    yummy_rect.x = x
    yummy_rect.y = y
    surface.blit(yummy_image, yummy_rect)

# 닿았을 때 깨진 하트 이미지 설정
def occur_heart(surface, x, y):
    heart_image = pygame.image.load('heart.png')
    heart_rect = heart_image.get_rect()
    heart_rect.x = x
    heart_rect.y = y
    surface.blit(heart_image, heart_rect)

# 메인 게임 설정
def game_loop():
    default_font = pygame.font.Font('NanumGothic.ttf',28)
    font_100 = pygame.font.Font('BITBIT.ttf',100)
    font_80 = pygame.font.Font('BITBIT.ttf', 80)
    font_70 = pygame.font.Font('dangam.ttf',100)
    font_60 = pygame.font.Font('YY.ttf',60)
    font_40 = pygame.font.Font('YY.ttf',60)
    draw_x = int(BGWIDTH /2)
    draw_y = int(BGHEIGHT /4)
    background_image = pygame.image.load('background.png')

    fps_clock = pygame.time.Clock()

    sharkddi = Sharkddi()
    spaces = pygame.sprite.Group()
    fishes = pygame.sprite.Group()
    trashes = pygame.sprite.Group()

    occur_fprob = 200
    occur_tprob = 100
    clean_count = 0
    suv_count = 5

    done = False
    while not done:
        # 상어 키 조종
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    sharkddi.dx -= 10
                elif event.key == pygame.K_RIGHT:
                    sharkddi.dx += 10
                elif event.key == pygame.K_SPACE:
                    space = Space(sharkddi.rect.centerx, sharkddi.rect.y, 10)
                    spaces.add(space)


            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    sharkddi.dx = 0
                elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    sharkddi.dy = 0

        screen.blit(background_image, background_image.get_rect())

        # 물고기, 쓰레기의 속도와 빈도 설정
        occur_of_fishes = 1
        min_fish_speed = 1 + int(clean_count / 2000)
        max_fish_speed = 1 + int(clean_count / 1000)

        occur_of_trashes = 1
        min_trash_speed = 1 + int(clean_count / 2000)
        max_trash_speed = 1 + int(clean_count / 1000)
                

        if random.randint(1, occur_fprob) == 1:
            for i in range(occur_of_fishes):
                speed = random.randint(min_fish_speed, max_fish_speed)
                fish = Fish(random.randint(0, BGWIDTH - 30), 0, speed)
                fishes.add(fish)

        if random.randint(1, occur_tprob) == 1:
            for i in range(occur_of_trashes):
                speed = random.randint(min_trash_speed, max_trash_speed)
                trash = Trash(random.randint(0, BGWIDTH - 30), 0, speed)
                trashes.add(trash)

        # 화면 속 글씨 설정
        draw_text('점수: {}'.format(clean_count), default_font, screen, 100, 20, YELLOW)
        draw_text('목숨: {}'.format(suv_count), default_font, screen, 900, 20, RED)

        # 물방울 충돌 감지 설정
        for space in spaces:
            trash = space.collide(trashes)
            if trash:
                space.kill()
                trash.kill()
                occur_yummy(screen, trash.rect.x, trash.rect.y)
                clean_count += 100
                

        for space in spaces:
            fish = space.collide(fishes)
            if fish:
                fish.kill()
                occur_heart(screen, fish.rect.x, fish.rect.y)
                suv_count -= 1

        # 쓰레기가 화면 밖으로 나갔을 때의 설정
        for trash in trashes:
            if trash.out_of_screen():
                trash.kill()
                occur_heart(screen, sharkddi.rect.x, sharkddi.rect.y)
                suv_count -= 1
                
        fishes.update()
        fishes.draw(screen)
        trashes.update()
        trashes.draw(screen)
        spaces.update()
        spaces.draw(screen)
        sharkddi.update()
        sharkddi.draw(screen)
        pygame.display.flip()

        # 게임의 끝 설정
        if suv_count <= 0:
            occur_yummy(screen, sharkddi.rect.x, sharkddi.rect.y)
            pygame.display.update()
            sleep(1)
            done = True

            gameover_image = pygame.image.load('background.png')
            screen.blit(gameover_image, [0,0])

            draw_text('- GAME OVER -', font_100, screen, draw_x, draw_y,RED)
            draw_text('점수: {}'.format(clean_count), font_80, screen, draw_x, draw_y+150, RED)
            draw_text('엔터키를 누르면', font_60, screen, draw_x, draw_y + 300,WHITHE)
            draw_text('게임 START_왌', font_60, screen, draw_x, draw_y + 370,WHITHE)

            pygame.display.update()
            
            action2 = 'game_menu2'
            while action2 != 'quit':
                if action2 == 'game_menu2':
                    action2 = game_menu2()
                elif action2 == 'play':
                    action2 = game_loop()

        elif clean_count == 10000:
            pygame.display.update()
            sleep(1)
            done = True

            con_image = pygame.image.load('background.png')
            screen.blit(con_image, [0,0])

            draw_text('congratulation', font_70, screen, draw_x, draw_y,YELLOW)
            draw_text('점수: {}'.format(clean_count), font_80, screen, draw_x, draw_y+150, RED)
            draw_text('엔터키를 누르면', font_60, screen, draw_x, draw_y + 300,WHITHE)
            draw_text('게임 START_읿', font_60, screen, draw_x, draw_y + 370,WHITHE)

            pygame.display.update()

            action2 = 'game_menu2'
            while action2 != 'quit':
                if action2 == 'game_menu2':
                    action2 = game_menu2()
                elif action2 == 'play':
                    action2 = game_loop()
            
        fps_clock.tick(FPS)

    return 'game_menu2'

# 첫 시작 화면 설정
def game_menu():
    start_image = pygame.image.load('background.png')
    screen.blit(start_image, [0,0])
    draw_x = int(BGWIDTH /2)
    draw_y = int(BGHEIGHT /4)
    font_70 = pygame.font.Font('dangam.ttf',100)
    font_40 = pygame.font.Font('YY.ttf',60)
    
    draw_text('SHARKDDI', font_70, screen, draw_x, draw_y,YELLOW)
    draw_text('엔터키를 누르면', font_40, screen, draw_x, draw_y + 200,WHITHE)
    draw_text('게임 START_읿', font_40, screen, draw_x, draw_y + 270,WHITHE)

    pygame.display.update()
    
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                return 'play'
            elif event.key == pygame.K_UP:
                game_method = pygame.image.load('oioio.png')
                screen.blit(game_method, [0,0])
                
        if event.type == QUIT:
            return 'quit'
    
    return 'game_menu'

# 게임을 다시 할 수 있게 하기 위한 설정
def game_menu2():
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                game_loop()
            
        if event.type == QUIT:
            return 'quit'

    return 'game_menu2'
    
# 게임의 메인 설정
def main():
    global screen
    
    pygame.init()
    screen = pygame.display.set_mode((BGWIDTH, BGHEIGHT))
    pygame.display.set_caption('Sharkddi')

    action = 'game_menu'
    while action != 'quit':
        if action == 'game_menu':
            action = game_menu()        
        elif action == 'play':
            action = game_loop()

    pygame.quit()
    
# 함수 실행
if __name__ == "__main__":
    main()
            
