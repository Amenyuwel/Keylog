import pyautogui
import time
import keyboard
import mouse
import pickle  # Import the pickle module

def click_fruit(x, y):
    """Clicks on the fruit at the specified coordinates."""
    pyautogui.click(x, y)
    print(f"Clicked fruit at {x}, {y}")

def click_machine(x, y):
    """Clicks on the machine at the specified coordinates."""
    pyautogui.click(x, y)
    print(f"Clicked machine at {x}, {y}")

def collect_honey(x, y):
    """Clicks to collect the honey at the specified coordinates."""
    pyautogui.click(x, y)
    print(f"Collected honey at {x}, {y}")

def record_actions():
    """Records mouse clicks and key presses until 'q' is pressed."""
    actions = []
    print("Recording started. Press 'q' to stop.")

    def on_mouse_event(event):
        if isinstance(event, mouse.ButtonEvent) and event.event_type == 'down':
            x, y = mouse.get_position()
            actions.append({
                'type': 'click',
                'x': x,
                'y': y,
                'button': event.button
            })
            print(f"Click recorded at {x}, {y} with button {event.button}")

    def on_key_event(event):
        if event.name.lower() != 'q':  # Exclude 'q' from recorded actions
            actions.append({'type': 'key', 'key': event.name})
            print(f"Key {event.name} pressed")

    mouse.hook(on_mouse_event)
    keyboard.on_press(on_key_event)

    keyboard.wait('q')  # Wait until 'q' is pressed
    mouse.unhook(on_mouse_event)
    keyboard.unhook_all()

    print("Recording stopped.")
    return actions

def save_actions(actions, filename="recorded_actions.pkl"):
    """Saves the recorded actions to a file using pickle."""
    with open(filename, 'wb') as f:
        pickle.dump(actions, f)
    print(f"Actions saved to {filename}")

def load_actions(filename="recorded_actions.pkl"):
    """Loads the recorded actions from a file using pickle."""
    try:
        with open(filename, 'rb') as f:
            actions = pickle.load(f)
        print(f"Actions loaded from {filename}")
        return actions
    except FileNotFoundError:
        print(f"File {filename} not found.  Please record actions first.")
        return None

def replay_actions(actions):
    """Replays the recorded actions with a 30-second wait after the first 'E'."""
    print("Replaying actions...")
    e_count = 0  # Counter to track 'E' key presses
    for action in actions:
        if action['type'] == 'click':
            pyautogui.click(x=action['x'], y=action['y'], button=action['button'])
            print(f"Replayed click at {action['x']}, {action['y']} with button {action['button']}")
        elif action['type'] == 'key':
            keyboard.press(action['key'])
            keyboard.release(action['key'])
            print(f"Replayed key press: {action['key']}")

            if action['key'].lower() == 'e':
                e_count += 1
                if e_count == 1:  # Wait only after the *first* 'E'
                    print("Waiting 30 seconds to simulate growth/processing...")
                    time.sleep(31)

        time.sleep(0.1)  # Slight delay between all actions
    print("Replay finished.")

def main():
    """Main function to record and replay actions in a loop."""
    try:
        window = pyautogui.getWindowsWithTitle("Roblox")[0]
        window.activate()
        print("Game window activated.")
    except IndexError:
        print("Game window not found. Make sure the title is correct.")
        return

    # Try to load actions from file
    actions = load_actions()

    # If no actions are loaded, record new actions
    if actions is None:
        actions = record_actions()
        save_actions(actions)  # Save actions after recording

    if actions: # Only replay if actions were loaded or recorded
        stop_replay = False  # Flag to stop the replay loop

        def on_space_press(event):
            nonlocal stop_replay
            if event.name == 'space':
                print("Space key pressed. Exiting replay loop.")
                stop_replay = True

        keyboard.on_press(on_space_press)  # Set the callback for any key press

        while not stop_replay:  # Loop until stop_replay is True
            replay_actions(actions)
            print("Replay finished. Starting replay again...")

        keyboard.unhook_all()  # Unhook all keys
        print("Exiting main loop.")

if __name__ == "__main__":
    main()
