#the ball deviation after hitting the walls is made with the basic theory of incident angle
#the ball deviation due to it hitting the paddle does not use actual physics but deviates based on where the ball hit.the angle of deviation is based here on the direction of the centre of the paddle to the place where the ball hit

import pygame
pygame.init()
pygame.font.init()

win_width,win_height=700,500
win=pygame.display.set_mode((win_width,win_height))
pygame.display.set_caption("Ping Pong")

paddleWidth,paddleHeight=20,100
ballRadius=7

#font section
scoreFont=pygame.font.SysFont('comicsans',50)

class Paddle:
    def __init__(self,x,y,width,height):
        self.x=x
        self.y=y
        self.org_x=x
        self.org_y=y
        self.width=width
        self.height=height
        self.vel=4
    
    def draw(self,win):
        pygame.draw.rect(win,(255,255,255),(self.x,self.y,self.width,self.height))

class Ball:
    max_vel=5
    def __init__(self,x,y,radius):
        self.x=x
        self.y=y
        self.org_x=x
        self.org_y=y
        self.radius=radius
        self.xVel=self.max_vel
        self.yVel=0
    
    def draw(self,win):
        pygame.draw.circle(win,(255,255,255),(self.x,self.y),self.radius)

    def move(self):
        self.x+=self.xVel
        self.y+=self.yVel
    
def draw(paddles,ball,left_score,right_score):
    win.fill((0,0,0))

    left_text=scoreFont.render(f"{left_score}",1,(255,255,255))
    right_text=scoreFont.render(f"{right_score}",1,(255,255,255))
    win.blit(left_text,(win_width//4-left_text.get_width()//2,20))
    win.blit(right_text,(win_width*(3/4)-right_text.get_width()//2,20))

    for paddle in paddles:
        paddle.draw(win)

    for i in range(10,win_height,win_height//20):
        if i%2==1:
            continue
        pygame.draw.rect(win,(255,255,255),(win_width//2-5,i,10,win_height//20))

    ball.draw(win)

    pygame.display.update()

def paddle_move(keys,leftPaddle,rightPaddle):
    if keys[pygame.K_w] and leftPaddle.y>=leftPaddle.vel:
        leftPaddle.y-=leftPaddle.vel
    if keys[pygame.K_s] and leftPaddle.y+leftPaddle.vel+leftPaddle.height<=win_height:
        leftPaddle.y+=leftPaddle.vel
    
    if keys[pygame.K_UP] and rightPaddle.y>=rightPaddle.vel:
        rightPaddle.y-=rightPaddle.vel
    if keys[pygame.K_DOWN] and rightPaddle.y+rightPaddle.vel+rightPaddle.height<=win_height:
        rightPaddle.y+=rightPaddle.vel

def handle_collision(ball,leftPaddle,rightPaddle):
    if ball.y+ball.radius>=win_height:
        ball.yVel*=-1
    elif ball.y-ball.radius<=0:
        ball.yVel*=-1

    if ball.xVel<0:
        if ball.y>=leftPaddle.y and ball.y<=leftPaddle.y+leftPaddle.height:
            if ball.x-ball.radius<=leftPaddle.x+leftPaddle.width:
                ball.xVel*=-1

                middle_y=leftPaddle.y+leftPaddle.height//2
                difference_y=middle_y-ball.y
                reduction_factor=(leftPaddle.height/2)/ball.max_vel
                yVel=difference_y/reduction_factor
                ball.yVel=-1*yVel

    else:
        if ball.y>=rightPaddle.y and ball.y<=rightPaddle.y+rightPaddle.height:
            if ball.x+ball.radius>=rightPaddle.x:
                ball.xVel*=-1

                middle_y=rightPaddle.y+rightPaddle.height//2
                difference_y=middle_y-ball.y
                reduction_factor=(rightPaddle.height/2)/ball.max_vel
                yVel=difference_y/reduction_factor
                ball.yVel=-1*yVel


def main():
    run=True
    clock=pygame.time.Clock()

    leftPaddle=Paddle(10,win_height//2-paddleHeight//2,paddleWidth,paddleHeight)
    rightPaddle=Paddle(win_width-10-paddleWidth,win_height//2-paddleHeight//2,paddleWidth,paddleHeight)
    ball=Ball(win_width//2,win_height//2,ballRadius)

    left_score=0
    right_score=0

    while run:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run=False
                break

        keys=pygame.key.get_pressed()
        paddle_move(keys,leftPaddle,rightPaddle)
        ball.move()
        handle_collision(ball,leftPaddle,rightPaddle)

        if ball.x<0:
            right_score+=1
            ball.x=ball.org_x
            ball.y=ball.org_y
            leftPaddle.x=leftPaddle.org_x
            leftPaddle.y=leftPaddle.org_y
            rightPaddle.x=rightPaddle.org_x
            rightPaddle.y=rightPaddle.org_y
            pygame.time.delay(2000)

        elif ball.x>win_width:
            left_score+=1
            ball.x=ball.org_x
            ball.y=ball.org_y
            leftPaddle.x=leftPaddle.org_x
            leftPaddle.y=leftPaddle.org_y
            rightPaddle.x=rightPaddle.org_x
            rightPaddle.y=rightPaddle.org_y
            pygame.time.delay(2000)


        draw([leftPaddle,rightPaddle],ball,left_score,right_score)


    
    
    pygame.quit()

if __name__=="__main__":
    main()
        

