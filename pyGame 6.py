# TODO: add restart or end-game

import pygame

pygame.init()

win = pygame.display.set_mode((500, 480))
pygame.display.set_caption("First Game")

# Walking sprites and background
walkRight = [pygame.image.load('images/R1.png'), pygame.image.load('images/R2.png'), pygame.image.load('images/R3.png'), pygame.image.load(
	'images/R4.png'), pygame.image.load('images/R5.png'), pygame.image.load('images/R6.png'), pygame.image.load(
	'images/R7.png'), pygame.image.load('images/R8.png'), pygame.image.load('images/R9.png')]
walkLeft = [pygame.image.load('images/L1.png'), pygame.image.load('images/L2.png'), pygame.image.load('images/L3.png'), pygame.image.load(
	'images/L4.png'), pygame.image.load('images/L5.png'), pygame.image.load('images/L6.png'), pygame.image.load(
	'images/L7.png'), pygame.image.load('images/L8.png'), pygame.image.load('images/L9.png')]
bg = pygame.image.load('images/bg.jpg')
char = pygame.image.load('images/standing.png')

clock = pygame.time.Clock()

bulletSound = pygame.mixer.Sound('sounds/bullet.wav')
hitSound = pygame.mixer.Sound('sounds/hit.wav')

pygame.mixer.music.load('sounds/music.mp3')
pygame.mixer.music.play(-1)
score = 0


