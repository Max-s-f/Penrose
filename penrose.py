import math
import cairo
import cmath
import random as r

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


"""
Goal here is to take a triangle, if it's a thicc boy then we split it to have two new vertices along edges
A and B and B and C that satisfy phi

If it's not a thicc boy then we split along edge AB to add a new vertex that will also satisfy phi

We return a new list of triangles generated from the list given (result)
"""
def split(triangles):
    result = []

    for thicc, A, B, C in triangles:
        if thicc:
            # Vertex along edge AB
            V1 = B + (A-B) / goldenRatio
            
            # Vertex along BC
            V2 = B + (C-B) / goldenRatio

            # The result of this split creates two new thicc boys and one new thinn boy
            result += [(1, V2, C, A), (1, V1, V2, B), (0, V2, V1, A)]
        else:
            # New vertex along edge AB 
            V1 = A + (B-A) / goldenRatio
            
            # Result of this split creates one new thicc boy and one new thinn boy
            result += [(1, V1, C, A), (0, C, V1, B)]
        
    return result


""" 
Method to draw the triangles

"""
def draw(triangles, colours_input, cr):
    print("COLOURS", colours[colour_choices[1]][0])

    # Basically just outline the edges then fill with appropriate colour option
    for thicc, A, B, C in triangles:
        if not thicc:
            cr.move_to(A.real, A.imag)
            cr.line_to(B.real, B.imag)
            cr.line_to(C.real, C.imag)
            cr.close_path()
    cr.set_source_rgb(colours[colour_choices[1]][0], colours[colour_choices[1]][1], colours[colour_choices[1]][2])
    cr.fill()

    for thicc, A, B, C in triangles:
        if thicc:
            cr.move_to(A.real, A.imag)
            cr.line_to(B.real, B.imag)
            cr.line_to(C.real, C.imag)
            cr.close_path()
    cr.set_source_rgb(colours[colour_choices[0]][0], colours[colour_choices[0]][1], colours[colour_choices[0]][2])
    cr.fill()

    thicc, A, B, C = triangles[0]
    cr.set_line_width(abs(B - C) / (5 * 2))
    cr.set_line_join(cairo.LINE_JOIN_ROUND)

    # Draw outlines
    for thicc, A, B, C in triangles:
        cr.move_to(C.real, C.imag)
        cr.line_to(A.real, A.imag)
        cr.line_to(B.real, B.imag)
    cr.set_source_rgb(colours[colour_choices[2]][0], colours[colour_choices[2]][1], colours[colour_choices[2]][2])
    cr.stroke()

def main():
    get_user_input()

    # set up canvas
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, 1080, 1080)
    cr = cairo.Context(surface)
    # Chaange divisor to 1 for zoom in
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