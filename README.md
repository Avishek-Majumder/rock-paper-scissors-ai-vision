# 🎮 Rock Paper Scissors AI Vision

An immersive, full-screen Rock Paper Scissors game powered by computer vision and hand gesture recognition. Battle against a smart AI using real-time hand tracking in stunning 1080p!

## ✨ Features

### 🎯 **Interactive Gameplay**
- **Full HD Experience** - Stunning 1920x1080 full-screen gameplay
- **Real-time Hand Tracking** - Advanced MediaPipe-powered gesture recognition
- **Smart AI Opponent** - Challenging computer opponent with realistic hand animations
- **Synchronized Battles** - Fair "Rock, Paper, Scissors, Shoot!" countdown system

### 🤖 **Advanced AI Visualization**
- **Realistic AI Hands** - Human-like skin tone with detailed finger joints
- **Split-screen Arena** - Epic battle visualization
- **Smooth Animations** - Fluid countdown and result displays

### 🎮 **Gesture Controls**
- **👍 Thumbs Up** - Start new game
- **👎 Thumbs Down** - Exit game or go back
- **👉 Pointing** - Navigate menus with finger pointing
- **✊✋✌️ Rock/Paper/Scissors** - Battle gestures

### 📊 **Game Features**
- **Persistent Statistics** - Track your wins, losses, and ties
- **Live Performance** - Real-time FPS counter and gesture confidence
- **Interactive Menus** - Touch-free navigation system
- **Professional UI** - Polished interface with glow effects and animations

## 🚀 Quick Start

### Prerequisites
```bash
Python 3.8 or higher
Webcam (built-in or USB)
```

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/Avishek-Majumder/rock-paper-scissors-ai-vision.git
cd rock-paper-scissors-ai-vision
```

2. **Install dependencies**
```bash
pip install opencv-python mediapipe numpy
```

3. **Run the game**
```bash
python rock_paper_scissors_world.py
```

## 🎮 How to Play

### 🏠 **Main Menu Navigation**
1. **Point** your index finger at menu options to highlight them
2. **Thumbs up** 👍 to start a game
3. **Thumbs down** 👎 to exit
4. **Point and hold** on buttons to select them

### ⚔️ **Battle Mode**
1. Wait for the countdown: "ROCK... PAPER... SCISSORS... SHOOT!"
2. Show your gesture at "SHOOT!":
   - **✊ Rock** - Closed fist
   - **✋ Paper** - Open hand (4-5 fingers)
   - **✌️ Scissors** - Index and middle finger in V-shape
3. See the results and your updated score!

### 📊 **Statistics**
- View your win/loss record in the Options menu
- Stats are automatically saved between sessions
- Track your improvement over time

## 🛠️ Technical Details

### 🔧 **Built With**
- **Python 3.8+** - Core programming language
- **OpenCV** - Computer vision and display
- **MediaPipe** - Google's hand tracking ML solution
- **NumPy** - Numerical computations
- **JSON** - Data persistence

### 🎯 **Key Components**
- **Gesture Recognition** - Advanced finger position analysis
- **State Management** - Clean game state transitions
- **Real-time Rendering** - 60+ FPS performance
- **Data Persistence** - Automatic save/load system

### ⚡ **Performance**
- **Resolution:** 1920x1080 Full HD
- **Frame Rate:** 60+ FPS (hardware dependent)
- **Latency:** <100ms gesture response time
- **Memory:** ~50MB typical usage

## 📁 Project Structure

```
rock-paper-scissors-ai-vision/
│
├── rock_paper_scissors_world.py    # Main game file
├── rps_stats.json                  # Statistics data (auto-generated)
├── README.md                       # This file
├── requirements.txt               # Python dependencies
├── LICENSE                        # MIT License
└── screenshots/                   # Game screenshots
    ├── menu.png
    ├── battle.png
    └── stats.png
