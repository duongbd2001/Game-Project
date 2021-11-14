import pygame,sys,random   # (pygame: thu vien cua python, sys:sua loi system  not initialized , random :bat ky)
def draw_floor():  #ham tao 2 san de chay trong khung hinh, tranh loi dut quang san
	screen.blit(floor,(floor_x_pos,650)) #san chay theo khung hinh
	screen.blit(floor,(floor_x_pos+432,650)) #san chay theo khung hinh, cong them de chay lien tucc
def create_pipe():
	random_pipe_pos=random.choice(pipe_height) # chon chieu cao ngau nhien cua ong tu list pipe_height
	bottom_pipe=pipe_surface.get_rect(midtop=(500,random_pipe_pos))  #do dai cua ong xuat hien o duoi la ngau nhien
	top_pipe=pipe_surface.get_rect(midtop=(500,random_pipe_pos-750))
	return bottom_pipe,top_pipe # ham tao ong
def move_pipe(pipes): # ham de di chuyen ong
	for pipe in pipes:
		pipe.centerx  -= 3       #lay nhung cai ong dc tao ra va di chuyen sang ben trai(toc do di chuyen cua ong)
	return pipes
def draw_pipe(pipes): #ham ve ong
	for pipe in pipes:
		if pipe.bottom>= 600:  #neu lon hon chieu dai cua so game, thi la ong o duoi, tranh bi nguoc ong
			screen.blit(pipe_surface,pipe)
		else:
			flip_pipe=pygame.transform.flip(pipe_surface,False,True)   # False: ko lap theo truc nam ngang, True: lap theo truc y(nam doc)
			screen.blit(flip_pipe,pipe)
def check_collison(pipes) :  #ham kiem tra va cham vao ong va roi xuong
	for pipe in pipes:                   
		if bird_rect.colliderect(pipe): # chim va cham vao cot
			hit_sound.play()  # khi chim va cham cot thi se xuat hiem an thanh
			return False  # se chuyen sang man hinh ket thuc neu va cham ong
	if bird_rect.top<=15 or bird_rect.bottom>=650: #chim rot xuong hoac bay cao qua
		hit_sound.play()
		return False      #  se chuyen sang man hinh ket thuc neu rot xuong san hoac bay cao
	return True
def rotate_bird(bird1): #ham xoay chim
	new_bird=pygame.transform.rotozoom(bird1,-bird_movement*3,1)   #xoay cua con chim xuong
	return new_bird
def bird_animation():  #  ham tao hieu ung dap canh cho chim
	new_bird= bird_list[bird_index]
	new_bird_rect=new_bird.get_rect(center=(100,bird_rect.centery))
	return new_bird, new_bird_rect
def score_display(game_state):  #ham de hien thi 2 diem
	if game_state=='main game': #nghia la tro choi dang hoat dong
		score_surface=game_font.render(str(int(score)),True,(255,255,255)) #de load phong chu trong pygame,(255,255,255:mau trang)
		score_rect=score_surface.get_rect(center=(216,100))   # tao rect cho o chu(cho o vi tri turng tam)
		screen.blit(score_surface,score_rect)     # ve 2 gia tri score_surface, score_rect len man hinh

	if game_state=='game_over':   #nghia la tro choi ket thuc
	    #hien thi diem
		score_surface=game_font.render(f'Score :{int(score)}',True,(255,255,255)) 
		score_rect=score_surface.get_rect(center=(216,100))   
		screen.blit(score_surface,score_rect)
        #hien thi diem cao
		high_score_surface=game_font.render(f'High Score :{int(high_score)}',True,(255,255,255)) 
		high_score_rect=high_score_surface.get_rect(center=(216,630))   # 610: de high score cach score 1 khoang nhat dinh(gan san), cho nay de chinh vi tri high score
		screen.blit(high_score_surface,high_score_rect)     
def update_score(score,high_score):  # ham de cap nhat diem
	if score>high_score:  #high_score luc dau bang 0
		high_score=score
	return high_score

pygame.mixer.pre_init()  # chinh gia tri am thanh ve thich hop voi pygame hon
pygame.init()  #de su dung cac ham cua pygame
screen=pygame.display.set_mode((432,768)) # tao cua so pygame
clock=pygame.time.Clock()
game_font=pygame.font.Font('04B_19.ttf',40)   #phong chu
# tao cac bien cho tro choi
gravity=0.25      #trong luc cua chim 
bird_movement=0   # di chuyen cua chim
game_active=True  # xet hoat dong cua game, neu ma sang False thi game ket thuc
score=0  #lucs bat dau diem bang 0
high_score=0  #diem cao
#chen man hinh bat dau

#chen background
bg=pygame.image.load('Images/background-night.png').convert()   # lay hinh anh tu file
bg=pygame.transform.scale2x(bg)  # nhan doi background, chiem het khung hinh game

#chen san
floor=pygame.image.load('Images/floor.png').convert()
floor=pygame.transform.scale2x(floor) # nhan doi san, phu hop voi khung hinh
floor_x_pos=0  # vi tri ban dau cua san

