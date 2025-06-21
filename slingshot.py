import pygame
import math 

pygame.init()

WIDTH, HEIGHT = 800, 600
window = pygame.display.set_mode((WIDTH,HEIGHT))
OBJECT_SIZE = 5
Planet_Size = 100
G = 10
VELOCITY_SCALE = 50
OBJECT_MASS = 5
FPS = 60

planet_options = [('Earth', (100,200)), ('Jupiter', (100,250)), ('Mars', (100,300)), ('Neptune', (100,350))]
planet_charactersitics = {
    'earth' : 100, 
    'jupiter': 200, 
    'mars' : 80, 
    'neptune': 140
}




pygame.display.set_caption('Welcome to the Slingshot Effect Simulation')
Background = pygame.transform.scale(pygame.image.load('background.png'), (WIDTH, HEIGHT))

WHITE = (255,255,255)
RED = (255,0,0)
BLUE = (0,0,255)

def draw_game_scene(selected_planet):
    
    if selected_planet.lower() == 'earth':
        return pygame.transform.scale(pygame.image.load("earth.png"), (50 * 2, 50 * 2))

    elif selected_planet.lower() == 'jupiter':
        return pygame.transform.scale(pygame.image.load("jupiter.png"), (50 * 2, 50 * 2))
    
    elif selected_planet.lower() == 'mars':
        return pygame.transform.scale(pygame.image.load("mars.png"), (50 * 2, 50 * 2))

    else:
        
        return pygame.transform.scale(pygame.image.load("neptune.png"), (50 * 2, 50 * 2))



class Planet():
    def __init__(self,x,y,mass, image):
        self.x = x
        self.y = y
        self.mass = mass
        self.image = image
        self.radius = image.get_width() // 2

    def draw(self):
        rect = self.image.get_rect(center=(self.x, self.y))
        window.blit(self.image, rect)

class Spaceship():
    def __init__(self, x, y , velocity_x, velocity_y, mass):
        self.x = x
        self.y = y
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y
        self.mass = mass

    def move(self,planet):
        distance = math.sqrt((self.x - planet.x)**2 + (self.y - planet.y)**2)
        force = (G*self.mass*planet.mass)/distance**2
        acceleration = force/self.mass
        angle = math.atan2(planet.y - self.y, planet.x - self.x)

        acceleration_x = acceleration * math.cos(angle)
        acceleration_y = acceleration * math.sin(angle)

        self.velocity_x += acceleration_x
        self.velocity_y += acceleration_y

        self.x += self.velocity_x
        self.y += self.velocity_y

    def draw_self(self):
        pygame.draw.circle(window, BLUE, (int(self.x), int(self.y)), OBJECT_SIZE )

def create_ship(location, mouse):
    initial_x, initial_y = location

    mouse_x,mouse_y = mouse

    velocity_x =(mouse_x - initial_x) / VELOCITY_SCALE
    velocity_y = (mouse_y - initial_y) / VELOCITY_SCALE

    object = Spaceship(initial_x, initial_y, velocity_x, velocity_y, OBJECT_MASS)

    return object


def generate_buttons(planet_options):
    buttons = []

    for name,(x,y) in planet_options:
        rectangle = pygame.Rect(x,y,200,40)
        buttons.append((name,rectangle))

    return buttons

    
def main():
    running = True
    clock = pygame.time.Clock()
    object_position = None
    objects = []
    selected_planet = None
    show_menu = True

    buttons = generate_buttons(planet_options)

    while running:
        clock.tick(FPS)
        mouse_position = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running  = False

            if show_menu == True and event.type == pygame.MOUSEBUTTONDOWN:
                
                for name, rectangle in buttons:
                    if rectangle.collidepoint(mouse_position):
                        selected_planet = name
                        
                        planet_image = draw_game_scene(selected_planet)
                        
                        show_menu = False
                        print('Selected: ', name)
                        
                        
            
            elif not show_menu and event.type == pygame.MOUSEBUTTONDOWN:
                if object_position:
                    object = create_ship(object_position, mouse_position)
                    objects.append(object)
                    object_position = None
                else:
                    object_position = pygame.mouse.get_pos()


        window.blit(Background, (0,0))
        if show_menu:
            overlay = pygame.Surface((WIDTH, HEIGHT))
            overlay.set_alpha(180)
            overlay.fill((0, 0, 0))
            window.blit(overlay, (0, 0))

            pygame.draw.rect(window, (0, 0, 0), (80, 160, 240, 240))
            title = pygame.font.Font(None, 36).render("Select a Planet", True, WHITE)
            window.blit(title, (100, 170))

            for name, rectangle in buttons:
                pygame.draw.rect(window, (200, 200, 200), rectangle)
                text = pygame.font.Font(None, 28).render(name, True, (0, 0, 0))
                window.blit(text, (rectangle.x, rectangle.y))

            pygame.display.flip()
            continue


          
        planet = Planet(WIDTH // 2, HEIGHT // 2, planet_charactersitics[selected_planet.lower()], planet_image)

        planet.draw() 
        if object_position:
            pygame.draw.line(window, WHITE, object_position, mouse_position,  2)
            pygame.draw.circle(window, BLUE, object_position, OBJECT_SIZE)

        for object in objects:
            object.draw_self()
            object.move(planet)
            off_screen = object.x > WIDTH or object.x < 0 or object.y < 0 or object.y > HEIGHT
            collided = math.sqrt((object.x - planet.x)**2 + (object.y - planet.y)**2) < planet.radius

            if off_screen or collided:
                objects.remove(object)


    
        pygame.display.update()

    pygame.quit()


if __name__ == '__main__':

    main()




