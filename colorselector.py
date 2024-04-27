import tkinter as tk
def color_update(val):
    red = red_slider.get()
    green = green_slider.get()
    blue = blue_slider.get()
    colour = f"#{red:02x}{green:02x}{blue:02x}"
    canvas.config(bg=colour)
    hex_text.delete(0, tk.END)
    hex_text.insert(0, colour)

window = tk.Tk()
window.title('顏色選擇器')
red_slider = tk.Scale(window, from_=0, to=255, command=color_update)
green_slider = tk.Scale(window, from_=0, to=255, command=color_update)
blue_slider = tk.Scale(window, from_=0, to=255, command=color_update)
red_slider.grid(row=1, column=1)
green_slider.grid(row=1, column=2)
blue_slider.grid(row=1, column=3)
canvas = tk.Canvas(window, width=300, height=200)
canvas.grid(row=2, column=1, columnspan=3)
hex_text = tk.Entry(window)
hex_text.grid(row=3, column=1, columnspan=3)
tk.mainloop()