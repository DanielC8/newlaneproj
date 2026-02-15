# Autonomous Lane Detection and Vehicle Control System

This project uses OpenCV and Tkinter to provide a GUI-based autonomous lane detection system with user authentication and vehicle command controls. The program processes video frames in real time to detect lane lines using edge detection and the Hough Line Transform, overlays them on the original feed, and provides directional controls for a connected vehicle/robot. All user actions are logged with timestamps.

## Features

- **Lane Detection**: Detects left and right lane lines from video using Canny edge detection and Hough Line Transform, with slope-based classification.
- **Car Detection and Collision Warning**: Uses a Haar Cascade classifier to detect vehicles in the frame and overlays a warning when a detected car occupies a significant portion of the view.
- **Dual Video Feeds**: Displays a processed feed with lane overlays alongside a raw unprocessed feed.
- **Vehicle Command Interface**: Directional controls (forward, backward, left, right, play, stop) for sending commands to a robot/vehicle.
- **User Authentication**: Account creation and login system backed by SQLite with SHA-256 password hashing.
- **Session Logging**: Every command is logged to a timestamped text file and displayed in a real-time log panel within the GUI.

## Project Structure

- `main.py` — Entry point. Initializes the database and launches the GUI.
- `GUI.py` — Tkinter GUI with login, account creation, and the main control interface (dual feeds, command buttons, live log).
- `process.py` — Core lane detection pipeline: grayscale conversion, Gaussian blur, Canny edges, ROI masking, Hough lines, slope classification, and car detection.
- `camfeeds.py` — Manages two video feeds: one with lane detection overlay and one raw.
- `direction.py` — Sends movement commands to the vehicle/robot.
- `info_and_check.py` — Handles user input validation and authentication logic.
- `sql_program.py` — SQLite database operations for user registration and login.
- `car2.xml` — Pre-trained Haar Cascade classifier for car detection.
- `forward.png` — Direction indicator overlay image.
- `warning.png` — Collision warning overlay image.

## How It Works

1. **Launch**: `main.py` creates the user database if it doesn't exist and opens the login window.
2. **Authentication**: Users create an account or log in. Passwords are hashed with SHA-256 before storage.
3. **Main Interface**: After login, a 4-panel window opens:
   - **Top-left**: Video feed with lane detection overlay.
   - **Top-right**: Directional control buttons.
   - **Bottom-left**: Raw video feed.
   - **Bottom-right**: Real-time command log.
4. **Lane Detection Pipeline**: Each frame goes through grayscale conversion → Gaussian blur → Canny edge detection → triangular ROI mask → car detection and masking → Hough Line Transform → slope-based left/right lane classification → green lane overlay with center line.
5. **Car Detection**: Detected cars are masked out of the lane detection area. If a car takes up more than 20% of the frame, a warning overlay is displayed.
6. **Logging**: Each button press is timestamped and written to both the GUI log panel and a session log file.

## Usage

**Place your video file** in the project directory. The default filename is `Lane2.mp4`. Update the path in `camfeeds.py` if using a different file.

**Run the program:**

```bash
python main.py
```

1. Create an account or log in.
2. Use the directional buttons to send commands.
3. View the lane detection overlay in the top-left panel and raw feed in the bottom-left.
4. All actions appear in the bottom-right log panel.
5. Click **Logout** to end the session and return to the login screen.

## Functions

### main.py
- Initializes `USER.db` and calls `window()` to start the application.

### process.py
- `process(frame, leftl, rightl, count)` — Runs the full lane detection pipeline on a single frame. Returns the annotated frame, left/right lane coordinates, and a persistence counter for maintaining lane lines across frames when detection gaps occur.

### camfeeds.py
- `update_overlay_feed(top_left_frame)` — Reads video frames, applies `process()`, and displays the result in the given Tkinter frame.
- `update_camera_feed(bottom_left_frame)` — Reads and displays raw video frames without processing.

### GUI.py
- `window()` — Main login/registration screen.
- `create()` — Account creation form.
- `login()` — Login form.
- `loggedin(username, password, key, name)` — Main application window with feeds, controls, and logging.

### sql_program.py
- `save_sql()` — Creates the user table and inserts a new user with a unique 6-digit key and hashed password.
- `get_sql(username, password)` — Validates credentials and returns the user key.
- `first(username, password)` — Retrieves the user's first name for the welcome message.

### info_and_check.py
- `save_info(creates, user_info, name_entry, last_entry, user_entry, passw_entry)` — Collects form data and saves to the database.
- `check_login(logins, userlogin_entry, passwlogin_entry)` — Validates login credentials and transitions to the main interface.

### direction.py
- `send_command(direction)` — Sends a movement command (`forward`, `backward`, `left`, `right`, `play`, `stop`). Currently prints to console; intended for hardware integration.

## Requirements

- Python 3.x
- OpenCV (`cv2`)
- NumPy
- Pillow (`PIL`)
- Tkinter (included with Python)
- SQLite3 (included with Python)

**Install dependencies:**

```bash
pip install opencv-python numpy pillow
```
