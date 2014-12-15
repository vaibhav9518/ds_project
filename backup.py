# Embedded file name: C:\Users\vaibhav sharma\Desktop\backup.py
import math, random

def addVectors((angle1, length1), (angle2, length2)):
    x = math.sin(angle1) * length1 + math.sin(angle2) * length2
    y = math.cos(angle1) * length1 + math.cos(angle2) * length2
    angle = 0.5 * math.pi - math.atan2(y, x)
    length = math.hypot(x, y)
    return (angle, length)


def combine(p1, p2):
    if math.hypot(p1.x - p2.x, p1.y - p2.y) < p1.size + p2.size:
        total_mass = p1.mass + p2.mass
        p1.x = (p1.x * p1.mass + p2.x * p2.mass) / total_mass
        p1.y = (p1.y * p1.mass + p2.y * p2.mass) / total_mass
        p1.angle, p1.speed = addVectors((p1.angle, p1.speed * p1.mass / total_mass), (p2.angle, p2.speed * p2.mass / total_mass))
        p1.speed *= p1.elasticity * p2.elasticity
        p1.mass += p2.mass
        p1.collide_with = p2


class Particle:

    def __init__(self, (x, y), size, mass = 1):
        self.x = x
        self.y = y
        self.size = size
        self.colour = (0, 0, 255)
        self.thickness = 0
        self.speed = 0
        self.angle = 0
        self.mass = mass
        self.drag = 1
        self.elasticity = 0.9
        self.acceleration = 0

    def move(self):
        self.x += math.sin(self.angle) * self.speed
        self.y -= math.cos(self.angle) * self.speed

    def accelerate(self, vector):
        self.angle, self.speed = addVectors((self.angle, self.speed), vector)

    def attract(self, other):
        dx = self.x - other.x
        dy = self.y - other.y
        dist = math.hypot(dx, dy)
        if dist < self.size + other.size:
            return True
        theta = math.atan2(dy, dx)
        force = 0.2 * self.mass * other.mass / dist ** 2
        self.acceleration = force / self.mass
        self.accelerate((theta - 0.5 * math.pi, force / self.mass))


class NODE:

    def __init__(self, particle, m):
        self.data = [particle.x, particle.y]
        self.particle = particle
        self.left = []
        self.right = []
        self.center = self.data
        self.mass = m
        self.L = 0
        self.size = particle.size

    def update(self):
        self.data = [self.particle.x, self.particle.y]

    def LEFT(self, node):
        self.left = node

    def RIGHT(self, node):
        self.right = node


def COM(m1, lis, m2, lis2):
    r = []
    i = 0
    while i < len(lis):
        r += [(lis[i] * m1 + lis2[i] * m2) / (m1 + m2)]
        i += 1

    return r


def dist(x, y, x1, y1):
    return pow((x - x1) ** 2 + (y - y1) ** 2, 0.5)


