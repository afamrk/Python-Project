from tkinter import ttk
import tkinter as tk
from os import path
import sys
from PIL import Image, ImageTk
from collections import deque
from random import randint
from itertools import islice

MOVE_INCREMENT = 20

class Snake(tk.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setup()


    def setup(self):
        self.move_per_second = 15
        self.game_speed = 1000 // self.move_per_second
        self.delete(tk.ALL)
        self.snake_position = deque([(100,100), (80,100), (60,100)])
        self.food_position = self.set_new_food_position()
        self.score = 0
        self.bind_all('<Key>', self.on_key_press)
        self.direction = 'Right'

        self.load_resourse()
        self.create_objects()
        self.perform_action()
        self.current_job = None

    def load_resourse(self):
        try:
            bundle_dir = getattr(sys, "_MEIPASS")
            path_to_snake = path.join(bundle_dir, 'assets', 'snake.png')
            path_to_food = path.join(bundle_dir, 'assets', 'food.png')
            self.snake_body_image = Image.open(path_to_snake)
            self.snake_body = ImageTk.PhotoImage(self.snake_body_image)


            self.snake_food_image = Image.open(path_to_food)
            self.snake_food = ImageTk.PhotoImage(self.snake_food_image)

        except IOError as e:
            print(e)
            root.destroy()

    def create_objects(self):
        self.create_text(45, 12, text=f'Score: {self.score}',
                         tags='score', fill='#fff',
                         font=('TkDefaultFont', 14))


        for x_pos, y_pos in self.snake_position:
            self.create_image(x_pos, y_pos,
                              image=self.snake_body, tags='snake')

        self.create_image(*self.food_position,
                          image=self.snake_food, tags='food')


        self.create_rectangle(7, 27, 593, 613, outline='red')

    def move_snake(self):
        self.snake_position.pop()
        if self.direction == 'Right':
            self.snake_position.appendleft((self.snake_position[0][0] + MOVE_INCREMENT, self.snake_position[0][1]))
        elif self.direction == 'Left':
            self.snake_position.appendleft((self.snake_position[0][0] - MOVE_INCREMENT, self.snake_position[0][1]))
        elif self.direction == 'Up':
            self.snake_position.appendleft((self.snake_position[0][0] , self.snake_position[0][1] - MOVE_INCREMENT))
        elif self.direction == 'Down':
            self.snake_position.appendleft((self.snake_position[0][0], self.snake_position[0][1] + MOVE_INCREMENT))

        for segment, position in zip(self.find_withtag("snake"), self.snake_position):
            self.coords(segment, position)

    def perform_action(self):
        if self.check_collision():
            self.end_game()
            #self.current_job = None
            return
        self.check_food_collision()
        self.move_snake()
        self.current_job = self.after(self.game_speed, self.perform_action)

    def check_collision(self):
        head_x, head_y = self.snake_position[0]

        return (
            head_x in (0, 600)
            or head_y in (20, 620)
            or (head_x, head_y) in islice(self.snake_position,1,200)
        )

    def on_key_press(self, e):
        all_direction = {'Right', 'Up', 'Left', 'Down'}
        opposit_direction = ({'Down', 'Up'}, {'Left', 'Right'})
        new_direction = e.keysym

        if (new_direction in all_direction
                and {new_direction, self.direction} not in opposit_direction):
            self.direction = new_direction
            #if self.current_job:
            #    self.after_cancel(self.current_job)
            #    self.current_job = None
            #self.perform_action()

    def check_food_collision(self):
        if self.snake_position[0] == self.food_position:
            self.score += 1
            self.snake_position.append(self.snake_position[-1])
            if self.score % 5 == 0:
                self.increase_speed()
            self.create_image(*self.snake_position[-1], image=self.snake_body, tag="snake")
            score = self.find_withtag('score')
            self.food_position = self.set_new_food_position()
            food = self.find_withtag('food')
            self.coords(food, self.food_position)
            self.itemconfigure(score, text=f'Score: {self.score}')

    def increase_speed(self):
        self.move_per_second += 1
        self.game_speed = 1000 // self.move_per_second

    def set_new_food_position(self):
        while True:
            x_pos = randint(1,29) * MOVE_INCREMENT
            y_pos = randint(3,30) * MOVE_INCREMENT

            if (x_pos, y_pos) not in self.snake_position:
                return (x_pos, y_pos)

    def end_game(self):
        self.delete(tk.ALL)
        self.create_text(
            self.winfo_width()/2,
            self.winfo_height()/2,
            text=f'Game over! You scored {self.score}',
            fill='white',
            font=('TkDefaultFont', 24)
        )
        button = ttk.Button(text='Restart', command=self.setup)
        self.create_window((self.winfo_width()/2,(self.winfo_height()/2)+100), window=button, anchor="center")


root = tk.Tk()
root.title('snake game')
board = Snake(root, width=600, height=620, background='black', highlightthickness=0)
board.pack()
root.mainloop()
