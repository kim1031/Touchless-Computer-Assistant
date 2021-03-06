# Touchless-Computer-Assistant

Touchless Computer Assistant (TCA) enables you to control your Mac with just speech and gesture commands. 

## Folder Contents:
- ./src/Assistant.py: contains code needed to activate TCA (enables controllers for speech and gesture commands)
- ./src/Mouse.py: contains helper code for performing cursor movements such as scrolling or moving your mouse
- new_help.pdf: the user guide (able to open using voice commands)
- ./lib: contains relevant Leap SDK files needed to connect the Leap Motion Controller to Python, should be replaced

## Requirements for using TCA:
### Hardware:
- Leap Motion Controller
- Mac Laptop
- Headphones with a mic (although this is not a must, it's needed for good user experience)

### Software:
- Python 2.7
- Leap Motion SDK for macOS (download from here: https://developer.leapmotion.com/sdk-leap-motion-controller/)
- portaudio (download using ```brew install portaudio```)
- swig (download using ```brew install swig```)
- Required Python packages (install using ```pip install```)
  - pyobjc
  - Pillow
  - PyAudio
  - PyAutoGUI=0.9.40
  - SpeechRecognition
  - wheel
  - MouseInfo
  - rubicon-objc

## Additional Set-up:
1. Enable terminal to access keyboard/mouse: Go into System Preferences -> Security & Privacy -> Privacy -> Accessibility and allow Terminal (or wherever you wish to run the prgoram from) to control your computer
2. Using your terminal, set up a virtual environment as follows: (Note that you need to ```conda activate leap``` each time you restart your Terminal)
```
conda create -n leap python=2.7
conda activate leap
```
3. Download the Leap Motion SDK and replace the contents of the current ```lib``` folder (of this repo) with the contents of the ```lib``` folder in the downloaded SDK
3. Patch LeapPython.so by performing the following commands. Note that you need to find and replace ```[path-to-libpython2.7.dylib]```. This is the absolute path to the file ```libpython2.7.dylib``` which comes as part of your Python environment that you set up in Step 2.
```
cd lib
install_name_tool -change /Library/Frameworks/Python.framework/Versions/2.7/Python [path-to-libpython2.7.dylib] LeapPython.so
```
You may receive a warning, but that's okay!
4. Install the required Python packages from above

## Running the Program:
```
cd src
python Assistant.py
```
Connect your Leap sensor to the laptop and run the above command -- TCA should start! Please note that you should have your headphones in for the best experience.
