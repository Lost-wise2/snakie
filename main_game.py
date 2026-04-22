#This should be the main game file
import tkinter
import random

Rows = 30
Cols = 25
TileSize = 25

Window_Width = TileSize * Rows
Window_Height = TileSize * Cols

#game windoww
Window = tkinter.Tk()
Window.title("Snakie")
Window.resizable(False, False)

Canvas = tkinter.Canvas(Window, bg= "black", width=Window_Width, height=Window_Height, borderwidth=0, highlightthickness=0)
Canvas.pack()
Window.update()

#location
window_width = Window.winfo_width()
window_height = Window.winfo_height()
screen_width = Window.winfo_screenwidth()
screen_height = Window.winfo_screenheight()

Window_x = int((screen_width/2) - (window_width/2))
Window_y = int((screen_height/2) - (window_height/2))

Window.geometry(f"{window_width}x{window_height}+{Window_x}+{Window_y}")




Window.mainloop()