class K_D_tree:

    def __init__(self, dim, alpha):
        self.dim = dim
        self.root = []
        self.alpha = alpha

    def KDNode(self, x, m):
        node = NODE(x, m)
        return node

    def insert(self, POINT, KDNODE, cd, m):
        pt = [POINT.x, POINT.y]
        if KDNODE == []:
            KDNODE = self.KDNode(POINT, m)
        else:
            if pt == KDNODE.data:
                print POINT
                print 'error!duplicate2'
                return
            if pt[cd] < KDNODE.data[cd]:
                dis = dist(KDNODE.center[0], KDNODE.center[1], POINT.x, POINT.y)
                KDNODE.L = max(KDNODE.L, dis)
                KDNODE.center = COM(KDNODE.mass, KDNODE.data, m, [POINT.x, POINT.y])
                KDNODE.mass += m
                KDNODE.size += POINT.size / 3
                KDNODE.left = self.insert(POINT, KDNODE.left, (cd + 1) % self.dim, m)
            else:
                dis = dist(KDNODE.center[0], KDNODE.center[1], POINT.x, POINT.y)
                KDNODE.L = max(KDNODE.L, dis)
                KDNODE.center = COM(KDNODE.mass, KDNODE.data, m, [POINT.x, POINT.y])
                KDNODE.mass += m
                KDNODE.size += POINT.size / 3
                KDNODE.right = self.insert(POINT, KDNODE.right, (cd + 1) % self.dim, m)
        return KDNODE

    def ins(self, POINT, m):
        self.root = self.insert(POINT, self.root, 0, m)

    def find_min(self, NODE_T, dim, CD):
        if NODE_T == []:
            return []
        if CD == dim:
            if NODE_T.left == []:
                return NODE_T
            else:
                return self.find_min(NODE_T.left, dim, (CD + 1) % self.dim)
        else:
            x = self.find_min(NODE_T.left, dim, (CD + 1) % self.dim)
            y = self.find_min(NODE_T.right, dim, (CD + 1) % self.dim)
            lis = []
            if x != []:
                lis += [x]
            if y != []:
                lis += [y]
            if NODE_T.data != []:
                lis += [NODE_T]
            return min(lis, key=lambda x: x.data[CD])

    def minimum(self):
        return self.find_min(self.root, self.dim, 0)

    def delete(self, POINT_X, NODE_T, cd):
        if NODE_T == []:
            print 'point not found'
            return []
        PT = POINT_X.data
        next_cd = (cd + 1) % self.dim
        if PT == NODE_T.data:
            if NODE_T.right != []:
                NODE_T = self.find_min(NODE_T.right, cd, next_cd)
                NODE_T.right = self.delete(NODE_T, NODE_T.right, next_cd)
            elif NODE_T.left != []:
                NODE_T = self.find_min(NODE_T.left, cd, next_cd)
                NODE_T.right = self.delete(NODE_T, NODE_T.left, next_cd)
            else:
                NODE_T = []
        elif PT[cd] < NODE_T.data[cd]:
            NODE_T.left = self.delete(POINT_X, NODE_T.left, next_cd)
        else:
            NODE_T.right = self.delete(POINT_X, NODE_T.right, next_cd)
        return NODE_T

    def print_in_order(self, NODE, given):
        if NODE == []:
            return
        if NODE.particle != given:
            R = math.hypot(NODE.particle.x - given.x, NODE.particle.y - given.y)
            Acceleration = given.acceleration
            val = NODE.particle.mass * (NODE.L / R) ** 2 / R
            if val <= self.alpha * Acceleration:
                P = Particle((NODE.center[0], NODE.center[1]), NODE.size, NODE.mass)
                given.attract(P)
            else:
                given.attract(NODE.particle)
        self.print_in_order(NODE.left, given)
        self.print_in_order(NODE.right, given)

    def DEL(self, POINT):
        self.root = self.delete(POINT, self.root, 0)
        return self.root


class Environment:

    def __init__(self, (width, height)):
        self.tree = K_D_tree(2, 3)
        self.width = width
        self.height = height
        self.particles = []
        self.colour = (255, 255, 0)
        self.mass_of_air = 0.2
        self.elasticity = 0.75
        self.acceleration = (0, 0)
        self.particle_functions1 = []
        self.particle_functions2 = []
        self.function_dict = {'move': (1, lambda p: p.move()),
         'combine': (2, lambda p1, p2: combine(p1, p2)),
         'attract': (2, lambda p1, p2: p1.attract(p2))}

    def addFunctions(self, function_list):
        for func in function_list:
            n, f = self.function_dict.get(func, (-1, None))
            if n == 1:
                self.particle_functions1.append(f)
            elif n == 2:
                self.particle_functions2.append(f)
            else:
                print 'No such function: %s' % f

        return None

    def addParticles(self, n = 1, **kargs):
        for i in range(n):
            size = kargs.get('size', random.randint(10, 20))
            mass = kargs.get('mass', random.randint(100, 10000))
            x = kargs.get('x', random.uniform(size, self.width - size))
            y = kargs.get('y', random.uniform(size, self.height - size))
            particle = Particle((x, y), size, mass)
            particle.speed = kargs.get('speed', random.random())
            particle.angle = kargs.get('angle', random.uniform(0, math.pi * 2))
            particle.colour = kargs.get('colour', (0, 0, 255))
            particle.drag = (particle.mass / (particle.mass + self.mass_of_air)) ** particle.size
            self.tree.ins(particle, particle.mass)
            self.particles.append(particle)

    def update(self):
        for i, particle in enumerate(self.particles):
            particle.move()
            for particle2 in self.particles[i + 1:]:
                combine(particle, particle2)

            self.tree.print_in_order(self.tree.root, particle)

        self.tree = K_D_tree(2, 3)
        for particle in self.particles:
            self.tree.ins(particle, particle.mass)
