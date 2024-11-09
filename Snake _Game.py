# import Modul
import pygame
import sys
import os
import random
import math

pygame.init()
pygame.display.set_caption("My Snake Game")
pygame.font.init()
random.seed()
# we will declare global constant definitions
speed = 0.36
Snake_size = 9
Apple_size = Snake_size # i want to apple size and snake size as same
Separation = 10 # separation between two pixels
Screen_Hight = 600
Screen_Width = 800
FPS = 25
Key = {"UP" : 1, "DOWN" : 2, "LEFT" : 3, "RIGHT" : 4 }
# we will initialise screen
Screen = pygame.display.set_mode((Screen_Width, Screen_Hight),pygame.HWSURFACE)
# we have used hw surface which stands for hardware surface refers to using memory on the video card for storing
# draws as opposed to main memory
# Resources
score_font = pygame.font.Font(None,37)
score_numb_font = pygame.font.Font(None,28)
game_over_font = pygame.font.Font(None,46)
play_again_font = score_numb_font
score_msg = score_font.render("Score : ",1, pygame.Color("green"))
score_msg_size = score_font.size("Score")
background_color = pygame.Color(0,0,0) # we will fill background color as black
black = pygame.Color(0,0,0)
# for clock at the left corner
game_clock = pygame.time.Clock()
def checkCollision(posA,As ,posB , Bs):    # As is the size of a and Bs is the size of b
    if(posA.x < posB.x+Bs and posA.x+As > posB.x and posA.y < posB.y+Bs and posA.y+As > posB.y):
        return True
    return False
# to check the boundaries  here we are not limiting boundaries like 
# it can pass through screen and come from other side
def checkLimits(Snake):
    if(Snake.x>Screen_Width):
        Snake.x = Snake_size
    if(Snake.x<0): # this will be checked when some part of snake is on other side and some on opposite side
        Snake.x = Screen_Width-Snake_size
    if (Snake.y>Screen_Hight):
        Snake.y = Snake_size
    if(Snake.y < 0):   # this also same half half
        Snake.y = Screen_Hight - Snake_size

# we will make class for food of the snake let's name it as apple

class Apple:
    def __init__(self, x ,y,state):
        self.x = x
        self.y = y
        self.state = state
        self.color = pygame.color.Color("orange")     # color of food

    def draw(self,screen):
        pygame.draw.rect(screen,self.color,(self.x,self.y,Apple_size,Apple_size),0)

class segment:
    # initially snake will move in up direction
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.direction = Key["UP"]
        self.color = "white"

class snake:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.direction = Key["UP"]
        self.stack =[]   # initially it will be empty
        self.stack.append(self)
        blackBox = segment(self.x , self.y + Separation)
        blackBox.direction = Key["UP"]
        blackBox.color = "NULL"
        self.stack.append(blackBox)

