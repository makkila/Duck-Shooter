from tkinter import *
from time import sleep
from random import *
from time import time
import math

tk = Tk()
canvas = Canvas(width=550, height=800, background="white")
canvas.pack()
# Make cursor invisible
tk.config(cursor="none")
# Function to draw target cursor
def cursor_replace(event):
    global crosshair_one, crosshair_two, circle
    
    try:
        canvas.delete(crosshair_one,
                      crosshair_two,
                      circle)
    except NameError:
        pass
    finally:
        circle = canvas.create_oval(event.x-15, event.y-15, event.x+15, event.y+15, width=2, fill="", outline="red")
        crosshair_one = canvas.create_line(event.x, event.y-20, event.x, event.y+20, width=2, fill="red")
        crosshair_two = canvas.create_line(event.x-20, event.y, event.x+20, event.y, width=2, fill="red")
# Game main function
def game():
    # Try to delete "play again" screen, won' work if first game
    try:
        canvas.delete(score_title, score_final,play_again_one, play_again_two)
    except NameError:
        pass
    # Delete home screen
    canvas.delete(play, title_one, title_two)
    # Import images and draw setting
    water_image = PhotoImage(file="water.gif")
    duck_image = PhotoImage(file="duck.gif")
    water_one = canvas.create_image(275, 500, image=water_image)
    water_two = canvas.create_image(275, 600, image=water_image)
    water_three = canvas.create_image(275, 700, image=water_image)
    scoreboard = canvas.create_rectangle(-5, -5, 805, 100, fill="gray10", outline="")

    start_time = time()
    end_time = time() + 30
    time_left = int(end_time - time())
    score = 0
    break_loop = False

    canvas.create_text(100, 20, text="Score", fill="white")
    score_display = canvas.create_text(100, 60, text=score, font=("Arial", 35), fill="white")
    canvas.create_text(450, 20, text="Time Left", fill="white")
    time_left_display = canvas.create_text(450, 60, text=time_left, font=("Arial", 35), fill="white")
    tk.configure(background="white")
    # Draw duck in specified lane
    def draw_duck(lane):
        # Move duck across screen until clicked on
        def animate_duck(duck_x, duck_y):
            global duck
            nonlocal time_left_display, start_time
            # Ends when duck is out of view or break_loop is True (will only be True when duck has been clicked on)
            while duck_x >= -25 and break_loop == False:
                if end_time - time() >= -1.0:
                    if time() - start_time >= 1.0:
                        time_left = math.ceil(end_time - time())
                        canvas.delete(time_left_display)
                        time_left_display = canvas.create_text(450, 60, text=time_left, font=("Arial", 35), fill="white")
                        start_time = time()

                duck_x -= 5
                duck = canvas.create_image(duck_x, duck_y, image=duck_image)
                canvas.tag_lower(duck)
                # Check if click is on within range of duck
                def check_click(event):
                    nonlocal score, score_display, break_loop
                    
                    if event.x < duck_x + 45.5 and event.x > duck_x - 45.5 and event.y < duck_y + 33.5 and event.y > duck_y - 33.5:
                        score += 1
                        canvas.delete(score_display)
                        score_display = canvas.create_text(100, 60, text=score, font=("Arial", 35), fill="white")
                        canvas.delete(duck)
                        break_loop = True

                canvas.bind("<ButtonPress-1>", check_click)      

                sleep(0.01)
                canvas.update()
                canvas.delete(duck)

        if lane == 1:
            duck_x = 575
            duck_y = 480
            animate_duck(duck_x, duck_y)       
        elif lane == 2:
            duck_x = 575
            duck_y = 580
            animate_duck(duck_x, duck_y)
        elif lane == 3:
            duck_x = 575
            duck_y = 677
            animate_duck(duck_x, duck_y)

    canvas.bind("<Motion>", cursor_replace)
    # Continue drawing ducks until time is up
    while time() < end_time:
        lane = randint(1, 3)
        break_loop = False
        draw_duck(lane)
            
        canvas.bind("<Motion>", cursor_replace)
    # Display game over screen and create play again button when time is up
    canvas.delete("all")
    tk.configure(background="blue")
    
    global score_title, score_final,play_again_one, play_again_two
    score_title = canvas.create_text(275, 300, text="Score", font="Arial 50")
    score_final = canvas.create_text(275, 500, text=score, font="Arial 30")
    play_again_one = canvas.create_rectangle(150, 600, 400, 700)
    play_again_two = canvas.create_text(275, 650, text="Play Again", font="Arial 25")

    def play_again_click(event):
        if event.x < 400 and event.x > 150 and event.y < 700 and event.y > 600:
            game()

    canvas.bind("<ButtonPress-1>", play_again_click)
        
    tk.mainloop()

# Display home screen when user first starts game
title_one = canvas.create_text(275, 400, text="DUCK", font="Arial 35")
title_two = canvas.create_text(275, 450, text="SHOOTER", font="Arial 35")
play = canvas.create_text(275, 525, text="Play", font="Arial 25")

def play_click(event):
    if event.x < 300 and event.x > 250 and event.y < 550 and event.y > 500:
        game()
        

canvas.bind("<ButtonPress-1>", play_click)
canvas.bind("<Motion>", cursor_replace)
tk.mainloop()


