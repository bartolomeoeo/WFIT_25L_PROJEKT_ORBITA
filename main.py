import pygame
import math


# WFIT_25L_PROJEKT_ORBITA
# Authors: Jakub Falba, Bartosz Woźniak


# Initialize Pygame
pygame.init()

# Screen setup
WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("2D Orbit Simulation")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (100, 149, 237)
RED = (255, 0, 0)
DARKGRAY = (58, 58, 58)
GRAY = (200, 200, 200)

# Constants
G = 6.67430e-11  # gravitational constant (m^3 kg^-1 s^-2)
M = 5.976e24  # mass of the planet (Earth) in kg
R_PLANET = 6371000  # radius of planet in meters
SCALE = 30 / R_PLANET  # scale: meters to pixels (so planet fits nicely)
r = 400000 + R_PLANET

# Time step
dt = 1  # seconds per frame (you can adjust to speed up or slow down simulation)
dt_temp = 0
#FPS
FPS = 60

# Initial satellite parameters
sat_mass = 1000  # mass of satellite (not needed for simple gravity simulation)
sat_x = R_PLANET + 400000  # 400 km above surface, meters
sat_y = 0
sat_vx = 0
sat_vy = 7600  # approx orbital velocity at 400km (m/s)


# Convert initial position to screen coordinates
def to_screen(x, y):
    return int(screen.get_size()[0] / 2 + x * SCALE), int(screen.get_size()[1] / 2 - y * SCALE)

