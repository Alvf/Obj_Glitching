# script to handle large .obj files and mix their vert rows.
# very procedural; reads a filename and makes an output .txt

import random
import math

# swaps array[i] and array[j]
def swap(array, i, j):
    temp = array[i]
    array[i] = array[j]
    array[j] = array[i]


# arr_to_str: format the contents of an array into a space-deliniated string
#   inputs: array of printables
#   returns: string with each element separated by space
def arr_to_str(array):
    ret_str = ""
    for x in array:
        ret_str += x
        ret_str += " "
    return ret_str[:-1]


# prox_swap: take a random element in the array and then swap it with another
# in some proximity radius.
#   inputs: array of printables
#           radius to pick from on swap
def prox_swap(array, radius):
    i = random.randrange(0, len(array))
    j = random.randrange(i - radius, i + radius + 1)
    if j <= 0:
        j = 0
    if j >= len(array):
        j = len(array) - 1
    swap(array, i, j)


# prox_shuffle: does repeated prox swaps
def prox_shuffle(array, iterations, radius):
    for j in range(0, iterations):
        prox_swap(array, radius)


# shuffle: does a proper combinatoric shuffle on an array
# starting from index i and ending on index j (noninclusive)
def shuffle(array, i, j):
    assert(i <= j)
    assert(i >= 0)
    assert(j <= len(array))
    for k in range(i, j-1):
        swap(array, k, random.randrange(k + 1, j))


# displace: displaces x (1), y(2), or z(3) of a printable
# in some random magnitude
def displace(array, coor, mag):
    assert(coor == 1 or coor == 2 or coor == 3)
    array[coor] = str(float(array[coor]) + random.uniform(-mag, mag))


# displaces random verts iter times
def displace_its(array, mag, iter):
    for j in range(0, iter):
        i = random.randrange(0, len(array))
        displace(array[i], random.randrange(1, 4), mag)


# sort: sorts the printables by x (1), y (2), or z (3).
def sort_coord(array, coor):
    array.sort(key = lambda array: float(array[coor]))


# rotates by some axis (1, 2, 3) by angle theta (radians)
def rot_coord(p, axis, thet):
    if axis == 1:
        y = float(p[2])
        z = float(p[3])
        p[2] = str(y * math.cos(thet) - z * math.sin(thet))
        p[3] = str(z * math.cos(thet) + y * math.sin(thet))
    elif axis == 2:
        x = float(p[1])
        z = float(p[3])
        p[1] = str(x * math.cos(thet) - z * math.sin(thet))
        p[3] = str(z * math.cos(thet) + x * math.sin(thet))
    elif axis ==3:
        x = float(p[1])
        y = float(p[2])
        p[1] = str(x * math.cos(thet) - y * math.sin(thet))
        p[2] = str(y * math.cos(thet) + x * math.sin(thet))


# does a spiral maneuver on the points (no idea if this will turn into anything cool)
def spiral(array, axis, max_thet, start_ind, end_ind):
    for i in range(start_ind, end_ind + 1):
        rot_coord(array[i], axis, i / end_ind * max_thet)


# replaces a segment of a list with the replacement list at start_index
def array_replace(array, replacement, start_ind):
    for i in range(0, len(replacement)):
        array[start_ind + i] = replacement[i]


# sorts a segment of an array
def sort_coord_replace(array, coor, start_ind, end_ind):
    replacement = array[start_ind : end_ind + 1]
    sort_coord(replacement, coor)
    array_replace(array, replacement, start_ind)


def main():
    print("Input file: ", end = "")
    FILENAME = input()

    count = 0
    headers = []
    verts = []
    tangents_normals = []
    mtl_info = []
    faces = []
    with open(FILENAME) as file:
        line = file.readline()
        while line:
            line = line.split()
            if line[0] == "v":
                verts.append(line)
            elif line[0] in ["vt", "vn"]:
                tangents_normals.append(line)
            elif line[0] in ["usemtl", "s"]:
                mtl_info.append(line)
            elif line[0] in ["f"]:
                faces.append(line)
            else:
                headers.append(line)
            line = file.readline()

    vlen = len(verts)

    while True:
        print("(p)rox shuffle, (s)huffle, (d)isplace, s(o)rt, sp(i)ral, or (f)inish?")
        MODE = input()
        if (MODE == "p"):
            print("iterations? Verts len is " + str(vlen))
            iterations = int(input())
            print("radius?")
            radius = int(input())
            prox_shuffle(verts, iterations, radius)
        elif (MODE == "s"):
            print("lower index? Max is " + str(vlen - 1))
            i = int(input())
            print("highest index (noninclusive)? Max is " + str(vlen))
            j = int(input())
            shuffle(verts, i, j)
        elif (MODE == "d"):
            print("iterations? Verts len is " + str(vlen))
            iter = int(input())
            print("magnitude?")
            mag = float(input())
            displace_its(verts, mag, iter)
        elif (MODE == "o"):
            print("coordinate? 1, 2, or 3")
            coor = int(input())
            print("lower index? Max is " + str(vlen - 1))
            start_ind = int(input())
            print("upper index? Max is " + str(vlen))
            end_ind = int(input())
            sort_coord_replace(verts, coor, start_ind, end_ind)
        elif (MODE == "i"):
            print("axis? 1, 2, or 3")
            axis = int(input())
            print("maximum angle in radians?")
            max_ang = float(input())
            print("lower index? Max is " + str(vlen - 1))
            start_ind = int(input())
            print("upper index? Max is " + str(vlen))
            end_ind = int(input())
            spiral(verts, axis, max_ang, start_ind, end_ind)
        elif (MODE == "f"):
            print("Output file: ", end = "")
            OUTPUT = input()
            break 
    
    with open(OUTPUT, "w") as file:
        for l in headers:
            file.write(arr_to_str(l) + "\n")
        for l in verts:
            file.write(arr_to_str(l) + "\n")
        for l in tangents_normals:
            file.write(arr_to_str(l) + "\n")
        for l in mtl_info:
            file.write(arr_to_str(l) + "\n")
        for l in faces:
            file.write(arr_to_str(l) + "\n")
        
    print("Done! {} made.".format(OUTPUT))

if __name__ == "__main__":
    main()