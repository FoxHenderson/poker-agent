from game import *
import pygame
g = Game()
pygame.init()
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
window = pygame.display.set_mode((600,600))
def CreateCentreCards(window, cards):
    centrecarddiv = pygame.Rect(SCREEN_WIDTH, 0, SCREEN_WIDTH/4, 150)
    for i in range(0, len(cards)):
        card = cards[i]
        print(card)
        if card == None:
            imp = pygame.image.load("blank.png").convert()
            imp = pygame.transform.scale(imp, (54, 81))
            centrecarddiv.blit(imp, (300 + 60*(i-1), 200))
    pygame.display.flip()


#def FlipCardButton(window):
    


CreateCentreCards(window,g.table.get_cards())
#img = tk.PhotoImage(file="blank.png")
#img_label = tk.Label(window, image=img)
#img_label.grid(column=1)
#
#img2 = tk.PhotoImage(file="blank.png")
#img_label2 = tk.Label(window, image=img)
#img_label2.grid(column=2)