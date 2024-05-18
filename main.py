# перемещение картинки с помощью стрелок

import pygame
pygame.init()


windows_size=(800,600)
screen=pygame.display.set_mode(windows_size)
pygame.display.set_caption("Тестовый проект")
image = pygame.image.load("python.jpg")
image_rect= image.get_rect()
speed = 5 # скорость


# добавим игровой цикл, без него ничего не выводится

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        image_rect.x-= speed
    if keys[pygame.K_RIGHT]:
        image_rect.x += speed
    if keys[pygame.K_UP]:
        image_rect.y -= speed
    if keys[pygame.K_DOWN]:
        image_rect.y += speed
    screen.fill((0,0,0)) # пример цветов
    screen.blit(image, image_rect)
    pygame.display.flip()
pygame.quit()
