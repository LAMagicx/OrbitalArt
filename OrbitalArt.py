import pygame
from math import *


def maps(value,istart,istop,ostart,ostop):
    return ostart+(ostop-ostart)*((value-istart)/(istop-istart))

def display(value,pos,words):
    text = smallfont.render(words+str(value), True, white)
    screen.blit(text, pos)

def pause():
    paused = True
    while paused:
        target = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p: paused = False
                elif event.key == pygame.K_ESPACE: pygame.quit()
        # screen.fill(grey)
        pygame.display.update()
        clock.tick(5)

def limit(x,m):
    if x > m:
        if x != 0 and x != 1:
            x /= x
        x *= m

    return x

class PVector:

    def __init__(self,x,y):
            self.x = x
            self.y = y

    def fromAngle(angle):
        return PVector(cos(angle), sin(angle))

    def getAngle(self):
        return atan2(self.y, self.x)

    def mag(self):
            return sqrt(self.x*self.x + self.y*self.y)

    def plus(self,v):
            self.x += v.x
            self.y += v.y

    def sub(self,v):
            self.x -= v.x
            self.y -= v.y

    def mult(self,n):
            self.x *= n
            self.y *= n

    def div(self,n):
            self.x /= n
            self.y /= n

    def dist(self,v):
            dx = self.x - v.x
            dy = self.y - v.y
            return sqrt(dx*dx + dy*dy)

    def normalize(self):
            m = self.mag()
            if m !=0 and m != 1:
                                self.div(m)

    def limit(self,maxi):
            if self.mag() > maxi:
                                self.normalize()
                                self.mult(maxi)
    
    def setMag(self,n):
            self.normalize()
            self.mult(n)

    def copy(self):
        return PVector(self.x, self.y)



class Block:

    def __init__(self, pos, m, vel = PVector(0,0), acc = PVector(0,0),c=(200,200,200)):
        self.pos = pos
        self.vel = vel
        self.acc = acc
        self.mass = pow(m/2, 4)
        self.r = m*5
        self.maxspeed = 5
        self.air_res = 1
        self.wall_res = 0.9
        self.bounce_res = 1
        self.colour = c
        self.immobile = False

    def run(self,w,h):
        self.draw()
        self.update()
        # self.walls(w,h)

    def draw(self):
        pygame.draw.circle(screen, self.colour, (int(self.pos.x), int(self.pos.y)), self.r)
        pygame.draw.circle(screen, black, (int(self.pos.x), int(self.pos.y)), self.r,2)

    def update(self):
        self.vel.plus(self.acc)
        self.pos.plus(self.vel)
        self.acc.mult(0)

    def applyForce(self, f):
        self.acc.plus(f)

    def walls(self, w,h):
        if (self.pos.x - self.r <= 0 or self.pos.x + self.r >= w):
            self.vel.x *= -self.wall_res
        elif (self.pos.y - self.r <= 0 or self.pos.y + self.r >= h):
            self.vel.y *= -self.wall_res

    def caculateVel(a,b):
        v1 = a.vel.mag()
        θ1 = atan2(a.vel.y,a.vel.x)
        m1 = a.mass

        v2 = b.vel.mag()
        θ2 = atan2(b.vel.y,b.vel.x)
        m2 = b.mass

        cpx = ((a.pos.x * b.r) + (b.pos.x * a.r))/(a.r+b.r)
        cpy = ((a.pos.y * b.r) + (b.pos.y * a.r))/(a.r+b.r)
        ϕ = atan2(a.pos.y - cpy, a.pos.x - cpx)

        vx = (((v1 * cos(θ1 - ϕ) * (m1 - m2)) + (2 * m2 * v2 * cos(θ2 - ϕ)))/(m1 + m2)) * cos(ϕ) + v1 * sin(θ1 - ϕ) * cos(ϕ + pi/2)
        vy = (((v1 * cos(θ1 - ϕ) * (m1 - m2)) + (2 * m2 * v2 * cos(θ2 - ϕ)))/(m1 + m2)) * sin(ϕ) + v1 * sin(θ1 - ϕ) * sin(ϕ + pi/2)
        
        return PVector(vx, vy)

    def bounce(a,b):
        d = a.pos.dist(b.pos)
        a_new_vel = a.vel
        b_new_vel = b.vel
        
        if (d > (a.r + b.r)):
            force = G * ((a.mass * b.mass)/d)
            y,x = b.pos.y - a.pos.y, b.pos.x - a.pos.x

            a_new_vel_x = a.vel.x + cos(atan2(y,x)) * force
            a_new_vel_y = a.vel.y + sin(atan2(y,x)) * force
            b_new_vel_x = b.vel.x + cos(atan2(-y,-x)) * force
            b_new_vel_y = b.vel.y + sin(atan2(-y,-x)) * force


            if not a.immobile: a_new_vel = PVector(a_new_vel_x, a_new_vel_y)
            if not b.immobile: b_new_vel = PVector(b_new_vel_x, b_new_vel_y)

            
        elif (d <= (a.r + b.r)):

            if not a.immobile: a_new_vel = Block.caculateVel(a,b)
            if not b.immobile: b_new_vel = Block.caculateVel(b,a)

        a.vel = a_new_vel
        b.vel = b_new_vel
            
        

