#from LeapListeners import *
import Mouse
import speech_recognition as sr
import sys, math, thread, time, pyautogui, os, subprocess
from AppKit import NSWorkspace, NSScreen
sys.path.insert(0, "../lib")
import Leap
#from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture

sound = True
haley = True
halp = False

class ScrollListener(Leap.Listener):
    def __init__(self):
        super(ScrollListener, self).__init__()
        self.cursor = Mouse.cursor()
        self.HIGH_THRESHOLD = 0.8
        self.LOW_THRESHOLD = 0.5
        self.ZOOM_THRESHOLD = 0.7
        self.zoom_o = 1
        self.zoom_i = 1
        self.document = NSWorkspace.sharedWorkspace().activeApplication()['NSApplicationName']       
        self.center = {'x':NSScreen.mainScreen().frame().size.width/2, 'y': NSScreen.mainScreen().frame().size.height/2}
        self.scale_factor = {'x':NSScreen.mainScreen().frame().size.width/250, 'y': NSScreen.mainScreen().frame().size.height/320}

    def on_init(self, controller):
        print "Initialized"

    def on_connect(self, controller):
        print "Connected"
        controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE);
        controller.enable_gesture(Leap.Gesture.TYPE_KEY_TAP);
        controller.enable_gesture(Leap.Gesture.TYPE_SCREEN_TAP);

    def on_disconnect(self, controller):
        print "Disconnected"

    def on_exit(self, controller):
        print "Exited"

    def on_frame(self, controller):
        self.document = NSWorkspace.sharedWorkspace().activeApplication()['NSApplicationName']
        if self.document == "Preview":
            self.perform_document_commands(controller)
        elif self.document == "Finder":
            self.perform_finder_commands(controller)
        elif self.document == "Google Chrome":
            self.perform_chrome_commands(controller)
        elif self.document == "Microsoft Word":
            self.perform_word_commands(controller)

    def perform_document_commands(self, controller):
        frame = controller.frame()
        if not frame.hands.is_empty and len(frame.hands) == 1:
            hand = frame.hands[0]
            if not hand.is_valid:
                return

            extended_fingers = hand.fingers.extended()
            normal = hand.palm_normal

            #print(len(extended_fingers))

            if len(extended_fingers) == 1 and extended_fingers[0].type == 1:
                # highlight
                hand_pos = hand.stabilized_palm_position
                x, y = self.map_to_screen_coordinates(hand_pos.x, hand_pos.y)

                # move cursor to x, y
                self.cursor.move(x,y)

                for gesture in frame.gestures():
                    if gesture.type == Leap.Gesture.TYPE_KEY_TAP or gesture.type == Leap.Gesture.TYPE_SCREEN_TAP:
                        self.cursor.click()

            elif len(extended_fingers) == 0 and hand.grab_strength > self.ZOOM_THRESHOLD: # zoom out
                if self.zoom_o == 0:
                    self.cursor.zoom_out()
                    self.zoom_o += 1
                else:
                    self.zoom_o = (self.zoom_o + 1) % 5

            elif normal.x < self.LOW_THRESHOLD and abs(normal.y) > self.HIGH_THRESHOLD and normal.z < self.LOW_THRESHOLD:
                # scroll up/down
                self.cursor.scroll(0, 10*normal.y/abs(normal.y))

            elif abs(normal.x) > self.HIGH_THRESHOLD and normal.y < self.LOW_THRESHOLD and normal.z < self.LOW_THRESHOLD:
                # scroll sideways
                if hand.is_left:
                    self.cursor.scroll(-10, 0)
                else:
                    self.cursor.scroll(10, 0)

            elif abs(normal.z) > self.HIGH_THRESHOLD and normal.y < self.LOW_THRESHOLD and normal.x < self.LOW_THRESHOLD:
                if self.zoom_i == 0:
                    self.cursor.zoom_in()
                    self.zoom_i += 1
                else:
                    self.zoom_i = (self.zoom_i + 1) % 5
        elif len(frame.hands) == 2:
            left = None
            right = None
            if frame.hands[0].is_left:
                left = frame.hands[0]
                right = frame.hands[1]
            else:
                left = frame.hands[1]
                right = frame.hands[0]

            if len(left.fingers.extended()) == 0:
                hand_pos = right.stabilized_palm_position
                x, y = self.map_to_screen_coordinates(hand_pos.x, hand_pos.y)

                # move cursor to x, y
                self.cursor.highlightMove(x,y)

                for gesture in frame.gestures():
                    if gesture.type == Leap.Gesture.TYPE_KEY_TAP or gesture.type == Leap.Gesture.TYPE_SCREEN_TAP:
                        self.cursor.highlight()

    def perform_chrome_commands(self, controller):
        frame = controller.frame()
        if not frame.hands.is_empty and len(frame.hands) == 1:
            hand = frame.hands[0]
            if not hand.is_valid:
                return

            extended_fingers = hand.fingers.extended()
            normal = hand.palm_normal

            if len(extended_fingers) == 1 and extended_fingers[0].type == 1:
                # highlight
                hand_pos = hand.stabilized_palm_position
                x, y = self.map_to_screen_coordinates(hand_pos.x, hand_pos.y)

                # move cursor to x, y
                self.cursor.move(x,y)

                for gesture in frame.gestures():
                    if gesture.type == Leap.Gesture.TYPE_KEY_TAP or gesture.type == Leap.Gesture.TYPE_SCREEN_TAP:
                        self.cursor.click()

            elif len(extended_fingers) == 0 and hand.grab_strength > self.ZOOM_THRESHOLD: # zoom out
                if self.zoom_o == 0:
                    self.cursor.zoom_out()
                    self.zoom_o += 1
                else:
                    self.zoom_o = (self.zoom_o + 1) % 5

            elif normal.x < self.LOW_THRESHOLD and abs(normal.y) > self.HIGH_THRESHOLD and normal.z < self.LOW_THRESHOLD:
                # scroll up/down
                self.cursor.scroll(0, 10*normal.y/abs(normal.y))

            elif abs(normal.x) > self.HIGH_THRESHOLD and normal.y < self.LOW_THRESHOLD and normal.z < self.LOW_THRESHOLD:
                # scroll sideways
                if hand.is_left:
                    self.cursor.scroll(-5, 0)
                else:
                    self.cursor.scroll(5, 0)

            elif abs(normal.z) > self.HIGH_THRESHOLD and normal.y < self.LOW_THRESHOLD and normal.x < self.LOW_THRESHOLD:
                if self.zoom_i == 0:
                    self.cursor.zoom_in()
                    self.zoom_i += 1
                else:
                    self.zoom_i = (self.zoom_i + 1) % 5

    def perform_word_commands(self, controller):
        frame = controller.frame()
        if not frame.hands.is_empty and len(frame.hands) == 1:
            hand = frame.hands[0]
            if not hand.is_valid:
                return

            extended_fingers = hand.fingers.extended()
            normal = hand.palm_normal

            if len(extended_fingers) == 1 and extended_fingers[0].type == 1:
                # highlight
                hand_pos = hand.stabilized_palm_position
                x, y = self.map_to_screen_coordinates(hand_pos.x, hand_pos.y)

                # move cursor to x, y
                self.cursor.move(x,y)

                for gesture in frame.gestures():
                    if gesture.type == Leap.Gesture.TYPE_KEY_TAP or gesture.type == Leap.Gesture.TYPE_SCREEN_TAP:
                        self.cursor.click()

            elif len(extended_fingers) == 0 and hand.grab_strength > self.ZOOM_THRESHOLD: # zoom out
                if self.zoom_o == 0:
                    self.cursor.zoom_out()
                    self.zoom_o += 1
                else:
                    self.zoom_o = (self.zoom_o + 1) % 5

            elif normal.x < self.LOW_THRESHOLD and abs(normal.y) > self.HIGH_THRESHOLD and normal.z < self.LOW_THRESHOLD:
                # scroll up/down
                self.cursor.scroll(0, 10*normal.y/abs(normal.y))

            elif abs(normal.x) > self.HIGH_THRESHOLD and normal.y < self.LOW_THRESHOLD and normal.z < self.LOW_THRESHOLD:
                # scroll sideways
                if hand.is_left:
                    self.cursor.scroll(-10, 0)
                else:
                    self.cursor.scroll(10, 0)

            elif abs(normal.z) > self.HIGH_THRESHOLD and normal.y < self.LOW_THRESHOLD and normal.x < self.LOW_THRESHOLD:
                if self.zoom_i == 0:
                    self.cursor.zoom_in()
                    self.zoom_i += 1
                else:
                    self.zoom_i = (self.zoom_i + 1) % 5

        elif len(frame.hands) == 2:
            left = None
            right = None
            if frame.hands[0].is_left:
                left = frame.hands[0]
                right = frame.hands[1]
            else:
                left = frame.hands[1]
                right = frame.hands[0]

            if len(left.fingers.extended()) == 0:
                hand_pos = right.stabilized_palm_position
                x, y = self.map_to_screen_coordinates(hand_pos.x, hand_pos.y)

                # move cursor to x, y
                self.cursor.move(x,y)

                for gesture in frame.gestures():
                    if gesture.type == Leap.Gesture.TYPE_KEY_TAP or gesture.type == Leap.Gesture.TYPE_SCREEN_TAP:
                        self.cursor.select()

    def perform_finder_commands(self, controller):
        frame = controller.frame()

        if not frame.hands.is_empty:
            hand = frame.hands[0]
            if not hand.is_valid:
                return
            hand_pos = hand.stabilized_palm_position
            x, y = self.map_to_screen_coordinates(hand_pos.x, hand_pos.y)

            # move cursor to x, y
            self.cursor.move(x,y)

            for gesture in frame.gestures():
                if gesture.type == Leap.Gesture.TYPE_KEY_TAP or gesture.type == Leap.Gesture.TYPE_SCREEN_TAP:
                    # check if opening document
                    # x, y = self.map_to_screen_coordinates(hand_pos.x, hand_pos.y)
                    self.cursor.click(x, y)

            
    def map_to_screen_coordinates(self, x, y): 
        new_x, new_y = (
            int(self.scale_factor['x'] * x + self.center['x']),
            -int(self.scale_factor['y'] * (y - 500) + self.center['y'])        
        )
        return (new_x, new_y)

