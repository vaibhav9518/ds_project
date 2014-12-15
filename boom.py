import random
import pygame
import backup as PyParticles

(width, height) = (640,640)
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Star formation')

universe = PyParticles.Environment((width, height))
universe.colour = (49,79,79)
universe.addFunctions(['move', 'attract', 'combine'])

def calculateRadius(mass):
    return  mass ** (0.75)

for p in range(200):
    particle_mass = random.randint(1,4)
    particle_size = calculateRadius(particle_mass)
    universe.addParticles(mass=particle_mass, size=particle_size, speed=0, colour=(255,255,255))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            running = False

    screen.fill(universe.colour)
    universe.update()
    
    particles_to_remove = []
    for p in universe.particles:
        if 'collide_with' in p.__dict__:
            particles_to_remove.append(p.collide_with)
            p.size = calculateRadius(p.mass)
            del p.__dict__['collide_with']

        if p.size < 2:
            pygame.draw.rect(screen,(255,215,0), (int(p.x), int(p.y), 2, 2))
        else:
            pygame.draw.ellipse(screen,(255,215,0), (int(p.x), int(p.y), int(p.size),1.5*int(p.size)), 0)
    
    for p in particles_to_remove:
        if p in universe.particles:
            universe.particles.remove(p)

    pygame.display.flip()
