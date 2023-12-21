import numpy as np
import matplotlib.pyplot as plt

vertices = []
vertices1 = []
a = []


class Point:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z


def Pixel(col):
    imgData = np.zeros((1, 1, 4), dtype=np.uint8)
    imgData[0, 0, 0] = col['r']
    imgData[0, 0, 1] = col['g']
    imgData[0, 0, 2] = col['b']
    imgData[0, 0, 3] = col['a']
    return imgData


def Grafic():
    # big pyramid
    vertices.extend([Point(180, 65, 0), Point(490, 340, 550), Point(50, 184, 550),
                     Point(350, 181, 550)])

    # BC
    vertices.extend([vertices[1], vertices[2]])
    # CD
    vertices.extend([vertices[2], vertices[3]])
    # DB
    vertices.extend([vertices[3], vertices[1]])

    # в алгоритме Z-буфера рассматриваю грани
    # (ABC)
    Z_buf(vertices[0], vertices[1], vertices[3], {'r': 165, 'g': 12, 'b': 15, 'a': 250})
    # (ACD)
    Z_buf(vertices[0], vertices[3], vertices[5], {'r': 255, 'g': 25, 'b': 9, 'a': 255})
    # (ABD)
    Z_buf(vertices[0], vertices[1], vertices[5], {'r': 2, 'g': 2, 'b': 5, 'a': 255})

    # (BCD)
    Z_buf(vertices[1], vertices[3], vertices[5], {'r': 229, 'g': 102, 'b': 153, 'a': 255})

    # short pyramid
    vertices1.extend([Point(200, 140, 0), Point(360, 330, 200), Point(150, 240, 200),
                      Point(360, 245, 200)])

    # BC
    vertices1.extend([vertices1[1], vertices1[2]])
    # CD
    vertices1.extend([vertices1[2], vertices1[3]])
    # DB
    vertices1.extend([vertices1[3], vertices1[1]])

    # (ABC)
    Z_buf(vertices1[0], vertices1[1], vertices1[3], {'r': 15, 'g': 102, 'b': 105, 'a': 255})
    # (ACD)
    Z_buf(vertices1[0], vertices1[3], vertices1[5], {'r': 250, 'g': 255, 'b': 9, 'a': 255})
    # (ABD)
    Z_buf(vertices1[0], vertices1[1], vertices1[5], {'r': 225, 'g': 2, 'b': 105, 'a': 255})

    # (BCD)
    Z_buf(vertices1[1], vertices1[3], vertices1[5], {'r': 220, 'g': 212, 'b': 15, 'a': 255})



# алгоритм Z-буфера реализую с помощью растеризации треугольника
def Z_buf(b1, b2, b3, col):
    foc = 500000
    dx13, dx12, dx23 = 0, 0, 0
    dz13, dz12, dz23 = 0, 0, 0
    kz, bz = 0, 0

    # упорядочиваем координаты по значению y
    if b2.y < b1.y:
        b1, b2 = b2, b1
    if b3.y < b1.y:
        b1, b3 = b3, b1
    if b3.y < b2.y:
        b2, b3 = b3, b2

    # нахождение приращения
    if b3.y != b1.y:
        dx13 = (b3.x - b1.x) / (b3.y - b1.y)
        dz13 = (b3.z - b1.z) / (b3.y - b1.y)

    if b2.y != b1.y:
        dx12 = (b2.x - b1.x) / (b2.y - b1.y)
        dz12 = (b2.z - b1.z) / (b2.y - b1.y)

    if b3.y != b2.y:
        dx23 = (b3.x - b2.x) / (b3.y - b2.y)
        dz23 = (b3.z - b2.z) / (b3.y - b2.y)

    wx1, wx2, _dx13 = int(b1.x), int(b1.x), dx13
    wz1, wz2, _dz13 = int(b1.z), int(b1.z), dz13

    # упорядочиваем приращения
    if dx13 > dx12:
        dx13, dx12 = dx12, dx13
    if dz13 > dz12:
        dz13, dz12 = dz12, dz13

    # первый полутреугольник
    for i in range(int(b1.y), int(b2.y)):
        if wx1 != wx2:  # Check if the denominator is not zero
            kz = (wz1 - wz2) / (wx1 - wx2)
            bz = wz2 - (kz * wx2)
            for j in range(int(wx1), int(wx2) + 1):
                z_gr = j * kz + bz
                if a[i][j] > z_gr:
                    a[i][j] = z_gr
                    x_gr = round(foc * j / (z_gr + foc))
                    y_gr = round(foc * i / (z_gr + foc))
                    context[y_gr, x_gr] = [col['r'], col['g'], col['b'], col['a']]

        wx1 += dx13
        wx2 += dx12
        wz1 += dz13
        wz2 += dz12

    # случай когда верхнего треугольника нет
    if b1.y == b2.y:
        wx1, wx2 = int(b1.x), int(b2.x)
        wz1, wz2 = int(b1.z), int(b2.z)

    # упорядочиваем приращения
    if _dx13 < dx23:
        _dx13, dx23 = dx23, _dx13
    if _dz13 < dz23:
        _dz13, dz23 = dz23, _dz13

    # второй полутреугольник
    for i in range(int(b2.y), int(b3.y) + 1):
        if wx1 != wx2:  # Check if the denominator is not zero
            kz = (wz1 - wz2) / (wx1 - wx2)
            bz = wz2 - (kz * wx2)
            for j in range(int(wx1), int(wx2) + 1):
                z_gr = j * kz + bz
                if a[i][j] > z_gr:
                    a[i][j] = z_gr
                    x_gr = round(foc * j / (z_gr + foc))
                    y_gr = round(foc * i / (z_gr + foc))
                    context[y_gr, x_gr] = [col['r'], col['g'], col['b'], col['a']]

        wx1 += _dx13
        wx2 += dx23
        wz1 += _dz13
        wz2 += dz23


context = np.zeros((500, 500, 4), dtype=np.uint8)
a = np.full((1500, 1500), 10000000.0)

Grafic()
plt.imshow(context)
plt.show()
