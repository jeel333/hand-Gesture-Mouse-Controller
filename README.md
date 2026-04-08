🖐️ AI Gesture Mouse Controller

Control your computer using hand gestures via webcam 🎥
This project uses Computer Vision + AI (MediaPipe) to replace your mouse with hand movements.

✨ Features
🖱️ Cursor movement using thumb
👆 Left click using index finger
👉 Right click using middle finger
✊ Double click using 4 fingers
🔄 Swipe gesture for:
▶ Next media
◀ Previous media
⚡ Smooth and optimized cursor movement

🛠️ Technologies Used
Python
OpenCV
MediaPipe
PyAutoGUI
NumPy


📁 Project Setup (VS Code)
1️⃣ Clone Repository
git clone https://github.com/your-username/AI-Gesture-Mouse-Controller.git
cd AI-Gesture-Mouse-Controller
2️⃣ Open in VS Code
Open VS Code
Click File → Open Folder
Select project folder
3️⃣ Create Virtual Environment
python -m venv .venv
4️⃣ Activate Virtual Environment

👉 Windows:
.venv\Scripts\activate

👉 You should see:
(.venv)
5️⃣ Install Dependencies
pip install --upgrade pip
pip install mediapipe==0.10.9 opencv-python pyautogui numpy
▶️ Run the Project
python hand_mouse_control.py


🎮 Controls / Gestures
Gesture	Action
👍 Thumb Move	Cursor Movement
👆 Index Down	Left Click
👉 Middle Down	Right Click
✊ 4 Fingers Down	Double Click
➡️ Swipe Right	Next Media
⬅️ Swipe Left	Previous Media


⚠️ Important Notes
Close other apps using camera (Zoom, Chrome, etc.)
If camera error occurs, replace:
cv2.VideoCapture(0)

with:

cv2.VideoCapture(0, cv2.CAP_DSHOW)
Avoid running project inside OneDrive folder


🧠 How It Works
Webcam captures hand
MediaPipe detects 21 hand landmarks
Coordinates mapped to screen
Gestures converted into mouse actions



📸 Future Improvements
🔽 Scroll gesture
✊ Drag & drop
🔊 Volume control
🎯 Better FPS optimization


Author
jeel fadadu

⭐ Support

If you like this project:

⭐ Star the repo
🍴 Fork it
📢 Share it
