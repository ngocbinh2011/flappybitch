import pygame
import random
pygame.init()

red = [255,0,0]
blue = [0,0,255]
black = [0,0,0]
white =[255, 255, 255]
font_start = pygame.font.SysFont(None, 25)
font_end = pygame.font.SysFont(None, 30)
font_score = pygame.font.SysFont(None, 50)
bg = pygame.image.load("bg.png")
img_base = pygame.image.load("base.png")
display_width = bg.get_width()
display_height = bg.get_height()
pygame.display.set_caption("Your bird<3")
game_display = pygame.display.set_mode([display_width, display_height])
image_game_over = pygame.image.load("gameover.png")
image_game_start = pygame.image.load("message.png")
point_music = pygame.mixer.Sound("point.wav")
hit_music = pygame.mixer.Sound("hit.wav")
bg_music = pygame.mixer.Sound("piano.wav")
bg_music.play()
bg_music.set_volume(0.2) 
play_music = True
clock = pygame.time.Clock()

img_score = [pygame.image.load("0.png"), pygame.image.load("1.png"), pygame.image.load("2.png"),\
			pygame.image.load("3.png"), pygame.image.load("4.png"), pygame.image.load("5.png"),\
			pygame.image.load("6.png"), pygame.image.load("7.png"), pygame.image.load("8.png"),\
			pygame.image.load("9.png")]

class make_tube():
	img_bottom_tube = [pygame.image.load("bottomtube.png"), pygame.image.load("bot+34.png"),\
					pygame.image.load("bot-40.png"), pygame.image.load("bot+92.png"),\
					pygame.image.load("bot+67.png"), pygame.image.load("bot-100.png"),\
					pygame.image.load("bot-35.png"), pygame.image.load("bot-78.png"),\
					pygame.image.load("bot+92.png")]

	img_top_tube = 	[pygame.image.load("toptube.png"), pygame.image.load("top-34.png"),\
					pygame.image.load("top+40.png"), pygame.image.load("top-92.png"),\
					pygame.image.load("top-67.png"), pygame.image.load("top+100.png"),\
					pygame.image.load("top+35.png"), pygame.image.load("top+78.png"),\
					pygame.image.load("top-92.png")]
	tube_width = img_top_tube[0].get_width()

	def __init__(self, x_tube, y_tube_top, y_tube_bottom, check, x_change, y_change):
		self.x_tube = x_tube
		self.y_tube_top = y_tube_top
		self.y_tube_bottom = y_tube_bottom
		self.check = check
		self.distance = 290
		self.x_change = x_change
		self.y_change = y_change
		self.tube_dem = 0
		self.value_change = self.x_change
		self.view_tube = [8,7,6,5,4,3,2,1,0]
		self.sum_tube_change = 0

	def draw_tube(self): 
		if self.check:
			self.x_change = 180
			for i in range(20):
				self.img_top_tube.reverse()
				self.img_bottom_tube.reverse()
				for j in range(len(self.img_top_tube)):
					height_plus = self.img_top_tube[j].get_height()
					game_display.blit(self.img_top_tube[j], [self.x_tube+self.x_change, self.y_tube_top])
					game_display.blit(self.img_bottom_tube[j], [self.x_tube+self.x_change,\
										height_plus+self.y_change])
					self.x_change+= self.distance			

class make_bird():
	img_bird = 	[pygame.image.load("midbird.png"), pygame.image.load("midbird.png"),\
	 			pygame.image.load("midbird.png"), pygame.image.load("midbird.png"),\
	 			pygame.image.load("upbird.png"), pygame.image.load("upbird.png"),\
				pygame.image.load("upbird.png"), pygame.image.load("upbird.png"),\
				pygame.image.load("downbird.png"), pygame.image.load("downbird.png"),\
				pygame.image.load("downbird.png"), pygame.image.load("downbird.png")]
	bird_width = img_bird[0].get_width()
	bird_height = img_bird[0].get_height()

	def __init__(self, x_bird, y_bird, y_change_bird, step, t, frame_bird):
		self.x_bird = x_bird
		self.y_bird = y_bird
		self.y_change_bird = y_change_bird
		self.step = step
		self.check_space = False
		self.t = 0
		self.frame_bird = frame_bird
		self.frame_change = 0
		self.check_collision_first = False

	def draw_bird(self):
		if self.frame_change < self.frame_bird:
			game_display.blit(self.img_bird[self.frame_change % 12], [int(self.x_bird), int(self.y_bird)])	
			self.frame_change += 1	
		else:
			self.frame_change = 0


	def jump_bird(self):
		if self.check_space:
			self.t = 0 
			self.y_change_bird = -5
		else:
			self.y_change_bird = self.t * 0.35
			self.t += 0.5
		self.y_bird += self.y_change_bird

def background_scroll(x, y):
	global bgX
	bgX += x
	if bgX >= display_width//5:
		tube.check= True
	bgX %= display_width
	game_display.blit(img_base, [-bgX, display_height-20])
	game_display.blit(img_base, [-bgX+display_width, display_height-20])

def tube_scroll(x, y):
	global sum_tube_change
	tube.x_tube -= x
	tube.sum_tube_change += x
	tube.draw_tube()

