import pygame
import random
import sys


pygame.init()


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("슈팅 게임 - 점수 & 게임오버")


clock = pygame.time.Clock()


background = pygame.image.load("C:\minseung\Python\images\qqqq.png")
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

player = pygame.image.load("C:\minseung\Python\images\char.png")
player = pygame.transform.scale(player, (80, 100))
player_rect = player.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 80))

enemy_img = pygame.image.load("C:\minseung\Python\images\enemy.png")
enemy_img = pygame.transform.scale(enemy_img, (60, 60))


player_speed = 7
bullet_speed = -10
enemy_speed = 3

bullets = []
enemies = []
enemy_spawn_timer = 0
score = 0
font = pygame.font.Font(None, 40)

game_over = False


def draw_text(text, x, y, color=(255, 255, 255), size=40, center=False):
    font_obj = pygame.font.Font(None, size)
    text_surface = font_obj.render(text, True, color)
    text_rect = text_surface.get_rect()
    if center:
        text_rect.center = (x, y)
    else:
        text_rect.topleft = (x, y)
    screen.blit(text_surface, text_rect)


running = True
while running:
    clock.tick(60)


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if not game_over:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bullet_rect = pygame.Rect(player_rect.centerx - 3, player_rect.top, 6, 20)
                    bullets.append(bullet_rect)

        else:

            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
        
                bullets.clear()
                enemies.clear()
                player_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 80)
                score = 0
                game_over = False


    if not game_over:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_rect.left > 0:
            player_rect.x -= player_speed
        if keys[pygame.K_RIGHT] and player_rect.right < SCREEN_WIDTH:
            player_rect.x += player_speed
        if keys[pygame.K_UP] and player_rect.top > 0:
            player_rect.y -= player_speed
        if keys[pygame.K_DOWN] and player_rect.bottom < SCREEN_HEIGHT:
            player_rect.y += player_speed


        for bullet in bullets[:]:
            bullet.y += bullet_speed
            if bullet.bottom < 0:
                bullets.remove(bullet)


        enemy_spawn_timer += 1
        if enemy_spawn_timer > 40:
            enemy_rect = enemy_img.get_rect(center=(random.randint(40, SCREEN_WIDTH - 40), 0))
            enemies.append(enemy_rect)
            enemy_spawn_timer = 0


        for enemy in enemies[:]:
            enemy.y += enemy_speed
            if enemy.top > SCREEN_HEIGHT:
                enemies.remove(enemy)


        for bullet in bullets[:]:
            for enemy in enemies[:]:
                if bullet.colliderect(enemy):
                    bullets.remove(bullet)
                    enemies.remove(enemy)
                    score += 10  
                    break


        for enemy in enemies:
            if player_rect.colliderect(enemy):
                game_over = True


    screen.blit(background, (0, 0))

    if not game_over:
        screen.blit(player, player_rect)


        for bullet in bullets:
            pygame.draw.rect(screen, (255, 255, 0), bullet)


        for enemy in enemies:
            screen.blit(enemy_img, enemy)


        draw_text(f"Score: {score}", 10, 10)

    else:

        draw_text("GAME OVER", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50, (255, 0, 0), 80, center=True)
        draw_text(f"Final Score: {score}", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20, (255, 255, 255), 50, center=True)
        draw_text("Press R to Restart", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 90, (200, 200, 200), 35, center=True)

    pygame.display.flip()


pygame.quit()
sys.exit()