import pyautogui
import time
import keyboard
import mouse

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
        actions.append({'type': 'key', 'key': event.name})
        print(f"Key {event.name} pressed")

    mouse.hook(on_mouse_event)
    keyboard.on_press(on_key_event)

    keyboard.wait('q')  # Wait until 'q' is pressed
    mouse.unhook(on_mouse_event)
    keyboard.unhook_all()

    print("Recording stopped.")
    return actions

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
                    print("Waiting 35 seconds to simulate growth/processing...")
                    time.sleep(35)

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

    actions = record_actions()  # Record actions only once

    while True:  # Loop indefinitely
        replay_actions(actions)
        print("Replay finished. Starting replay again...")

if __name__ == "__main__":
    main()