def perform_search(phrase):
    say_something('searching for '+phrase)
    pyautogui.keyDown('command')
    pyautogui.press('f')
    pyautogui.keyUp('command')
    pyautogui.write(phrase)
    pyautogui.press('enter')

def stop_search():
    say_something('stopping search')
    pyautogui.press('esc')

def say_something(phrase):
    os.system('say '+phrase)

def bookmark_page(num):
    if num != "-1":
        pyautogui.keyDown('command')
        pyautogui.keyDown('option')
        pyautogui.press('g')
        pyautogui.keyUp('option')
        pyautogui.keyUp('command')
        pyautogui.write(num)
        pyautogui.press('enter')
    pyautogui.keyDown('command')
    pyautogui.press('d')
    pyautogui.keyUp('command')

def go_to_page(num):
    pyautogui.keyDown('command')
    pyautogui.keyDown('option')
    pyautogui.press('g')
    pyautogui.keyUp('option')
    pyautogui.keyUp('command')
    pyautogui.write(num)
    pyautogui.press('enter')

def text_to_num(num):
    if len(num) == 1:
        return num
    else:
        units = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight","nine", "ten"]
        return str(units.index(num))

def save_document():
    say_something('saving document')
    pyautogui.keyDown('command')
    pyautogui.press('s')
    pyautogui.keyUp('command')

