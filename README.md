# 🖱️ Virtual Mouse using Hand Gestures

A computer vision based **Virtual Mouse** that allows users to control their computer cursor using **hand gestures through a webcam**.  
The system tracks hand landmarks in real-time and converts finger movements into mouse actions such as **cursor movement, left click, and right click**.

This project is built using **Python, OpenCV, MediaPipe, and PyAutoGUI**, demonstrating how gesture recognition can replace traditional input devices.

---

# 🚀 Features

- Real-time **hand tracking using MediaPipe**
- **Thumb controls cursor movement**
- **Thumb + Index finger pinch → Left Click**
- **Thumb + Pinky finger pinch → Right Click**
- Smooth cursor movement using interpolation
- Region Of Interest (ROI) mapping for better screen control
- Works using a standard **webcam**

---

# 🏗️ Project Architecture

```
Webcam Input
     │
     ▼
OpenCV Frame Capture
     │
     ▼
MediaPipe Hand Detection
     │
     ▼
Hand Landmark Extraction
     │
     ▼
Gesture Recognition
     │
     ├── Thumb movement → Cursor Movement
     ├── Thumb + Index → Left Click
     └── Thumb + Pinky → Right Click
     │
     ▼
PyAutoGUI
     │
     ▼
Mouse Control on System
```

---

# 🛠️ Technologies Used

- **Python**
- **OpenCV**
- **MediaPipe**
- **NumPy**
- **PyAutoGUI**

---

# 📦 Installation

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/yourusername/virtual-mouse.git
cd virtual-mouse
```

### 2️⃣ Install Dependencies

```bash
pip install opencv-python mediapipe numpy pyautogui
```

---

# ▶️ How to Run

Run the Python script:

```bash
python hand_mouse_controller.py
```

Once the program starts, your webcam will activate and the virtual mouse system will begin.

Press **`q`** to exit the program.

---

# 🎮 How to Use

| Gesture | Action |
|------|------|
| Move **Thumb** inside the box | Move Cursor |
| **Thumb + Index pinch** | Left Click |
| **Thumb + Pinky pinch** | Right Click |
| Press **Q** | Exit Program |

Make sure your hand stays inside the **ROI box** shown on the screen for accurate detection.

---

# 📂 Project Structure

```
virtual-mouse
│
├── hand_mouse_controller.py   # Main program
├── README.md                  # Project documentation
```

---

# 💡 Future Improvements

- Scroll gesture support
- Drag and drop functionality
- Multi-hand support
- Gesture customization
- GUI settings panel

---

# 📜 License

This project is open-source and available under the **MIT License**.

---

# 👨‍💻 Author

Developed by **Adithya M**

If you like this project, feel free to ⭐ the repository.
