import pygame
import math
import sys

# --- НАЛАШТУВАННЯ ---
SCREEN_WIDTH, SCREEN_HEIGHT = 1000, 700
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 0, 0)
GREEN = (0, 200, 0)
BLUE = (0, 100, 255)


# ==========================================
# 🧱 КЛАС БпЛА Raybird-3
# ==========================================
class Raybird3:
    def __init__(self, x, y):
        self.x, self.y = float(x), float(y)
        self.angle = 0.0
        self.speed = 0.0
        self.max_speed = 4.0
        self.fuel = 100.0
        self.engine_on = False

        # Автопілот
        self.waypoints = [(100, 100), (900, 100), (900, 600), (100, 600)]
        self.current_wp = 0
        self.autopilot = False

    def send_coordinates(self):
        """Симуляція передачі даних розвідки"""
        if self.engine_on:
            print(f"📡 [DATA LINK] Об'єкт зафіксовано! Координати: X:{self.x:.1f}, Y:{self.y:.1f}")
            return True
        return False

    def update(self, keys):
        if not self.engine_on: return

        # 1. Витрата пального
        self.fuel -= 0.01
        if self.fuel <= 0:
            self.fuel = 0
            self.engine_on = False

        # 2. Керування: Автопілот vs Ручне
        if self.autopilot and self.current_wp < len(self.waypoints):
            target = self.waypoints[self.current_wp]
            dx, dy = target[0] - self.x, target[1] - self.y
            dist = math.hypot(dx, dy)
            if dist < 15:
                self.current_wp += 1
            else:
                target_angle = math.degrees(math.atan2(-dy, dx)) % 360
                angle_diff = (target_angle - self.angle + 180) % 360 - 180
                self.angle += max(min(angle_diff, 3), -3)
                self.speed = 3.0
        else:
            # Ручне керування стрілками
            if keys[pygame.K_LEFT]: self.angle += 3
            if keys[pygame.K_RIGHT]: self.angle -= 3
            if keys[pygame.K_UP]: self.speed = min(self.speed + 0.1, self.max_speed)
            if keys[pygame.K_DOWN]: self.speed = max(self.speed - 0.1, 0)

        # 3. Рух
        rad = math.radians(self.angle)
        self.x += self.speed * math.cos(rad)
        self.y -= self.speed * math.sin(rad)

    def draw(self, surf):
        # Малюємо точки маршруту
        for wp in self.waypoints:
            pygame.draw.circle(surf, GREEN, wp, 10, 2)

        # Малюємо дрон (трикутник)
        pts = [
            (self.x + 20 * math.cos(math.radians(self.angle)), self.y - 20 * math.sin(math.radians(self.angle))),
            (self.x + 15 * math.cos(math.radians(self.angle + 140)),
             self.y - 15 * math.sin(math.radians(self.angle + 140))),
            (self.x + 15 * math.cos(math.radians(self.angle - 140)),
             self.y - 15 * math.sin(math.radians(self.angle - 140)))
        ]
        pygame.draw.polygon(surf, RED if not self.autopilot else BLUE, pts)


# ==========================================
# 🎮 ГОЛОВНИЙ ЦИКЛ
# ==========================================
def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Raybird-3 Simulator (NUFT Lab)")
    clock = pygame.time.Clock()
    drone = Raybird3(500, 350)
    font = pygame.font.SysFont("Consolas", 18)
    msg_timer = 0

    while True:
        screen.fill(WHITE)
        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s: drone.engine_on = True
                if event.key == pygame.K_a: drone.autopilot = not drone.autopilot
                if event.key == pygame.K_SPACE:
                    if drone.send_coordinates(): msg_timer = 60

        drone.update(keys)
        drone.draw(screen)

        # Інтерфейс
        info = [
            f"Engine: {'ON' if drone.engine_on else 'OFF'} (Press S)",
            f"Mode: {'AUTOPILOT' if drone.autopilot else 'MANUAL'} (Press A)",
            f"Fuel: {drone.fuel:.1f}%",
            f"Coords: X:{drone.x:.1f} Y:{drone.y:.1f}",
            "Space: SEND COORDS | Arrows: MOVE"
        ]
        for i, text in enumerate(info):
            screen.blit(font.render(text, True, BLACK), (20, 20 + i * 25))

        if msg_timer > 0:
            screen.blit(font.render("DATA SENT TO BASE!", True, GREEN), (SCREEN_WIDTH // 2 - 80, 50))
            msg_timer -= 1

        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    main()