def check_collision():
	global tube, game_over, run, score
	if not bird.check_collision_first:
		max_tube = 6*display_width//5 + tube.value_change - display_width//6 + tube.tube_width
		min_tube = 6*display_width//5 + tube.value_change - display_width//6
		if tube.sum_tube_change <= max_tube and tube.sum_tube_change >= min_tube:					
			tube_collision_top = tube.img_top_tube[tube.view_tube[0]].get_height()
			if bird.y_bird + bird.bird_height + 2 >= tube_collision_top + tube.y_change\
				or bird.y_bird - 2 <= tube_collision_top:
				hit_music.play()
				run = Falsegame_out = False
				game_over = True
				pygame.time.delay(800)
		if tube.sum_tube_change > max_tube:
			point_music.play()
			tube.sum_tube_change = 0
			score += 1
			tube.tube_dem += 1
			bird.check_collision_first = True
	else:
		if tube.sum_tube_change <= tube.distance and tube.sum_tube_change >= tube.distance-tube.tube_width:
			tube_collision_top = tube.img_top_tube[tube.view_tube[tube.tube_dem]].get_height()
			if bird.y_bird + bird.bird_height + 2 >= tube_collision_top + tube.y_change\
				or bird.y_bird - 2 <= tube_collision_top:
				hit_music.play()
				run = False
				game_over = True
				pygame.time.delay(800)
		if tube.sum_tube_change > tube.distance:
			point_music.play()
			tube.sum_tube_change = 0
			score += 1
			tube.tube_dem += 1
			if tube.tube_dem == len(tube.view_tube):
				tube.view_tube.reverse()
				tube.tube_dem = 0

def fix_score():
	global value, score
	value = str(score)
	add_core_x= -20
	for i in value:
		game_display.blit(img_score[int(i)], [display_width//2 + add_core_x, display_height//7])
		add_core_x += 22
	pygame.display.update()

def music_control():
	global play_music
	KEY = pygame.key.get_pressed()
	if KEY[pygame.K_m]:
		play_music= not play_music
		pygame.time.delay(100)
	if play_music:
		pygame.mixer.unpause()
	else:
		pygame.mixer.pause()

def pause_game():
	global check_pause, run, game_out
	check_pause = True
	while check_pause:
		for evt_pause in pygame.event.get():
			if evt_pause.type == pygame.QUIT:
				run = False
				game_out = True
				check_pause = False
			if evt_pause.type == pygame.KEYDOWN:
				if evt_pause.key == pygame.K_p:
					check_pause = False




def is_start():
	global game_out, start
	start = False
	text_start = font_start.render("Press any key to start", True, black)
	text_tutorial = font_start.render("SPACE to jump/ M to turn on/off music", True, black)
	while not start:
		game_display.blit(bg, [0,0])
		game_display.blit(image_game_start, [100, 100])
		game_display.blit(text_start, [display_width//4 ,display_height-50])
		game_display.blit(text_tutorial, [display_width//10, display_height-30])
		pygame.display.update()
		for ev in pygame.event.get():
			if ev.type == pygame.QUIT:
				start = True
				game_out = True
			if ev.type == pygame.KEYDOWN:
				start = True
				game_out = False

def game_end():
	global game_over, run, game_out, score, check_pause
	text_end = font_end.render("Press C to continue/ Q to quit", True, black)
	pygame.time.delay(50)
	check_pause = False
	game_display.blit(bg, [0,0])
	game_display.blit(image_game_over, [display_width//4, display_height//3])
	game_display.blit(text_end, [display_width//10, display_height//3-50])
	val = str(score)
	add_core_x= -20
	music_control()
	for i in val:
		game_display.blit(img_score[int(i)], [display_width//2 + add_core_x, display_height//2])
		add_core_x += 22
	pygame.display.update()
	pygame.display.update()
	pygame.time.delay(100)
	for evt in pygame.event.get():
		if evt.type == pygame.QUIT:
			game_over = False
			game_out = True
		if evt.type == pygame.KEYDOWN:
			if evt.key == pygame.K_c:
				game_loop()
			if evt.key == pygame.K_q:
				game_over = False
				game_out = True
	pygame.display.update()

def game_loop():
	global game_over, game_out, bgX, run, score, bird, tube, check_pause
	score = 0
	game_over = False
	game_out = False
	run = True
	bgX=0
	check_pause = False
	bird = make_bird(display_width//6, display_height//2, 2, 5, 0, 12)
	tube = make_tube(6*display_width//5, 0, 0, False, 180, 100)
	pygame.display.update()
	while not game_out:
		while game_over:
			game_end()
		while run:
			game_display.blit(bg, [0,0])
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					run = False
					game_out = True
				if event.type == pygame.KEYUP:
					if event.key == pygame.K_SPACE:
						bird.check_space = False
			keys = pygame.key.get_pressed()
			if keys[pygame.K_SPACE]:
				bird.check_space = True
			if keys[pygame.K_p]:
				pause_game()
			background_scroll(3,0)	
			bird.jump_bird()
			tube_scroll(3,0)
			bird.draw_bird()
			check_collision() 
			fix_score()
			music_control()

			clock.tick(60)
			pygame.display.update()

is_start()
if not game_out:
	game_loop()
pygame.quit()