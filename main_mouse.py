# перемещение картинки с помощью мышки

import pygame
pygame.init()
import time


windows_size=(800,600)
screen=pygame.display.set_mode(windows_size)
pygame.display.set_caption("Тестовый проект")
image1 = pygame.image.load("python.jpg")
image_rect1= image1.get_rect()

image2 = pygame.image.load("python2.jpg")
image_rect2= image2.get_rect()



# добавим игровой цикл, без него ничего не выводится

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    if event.type == pygame.MOUSEMOTION:
        mouseX, mouseY = pygame.mouse.get_pos()
        image_rect1.x = mouseX - 80
        image_rect1.y = mouseY - 60

    if image_rect1.colliderect(image_rect2):
        print("Произошло столкновение")
        time.sleep(1)

    screen.fill((0,0,0)) # пример цветов
    screen.blit(image1, image_rect1)
    screen.blit(image2, image_rect2)



    pygame.display.flip()
pygame.quit()