# Button class representing buttons on the screen
class Button:
    def __init__(self, text, size, color, text_color):
        self.text = text
        self.size = size
        self.color = color
        self.text_color = text_color
        self.font = pygame.font.Font('freesansbold.ttf', 20)

    def draw(self, screen, position):
        # Draw rectangle
        pygame.draw.rect(screen, self.color, (*position, *self.size))

        # Draw text
        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=(position[0] + self.size[0] // 2, position[1] + self.size[1] // 2))
        screen.blit(text_surf, text_rect)

        # Return the button's position for click detection
        return position
# Initiating button objects
start_button = Button("Start", (70, 30), GRAY, WHITE)
reset_button = Button("Reset", (70, 30), GRAY, WHITE)
quit_button = Button("Quit", (70, 30), GRAY, WHITE)
stop_button = Button("Stop/Resume", (230, 30), GRAY, WHITE)
SimulationSpeed_button = Button("Simulation speed", (230, 30), DARKGRAY, WHITE)
SimPlus_button = Button("+", (112, 30), GRAY, WHITE)
SimMinus_button = Button("-", (112, 30), GRAY, WHITE)
Velocity = Button("0", (200, 30), GRAY, WHITE)
Vx_button = Button("Vx", (230, 30), DARKGRAY, WHITE)
VxPlus_button = Button("+", (112, 30), GRAY, WHITE)
VxMinus_button = Button("-", (112, 30), GRAY, WHITE)
Vy_button = Button("Vy", (230, 30), DARKGRAY, WHITE)
VyPlus_button = Button("+", (112, 30), GRAY, WHITE)
VyMinus_button = Button("-", (112, 30), GRAY, WHITE)
H_button = Button("H: 400KM", (230, 30), DARKGRAY, WHITE)
HPlus_button = Button("+", (112, 30), GRAY, WHITE)
HMinus_button = Button("-", (112, 30), GRAY, WHITE)

# List containing points that the satellite has visited, used to draw a trail
trail = []

# Initial simulation parameters

running = True
run_animation = False
clock = pygame.time.Clock()

# Main simulation body

while running:
    clock.tick(FPS)  # FPS

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN: # Detecting button clicks
            mouse_pos = pygame.mouse.get_pos()
            start_pos = (screen.get_size()[0] - start_button.size[0] - 10, 10)
            reset_pos = (screen.get_size()[0] - reset_button.size[0] - 10, 50)
            quit_pos = (screen.get_size()[0] - quit_button.size[0] - 10, 90)
            stop_pos = (screen.get_size()[0] - stop_button.size[0] - 10, 130)
            SimPlus_pos = (screen.get_size()[0] - SimPlus_button.size[0] -10, 210)
            SimMinus_pos = (screen.get_size()[0] - SimMinus_button.size[0]-128, 210)
            VxPlus_pos =  (screen.get_size()[0] - VxPlus_button.size[0]-10, 290)
            VxMinus_pos = (screen.get_size()[0] - VxMinus_button.size[0]-128, 290)
            VyPlus_pos = (screen.get_size()[0] - VyPlus_button.size[0] - 10, 370)
            VyMinus_pos = (screen.get_size()[0] - VyMinus_button.size[0] - 128, 370)
            HPlus_pos = (screen.get_size()[0] - VyPlus_button.size[0] - 10, 450)
            HMinus_pos = (screen.get_size()[0] - VyMinus_button.size[0] - 128, 450)
            if quit_pos[0] <= mouse_pos[0] <= quit_pos[0] + quit_button.size[0] and \
                    quit_pos[1] <= mouse_pos[1] <= quit_pos[1] + quit_button.size[1]:
                running = False
            if stop_pos[0] <= mouse_pos[0] <= stop_pos[0] + stop_button.size[0] and \
                    stop_pos[1] <= mouse_pos[1] <= stop_pos[1] + stop_button.size[1]:
                if dt == 0:
                    dt = dt_temp
                else:
                    dt_temp = dt
                    dt = 0
            if start_pos[0] <= mouse_pos[0] <= start_pos[0] + start_button.size[0] and \
                    start_pos[1] <= mouse_pos[1] <= start_pos[1] + start_button.size[1]:
                run_animation = True
            if reset_pos[0] <= mouse_pos[0] <= reset_pos[0] + reset_button.size[0] and \
                    reset_pos[1] <= mouse_pos[1] <= reset_pos[1] + reset_button.size[1]:
                run_animation = False
                sat_x = R_PLANET + 400000
                sat_y = 0
                sat_vx = 0
                sat_vy = 7600
                trail = []
                dt = 1
                FPS = 60
            if SimPlus_pos[0] <= mouse_pos[0] <= SimPlus_pos[0] + SimPlus_button.size[0] and \
                    SimPlus_pos[1] <= mouse_pos[1] <= SimPlus_pos[1] + SimPlus_button.size[1]:
                if dt <100 and FPS <200:
                    dt += 10
                    FPS += 14
            if SimMinus_pos[0] <= mouse_pos[0] <= SimMinus_pos[0] + SimMinus_button.size[0] and \
                    SimMinus_pos[1] <= mouse_pos[1] <= SimMinus_pos[1] + SimMinus_button.size[1]:
                if dt > 1 and FPS > 60:
                    dt -=10
                    FPS -=14
            if VxPlus_pos[0] <= mouse_pos[0] <= VxPlus_pos[0] + VxPlus_button.size[0] and \
                    VxPlus_pos[1] <= mouse_pos[1] <= VxPlus_pos[1] + VxPlus_button.size[1]:
                sat_vx +=100
            if VxMinus_pos[0] <= mouse_pos[0] <= VxMinus_pos[0] + VxMinus_button.size[0] and \
                    VxMinus_pos[1] <= mouse_pos[1] <= VxMinus_pos[1] + VxMinus_button.size[1]:
                sat_vx -=100
            if VyPlus_pos[0] <= mouse_pos[0] <= VyPlus_pos[0] + VyPlus_button.size[0] and \
                    VyPlus_pos[1] <= mouse_pos[1] <= VyPlus_pos[1] + VyPlus_button.size[1]:
                sat_vy +=100
            if VyMinus_pos[0] <= mouse_pos[0] <= VyMinus_pos[0] + VyMinus_button.size[0] and \
                    VyMinus_pos[1] <= mouse_pos[1] <= VyMinus_pos[1] + VyMinus_button.size[1]:
                sat_vy -=100
            if HPlus_pos[0] <= mouse_pos[0] <= HPlus_pos[0] + HPlus_button.size[0] and \
                    HPlus_pos[1] <= mouse_pos[1] <= HPlus_pos[1] + HPlus_button.size[1]:
                sat_x = (r+100000)*sat_x/r
                sat_y = (r+100000)*sat_y/r
                r += 100000

            if HMinus_pos[0] <= mouse_pos[0] <= HMinus_pos[0] + HMinus_button.size[0] and \
                    HMinus_pos[1] <= mouse_pos[1] <= HMinus_pos[1] + HMinus_button.size[1]:
                if math.sqrt(sat_x ** 2 + sat_y ** 2)-R_PLANET>0:
                    sat_x = (r - 100000) * sat_x / r
                    sat_y = (r - 100000) * sat_y / r
                    r -= 100000

        if event.type == pygame.MOUSEWHEEL:
            if event.y > 0:
                SCALE += 5/R_PLANET
            else:
                if SCALE > 6/R_PLANET:
                    SCALE -= 5 / R_PLANET

    if run_animation:
        # Calculate distance from planet center
        r = math.sqrt(sat_x ** 2 + sat_y ** 2)
        if r<R_PLANET:
            run_animation = False
        # Calculate gravitational acceleration magnitude
        a = G * M / r ** 2

        # Calculate acceleration components (towards the planet center)
        ax = -a * (sat_x / r)
        ay = -a * (sat_y / r)

        # Update velocity
        sat_vx += ax * dt
        sat_vy += ay * dt

        # Update position
        sat_x += sat_vx * dt
        sat_y += sat_vy * dt

     # Update trail
    if len(trail) > 3500:
        trail.pop(0)
        trail.append((sat_x, sat_y))
    else:
        trail.append((sat_x, sat_y))
    # Drawing background
    screen.fill(BLACK)

    # Draw planet
    pygame.draw.circle(screen, BLUE, (screen.get_size()[0] // 2, screen.get_size()[1] // 2), int(R_PLANET * SCALE))

    # Draw trail
    for pos in trail:
        pygame.draw.circle(screen, WHITE, to_screen(pos[0],pos[1]), 1)  # Small white dots for the trail

    # Draw satellite
    sat_pos = to_screen(sat_x, sat_y)
    pygame.draw.circle(screen, RED, sat_pos, 5)

    # Draw buttons
    start_button.draw(screen, (screen.get_size()[0] - start_button.size[0] - 10, 10))
    reset_button.draw(screen, (screen.get_size()[0] - quit_button.size[0] - 10, 50))
    quit_button.draw(screen, (screen.get_size()[0] - quit_button.size[0] - 10, 90))
    stop_button.draw(screen, (screen.get_size()[0] - stop_button.size[0] - 10, 130))
    SimulationSpeed_button.draw(screen, (screen.get_size()[0] - SimulationSpeed_button.size[0] - 10, 170))
    SimPlus_button.draw(screen, (screen.get_size()[0] - SimPlus_button.size[0]-10, 210))
    SimMinus_button.draw(screen, (screen.get_size()[0] - SimMinus_button.size[0]-128, 210))
    Velocity.text = str(int(math.sqrt(sat_vx**2 + sat_vy**2))) + " m/s"
    Velocity.draw(screen, (screen.get_size()[0]//2-Velocity.size[0]/2 , 0))
    Vx_button.text = "Vx: " +str(int(sat_vx)) + " m/s"
    Vx_button.draw(screen, (screen.get_size()[0] - Vx_button.size[0]-10, 250))
    VxPlus_button.draw(screen, (screen.get_size()[0] - VxPlus_button.size[0]-10, 290))
    VxMinus_button.draw(screen,(screen.get_size()[0] - VxMinus_button.size[0] - 128, 290))
    Vy_button.text = "Vy: " + str(int(sat_vy)) + " m/s"
    Vy_button.draw(screen, (screen.get_size()[0] - Vy_button.size[0] - 10, 330))
    VyPlus_button.draw(screen, (screen.get_size()[0] - VyPlus_button.size[0] - 10, 370))
    VyMinus_button.draw(screen, (screen.get_size()[0] - VyMinus_button.size[0] - 128, 370))
    H_button.text = "H: " + str(int(math.sqrt(sat_x ** 2 + sat_y ** 2)-R_PLANET)/1000) + " km"
    H_button.draw(screen, (screen.get_size()[0] - Vy_button.size[0] - 10, 410))
    HPlus_button.draw(screen, (screen.get_size()[0] - VyPlus_button.size[0] - 10, 450))
    HMinus_button.draw(screen, (screen.get_size()[0] - VyMinus_button.size[0] - 128, 450))

    # Update display
    pygame.display.flip()

pygame.quit()