def close_document():
    say_something('closing document')
    pyautogui.keyDown('command')
    pyautogui.keyDown('shift')
    pyautogui.press('w')
    pyautogui.keyUp('shift')
    pyautogui.keyUp('command')
    pyautogui.click()

def go_down():
    say_something('going to next page')
    pyautogui.keyDown('option')
    pyautogui.press('down')
    pyautogui.keyUp('option')

def go_up():
    say_something('going to previous page')
    pyautogui.keyDown('option')
    pyautogui.press('up')
    pyautogui.keyUp('option')

def zoom_in():
    say_something('zooming in')
    pyautogui.keyDown('command')
    pyautogui.press('=')
    pyautogui.keyUp('command')

def zoom_out():
    say_something('zooming out')
    pyautogui.keyDown('command')
    pyautogui.press('-')
    pyautogui.keyUp('command')

def open_bar(bar):
    if 'thumbnail' in bar:
        num = '2'
        say_something('opening thumbnails')
    elif 'content' in bar:
        num = '3'
        say_something('opening table of contents')
    elif 'bookmark' in bar:
        num = '5'
        say_something('opening bookmarks')

    pyautogui.keyDown('command')
    pyautogui.keyDown('option')
    pyautogui.press(num)
    pyautogui.keyUp('command')
    pyautogui.keyUp('option')

