#!/usr/bin/env python3

import colorsys
import math
import time

import unicornhat as unicorn


print("""Demo

This pixel shading demo transitions between 4 classic graphics demo effects.

If you're using a Unicorn HAT and only half the screen lights up, 
edit this example and  change 'unicorn.AUTO' to 'unicorn.HAT' below.
""")

unicorn.set_layout(unicorn.AUTO)
unicorn.rotation(0) # tested on pHAT/HAT with rotation 0, 90, 180 & 270
unicorn.brightness(0.5)
u_width,u_height=unicorn.get_shape()


# twisty swirly goodness
def swirl(x, y, step):
    x -= (u_width/2)
    y -= (u_height/2)

    dist = math.sqrt(pow(x, 2)+pow(y,2)) / 2.0
    angle = (step / 10.0) + (dist * 1.5)
    s = math.sin(angle);
    c = math.cos(angle);

    xs = x * c - y * s;
    ys = x * s + y * c;

    r = abs(xs + ys)
    r = r * 64.0
    r -= 20

    return (r, r + (s * 130), r + (c * 130))

# roto-zooming checker board
def checker(x, y, step):
    x -= (u_width/2)
    y -= (u_height/2)

    angle = (step / 10.0)
    s = math.sin(angle);
    c = math.cos(angle);

    xs = x * c - y * s;
    ys = x * s + y * c;

    xs -= math.sin(step / 200.0) * 40.0
    ys -= math.cos(step / 200.0) * 40.0

    scale = step % 20
    scale /= 20
    scale = (math.sin(step / 50.0) / 8.0) + 0.25;

    xs *= scale
    ys *= scale

    xo = abs(xs) - int(abs(xs))
    yo = abs(ys) - int(abs(ys))
    l = 0 if (math.floor(xs) + math.floor(ys)) % 2 else 1 if xo > .1 and yo > .1 else .5

    r, g, b = colorsys.hsv_to_rgb((step % 255) / 255.0, 1, l)

    return (r * 255, g * 255, b * 255)

# weeee waaaah
def blues_and_twos(x, y, step):
    x -= (u_width/2)
    y -= (u_height/2)

    xs = (math.sin((x + step) / 10.0) / 2.0) + 1.0
    ys = (math.cos((y + step) / 10.0) / 2.0) + 1.0

    scale = math.sin(step / 6.0) / 1.5
    r = math.sin((x * scale) / 1.0) + math.cos((y * scale) / 1.0)
    b = math.sin(x * scale / 2.0) + math.cos(y * scale / 2.0)
    g = r - .8
    g = 0 if g < 0 else g

    b -= r
    b /= 1.4

    return (r * 255, (b + g) * 255, g * 255)

# rainbow search spotlights
def rainbow_search(x, y, step):
    xs = math.sin((step) / 100.0) * 20.0
    ys = math.cos((step) / 100.0) * 20.0

    scale = ((math.sin(step / 60.0) + 1.0) / 5.0) + 0.2
    r = math.sin((x + xs) * scale) + math.cos((y + xs) * scale)
    g = math.sin((x + xs) * scale) + math.cos((y + ys) * scale)
    b = math.sin((x + ys) * scale) + math.cos((y + ys) * scale)

    return (r * 255, g * 255, b * 255)

# zoom tunnel
def tunnel(x, y, step):

    speed = step / 100.0
    x -= (u_width/2)
    y -= (u_height/2)

    xo = math.sin(step / 27.0) * 2
    yo = math.cos(step / 18.0) * 2

    x += xo
    y += yo

    if y == 0:
        if x < 0:
            angle = -(math.pi / 2)
        else:
            angle = (math.pi / 2)
    else:
        angle = math.atan(x / y)

    if y > 0:
        angle += math.pi

    angle /= 2 * math.pi # convert angle to 0...1 range

    shade = math.sqrt(math.pow(x, 2) + math.pow(y, 2)) / 2.1
    shade = 1 if shade > 1 else shade


    angle += speed
    depth = speed + (math.sqrt(math.pow(x, 2) + math.pow(y, 2)) / 10)

    col1 = colorsys.hsv_to_rgb((step % 255) / 255.0, 1, .8)
    col2 = colorsys.hsv_to_rgb((step % 255) / 255.0, 1, .3)


    col = col1 if int(abs(angle * 6.0)) % 2 == 0 else col2

    td = .3 if int(abs(depth * 3.0)) % 2 == 0 else 0

    col = (col[0] + td, col[1] + td, col[2] + td)

    col = (col[0] * shade, col[1] * shade, col[2] * shade)

    return (col[0] * 255, col[1] * 255, col[2] * 255)

effects = [tunnel, rainbow_search, checker, swirl]

step = 0
while True:
    for i in range(500):
        for y in range(u_height):
            for x in range(u_width):
                r, g, b = effects[0](x, y, step)
                if i > 400:
                    r2, g2, b2 = effects[-1](x, y, step)

                    ratio = (500.00 - i) / 100.0
                    r = r * ratio + r2 * (1.0 - ratio)
                    g = g * ratio + g2 * (1.0 - ratio)
                    b = b * ratio + b2 * (1.0 - ratio)
                r = int(max(0, min(255, r)))
                g = int(max(0, min(255, g)))
                b = int(max(0, min(255, b)))
                unicorn.set_pixel(x, y, r, g, b)

        step += 1

        unicorn.show()

        time.sleep(0.01)

    effect = effects.pop()
    effects.insert(0, effect)