pygame.init()
w,h = 400,400
screen = pygame.display.set_mode((w,h))
clock = pygame.time.Clock()
smallfont = pygame.font.SysFont("comicsansms", 10)

grey = [146,149,145]
white = [255,255,255]
red = [229,0,0]
green = [21, 176, 26]
blue = [3, 67, 223]
black = [0,0,0]
G = 1 #45# is gold

r = int(w/2 - 50)
p1 = PVector.fromAngle(0)
p1.mult(r)
p2 = PVector.fromAngle((2*pi)/3)
p2.mult(r)
p3 = PVector.fromAngle(-(2*pi)/3)
p3.mult(r)

v1 = PVector.fromAngle(0 - pi/2)
v2 = PVector.fromAngle((2*pi)/3 - pi/2)
v3 = PVector.fromAngle(-(2*pi)/3 - pi/2)

p1.plus(PVector(int(w/2),int(w/2)))
p2.plus(PVector(int(w/2),int(w/2)))
p3.plus(PVector(int(w/2),int(w/2)))

b1 = Block(p1,1,v1,c=red)
b2 = Block(p2,1,v2,c=green)
b4 = Block(p3,1,v3,c=blue)

b3 = Block(PVector(int(w/2),int(w/2)),4,c=black)
b3.immobile = True

rapid = False
n = 0
FPS_base = 0
FPS = 300
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: pygame.quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE: pygame.quit()
            if event.key == pygame.K_p: pause()
            if event.key == pygame.K_c:
                rapid = True
            if event.key == pygame.K_f: FPS = 0
            if event.key == pygame.K_SPACE:  # reset
                r = int(w/2 - 50)
                p1 = PVector.fromAngle(0)
                p1.mult(r)
                p2 = PVector.fromAngle((2*pi)/3)
                p2.mult(r)
                p3 = PVector.fromAngle(-(2*pi)/3)
                p3.mult(r)

                v1 = PVector.fromAngle(0 - pi/2)
                v2 = PVector.fromAngle((2*pi)/3 - pi/2)
                v3 = PVector.fromAngle(-(2*pi)/3 - pi/2)

                p1.plus(PVector(int(w/2),int(w/2)))
                p2.plus(PVector(int(w/2),int(w/2)))
                p3.plus(PVector(int(w/2),int(w/2)))

                b1 = Block(p1,1,v1,c=red)
                b2 = Block(p2,1,v2,c=green)
                b4 = Block(p3,1,v3,c=blue)

                b3 = Block(PVector(int(w/2),int(w/2)),4,c=black)
                b3.immobile = True
                screen.fill(black)

            if event.key == pygame.K_o:
                print(G)

            if event.key == pygame.K_UP:
                FPS += 50
            if event.key == pygame.K_DOWN:
                FPS -= 50
            if event.key == pygame.K_RIGHT: G += 1
            if event.key == pygame.K_LEFT: G -= 1
            if event.key == pygame.K_s: FPS = 0
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_c:
                rapid = False
            if event.key == pygame.K_s: FPS = 300
            
    # screen.fill(grey)

    b1.run(w,h)
    b2.run(w,h)
    b3.run(w,h)
    b4.run(w,h)
    Block.bounce(b1,b2)
    Block.bounce(b1,b3)
    Block.bounce(b1,b4)
    Block.bounce(b2,b3)
    Block.bounce(b2,b4)
    Block.bounce(b4,b3)





    n += 1
    clock.tick(FPS)
    fps = round(clock.get_fps())


    if rapid:
        if n%500 == 0:
            G += 1

    pygame.display.update()
