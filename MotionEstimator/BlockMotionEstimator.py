#!/usr/bin/env python
import sys
import Image
import math
import random
import logging

def compute_offset(a, b, start_point):
    width, height = a.size
    x_start, y_start = start_point

    mask = ((-2, -2), (-1, -2), (0, -2), (1, -2), (2, -2),
            (-2, -1), (-1, -1), (0, -1), (1, -1), (2, -1),
            (-2,  0), (-1,  0), (0,  0), (1,  0), (2,  0),
            (-2,  1), (-1,  1), (0,  1), (1,  1), (2,  1),
            (-2, -2), (-1,  2), (0,  2), (1,  2), (2,  2))

    mask1 = ((-1, -1), (0, -1), (1, -1),
            (-1,  0), (0,  0), (1,  0),
            (-1,  1), (0,  1), (1,  1))

    best_match = 0, 0
    first_check = True
    smalest_difference = 0

    for (x_init, y_init) in mask:
        x, y = x_start + x_init, y_start + y_init
        difference = 0
        local_best_match = 0, 0

        for (x_delta, y_delta) in mask:
            x_checked, y_checked = x + x_delta, y + y_delta
            p1, p2 = a.getpixel((x, y)), b.getpixel((x_checked, y_checked))
            difference += abs(p1[0] - p2[0])

            if first_check or smalest_difference >= difference:
                first_check = False
                smalest_difference = difference
                local_best_match = x_delta, y_delta

        best_match = best_match[0] + local_best_match[0], best_match[1] + local_best_match[1]

    return best_match[0]/len(mask), best_match[1]/len(mask)


def compare_n_times(a, b, iterations):
    width, height = a.size
    a = a.resize((width*2, height*2)) 
    b = b.resize((width*2, height*2)) 

    width, height = a.size
    w = 4
    x, y = 0, 0

    for i in range(iterations):
        p = random.randrange(w, width-w), random.randrange(w, height-w)
        xn, yn = compute_offset(a, b, p)
        x, y = x + xn, y + yn

    return x / iterations, y / iterations

if __name__=="__main__":
    logging.basicConfig(level=logging.INFO)

    files = sys.argv[1], sys.argv[2]
    offsets = [(0,0), (1,1)]
    logging.info(files)

    images = map(Image.open, files)
    iterations = 20

    x, y = compare_n_times(images[0], images[1], iterations)
    error = abs(x - offsets[1][0]) + abs(y - offsets[1][1])
    print "(%2d %2d) -> (%2d, %2d) %d" % (offsets[1][0], offsets[1][1], x, y, error)
