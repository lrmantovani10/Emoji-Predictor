import keyboard, time
from backend import *

# Key press variables -- toggle predictions on / off with alt + w
w_pressed = False
alt_pressed = False

# Predictions on / off
predictor_on = False

# Dictionary of key and messages pairings -- replace these sentences with calls to
# a function in interface.py 
key_pairings = {'1': "agreement", '2':"disagreement", '3':"tentative",
'4': "happy", '5': "funny", '6': "witty", '7': "flirty", 
'8': "sad", '9': "standard", '0': "love"}

# Partial user input
partial_input = ""

# Characters to ignore
ignore_set = {"caps lock", "tab", "ctrl", "alt", "fn", "shift", "up", 
"down", "right", "left", "del", "esc"}

def toggle_predictor():
    global predictor_on, partial_input
    partial_input = ""
    if not predictor_on:
        print("predictor activated")
        predictor_on = True
    else:
        print("predictor deactivated")
        predictor_on = False

# Keys that generate sentences
def generate_sentence(message):
    keyboard.press_and_release('backspace')
    time.sleep(0.01)
    keyboard.write(message)

# Basic welcome message for desktop
welcome_message_desktop = '''
Welcome to the desktop version of the emoji predictor! To toggle the emoji predictor on/off, press alt + w.
Once it is on, inserting any number from 1- 10 will generate a sentence 
completion in a specific tone, according to the key / value pairs below. 

1: agreement
2: disagreement
3: tentative
4: happy
5: funny
6: witty
7: flirty
8: sad
9: insightful 
0: love

For example, after toggling Emoji predictor on and
typing "I love my cat " followed by a 0 might generate "I love my cat because he always
plays around with me. He's so sweet!"

Happy chatting!
'''
print(welcome_message_desktop)

### Main loop
while True:
    # Wait for the next event
    event = keyboard.read_event()

    # Handling key presses -- toggling Emoji predictor
    if event.event_type == keyboard.KEY_DOWN and event.name == 'w':
        w_pressed = True
    elif event.event_type == keyboard.KEY_DOWN and event.name == 'alt':
        alt_pressed = True

    # Handling key  -- toggling Emoji predictor
    if event.event_type == keyboard.KEY_UP and event.name == 'w':
        w_pressed = False
    elif event.event_type == keyboard.KEY_UP and event.name == 'alt':
        alt_pressed = False
    
    # If on, convert emojis into emotions
    if predictor_on and event.event_type == keyboard.KEY_DOWN:
        processed_event = event.name
        if processed_event == "space":
            processed_event = " "
        elif processed_event == "backspace":
            processed_event = ""
            partial_input = partial_input[:len(partial_input) - 1]
        elif processed_event in ignore_set:
            processed_event = ""
        elif event.name == "enter":
            partial_input, processed_event = "", ""
        
        partial_input += processed_event
        if event.name in key_pairings:
            partial_input = partial_input[:len(partial_input) - 1]
            generate_sentence(process_input(partial_input, key_pairings[processed_event]))
            partial_input = ""

    # Toggle Emoji predictor on / off
    if w_pressed and alt_pressed:
        toggle_predictor()