# we will define moves of the snake

    def move(self):
        last_element = len(self.stack)-1
        while(last_element != 0):
            self.stack[last_element].direction = self.stack[last_element-1].direction
            self.stack[last_element].x = self.stack[last_element-1].x 
            self.stack[last_element].y = self.stack[last_element-1].y 
            last_element-=1
        if(len(self.stack)<2):
            last_segment = self
        else:
            last_segment = self.stack.pop(last_element)
        last_segment.direction = self.stack[0].direction
        if(self.stack[0].direction ==Key["UP"]):
            last_segment.y = self.stack[0].y - (speed * FPS)
        elif(self.stack[0].direction == Key["DOWN"]):
            last_segment.y = self.stack[0].y + (speed * FPS) 
        elif(self.stack[0].direction ==Key["LEFT"]):
            last_segment.x = self.stack[0].x - (speed * FPS)
        elif(self.stack[0].direction == Key["RIGHT"]):
            last_segment.x = self.stack[0].x + (speed * FPS)
        self.stack.insert(0,last_segment)

    def getHead(self):    # head of the snake 
        return(self.stack[0])   # It will be always 0 index

    # now when snake its food it will grow so for that we will add that food to stack

    def grow(self):
        last_element = len(self.stack) -1
        self.stack[last_element].direction = self.stack[last_element].direction
        if(self.stack[last_element].direction == Key["UP"]):
            newSegment = segment(self.stack[last_element].x, self.stack[last_element].y -Snake_size)
            blackBox = segment(newSegment.x , newSegment.y-Separation)
        
        elif(self.stack[last_element].direction == Key["DOWN"]):
            newSegment = segment(self.stack[last_element].x, self.stack[last_element].y +Snake_size)
            blackBox = segment(newSegment.x , newSegment.y+Separation)

        elif(self.stack[last_element].direction == Key["LEFT"]):
            newSegment = segment(self.stack[last_element].x - Snake_size, self.stack[last_element].y)
            blackBox = segment(newSegment.x - Separation , newSegment.y)
        
        elif(self.stack[last_element].direction == Key["RIGHT"]):
            newSegment = segment(self.stack[last_element].x + Snake_size, self.stack[last_element].y)
            blackBox = segment(newSegment.x + Separation , newSegment.y)

        blackBox.color = "NULL"
        self.stack.append(newSegment)
        self.stack.append(blackBox)

    def iterateSegments(self,delta):
        pass

    def setDirection(self,direction):
        if(self.direction == Key["RIGHT"] and direction == Key["LEFT"] or self.direction == Key["LEFT"] and 
                direction == Key["RIGHT"]):
            pass
        elif(self.direction == Key["UP"] and direction == Key["DOWN"] or self.direction == Key["UP"] and 
                direction == Key["DOWN"]):
            pass
        else:
            self.direction = direction

    def get_rect(self):     # get the rectangle shape 
        rect = (self.x , self.y)
        return rect

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def setX(self,x):
        self.x = x
    
    def setY(self,y):
        self.y = y

    # we will make the function of crashing when snake eats itself

    def checkCrashing(self):
        counter = 1
        while(counter < len(self.stack)-1):
            if(checkCollision(self.stack[0], Snake_size , self.stack[counter], Snake_size) and 
                        self.stack[counter].color != "NULL"):
                return True
            counter +=1
        return False

    # we will draw the snake 
    def draw(self,screen):
        pygame.draw.rect(screen,pygame.color.Color("green"), (self.stack[0].x , self.stack[0].y, 
                Snake_size, Snake_size),0)
        counter = 1
        while(counter < len(self.stack)):
            if(self.stack[counter].color == "NULL"):
                counter +=1
                continue
            pygame.draw.rect(screen , pygame.color.Color("yellow"), (self.stack[counter].x,
                self.stack[counter].y, Snake_size , Snake_size),0)
            counter +=1


# we will define keys

def getkey():
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.Key == pygame.K_UP:
                return Key["UP"]
            elif event.Key == pygame.K_DOWN:
                return Key["DOWN"]
            elif event.Key == pygame.K_LEFT:
                return Key["LEFT"]
            elif event.Key == pygame.K_RIGHT:
                return Key["RIGHT"]
            # for exit 
            elif event.Key == pygame.K_ESCAPE:
                return "exit"
            # if we want to continue playing again
            elif event.Key == pygame.K_y:
                return "yes"
            # if we don't want to play game
            elif event.Key == pygame.K_n:
                return "no"
        if event.type == pygame.QUIT:
            sys.exit(0)

def endGame():
    message = game_over_font.render("Gsme Over",1,pygame.Color("white"))
    message_play_again = play_again_font.render("Play Again ? (Y/N)",1,pygame.Color("green"))
    Screen.blit(message,(320,240))
    Screen.blit(message_play_again,(320+12,240+40))

    pygame.display.flip()
    pygame.display.update()

    mKey = getkey()
    while(mKey != "exit"):
        if(mKey == "yes"):
            main()
        elif(mKey == "no"):
            break
        mKey = getkey()
        game_clock.tick(FPS)
    sys.exit(0)

