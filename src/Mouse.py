from Quartz.CoreGraphics import (CGEventCreateMouseEvent,CGEventPost,CGMainDisplayID,
    CGDisplayBounds,CGPointMake,CGEventCreateScrollWheelEvent,CGEventSourceCreate,
    kCGScrollEventUnitPixel,kCGScrollEventUnitLine,kCGEventMouseMoved,kCGEventLeftMouseDragged,
    kCGEventLeftMouseDown,kCGEventLeftMouseUp,kCGMouseButtonLeft,kCGEventRightMouseDown,
    kCGEventRightMouseDown,kCGEventRightMouseUp,kCGMouseButtonRight,kCGHIDEventTap)
from AppKit import NSWorkspace
# from pynput.mouse import Button, Controller
import pyautogui, os, time

def MouseMove(x,y):
    event = CGEventCreateMouseEvent(None, kCGEventMouseMoved, CGPointMake(x, y), 0)
    CGEventPost(kCGHIDEventTap, event)

def MouseClick(x,y):
    event = CGEventCreateMouseEvent(None, kCGEventLeftMouseDown, (x,y),0)
    CGEventPost(kCGHIDEventTap, event)

    event = CGEventCreateMouseEvent(None, kCGEventLeftMouseUp, (x,y), 0)
    CGEventPost(kCGHIDEventTap, event)

def MouseScroll(x_movement, y_movement):  #Movements should be no larger than +- 10
    scrollWheelEvent = CGEventCreateScrollWheelEvent(
            None,  #No source
            kCGScrollEventUnitPixel,  #We are using pixel units
            2,  #Number of wheels(dimensions)
            y_movement,
            x_movement)
    CGEventPost(kCGHIDEventTap, scrollWheelEvent)

class cursor(object):
    def __init__(self):
        self.x_max = CGDisplayBounds(CGMainDisplayID()).size.width - 1
        self.y_max = CGDisplayBounds(CGMainDisplayID()).size.height - 1
        self.x = 0
        self.y = 0
        self.h = True
        self.s = True

    def move(self, posx, posy):  #Move to coordinates
        self.x = posx
        self.y = posy
        if self.x > self.x_max: 
            self.x = self.x_max
        if self.y > self.y_max: 
            self.y = self.y_max
        if self.x < 0.0: 
            self.x = 0.0
        if self.y < 0.0: 
            self.y = 0.0
        # print 'move ' + str(self.x) + ',' + str(self.y)
        MouseMove(self.x, self.y)
        # pyautogui.moveTo(self.x, self.y)

    def click(self, posx=None, posy=None):  #Click at coordinates (current coordinates by default)
        if posx == None:
            posx = self.x
        if posy == None:
            posy = self.y
        print('\007')
        MouseClick(posx, posy)
        # pyautogui.moveTo(self.x, self.y)
        # pyautogui.click(posx, posy, clicks = 2)
        if NSWorkspace.sharedWorkspace().activeApplication()['NSApplicationName'] == "Finder":
            # pyautogui.keyDown('command')
            # pyautogui.press('o')
            # pyautogui.keyUp('command')
            pyautogui.doubleClick()

    def scroll(self, x_movement, y_movement):
        #print 'scroll ' + str(x_movement) + ',' + str(y_movement)
        # MouseScroll(x_movement, y_movement)
        # self.mouse.scroll(x_movement,y_movement)
        pyautogui.hscroll(x_movement)
        pyautogui.scroll(y_movement)

    def zoom_in(self):
        self.say_something('zooming in')
        pyautogui.keyDown('command')
        pyautogui.press('=')
        pyautogui.keyUp('command')

    def zoom_out(self):
        self.say_something('zooming out')
        pyautogui.keyDown('command')
        pyautogui.press('-')
        pyautogui.keyUp('command')

    def say_something(self, phrase):
        os.system('say '+phrase)

    def highlight(self):
        if self.h:
            #start highlighting
            self.say_something("highlighting")
            pyautogui.keyDown('command')
            pyautogui.keyDown('ctrl')
            pyautogui.press('h')
            pyautogui.keyUp('ctrl')
            pyautogui.keyUp('command')
            # pyautogui.click()
            # pyautogui.mouseDown()
            # pyautogui.keyDown('shift')
            # pyautogui.dragTo()
            # pyautogui.mouseDown()
            self.h = False
        else:
            #stop highlighting
            # pyautogui.keyUp('shift')
            pyautogui.mouseUp()

            self.say_something('stop highlighting')
            self.h = True

    def highlightMove(self, posx, posy):
        self.x = posx
        self.y = posy
        if self.x > self.x_max: 
            self.x = self.x_max
        if self.y > self.y_max: 
            self.y = self.y_max
        if self.x < 0.0: 
            self.x = 0.0
        if self.y < 0.0: 
            self.y = 0.0
        
        if not self.h:
            pyautogui.dragTo(self.x,self.y)
        else:
            MouseMove(self.x,self.y)

    def select(self):
        if self.s:
            #start selecting
            self.say_something('started selecting')
            pyautogui.mouseDown()
            self.s = False
        else:
            #stop highlighting
            pyautogui.mouseUp()
            self.s = True
        