def close_bar():
    say_something('closing sidebar')
    pyautogui.keyDown('command')
    pyautogui.keyDown('option')
    pyautogui.press('1')
    pyautogui.keyUp('command')
    pyautogui.keyUp('option')

def open_help():
    say_something('opening user guide')
    os.system('open ../new_help.pdf')

def close_help():
    say_something('closing user guide')
    pyautogui.keyDown('command')
    pyautogui.press('w')
    pyautogui.keyUp('command')

def finish_program():
    say_something('shutting down program')
    os._exit(1)

def sound_change():
    global sound
    sound = not sound

def new_tab():
    say_something('opening new tab')
    pyautogui.keyDown('command')
    pyautogui.press('t')
    pyautogui.keyUp('command')

def search_google(text):
    say_something('googling')
    pyautogui.keyDown('command')
    pyautogui.keyDown('option')
    pyautogui.press('f')
    pyautogui.keyUp('command')
    pyautogui.keyUp('option')

    pyautogui.write(text)
    pyautogui.press('enter')

def close_tab():
    say_something('closing tab')
    pyautogui.keyDown('command')
    pyautogui.press('w')
    pyautogui.keyUp('command')

def previous_tab():
    say_something('moving to previous tab')
    pyautogui.keyDown('ctrl')
    pyautogui.keyDown('shift')
    pyautogui.press('tab')
    pyautogui.keyUp('shift')
    pyautogui.keyUp('ctrl')

def next_tab():
    say_something('moving to next tab')
    pyautogui.keyDown('ctrl')
    pyautogui.press('tab')
    pyautogui.keyUp('ctrl')

def go_back():
    #back arrow
    say_something('moving back')
    pyautogui.keyDown('command')
    pyautogui.press('left')
    pyautogui.keyUp('command')

def select_all():
    pyautogui.keyDown('command')
    pyautogui.press('a')
    pyautogui.keyUp('command')

def bookmark_tab():
    pyautogui.keyDown('command')
    pyautogui.press('d')
    pyautogui.keyUp('command')

def open_bookmarks():
    pyautogui.keyDown('command')
    pyautogui.keyDown('option')
    pyautogui.press('b')
    pyautogui.keyUp('option')
    pyautogui.keyUp('command')

def open_history():
    pyautogui.keyDown('command')
    pyautogui.press('y')
    pyautogui.keyUp('command')

