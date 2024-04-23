import cv2
import mediapipe as mp
import pyautogui
import math

# Function to calculate distance between two points
def calculate_distance(point1, point2):
    return math.sqrt((point1.x - point2.x) ** 2 + (point1.y - point2.y) ** 2)

# Function to check for click actions
def check_click(hand_landmarks, results):
    global mouse_held
    global hand_one_loc
    # Get landmarks positions
    thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]  # Thumb tip landmark
    index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]  # Index finger tip landmark
    middle_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]

    # Calculate distances
    d_thbtip_midtip = calculate_distance(thumb_tip, middle_tip)
    d_thbtip_idxtip = calculate_distance(thumb_tip, index_tip)
    d_idxtip_midtip = calculate_distance(middle_tip, index_tip)

    # Clicking
    # If distance between thumb tip and index tip less than 0.05 and distance between thumb tip and middle tip more than 0.07 click
    if d_thbtip_idxtip < 0.05 and not d_thbtip_midtip < 0.07:
        # If only one hand is visible left click
        if len(results.multi_hand_landmarks) == 1:
            pyautogui.leftClick()
        # If both hands visible the hand which entered the screen first left click the second right click
        elif hand_landmarks == results.multi_hand_landmarks[0]:
            pyautogui.rightClick()
        else: #hand_landmarks == results.multi_hand_landmarks[1]:
            pyautogui.leftClick()

    # Dragging on pinch (the first hand, the one that moves the mouse)
    if len(results.multi_hand_landmarks) == 1:
        # If distance between thumb tip middle tip and index tip all less than 0.05 mouse down
        if d_thbtip_idxtip < 0.06 and d_thbtip_midtip < 0.06 and d_idxtip_midtip < 0.08:
            if not mouse_held:
                pyautogui.mouseDown()
                mouse_held = True
        # If fingers move away and mouse is down then mouse up
        elif mouse_held:
                pyautogui.mouseUp()
                mouse_held = False
    # Same as above but if we have two hands we use the one which controls the mouse
    elif hand_landmarks == results.multi_hand_landmarks[1]:
        if d_thbtip_idxtip < 0.06 and d_thbtip_midtip < 0.06 and d_idxtip_midtip < 0.08: 
            if not mouse_held:
                    pyautogui.mouseDown()
                    mouse_held = True
            elif mouse_held:
                    pyautogui.mouseUp()
                    mouse_held = False
    
    # Open keyboard when two idx tips touch !need program run in administrator mode to be able to click on the keyboard!
    if len(results.multi_hand_landmarks) == 2:
        if hand_landmarks == results.multi_hand_landmarks[0]:
            hand_one_loc = index_tip
        elif hand_landmarks == results.multi_hand_landmarks[1]:
            if calculate_distance(hand_one_loc, index_tip) < 0.01:
                pyautogui.hotkey('win', 'ctrlleft', 'o')
                hand_one_loc = None
    
# Function to move mouse
def move_mouse(hand_landmarks, SCREEN_WIDTH, SCREEN_HEIGHT):

    # Get landmarks positions and calculate distance
    index_finger_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP]

    # If only one hand visible cursor follows it
    if len(results.multi_hand_landmarks) == 1:
        pyautogui.moveTo(int(index_finger_mcp.x * SCREEN_WIDTH), int(index_finger_mcp.y * SCREEN_HEIGHT))
    # if two hands visible the cursor follows the first one which entered the screen
    elif results.multi_hand_landmarks[1] is not None:
        if hand_landmarks == results.multi_hand_landmarks[1]:
            pyautogui.moveTo(int(index_finger_mcp.x * SCREEN_WIDTH), int(index_finger_mcp.y * SCREEN_HEIGHT))

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.7, min_tracking_confidence=0.7)
SCREEN_WIDTH, SCREEN_HEIGHT = pyautogui.size()
mouse_held = False
hand_one_loc = None

# Capture video from camera
cap = cv2.VideoCapture(0)

# Read the frames from the camera if possible else break
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Convert the BGR image to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame
    results = hands.process(cv2.flip(rgb_frame, 1))
    frame = cv2.flip(frame, 1)

    # Check if hands are detected
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:

            # Draw landmarks on the frame
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Move mouse
            move_mouse(hand_landmarks, SCREEN_WIDTH, SCREEN_HEIGHT)

            # Check for click actions
            check_click(hand_landmarks, results)

    # Display the frame, turn of on 'q'
    cv2.imshow('Frame', cv2.flip(frame, 1))
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()