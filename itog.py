import os
import pygame
import math
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from PIL import Image as Image
import numpy
DropSpeed = 0.0
v = 4
pos0 = (0.0, 0.0, 1.0, 0.0)
pos1 = (150.0, 0.0, 700.0, 1.0)
direction = (0.0, 0.0, -100.0)
diffuseColor1 = (0.2, 0.4, 0.9, 0.0)
ambientColor0 = (0.2, 0.5, 0.8, 0.0)
diffuseColor0 = (0.9, 0.1, 0.2, 0.0)
h = 500
w = 500


def display():
    global pos0, pos1, direction, diffuseColor0, diffuseColor1, ambientColor0
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glLightfv(GL_LIGHT0, GL_DIFFUSE, diffuseColor0)
    glLightfv(GL_LIGHT0, GL_AMBIENT, ambientColor0)
    glLightfv(GL_LIGHT0, GL_POSITION, pos0)
    glLightfv(GL_LIGHT1, GL_DIFFUSE, diffuseColor1)
    glLightfv(GL_LIGHT1, GL_POSITION, pos1)
    glLightfv(GL_LIGHT1, GL_SPOT_DIRECTION, direction)
    glLightf(GL_LIGHT1, GL_SPOT_CUTOFF, 15.0)
    glLightf(GL_LIGHT1, GL_SPOT_EXPONENT, 100.0)
    #glutSolidSphere(150.0, 256, 256)# lighting sphere without texturing

    tex = read_texture('bruh.bmp') #sphere with texturing
    qobj = gluNewQuadric()
    gluQuadricTexture(qobj, GL_TRUE)
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, tex)
    glBegin(GL_TRIANGLES)
    gluSphere(qobj, 150, 256, 256)
    color = [1.0, 0.0, 0.0, 1.0]
    glMaterialfv(GL_FRONT, GL_DIFFUSE, color)

    glFlush()

def read_texture(filename):
    img = Image.open(filename)
    img_data = numpy.array(list(img.getdata()), numpy.int8)
    textID = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, textID)
    glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, img.size[0], img.size[1], 0, GL_RGB, GL_UNSIGNED_BYTE, img_data)
    return textID

def TimerFuncthion(value):
    global DropSpeed
    global v
    DropSpeed -= v
    glTranslatef(0, DropSpeed, 0)
    glutPostRedisplay()
    glutTimerFunc(30, TimerFuncthion, 1)
    if (DropSpeed <= -50):
        DropSpeed = abs(DropSpeed)
        DropSpeed += v


def main():
    glutInit()
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB | GL_DEPTH_BUFFER_BIT)
    glutInitWindowPosition(100, 100)
    glutInitWindowSize(500, 500)
    glutCreateWindow("DrawSphere")
    glClearColor(0.1, 0.1, 0.15, 0.0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-500, 500, -500, 500, -500, 500)
    glutDisplayFunc(display)
    #lighting
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHT1)
    #sphere bouncing
    glutTimerFunc(10, TimerFuncthion, 1)
    glutMainLoop()
    #lighting
    glDisable(GL_LIGHT0)
    glDisable(GL_LIGHT1)
    glDisable(GL_LIGHTING)
    glDisable(GL_DEPTH_TEST)


def handleResize(): #it is have no sence
    global w, h
    a = w / h
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glFrustum(-a, a, 1.0, 1.0, 2.0, 100.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


if __name__ == '__main__':
    main()