import cv2
import mediapipe as mp
import pyautogui
import math

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.7, min_tracking_confidence=0.7)
SCREEN_WIDTH, SCREEN_HEIGHT = pyautogui.size()

# Function to move mouse
def move_mouse(hand_landmarks, SCREEN_WIDTH, SCREEN_HEIGHT):

    # Get landmarks positions and calculate distance
    index_finger_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP]

    # If only one hand visible cursor follows it
    if len(results.multi_hand_landmarks) == 1:
        pyautogui.moveTo(int(index_finger_mcp.x * SCREEN_WIDTH), int(index_finger_mcp.y * SCREEN_HEIGHT))
    # If two hands visible the cursor follows the first one which entered the screen
    elif results.multi_hand_landmarks[1] is not None:
        if hand_landmarks == results.multi_hand_landmarks[1]:
            pyautogui.moveTo(int(index_finger_mcp.x * SCREEN_WIDTH), int(index_finger_mcp.y * SCREEN_HEIGHT))


# Capture video from camera
cap = cv2.VideoCapture(0)

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

            move_mouse(hand_landmarks, SCREEN_WIDTH, SCREEN_HEIGHT)

    # Display the frame
    cv2.imshow('Frame', cv2.flip(frame, 1))
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