```

## 🎮 Controls Reference

| Gesture | Action | Context |
|---------|--------|---------|
| 👍 Thumbs Up | Start Game | Main Menu |
| 👎 Thumbs Down | Exit/Back | Any Screen |
| 👉 Pointing | Select/Hover | Menu Navigation |
| ✊ Rock | Battle Gesture | During Countdown |
| ✋ Paper | Battle Gesture | During Countdown |
| ✌️ Scissors | Battle Gesture | During Countdown |
| `Q` or `ESC` | Quit Game | Keyboard Backup |

## 🔧 Configuration

### Camera Settings
The game automatically configures your camera for optimal performance:
- **Resolution:** 1920x1080
- **Frame Rate:** Maximum available
- **Auto-flip:** Enabled for mirror effect

### Gesture Sensitivity
- **Detection Confidence:** 0.5 (adjustable in code)
- **Tracking Confidence:** 0.3 (adjustable in code)
- **Stability Time:** 0.3-0.6s depending on gesture

## 🐛 Troubleshooting

### Common Issues

**Camera not detected:**
```bash
# Check available cameras
python -c "import cv2; print(cv2.VideoCapture(0).isOpened())"
```

**Low performance:**
- Ensure good lighting conditions
- Close other applications using the camera
- Update graphics drivers

**Gesture not recognized:**
- Ensure hand is clearly visible
- Maintain steady gesture for required time
- Check gesture confidence in top-right corner

**Full-screen issues:**
- Press `ESC` or `Q` to exit full-screen
- Check display scaling settings

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch** (`git checkout -b feature/amazing-feature`)
3. **Commit your changes** (`git commit -m 'Add amazing feature'`)
4. **Push to the branch** (`git push origin feature/amazing-feature`)
5. **Open a Pull Request**

### 💡 Ideas for Contributions
- Additional game modes (Tournament, Speed Mode)
- Sound effects and music
- Multiplayer support
- Custom AI difficulty levels
- Gesture training mode
- Mobile app version

## 📝 License

This project is licensed under the MIT License - see the (LICENSE) file for details.

## 🙏 Acknowledgments

- **Google MediaPipe** - Incredible hand tracking technology
- **OpenCV Community** - Computer vision foundation
- **Python Community** - Amazing ecosystem and support

## 📞 Support

Having issues? Found a bug? Want to suggest a feature?

- **Create an Issue** - Use GitHub Issues for bug reports
- **Discussions** - Use GitHub Discussions for questions
- **Email** - Reach out directly for urgent matters

## 🌟 Star the Project

If you enjoyed this game, please ⭐ star the repository to show your support!

---

### 🎮 Ready to Play?

```bash
git clone https://github.com/yourusername/rock-paper-scissors-ai-vision.git
cd rock-paper-scissors-ai-vision
pip install -r requirements.txt
python rock_paper_scissors_world.py
```

**Let the gesture battles begin!** 🥊✨

---

## 🔄 Recent Updates

### v1.0.0 (Latest)
- ✅ Full HD 1920x1080 support
- ✅ Improved gesture recognition accuracy
- ✅ Enhanced AI hand visualization
- ✅ Better menu navigation
- ✅ Performance optimizations

### Upcoming Features
- 🔜 Sound effects and background music
- 🔜 Tournament mode
- 🔜 Gesture training tutorial
- 🔜 Custom themes and skins

## 💻 System Requirements

### Minimum Requirements
- **OS:** Windows 10, macOS 10.14, or Linux (Ubuntu 18.04+)
- **Python:** 3.8+
- **RAM:** 4GB
- **Camera:** Any USB or built-in webcam
- **Display:** 1920x1080 recommended

### Recommended Requirements
- **OS:** Windows 11, macOS 12+, or Linux (Ubuntu 20.04+)
- **Python:** 3.9+
- **RAM:** 8GB+
- **Camera:** HD webcam with good low-light performance
- **Display:** 1920x1080 or higher

## 🔧 Advanced Configuration

### Custom Gesture Sensitivity
Edit the detection thresholds in `rock_paper_scissors_world.py`:

```python
# Adjust these values for sensitivity
min_detection_confidence = 0.5  # Lower = more sensitive
min_tracking_confidence = 0.3   # Lower = more responsive
```

### Performance Tuning
For better performance on lower-end hardware:

```python
# Reduce resolution for better FPS
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
```

---

**Made with ❤️ and lots of gesture recognition magic!**
