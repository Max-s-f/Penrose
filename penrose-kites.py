import math
import cairo
import cmath
import random as r
from penrose import draw

goldenRatio = (1 + (5 ** 0.5)) / 2

# User option variables
splits = 0
colour_choices = []
filename = ""
zoom = 2

goldenRatio = (1 + (5 ** 0.5)) / 2

colours = {
    "red":[1, 0, 0],
    "green":[0, 1, 0],
    "blue":[0, 0, 1],
    "white":[1, 1, 1],
    "black":[0, 0, 0],
    "yellow":[1, 1, 0],
    "cyan":[0, 1, 1],
    "magenta":[1, 0, 1],
    "orange":[1, 0.647, 0],
    "purple":[0.502, 0, 0.502],
    "pink":[1, 0.753, 0.796],
    "brown":[0.647, 0.165, 0.165],
    "gray":[0.502, 0.502, 0.502],
    "random":[(r.randint(1, 256))/256, (r.randint(1,256)/256), (r.randint(1,256)/256)]
}

def get_user_input():
    try:
        global splits 
        splits = int(input("Enter number of tiling subdivisions (int)"))
        if splits < 1:
            print("Error, must be greater than 0")
            SystemExit(0)
    except ValueError:
        print("Please enter an integer")
        SystemExit(0)
    try:
        global colour_choices
        colour_choices = input("Enter 3 space separated colours (see readme for list)").split()
    except ValueError:
        print("Input: [colour colour colour]")
        SystemExit(0)
    try:
        global filename
        filename = input("Enter filename you wish to save the image to (must end with .png)")
        if not filename.endswith(".png"):
            print("Please end with .png")
            SystemExit(0)
    except ValueError:
        print("Please enter valid filename")
        SystemExit(0)
    try:
        global zoom
        zoom = int(input("Enter 1 for zoomed in or 2 for full image"))
        if not 1 <= zoom <= 2:
            print("Please enter either 1 or 2")
            SystemExit(0)
    except ValueError:
        print("Enter 1 or 2")
        SystemExit(0)


def split(triangles):
    result = []
    for dart, A, B, C in triangles:
        if not dart:
            # Subdivide red (sharp isosceles) (half kite) triangle
            Q = A + (B - A) / goldenRatio
            R = B + (C - B) / goldenRatio
            result += [(1, R, Q, B), (0, Q, A, R), (0, C, A, R)]
        else:
            # Subdivide blue (fat isosceles) (half dart) triangle
            P = C + (A - C) / goldenRatio
            result += [(1, B, P, A), (0, P, C, B)]
    return result

def main():
    get_user_input()

    # set up canvas
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, 1080, 1080)
    cr = cairo.Context(surface)

    cr.scale(1080 / zoom, 1080 / zoom)
    cr.translate(0.5 * zoom, 0.5 * zoom)

    triangles = []
    for i in range(10):
        B = cmath.rect(1, (2 * i - 1) * math.pi / (5 * 2))
        C = cmath.rect(1, (2*i + 1) * math.pi / (5 * 2))

        if i % 2 == 0:
            B, C = C, B
        
        triangles.append((0, 0, B, C))
    
    for i in range(splits):
        triangles = split(triangles)
    
    draw(triangles, colour_choices, cr)

    surface.write_to_png(filename)


main()