def drawScore(score):
    score_numb = score_numb_font.render(str(score),1,pygame.Color("red"))
    Screen.blit(score_msg, (Screen_Width - score_msg_size[0]-60,10))
    Screen.blit(score_numb,(Screen_Width - 45,14))

def drawGameTime(gameTime):
    game_time = score_font.render("Time:" , 1, pygame.Color("white"))
    game_time_numb = score_numb_font.render(str(gameTime/1000),1,pygame.Color("white"))
    Screen.blit(game_time,(30,10))
    Screen.blit(game_time_numb,(105,14))

def exitScreen():
    pass

def respawnApple(apples , index , sx , sy):
    radius = math.sqrt((Screen_Width/2*Screen_Width/2 + Screen_Hight/2*Screen_Hight/2))/2
    angle = 999
    while(angle > radius):
        angle = random.uniform(0,800)*math.pi*2
        x = Screen_Width/2 + radius * math.cos(angle)
        y = Screen_Hight/2 + radius * math.sin(angle)
        if(x == sx and y == sy):
            continue
    newApple = Apple(x , y ,1)
    apples[index] = newApple

def respawnApples(apples , quantity , sx ,sy):
    counter = 0
    del apples[:]
    radius = math.sqrt((Screen_Width/2*Screen_Width/2 + Screen_Hight/2*Screen_Hight/2))/2
    angle = 999
    while(counter < quantity):
        while(angle > radius):
            angle = random.uniform(0,800) * math.pi*2
            x = Screen_Width/2 + radius * math.cos(angle)
            y = Screen_Hight/2 + radius * math.sin(angle)
            if((x-Apple_size == sx or x+Apple_size == sx) and (y-Apple_size == sy or y+Apple_size == sy) 
                    or radius - angle <= 10): 
                    continue
        apples.append(Apple(x,y,1))
        angle = 999
        counter +=1


def main():
    score = 0


    #initialisation of snake

    mySnake = snake(Screen_Width/2,Screen_Hight/2)
    mySnake.setDirection(Key["UP"])
    mySnake.move()
    start_segments = 3   # initially we will be having 3 segment long snake
    while(start_segments > 0):
        mySnake.grow()
        mySnake.move()
        start_segments -=1


    # food
    max_apples = 1  # 1 apple when snake eats 
    eaten_apple = False   # as snake will eat food apple will be disappear
    apples = [Apple(random.randint(60,Screen_Width), random.randint(60,Screen_Hight),1)]
    respawnApples(apples,max_apples , mySnake.x , mySnake.y)

    startTime = pygame.time.get_ticks()
    endgame = 0

    while(endgame != 1):
        game_clock.tick(FPS)

        # input
        keyPress = getkey()
        if keyPress == "exit":
            endgame = 1

        # to check collision
        checkLimits(mySnake)
        if(mySnake.checkCrashing() == True):
            endGame()

        for myApple in apples:
            if(myApple.state == 1):
                if(checkCollision(mySnake.getHead(),Snake_size,myApple,Apple_size)==True):
                    mySnake.grow()
                    myApple.state = 0
                    score += 10
                    eaten_apple = True

        # update position
        if(keyPress):
            mySnake.setDirection(keyPress)
        mySnake.move()

        # respawning food 
        if(eaten_apple == True):
            eaten_apple = False
            respawnApple(apples , 0 , mySnake.getHead().x , mySnake.getHead().y)

        #drawing
        Screen.fill(background_color)
        for myApple in apples:
            if(myApple.state == 1):
                myApple.draw(Screen)
        
        mySnake.draw(Screen)
        drawScore(score)
        gameTime = pygame.time.get_ticks() - startTime
        drawGameTime(gameTime)

        pygame.display.flip()
        pygame.display.update()

main()

