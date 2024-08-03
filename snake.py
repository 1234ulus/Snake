from tkinter import *
import random

#  define canvas for gameboard
game_width = 800
game_height = 600
#smaller number = higher speed
speed = 70
space_size = 40
prey_size = int(space_size / 2)
background_color = "#000000"
#starting parameters for snake
body_parts = 4
snake_color = "#00FF00" #green
#parameters for prey
prey_color = "#FF0000" #red


class Snake:
    def __init__(self):
        self.body_size = body_parts
        self.coordinates = []
        self.squares = []

        for i in range (0, body_parts):
            self.coordinates.append([0, 0])
        
        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + space_size, y + space_size, fill=snake_color, tag ="snake")
            self.squares.append(square)

class Prey:
   def __init__(self):
       px = random.randint(0, (game_width - space_size))
       py = random.randint(0, (game_height - space_size))

       self.coordinates = [px, py]
       canvas.create_oval(px, py, px + prey_size, py + prey_size, fill=prey_color, tag ="prey")
   

def next_turn(snake, prey):
    (x, y) = snake.coordinates[0]

    if direction == "up":
        y -= space_size

    elif direction == "down":
         y += space_size

    elif direction == "left":
         x -= space_size

    elif direction == "right":
        x += space_size

    snake.coordinates.insert(0, (x, y))
    square = canvas.create_rectangle(x, y, x + space_size, y + space_size, fill=snake_color)
    snake.squares.insert(0, square)
    #snake eats the prey so it is growing
    if x in range (prey.coordinates[0]- prey_size, prey.coordinates[0] + prey_size ) and y in range (prey.coordinates[1]- prey_size, prey.coordinates[1] + prey_size):
        global score
        score += 10
        label.config(text="Score:{}".format(score))
        canvas.delete("prey")
        prey = Prey()
    
    else:
    #snake is moving whitout elongation
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    #check if snake hit the wall
    if check_collision(snake):
        game_over()
    else:
        window.after(speed, next_turn, snake, prey)


def change_direction(new_direction):
    global direction
    if new_direction == "left":
        if direction != "right":
            direction = new_direction
    elif new_direction == "right":
        if direction != "left":
            direction = new_direction
    elif new_direction == "up":
        if direction != "down":
            direction = new_direction
    elif new_direction == "down":
        if direction != "up":
            direction = new_direction

def check_collision(snake):
    x, y = snake.coordinates[0]
# collision with the walls
    if x< 0 or x>= game_width:
        return True
    elif y< 0 or y>= game_height:
        return True
# collision with the snake body
    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True
    return False

def game_over():
    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/2, font=("Arial", 70), text="GAME OVER", fill="red")


#Create window
window = Tk()
#Name of game
window.title("Sssnake")
#Windows want change the size
window.resizable(False, False)
#inicial score
score = 0
#inicial direction of snake
direction = "down"
#Create information of score at top of the window
label = Label(window, text = "Score:{}".format(score), font=("arial", 40))
label.pack()
#create the canvas
canvas = Canvas(window, bg=background_color, height=game_height, width=game_width)
canvas.pack()

#place the window on the middle of screen
window.update()
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = int((screen_width/2) - (window_width/2))
y = int((screen_height/2) - (window_height/2))
window.geometry(f"{window_width}x{window_height}+{x}+{y}")

# controling snake from keybord
window.bind("<Left>", lambda event: change_direction("left"))
window.bind("<Right>", lambda event: change_direction("right"))
window.bind("<Up>", lambda event: change_direction("up"))
window.bind("<Down>", lambda event: change_direction("down"))

#Create object in class Snake and prey
snake = Snake()
prey = Prey()

next_turn(snake, prey)


window.mainloop()
