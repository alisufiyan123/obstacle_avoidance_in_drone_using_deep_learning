
import pygame
import json
import math

MAP_SIZE_COEFF = 5.14

pygame.init()
screen = pygame.display.set_mode([720, 720])
screen.fill((255, 255, 255))
running = True


class Background(pygame.sprite.Sprite):
    def __init__(self, image, location, scale):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image)
        self.image = pygame.transform.rotozoom(self.image, 0, scale)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location


def get_distance_between_points(pos0, pos1):
    x = abs(pos0[0] - pos1[0])
    y = abs(pos0[1] - pos1[1])
    dist_px = math.hypot(x, y)
    dist_cm = dist_px * MAP_SIZE_COEFF
    return int(dist_cm), int(dist_px)


def get_angle_btw_line(pos0, pos1, reference_position):
    ax = reference_position[0] - pos0[0]
    ay = reference_position[1] - pos0[1]
    bx = reference_position[0] - pos1[0]
    by = reference_position[1] - pos1[1]
    _dot = (ax * bx) + (ay * by)
    _magA = math.sqrt(ax**2 + ay**2)
    _magB = math.sqrt(bx**2 + by**2)
    _rad = math.acos(_dot / (_magA * _magB))
    angle = (_rad * 180) / math.pi
    return int(angle)


bground = Background('image.png', [0, 0], 1.6)
screen.blit(bground.image, bground.rect)

way_points_path = []
index = 0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            way_points_path.append(pos)
            if index > 0:
                pygame.draw.line(screen, (255, 0, 0), way_points_path[index-1], pos, 2)
            index += 1
    pygame.display.update()

way_points_path.insert(0, (way_points_path[0][0], way_points_path[0][1] - 10))

path_distance_from_p_t_p = []
path_dist_px = []
path_angle = []
for index in range(len(way_points_path)):
    if index > 1:
        dist_cm, dist_px = get_distance_between_points(way_points_path[index-1], way_points_path[index])
        path_distance_from_p_t_p.append(dist_cm)
        path_dist_px.append(dist_px)

    if index > 0 and index < (len(way_points_path) - 1):
        angle = get_angle_btw_line(way_points_path[index-1], way_points_path[index+1], way_points_path[index])
        path_angle.append(angle)

print('way_points_path: {}'.format(way_points_path))
print('dist_cm: {}'.format(path_distance_from_p_t_p))
print('dist_px: {}'.format(path_dist_px))
print('dist_angle: {}'.format(path_angle))

markersz = []
for index in range(len(path_distance_from_p_t_p)):
    markersz.append({
        "dist_cm": path_distance_from_p_t_p[index],
        "dist_px": path_dist_px[index],
        "angle_deg": path_angle[index]
    })

f = open('waypoint.json', 'w+')
way_points_path.pop(0)
json.dump({
    "wp": markersz,
    "pos": way_points_path
}, f, indent=4)