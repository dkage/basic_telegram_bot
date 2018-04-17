from basic_bot import *
import time


# Keeps script running and getting new updates
def main():
    last_update_id = None
    while True:
        updates = get_updates(last_update_id)
        if len(updates["result"]) > 0:
            last_update_id = get_last_update_id(updates) + 1
            echo_all(updates)
        time.sleep(0.5)


# Python main or modular check
if __name__ == '__main__':
    main()
