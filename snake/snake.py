import random
class Snake:
    def __init__(self,init_body,init_direction):
        self.body = init_body
        self.direction = init_direction

    def head(self):
        return self.body[-1]
    
    def take_step(self,position):
        self.body = self.body[1:] + [position]

    def extend_body(self,position):
        self.body.append(position)

    def set_direction(self,direction):
        self.direction = direction

    
class Apple:
    def __init__(self,location):
        self.location = location

class Game:
    
    EMPTY = 0
    BODY = 1
    HEAD = 2
    apple = 3
    
    SCORE = 0

    #DIRECTIONS
    DIR_UP=(0,1)
    DIR_DOWN=(0,-1)
    DIR_LEFT=(-1,0)
    DIR_RIGHT=(1,0)

    CHAR_UP = "W"
    CHAR_DOWN = "S"
    CHAR_LEFT= "A"
    CHAR_RIGHT= "D"

    #charARACTERS
    DISPLAY_CHARS = {
        0:" ",
        1: "0",
        2: "X",
        3: "*",
    }

    def __init__(self,height,width):
        self.height = height
        self.width = width
        init_body = [(0, 0), 
                    (1, 0),]

        self.snake = Snake(init_body, self.DIR_UP)

    def play(self):
        self.regenerate_apple()
        self.render()
    
        while True:
            char = input("Enter your next move(W,A,S,D): ").upper()
            if char == self.CHAR_UP and self.snake.direction != self.DIR_DOWN:
                self.snake.set_direction(self.DIR_UP)
            elif char == self.CHAR_DOWN and self.snake.direction != self.DIR_UP:
                self.snake.set_direction(self.DIR_DOWN)
            elif char == self.CHAR_LEFT and self.snake.direction != self.DIR_RIGHT:
                self.snake.set_direction(self.DIR_LEFT)
            elif char == self.CHAR_RIGHT and self.snake.direction != self.DIR_LEFT:
                self.snake.set_direction(self.DIR_RIGHT)

            next_position = self._next_position(self.snake.head(), self.snake.direction)
            if next_position in self.snake.body:
                print(f"You ate yourself, damn! You should have had breakfast. Anyway, your score is {self.SCORE} ")
                break
            
            if next_position == self.current_apple.location:
                    self.snake.extend_body(next_position)
                    self.regenerate_apple()
                    self.SCORE +=1

            else:
                self.snake.take_step(next_position)
                    
            self.render()


    def board_matrix(self):
        matrix = [[self.EMPTY for _ in range(self.height)] for _ in range(self.width)]
    
        for co in self.snake.body:
            matrix[co[0]][co[1]] = self.BODY

        head =self.snake.head()
        matrix[head[0]][head[1]] = self.HEAD

        apple_loc = self.current_apple.location
        
        matrix[apple_loc[0]][apple_loc[1]] = self.apple
        return matrix

    def render(self):
        board = self.board_matrix()
        top_and_bottom_border = "+" + "-" * self.width + "+"
        print(top_and_bottom_border)
        for y in range(0,self.height):
            line= "|"
            for x in range(0,self.width):
                cell_val=board[x][self.height-1-y]
                line += self.DISPLAY_CHARS[cell_val]
            line += "|"
            print(line)
        print(top_and_bottom_border) 

    def _next_position(self, position, step):
        return (
            (position[0] + step[0]) % self.width,
            (position[1] + step[1]) % self.height
        )

    def regenerate_apple(self):
        while True:
            new_apple_loc = (
                random.randint(0,self.width-1),
                random.randint(0,self.height-1)
            )
            if new_apple_loc not in self.snake.body:
                break

        self.current_apple = Apple(new_apple_loc)

game = Game(10,30)
game.play()