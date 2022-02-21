import pygame
from pygame.locals import *

# Variables used to draw the GO board
Horizontal_Line = 16  # A 15*15 board requires 16 horizontal and vertical lines respectively
UNIT = 40
BORDER_WIDTH = 50

# Color variables
antique = (240, 231, 218)
red_vine = (186, 73, 75)
rain_storm = (166, 180, 179)
sand = (175, 159, 140)

screen = None
go_list = []
# Build a stack of GO pieces, (1, [x,y])
go_stack = []
# 0 for on start, 1 for player A's turn, 2 for player B's turn
status = 0


# Initialize the game
def game_init():
    pygame.init()
    global screen, go_list
    # initialize go list
    # 0 for none, 1 for player A, -1 for player B
    # Form a screen
    screen = pygame.display.set_mode((2 * BORDER_WIDTH + UNIT * (Horizontal_Line - 1),
                                      2 * BORDER_WIDTH + UNIT * (Horizontal_Line - 1)))
    # Name the screen
    pygame.display.set_caption("Gomoku")
    # Fill the screen
    screen.fill(antique)
    draw_board()


# Draw a board
def draw_board():
    font = pygame.font.SysFont("arial", 12)
    # First, draw the rows
    for row in range(Horizontal_Line):
        pygame.draw.line(screen,
                         sand,
                         (BORDER_WIDTH, BORDER_WIDTH + UNIT * row),
                         (BORDER_WIDTH + UNIT * (Horizontal_Line - 1),
                          BORDER_WIDTH + UNIT * row))

        surface_row = font.render(chr(ord('A') + row), True, sand)
        screen.blit(surface_row, (BORDER_WIDTH + UNIT * row,
                                  BORDER_WIDTH - 25))

    # Then, draw the columns
    for column in range(Horizontal_Line):
        pygame.draw.line(screen,
                         sand,
                         (BORDER_WIDTH + UNIT * column, BORDER_WIDTH),
                         (BORDER_WIDTH + UNIT * column,
                          BORDER_WIDTH + UNIT * (Horizontal_Line - 1)))
        surface_row = font.render(f"{column + 1}", True, sand)
        screen.blit(surface_row, (BORDER_WIDTH - 25,
                                  BORDER_WIDTH + UNIT * column - 5))

# 绘制胜利界面,里面包含一个方框,当做再来一次按钮.
def draw_WIN_board(win_player = 0):
    pygame.draw.rect(screen,sand,
                     ((0,  (BORDER_WIDTH + UNIT * ((Horizontal_Line - 1)/2)-1.5 * BORDER_WIDTH)),
                      (2 * BORDER_WIDTH + UNIT * (Horizontal_Line - 1) , 3 * BORDER_WIDTH)
                      ))

    font = pygame.font.SysFont("微软雅黑", 48)

    if win_player==-1:
        surface_row = font.render("恭喜,玩家 1 获得了胜利", True, rain_storm)
    else:
        surface_row = font.render("恭喜,玩家 2 获得了胜利", True, red_vine)
    screen.blit(surface_row, (120, (BORDER_WIDTH + UNIT * ((Horizontal_Line - 1) / 2) - 1.5 * BORDER_WIDTH) + 40))

    #绘制 再来一局按钮
    pygame.draw.rect(screen, (255,255,255),
                     ((260,500),
                      (180,50)
                      ))
    font = pygame.font.SysFont("微软雅黑", 24)
    restart = font.render("再来一局", True, (0,0,0))
    screen.blit(restart, (300,510))