def perform_command(cmd):
    proc = True
    global halp

    if 'general' in cmd:
        go_to_page('1')
    elif 'stop using' in cmd:
        say_something('stopping use of haley to activate commands')
        global haley
        haley = False

    elif 'chrome' in cmd:
        if halp:
            go_to_page('4')
        else:
            say_something('opening chrome')
            os.system('open -a "Google Chrome"')

    elif 'finder' in cmd:
        say_something('opening finder')
        os.system('open -a "Finder"')

    elif 'word' in cmd:
        if halp:
            go_to_page('3')
        else:
            say_something('opening word document')
            os.system('open -a "Microsoft Word"')

    elif 'preview' in cmd:
        if halp:
            go_to_page('2')
        else:
            say_something('opening preview')
            os.system('open -a "Preview"')

    elif 'sound' in cmd:
        sound_change()

    elif 'close help' in cmd:
        halp = False
        close_help()

    elif 'help' in cmd:
        halp = True
        open_help()

    elif 'search for' in cmd:
        phrase = cmd.split('search for ')[1]
        if len(phrase) < 1:
            return False
        perform_search(phrase)

    elif 'exit search' in cmd:
        stop_search()

    elif 'zoom in' in cmd:
        zoom_in()

    elif 'zoom out' in cmd:
        zoom_out()

    elif 'stop program' in cmd:
        finish_program()
        return True

    else:

        app = NSWorkspace.sharedWorkspace().activeApplication()['NSApplicationName']

        if app == "Preview":
            if 'open' in cmd:
                open_bar(cmd.split('open ')[1])

            elif 'next' in cmd:
                pyautogui.press('enter')

            elif 'close sidebar' in cmd:
                close_bar()

            elif 'bookmark' in cmd:
                phrase = cmd.split('bookmark')[1]
                if 'this page' in phrase:
                    say_something('bookmarking current page')
                    bookmark_page("-1")
                elif 'page' in phrase:
                    num = phrase.split('page ')[1]
                    say_something('bookmarking page '+ num)
                    bookmark_page(text_to_num(num))
                else:
                    return False

            elif 'go to page' in cmd:
                num = cmd.split('go to page ')[1]
                go_to_page(text_to_num(num))

            elif 'go to next page' in cmd:
                go_down()

            elif 'go to previous page' in cmd:
                go_up()

            else:
                proc = False

            if 'save' in cmd:
                save_document()
                proc = True

            if 'close document' in cmd:
                close_document()
                return True

        elif app == "Google Chrome":
            if 'google' in cmd:
                search_google(cmd.split('google ')[1])
            elif 'new tab' in cmd:
                new_tab()
            elif 'close tab' in cmd:
                close_tab()
            elif 'previous tab' in cmd:
                previous_tab()
            elif 'next tab' in cmd:
                next_tab()
            elif 'next' in cmd:
                pyautogui.press('enter')
            elif 'back' in cmd:
                go_back()
            elif 'open bookmark' in cmd:
                open_bookmarks()
            elif 'open history' in cmd:
                open_history()
            elif 'bookmark' in cmd:
                bookmark_tab()
            else:
                proc = False

        elif app == "Microsoft Word":
            if 'write' in cmd:
                pyautogui.write(cmd.split('write')[1])
            elif 'right' in cmd:
                pyautogui.write(cmd.split('right')[1])
            elif 'delete' in cmd:
                pyautogui.press('del')
            elif 'bold' in cmd:
                pyautogui.keyDown('command')
                pyautogui.press('b')
                pyautogui.keyUp('command')
            elif 'underline' in cmd:
                pyautogui.keyDown('command')
                pyautogui.press('u')
                pyautogui.keyUp('command')
            elif 'italic' in cmd:
                pyautogui.keyDown('command')
                pyautogui.press('i')
                pyautogui.keyUp('command')
            elif 'next' in cmd:
                pyautogui.press('enter')
            elif 'save' in cmd:
                save_document()
            elif 'close document' in cmd:
                close_document()
            elif "select everything" in cmd:
                select_all()
            else:
                proc = False

    return proc

# this is called from the background thread
def callback(recognizer, audio):
    # received audio data, now we'll recognize it using Google Speech Recognition
    try:
        text = recognizer.recognize_google(audio).lower()
        print("Google Speech Recognition thinks you said " + text)
        if sound:
            print('\007')

        if haley:
            performed = False
            if 'haley' in text:
                performed = perform_command(text.split('haley')[1])
            elif 'hey leap' in text:
                performed = perform_command(text.split('hey leap')[1])
            elif 'hay lee' in text:
                performed = perform_command(text.split('hay lee')[1])
            elif 'hailey' in text:
                performed = perform_command(text.split('hailey')[1])

            if not performed:
                say_something("sorry I could not understand you")
        else:
            if not perform_command(text):
                say_something("sorry I could not understand you")

    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

def main():    
    global stopped 
    scroll_listener = ScrollListener()

    controller = Leap.Controller()
    controller.set_policy_flags(Leap.Controller.POLICY_BACKGROUND_FRAMES)

    # Have the sample listener receive events from the controller
    controller.add_listener(scroll_listener)

    r = sr.Recognizer()
    m = sr.Microphone()
    with m as source:
        r.adjust_for_ambient_noise(source)  # we only need to calibrate once, before we start listening

    # start listening in the background (note that we don't have to do this inside a `with` statement)
    stop_listening = r.listen_in_background(m, callback)
    # `stop_listening` is now a function that, when called, stops background listening

    os.system('say assistant enabled. say help if you want to see the user guide')

    # Keep this process running until Enter is pressed
    print "Press Enter to quit..."
    try:
        sys.stdin.readline()
    except KeyboardInterrupt:
        pass
    finally:
        # Remove the sample listener when done
        controller.remove_listener(scroll_listener)
        stop_listening(wait_for_stop=False)


if __name__ == "__main__":
    main()