class Player(object):
	def __init__(self, x, y, width, height):
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.vel = 5
		self.isJump = False
		self.jumpCount = 10
		self.left = False
		self.right = False
		self.walkCount = 0
		self.standing = True
		self.hitbox = (int(self.x + 17), int(self.y + 11), 29, 52)

	def draw(self, win):
		if self.walkCount + 1 >= 27:
			self.walkCount = 0

		if not self.standing:
			if self.left:
				win.blit(walkLeft[self.walkCount//3], (int(self.x), int(self.y)))
				self.walkCount += 1

			elif self.right:
				win.blit(walkRight[self.walkCount//3], (int(self.x), int(self.y)))
				self.walkCount += 1
		else:
			if self.right:
				win.blit(walkRight[0], (int(self.x), int(self.y)))
			else:
				win.blit(walkLeft[0], (int(self.x), int(self.y)))
		
		self.hitbox = (int(self.x + 17), int(self.y + 11), 29, 52)
		# pygame.draw.rect(win, (255,0,0), self.hitbox,2)

	def hit(self):
		self.isJump = False
		self.jumpCount = 10
		self.x = 60
		self.y = 410
		self.walkCount = 0
		font1 = pygame.font.SysFont('comicsans', 100)
		text = font1.render("-5", True, (255, 0, 0))
		win.blit(text, (250 - int(text.get_width()/2), 200))
		pygame.display.update()
		i = 0
		while i < 300:
			pygame.time.delay(10)
			i += 1
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					i = 301
					pygame.quit()


class Projectile(object):
	def __init__(self, x, y, radius, color, facing):
		self.x = x
		self.y = y
		self.radius = radius
		self.color = color
		self.facing = facing
		self.vel = 8 * self.facing

	def draw(self, win):
		pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)


class Enemy(object):
	walkRight = [pygame.image.load('images/R1E.png'), pygame.image.load('images/R2E.png'), pygame.image.load(
		'images/R3E.png'), pygame.image.load('images/R4E.png'), pygame.image.load('images/R5E.png'), pygame.image.load(
		'images/R6E.png'), pygame.image.load('images/R7E.png'), pygame.image.load('images/R8E.png'), pygame.image.load(
		'images/R9E.png'), pygame.image.load('images/R10E.png'), pygame.image.load('images/R11E.png')]
	walkLeft = [pygame.image.load('images/L1E.png'), pygame.image.load('images/L2E.png'), pygame.image.load(
		'images/L3E.png'), pygame.image.load('images/L4E.png'), pygame.image.load('images/L5E.png'), pygame.image.load(
		'images/L6E.png'), pygame.image.load('images/L7E.png'), pygame.image.load('images/L8E.png'), pygame.image.load(
		'images/L9E.png'), pygame.image.load('images/L10E.png'), pygame.image.load('images/L11E.png')]

	def __init__(self, x, y, width, height, end):
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.end = end
		self.path = [self.x, self.end]
		self.walkCount = 0
		self.vel = 3
		self.hitbox = (int(self.x + 13), int(self.y), 40, 58)
		self.health = 10
		self.visible = True

	def draw(self, win):
		self.move()
		if self.visible:
			if self.walkCount + 1 >= 33:
				self.walkCount = 0

			if self.vel > 0:
				win.blit(self.walkRight[self.walkCount//3], (self.x, self.y))
				self.walkCount += 1
			else:
				win.blit(self.walkLeft[self.walkCount//3], (self.x, self.y))
				self.walkCount += 1
			
			# health bar and hitbox
			pygame.draw.rect(win, (255,0,0), (self.hitbox[0], self.hitbox[1] - 20, 50, 10))
			pygame.draw.rect(win, (0,128,0), (self.hitbox[0], self.hitbox[1] - 20, 50 - (5*(10 - self.health)), 10))
			self.hitbox = (int(self.x + 13), int(self.y), 40, 58)
			# pygame.draw.rect(win, (255,0,0), self.hitbox,2)

	def move(self):
		if self.vel > 0:
			if self.x + self.vel < self.path[1]:
				self.x += self.vel
			else:
				self.vel = self.vel * -1
				self.walkCount = 0
		else:
			if self.x - self.vel > self.path[0]:
				self.x += self.vel
			else:
				self.vel = self.vel * -1
				self.walkCount = 0

	def hit(self):
		if self.health > 1:
			self.health -= 1
		else:
			self.visible = False
		# print("hit!")


def redrawGameWindow():
	win.blit(bg, (0, 0))
	text = font.render('Score: ' + str(score), True, (0, 0, 0))
	win.blit(text, (350, 10))
	man.draw(win)
	goblin.draw(win)
	for bullet in bullets:
		bullet.draw(win)
	pygame.display.update()


# main loop
font = pygame.font.SysFont('comicsans', 30, True)
man = Player(300, 410, 64, 64)
goblin = Enemy(0, 415, 64, 64, 450)
shootLoop = 0
bullets = []
run = True
while run:
	clock.tick(27)

	if goblin.visible:
		if man.hitbox[1] < goblin.hitbox[1] + goblin.hitbox[3] and man.hitbox[1] + man.hitbox[3] > goblin.hitbox[1]:
			if man.hitbox[0] + man.hitbox[2] > goblin.hitbox[0] and man.hitbox[0] < goblin.hitbox[0] + goblin.hitbox[2]:
				man.hit()
				score -= 5
		
	# pygame.time.delay(50) # like clock in game in ms
	if shootLoop > 0:
		shootLoop += 1
	if shootLoop > 3:
		shootLoop = 0
	# check for events (quit game - close window):
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False

	for bullet in bullets:
		if goblin.visible:
			if bullet.y - bullet.radius < goblin.hitbox[1] + goblin.hitbox[3] and bullet.y + bullet.radius > goblin.hitbox[1]:
				if bullet.x + bullet.radius > goblin.hitbox[0] and bullet.x - bullet.radius < goblin.hitbox[0] + goblin.hitbox[2]:
					hitSound.play()
					goblin.hit()
					score += 1
					bullets.pop(bullets.index(bullet))
		if 500 > bullet.x > 0:
			bullet.x += bullet.vel
		else:
			bullets.pop(bullets.index(bullet))

	keys = pygame.key.get_pressed()
	
	if keys[pygame.K_SPACE] and shootLoop == 0:
		bulletSound.play()
		if man.left:
			facing = -1
		else:
			facing = 1

		if len(bullets) < 5:
			bullets.append(Projectile(round(man.x + man.width//2), round(man.y + man.height//2), 6, (0,0,0), facing))

		shootLoop = 1

	if keys[pygame.K_LEFT] and man.x > man.vel:
		man.x -= man.vel
		man.left = True
		man.right = False
		man.standing = False

	elif keys[pygame.K_RIGHT] and man.x < (500 - man.width - man.vel):
		man.x += man.vel
		man.left = False
		man.right = True
		man.standing = False

	else:
		man.standing = True
		man.walkCount = 0

	if not man.isJump:
		if keys[pygame.K_UP]:
			man.isJump = True
			# man.right = False
			# man.left = False
			man.walkCount = 0
	else:
		if man.jumpCount >= -10:
			neg = 1
			if man.jumpCount < 0:
				neg = -1
			man.y -= (man.jumpCount ** 2) * 0.5 * neg
			man.jumpCount -= 1
		else:
			man.isJump = False
			man.jumpCount = 10

	redrawGameWindow()

pygame.quit()