#tao chim(chim xoay khi di chuyen)
bird_down=pygame.transform.scale2x(pygame.image.load('Images/yellowbird-downflap.png').convert_alpha())
bird_mid=pygame.transform.scale2x(pygame.image.load('Images/yellowbird-midflap.png').convert_alpha())
bird_up=pygame.transform.scale2x(pygame.image.load('Images/yellowbird-upflap.png').convert_alpha())
bird_list=[bird_down,bird_mid,bird_up]  #0,1,2
bird_index=0   # dieu chinh canh
bird=bird_list[bird_index]
bird_rect= bird.get_rect(center=(100,384))
#tao timer cho bird
birdflap=pygame.USEREVENT+1  #(USEREVENT+1 : muon cho pygame biet Event thu 2, danh cho con chim)
pygame.time.set_timer(birdflap,200)  # 200 mili giay 
#tao ong
pipe_surface=pygame.image.load('Images/obstacle.png').convert()
pipe_surface=pygame.transform.scale2x(pipe_surface) 
pipe_list=[]  # list cac chuong ngai vat

#tao timer
spawnpipe=pygame.USEREVENT
pipe_height=[200,300,400]
pygame.time.set_timer(spawnpipe,1200)  # sau 1,2 s thi se tao ra 1 ong moi
#tao man hinh ket thuc
game_over_surface=pygame.transform.scale2x(pygame.image.load('Images/gameover.png').convert_alpha())
game_over_rect= game_over_surface.get_rect(center=(216,384))  #chi so se bang 1 nua cua so game
#chen am thanh(#lenh de chen am thanh:pygame.mixed.Sound))
flap_sound=pygame.mixer.Sound('sound/sfx_wing.wav')  #chen tieng vo canh cua chim
hit_sound=pygame.mixer.Sound('sound/sfx_die.wav')  # chen am thanh khi dam trung cot
score_sound=pygame.mixer.Sound('sound/sfx_point.wav')  #chen am thanh khi duoc diem
score_sound_countdown=100
#while loop cua tro choi
while True:
	for event in pygame.event.get():
		if event.type== pygame.QUIT:
			pygame.quit()
			sys.exit()
		if event.type== pygame.KEYDOWN :   #khi co 1 phim vao dc an xuong thi chim bay len
			if event.key==pygame.K_SPACE and game_active: # khi ma game hoat dong, nhan space de choi
				bird_movement=0
				bird_movement=-6           # trong pygame muon di len phai -y
				flap_sound.play()           # khi nhan phim thi am thanh vo canh phat ra
			if event.key==pygame.K_SPACE and game_active==False: # khi ma game ket thuc
				game_active=True # kich hoat lai game
				pipe_list.clear()  # reset lai nhung cai ong  khi chuan bi bat dau
				bird_rect.center= (100,384)  # reset lai vi tri chim
				bird_movement=0               # reset lai buoc di chuyen cua chim
				score=0  #reset diem khi sau khi thua

		if event.type==spawnpipe:
			pipe_list.extend(create_pipe()) 
		if event.type== birdflap:
			if bird_index<2:
				bird_index+=1
			else:
				bird_index=0
			bird,bird_rect=bird_animation()
			
		    
	screen.blit(bg,(0,0))  #chen hinh anh vao khung hinh(toa do 0,0)  
	if game_active:   # neu game _active hoat dong(=True) thi tinh nag cua chim va ong moi duoc kich hoat
		bird_movement+=gravity   # di chuyen con chim
		bird_rect.centery+=bird_movement
		rotated_bird=rotate_bird(bird)
		screen.blit(rotated_bird,bird_rect)   #chen chim vao hinh anh
		game_active = check_collison(pipe_list)  # khi chim va cham cai ong, se chuyen sang ket thuc
		#ong
		pipe_list=move_pipe(pipe_list) # lay tat ca cac ong trong list va di chuyen va tra lai pine list moi
		draw_pipe(pipe_list)
		score+=0.01  # bay duoc cang lau thi cang cong diem, thay vi bay qua ong ms dc cong diem	
		score_display('main game')  # khi tro choi active(hoat dong) thi se chi in ra diem
		score_sound_countdown -=1
		if score_sound_countdown<=0:  # moi lan bay va ghi duoc 1 diem la co am thanh
			score_sound.play()
			score_sound_countdown=100
	else:
		screen.blit(game_over_surface,game_over_rect)
		high_score=update_score(score,high_score)
		score_display('game_over') # khi ket thuc thi se hien ra diem va diem cao
		pipe_move = 0

	if game_active:
		#san
		floor_x_pos-=1  # di chuyen lui lai ben trai
		draw_floor()  # goi ham de chay san
		if floor_x_pos<=-432:  #sau khi san thu 2 chay xong thi san thu nhat chay len, thay san thu 2, tranh bi loi
			floor_x_pos=0 
	else:
		floor_x_pos -= 0
		draw_floor()
	pygame.display.update()  # de cua so game hien len man hinh
	clock.tick(120)
