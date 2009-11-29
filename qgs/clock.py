# -*- coding: utf-8 -*-
"""The user interface for our app"""

import os,sys,time

# Import Qt modules
from PyQt4 import QtCore,QtGui, QtOpenGL

# Import the compiled UI module
from ui_clock import Ui_Form

from random import randint, shuffle

# Create a class for our main window
class Main(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)

        # This is always the same
        self.ui=Ui_Form()
        self.ui.setupUi(self)

        self.scene=QtGui.QGraphicsScene()
        self.scene.setSceneRect(0,0,600,400)
        self.ui.view.setScene(self.scene)
        #self.ui.view.setViewport(QtOpenGL.QGLWidget())
        self.populate()
        self.setWindowState(QtCore.Qt.WindowMaximized)

        self.animator=QtCore.QTimer()
        self.animator.timeout.connect(self.animate)
        self.animate()

    def populate(self):
        self.digits=[]
        self.animations=[]
        font=QtGui.QFont('White Rabbit')
        font.setPointSize(120)

        self.dot1=QtGui.QGraphicsTextItem(':')
        self.dot1.setFont(font)
        self.dot1.setPos(140,0)
        self.scene.addItem(self.dot1)
        self.dot2=QtGui.QGraphicsTextItem(':')
        self.dot2.setFont(font)
        self.dot2.setPos(410,0)
        self.scene.addItem(self.dot2)

        for i in range(60):
            l = QtGui.QGraphicsTextItem(str(i%10))
            l.setFont(font)
            l.setZValue(-100)
            l.setPos(randint(0,500),randint(150,300))
            l.setOpacity(.3)
            #l.setDefaultTextColor(QtGui.QColor('lightgray'))
            self.scene.addItem(l)
            self.digits.append(l)

    def animate(self):
        self.animations=range(0,60)

        def animate_to(t,item,x,y,angle):
            animation=QtGui.QGraphicsItemAnimation()
            timeline=QtCore.QTimeLine(1000)
            timeline.setFrameRange(0,100)
            animation.setPosAt(t,QtCore.QPointF(x,y))
            animation.setRotationAt(t,angle)
            animation.setItem(item)
            animation.setTimeLine(timeline)
            return animation

        offsets=range(6)
        shuffle(offsets)

        # Some, animate with purpose
        h1,h2=map(int,'%02d'%time.localtime().tm_hour)
        h1+=offsets[0]*10
        h2+=offsets[1]*10
        self.animations[h1]=animate_to(0.2,self.digits[h1],-40,0,0)
        self.animations[h2]=animate_to(0.2,self.digits[h2],50,0,0)

        m1,m2=map(int,'%02d'%time.localtime().tm_min)
        m1+=offsets[2]*10
        m2+=offsets[3]*10
        self.animations[m1]=animate_to(0.2,self.digits[m1],230,0,0)
        self.animations[m2]=animate_to(0.2,self.digits[m2],320,0,0)

        s1,s2=map(int,'%02d'%time.localtime().tm_sec)
        s1+=offsets[4]*10
        s2+=offsets[5]*10
        self.animations[s1]=animate_to(0.2,self.digits[s1],500,0,0)
        self.animations[s2]=animate_to(0.2,self.digits[s2],590,0,0)

        # Random animations
        for i in range(60):
            l = self.digits[i]
            if i in [h1,h2,m1,m2,s1,s2]:
                l.setOpacity(1)
                continue
            l.setOpacity(.3)
            self.animations[i]=animate_to(1,l,randint(0,500),randint(0,300),randint(0,0))

        [ animation.timeLine().start() for animation in self.animations ]


        self.animator.start(1000)
        

def main():
    # Again, this is boilerplate, it's going to be the same on
    # almost every app you write
    app = QtGui.QApplication(sys.argv)
    window=Main()
    window.show()


    # It's exec_ because exec is a reserved word in Python
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