# 判断胜负
def checkwin(Go_stack):
    global game_end_flag
    for item in Go_stack:
        flag = [1, 1, 1,1]  # 分别保存了，横，纵、斜，三个方向的判断结束的标志 1-表示一方胜利，0表示未结束。
        # 分别从三个方向判断是否已经连成五字
        for i in range(5):
            if [item[0], [item[1][0]+i, item[1][1]]] not in Go_stack:
                flag[0] = 0
            if [item[0], [item[1][0], item[1][1]+i]] not in Go_stack:
                flag[1] = 0
            if [item[0], [item[1][0]+i, item[1][1]+i]] not in Go_stack:
                flag[2] = 0
            if [item[0], [item[1][0]-i, item[1][1]+i]] not in Go_stack:
                flag[3] = 0
            # 减少比对时间，如果item表示的点确定无法练成五点一线，结束。
            if max(flag) == 0:
                continue
        # 如果连成了，就返回胜者编号
        if max(flag) > 0:
            game_end_flag = True
            return item[0]
    return 0


# Define a function, which is used to move the stones
def move(pos):
    global status
    item_1 = pygame.image.load("1.png")
    item_2 = pygame.image.load("2.png")

    # Restrict the area in which the stones can be placed
    if pos[0] < BORDER_WIDTH or pos[0] > BORDER_WIDTH + UNIT * (Horizontal_Line - 1) \
            or pos[1] < BORDER_WIDTH or pos[1] > BORDER_WIDTH + UNIT * (Horizontal_Line - 1):
        return

    # Use round function to place the stone on the exact point the player want it to be
    x = round((pos[0] - BORDER_WIDTH) / UNIT)
    y = round((pos[1] - BORDER_WIDTH) / UNIT)

    # 此处加入判断该位置是否已经有棋子落下的函数，

    for item in go_stack:
        if item[1][0] == x and item[1][1] == y:
            print("此处已经落子")
            return

    t = 1 if status == 1 else -1
    # Append the movement to the stack/push the newest stone to the stack
    go_stack.append([t, [x, y]])

    status = 2 if status == 1 else 1

    # 此处绘制按钮，有时间就改成贴图

    for item in go_stack:
        color_piece = red_vine if t == 1 else rain_storm
        '''
        pygame.draw.circle(screen,
                           color_piece,
                           (BORDER_WIDTH + UNIT * x,
                            BORDER_WIDTH + UNIT * y),
                           int(UNIT / 2.5))
        '''
        if status ==1:
            screen.blit(item_1,(BORDER_WIDTH + UNIT * x-16,BORDER_WIDTH + UNIT * y-16))
        elif status == 2:
            screen.blit(item_2, (BORDER_WIDTH + UNIT * x - 16, BORDER_WIDTH + UNIT * y - 16))
    #print(go_stack)
    if checkwin(go_stack) != 0:
        draw_WIN_board(item[0])


# Run the game
def game_run():

    global game_end_flag
    global go_stack
    game_end_flag = False

    # Main game loop, create a forever loop with while loop
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                # Exit
                exit()
            # click to place the stone
            if event.type == MOUSEBUTTONUP:
                move(event.pos)

            # 在check_win函数里修改的game_end_falg，如果确定结束，就开始绘制。
            elif game_end_flag:

                while game_end_flag:
                    for event in pygame.event.get():
                        if event.type == QUIT:
                            # Exit
                            exit()
                        if event.type == MOUSEBUTTONUP :
                            if(event.pos[0] < 260 or event.pos[0] > 260 + 180 or event.pos[1] < 500 or event.pos[1] > 550):
                                pass
                            else:
                                go_stack = []  # 清空棋子保存情况
                                game_end_flag = False  # 设置结束标志
                                print("再来一局")
                                screen.fill(antique)
                                draw_board()
                        #pygame.quit()
                        #quit()
                    pass

        # Update the screen
        pygame.display.update()


# Draw the GO pieces
def draw_pieces():
    for item in go_stack:
        color_piece = red_vine if item[0] == 1 else rain_storm
        pygame.draw.circle(screen,
                           color_piece,
                           (BORDER_WIDTH + UNIT * item[1][0],
                            BORDER_WIDTH + UNIT * item[1][1]),
                           int(UNIT / 2.5))


if __name__ == '__main__':
    game_init()
    draw_pieces()
    game_run()
