import keyboard, time
from sparkl_backend import *

# Key press variables -- toggle Sparkl on / off with s + p + k
s_pressed = False 
p_pressed = False 
k_pressed = False
alt_pressed = False

# Sparkl on / off
sparkl_on = False

# Dictionary of key and messages pairings -- replace these sentences with calls to
# a function in interface.py 
key_pairings = {'1': "agreement", '2':"disagreement", '3':"tentative",
'4': "happy", '5': "funny", '6': "witty", '7': "flirty", 
'8': "sad", '9': "insightful", '0': "love"}

# Partial user input
partial_input = ""

# Characters to ignore
ignore_set = {"caps lock", "tab", "ctrl", "alt", "fn", "shift", "up", 
"down", "right", "left", "del", "esc"}

def toggle_sparkl():
    global sparkl_on, partial_input
    partial_input = ""
    if not sparkl_on:
        print("Sparkl activated")
        sparkl_on = True
    else:
        print("Sparkl deactivated")
        sparkl_on = False
        
    # Remove "spk" text typed by the user
    for _ in range(3):
        keyboard.press_and_release('backspace')

# Keys that generate sentences
def generate_sentence(message):
    keyboard.press_and_release('backspace')
    time.sleep(0.01)
    keyboard.write(message)

# Basic welcome message

welcome_message_desktop = '''
Welcome to the mobile version of Sparkl! To toggle Sparkl on/off, press alt + s + p + k. 
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

For example, after toggling Sparkl on and
typing "I love my cat " followed by a 0 might generate "I love my cat because he always
plays around with me. He's so sweet!"

Happy chatting!
'''
print(welcome_message_desktop)

### Main loop
while True:
    # Wait for the next event
    event = keyboard.read_event()

    # Handling key presses -- toggling Sparkl
    if event.event_type == keyboard.KEY_DOWN and event.name == 's':
        s_pressed = True
    elif event.event_type == keyboard.KEY_DOWN and event.name == 'p':
        p_pressed = True
    elif event.event_type == keyboard.KEY_DOWN and event.name == 'k':
        k_pressed = True
    elif event.event_type == keyboard.KEY_DOWN and event.name == 'alt':
        alt_pressed = True

    # Handling key  -- toggling Sparkl
    if event.event_type == keyboard.KEY_UP and event.name == 's':
        s_pressed = False
    elif event.event_type == keyboard.KEY_UP and event.name == 'p':
        p_pressed = False
    elif event.event_type == keyboard.KEY_UP and event.name == 'k':
        k_pressed = False
    elif event.event_type == keyboard.KEY_UP and event.name == 'alt':
        alt_pressed = False
    
    # If on, convert emojis into emotions
    if sparkl_on and event.event_type == keyboard.KEY_DOWN:
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

    # Toggle Sparkl on / off
    if s_pressed and p_pressed and k_pressed:
        toggle_sparkl()
