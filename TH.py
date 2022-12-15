
import pygame, sys, time

pygame.init()
pygame.display.set_caption("Tours de Hanoi")
screen = pygame.display.set_mode((700, 500))
clock = pygame.time.Clock()

jeu_termine = False
fps = 60
#music
w=pygame.mixer.Sound('win.mp3')
m=pygame.mixer.music.load('click.mp3')

# Les variables:
pas = 0
n_disks = int(input("Donner le nbre de diques :"))
disks = []
towers_midx = [120, 320, 520]
pointing_at = 0
floating = False
floater = 0

# couleurs:
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
gold = (239, 229, 51)
blue = (78, 162, 196)
grey = (170, 170, 170)
green = (77, 206, 145)
# class_bouton
class bouton() :
    def __init__ (self,x,y,image):
        self.image=image
        self.rect=self.image.get_rect()
        self.rect.topleft =(x,y)
        self.clicked=False
    def draw(self):
        action=False
        screen.blit(self.image,(self.rect.x,self.rect.y))
        pos=pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0]==1 and self.clicked==False:
                self.clicked = True
                action = True
        return action

#image boutons
start= pygame.image.load('startb.jpg').convert_alpha()
reset= pygame.image.load('resetb.jpg').convert_alpha()
font=pygame.image.load('thhh.png').convert_alpha()

#boutons
startB=bouton(230,422,start)
resetB=bouton(10,50,reset)

def importation_texte(screen, text, midtop,font=None, font_name=None, size=None, color=(255, 0, 0)):
    if font is None:  # font option is provided to save memory if font is
        font = pygame.font.SysFont(font_name, size)  # font du jeu
    font_surface = font.render(text, True, color)
    font_rect = font_surface.get_rect()
    font_rect.midtop = midtop
    screen.blit(font_surface, font_rect)

def game_over():  # game over screen
    global screen, pas
    screen.fill(white)
    importation_texte(screen, 'VAINQUEUUUUR !', (320, 200), font_name='sans serif', size=72, color=gold)
    importation_texte(screen, 'VOS PAS : ' + str(pas), (320, 250), font_name='mono', size=30, color=black)

    pygame.display.flip()
    time.sleep(3)  # wait for 2 secs
    pygame.quit()  # pygame exit
    sys.exit()  # console exit


def Tours():
    global screen
    for xpos in range(40, 460 + 1, 200):
        pygame.draw.rect(screen, blue, pygame.Rect(xpos, 400, 160, 20))
        pygame.draw.rect(screen, black, pygame.Rect(xpos + 75, 200, 10, 200))
    importation_texte(screen, 'Depart', (towers_midx[0], 150), font_name='mono', size=14, color=black)
    importation_texte(screen, 'Milieu', (towers_midx[1], 150), font_name='mono', size=14, color=black)
    importation_texte(screen, 'Arrivée', (towers_midx[2], 150), font_name='mono', size=14, color=black)


def make_disks():
    global n_disks, disks
    disks = []
    height = 20
    ypos = 397 - height
    width = n_disks * 30
    for i in range(n_disks):
        disk = {}
        disk['rect'] = pygame.Rect(0, 0, width, height)
        disk['rect'].midtop = (120, ypos)
        disk['val'] = n_disks - i
        disk['tower'] = 0
        disks.append(disk)
        ypos -= height + 3
        width -= 23


def disques():
    global screen, disks
    for disk in disks:
        pygame.draw.rect(screen, gold, disk['rect'])
    return


def pointeur():
    ptr_points = [(towers_midx[pointing_at] -3, 440), (towers_midx[pointing_at] + 7, 440),
                  (towers_midx[pointing_at], 433)]
    pygame.draw.polygon(screen, red, ptr_points)
    return


def check_won():
    global disks
    over = True
    for disk in disks:
        if disk['tower'] != 2:
            over = False
    if over:
        time.sleep(0.2)
        w.play()
        game_over()


def reset():
    global pas, pointing_at, floating, floater
    pas = 0
    pointing_at = 0
    floating = False
    floater = 0
    #menu_screen()
    make_disks()
    pygame.mixer.music.play(-1)


#menu_screen()
make_disks()
# main game loop:
while not jeu_termine:


    importation_texte(screen, 'Inserer le nbre de disque:', (320, 220), font_name='sans serif', size=30,
                      color=red)
    importation_texte(screen, str(n_disks), (320, 250), font_name='sans serif', size=40, color=black)
    for event in pygame.event.get():
        clock.tick(60)
        if event.type == pygame.QUIT:
                jeu_termine= True

        if event.type == pygame.KEYDOWN : #lorceque on appuie sur le boutton
                pygame.mixer.music.play(1)
                if event.key == pygame.K_ESCAPE:
                    reset()
                if event.key == pygame.K_0:
                    jeu_termine = True
                if event.key == pygame.K_d :
                    pointing_at = (pointing_at+1)%3
                    if floating:
                        disks[floater]['rect'].midtop = (towers_midx[pointing_at], 100)
                        disks[floater]['tower'] = pointing_at
                if event.key == pygame.K_q:
                    pointing_at = (pointing_at-1)%3
                    if floating:
                        disks[floater]['rect'].midtop = (towers_midx[pointing_at], 100)
                        disks[floater]['tower'] = pointing_at
                if event.key == pygame.K_z and not floating:
                    for disk in disks[::-1]:
                        if disk['tower'] == pointing_at:
                            floating = True
                            floater = disks.index(disk)
                            disk['rect'].midtop = (towers_midx[pointing_at], 100)
                            break
                if event.key == pygame.K_s and floating:
                    for disk in disks[::-1]:
                        if disk['tower'] == pointing_at and disks.index(disk)!=floater:
                            if disk['val']>disks[floater]['val']:
                                floating = False
                                disks[floater]['rect'].midtop = (towers_midx[pointing_at], disk['rect'].top-23)
                                pas += 1
                            break
                    else:
                        floating = False
                        disks[floater]['rect'].midtop = (towers_midx[pointing_at], 400-23)
                        pas += 1
        screen.fill(white)

        screen.blit(font,(0,0))


        if resetB.draw():
            reset()



        Tours()
        disques()
        pointeur()
        #importation_texte(screen, 'Nbre de pas: '+str(steps), (320, 450), font_name='mono', size=30, color=black)
        importation_texte(screen, 'Tours de Hanoi', (340, 20), font_name='sans serif', size=90, color=black)
        importation_texte(screen, 'Tours de Hanoi', (337, 23), font_name='sans serif', size=90, color=red)
        pygame.display.flip()
        if not floating:
            check_won()
        clock.tick(fps)
