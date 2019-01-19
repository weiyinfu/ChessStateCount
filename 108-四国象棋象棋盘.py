from tkinter import *
from  math import *
import numpy as np

N = 4
width, height = 500, 500
r = 100
window = Tk()
canva = Canvas(window, width=width, height=height)
canva.pack()


def draw_N():
    centerx, centery = width / 2, height / 2
    for i in range(N):
        fx, fy = centerx + r * cos(pi * 2 / N * i), centery + r * sin(pi * 2 / N * i)
        tx, ty = centerx + r * cos(pi * 2 / N * (i + 1)), centery + r * sin(pi * 2 / N * (i + 1))
        grid_size = hypot(fx - tx, fy - ty) / 8
        dx, dy = (fx + tx) / 2 - centerx, (fy + ty) / 2 - centery
        dx, dy = dx / hypot(dx, dy) * grid_size, dy / hypot(dx, dy) * grid_size
        horizon = np.array([dx, dy])
        vdx, vdy = tx - fx, ty - fy
        vdx, vdy = vdx / hypot(vdx, vdy) * grid_size, vdy / hypot(vdx, vdy) * grid_size
        vertical = np.array([vdx, vdy])
        zero = np.array([fx, fy])
        for j in range(5):
            src = zero + horizon * j
            des = zero + horizon * j + vertical * 8
            canva.create_line(src[0], src[1], des[0], des[1])
        for j in range(9):
            src = zero + vertical * j
            des = zero + vertical * j + horizon * 4
            canva.create_line(src[0], src[1], des[0], des[1])
        src = zero + vertical * 3 + horizon * 4
        des = zero + vertical * 5 + horizon * 2
        canva.create_line(src[0], src[1], des[0], des[1])
        src = zero + vertical * 3 + horizon * 2
        des = zero + vertical * 5 + horizon * 4
        canva.create_line(src[0], src[1], des[0], des[1])


draw_N()
window.mainloop()
