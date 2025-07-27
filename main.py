import pygame
import sqlite3
import random
import time
import threading

conn = sqlite3.connect('music.db')

def playlist(random_id):
    try:
        c = conn.cursor()
        c.execute("SELECT * FROM Music_Path WHERE id = ?", (random_id,))
        r = c.fetchone()
        if r:
            print("Now playing:", r[1])
            return str(r[1])
        else:
            print("Error: No song found with that ID.")
            return None
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return None

def play():
    randomizer = random.randint(1, 2)
    pygame.init()
    pygame.mixer.init()

    filename = playlist(randomizer)
    if not filename:
        print("Skipping playback due to error.")
        return

    full_path = "/home/mathduck/Music/music/" + filename
    pygame.mixer.music.load(full_path)
    pygame.mixer.music.play()

    stop_requested = False

    def listen_for_stop():
        nonlocal stop_requested
        input("Press Enter to stop...\n")
        pygame.mixer.music.stop()
        stop_requested = True

    # Start listening for stop in a background thread
    threading.Thread(target=listen_for_stop, daemon=True).start()

    # Wait for music to finish or user to stop it
    while pygame.mixer.music.get_busy():
        time.sleep(0.1)

    if not stop_requested:
        print("Next track...")
        play()
    else:
        print("Stopped by user.")

# === Display logo and run ===
print("╔════════════════════════════════════════════════════╗")
print("║     _____                                          ║")
print("║ ___|    _|__  __   _  ______  ____  ______         ║")
print("║|    \  /  | ||  | | ||   ___||    ||   ___|        ║")
print("║|     \/   | ||  |_| ||      ||     |__    |        ║")
print("║|__/\__/|__|_||______||______||____||______|        ║")
print("║    |_____|                                         ║")
print("║     _____                                          ║")
print("║  __|__   |__  ____    ____  __    _ ______  _____  ║")
print("║ |     |     ||    |  |    \ \ \  //|   ___||     | ║")
print("║ |    _|     ||    |_ |     \ \ \// |   ___||     \ ║")
print("║ |___|     __||______||__|\__\/__/  |______||__|\__\║")
print("║    |_____|                                         ║")
print("╚════════════════════════════════════════════════════╝")

play()
