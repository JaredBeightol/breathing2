import asyncio
import math
import random
import pygame

# Initialize Pygame
pygame.init()

# Window settings
WIDTH, HEIGHT = 1080, 720
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE | pygame.SCALED)

pygame.display.set_caption("breathing")

score_font = pygame.font.Font(None, 36)
end_font = pygame.font.Font(None, 72)

# Circle settings
circle_color = (0, 150, 255)
circle_pos = (WIDTH // 2, HEIGHT // 2)
circle_pox = WIDTH // 2
circle_poy = HEIGHT // 2
player_x_vec = 0
player_y_vec = 0
radius = 50
min_radius = 10
max_radius = 300
radius_step = 2

# Player input settings
flagMouseLeftClick = False
flagMouseRightClick = False

# Enemy settings
enemy_color = (75, 200, 130)
enemy_pox = WIDTH
enemy_poy = HEIGHT
enemy_radius = 10
enemy_x_vec = 0
enemy_y_vec = 0

timer_divide = 100
clock = pygame.time.Clock()


class Button:
    def __init__(self, text, x, y, width, height, normal_color, hover_color):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.normal_color = normal_color
        self.hover_color = hover_color

        # Web-safe: Using None for system default font instead of SysFont Arial
        self.font = pygame.font.Font(None, 24)
        self.text_surf = self.font.render(self.text, True, (0, 0, 0))
        self.text_rect = self.text_surf.get_rect(center=self.rect.center)

    def draw(self, surface):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            current_color = self.hover_color
        else:
            current_color = self.normal_color

        pygame.draw.rect(surface, current_color, self.rect, border_radius=8)
        surface.blit(self.text_surf, self.text_rect)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                return True
        return False


async def main():
    global radius
    running = True
    score_value = 0
    flagMouseLeftClick = False
    flagMouseRightClick = False
    circle_pox = WIDTH // 2
    circle_poy = HEIGHT // 2
    enemy_x_vec = random.randint(-5, 0)
    enemy_y_vec = random.randint(-5, 0)
    player_x_vec = 0
    player_y_vec = 0
    enemy_pox = WIDTH
    enemy_poy = HEIGHT
    game_ove_ind = False
    timer = 1

    my_button = Button("PLAY AGAIN", WIDTH // 2 - 80, HEIGHT // 2 + 50, 160, 60, (50, 120, 200), (70, 150, 240))

    while running:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if not game_ove_ind:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        flagMouseLeftClick = True
                    elif event.button == 3:
                        flagMouseRightClick = True
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        flagMouseLeftClick = False
                    elif event.button == 3:
                        flagMouseRightClick = False

                keys = pygame.key.get_pressed()
                player_x_vec = 0
                player_y_vec = 0
                if keys[pygame.K_w]: player_y_vec = -3
                if keys[pygame.K_a]: player_x_vec = -3
                if keys[pygame.K_s]: player_y_vec = 3
                if keys[pygame.K_d]: player_x_vec = 3
            else:
                # If Game Over, check button clicks
                if my_button.is_clicked(event):
                    score_value = 0
                    flagMouseLeftClick = False
                    flagMouseRightClick = False
                    circle_pox = WIDTH // 2
                    circle_poy = HEIGHT // 2
                    enemy_x_vec = random.randint(-5, 0)
                    enemy_y_vec = random.randint(-5, 0)
                    player_x_vec = 0
                    player_y_vec = 0
                    enemy_pox = WIDTH
                    enemy_poy = HEIGHT
                    radius = 50
                    timer = 1
                    game_ove_ind = False

        if not game_ove_ind:
            # --- ACTIVE GAMEPLAY STATE ---
            timer += 100 / (timer + 1)

            if flagMouseLeftClick or flagMouseRightClick:
                if flagMouseLeftClick:
                    radius = min(radius + radius_step, max_radius)
                elif flagMouseRightClick:
                    radius = max(radius - radius_step, min_radius)
            else:
                radius = max(radius - radius_step / 4, min_radius)

            score_value += (math.sqrt(radius) + 1) / 40

            enemy_pox += enemy_x_vec
            enemy_poy += enemy_y_vec

            # Boundary logic
            if enemy_pox >= WIDTH:
                enemy_pox = WIDTH
                enemy_x_vec = random.randint(-int(timer / timer_divide), 0)
                enemy_y_vec = random.randint(-int(timer / timer_divide), int(timer / timer_divide))
            elif enemy_pox <= 0:
                enemy_pox = 0
                enemy_x_vec = random.randint(0, int(timer / timer_divide))
                enemy_y_vec = random.randint(-int(timer / timer_divide), int(timer / timer_divide))
            if enemy_poy >= HEIGHT:
                enemy_poy = HEIGHT
                enemy_y_vec = random.randint(-int(timer / timer_divide), 0)
                enemy_x_vec = random.randint(-int(timer / timer_divide), int(timer / timer_divide))
            elif enemy_poy <= 0:
                enemy_poy = 0
                enemy_y_vec = random.randint(0, int(timer / timer_divide))
                enemy_x_vec = random.randint(-int(timer / timer_divide), int(timer / timer_divide))

            if enemy_x_vec in {1, 2, 3}: enemy_x_vec = 4
            if enemy_x_vec in {-1, -2, -3}: enemy_x_vec = -4
            if enemy_y_vec in {1, 2, 3}: enemy_y_vec = 4
            if enemy_y_vec in {-1, -2, -3}: enemy_y_vec = -4

            circle_pox += player_x_vec
            circle_poy += player_y_vec

            if circle_pox > WIDTH:
                circle_pox = WIDTH
            elif circle_pox < 0:
                circle_pox = 0
            if circle_poy > HEIGHT:
                circle_poy = HEIGHT
            elif circle_poy < 0:
                circle_poy = 0

            # Collision calculation
            if math.dist((circle_pox, circle_poy), (enemy_pox, enemy_poy)) - (radius + enemy_radius) <= 0:
                game_ove_ind = True

            # Draw active game
            SCREEN.fill((30, 30, 30))
            pygame.draw.circle(SCREEN, circle_color, (int(circle_pox), int(circle_poy)), int(radius))
            pygame.draw.circle(SCREEN, enemy_color, (int(enemy_pox), int(enemy_poy)), enemy_radius)
            score_text = score_font.render(f"Score: {int(score_value)}", True, (255, 255, 255))
            SCREEN.blit(score_text, (20, 20))
        else:
            # --- GAME OVER STATE ---
            SCREEN.fill((30, 30, 30))
            score_text = score_font.render(f"Final Score: {int(score_value)}", True, (255, 255, 255))
            SCREEN.blit(score_text, (20, 20))
            end_text = end_font.render("GAME OVER", True, (255, 50, 50))
            end_rect = end_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
            SCREEN.blit(end_text, end_rect)
            my_button.draw(SCREEN)

        pygame.display.flip()
        await asyncio.sleep(0)  # Continuous execution safety for WebAssembly

    pygame.quit()


if __name__ == "__main__":
    asyncio.run(main())
