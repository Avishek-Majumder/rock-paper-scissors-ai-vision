import cv2
import mediapipe as mp
import random
import time
import numpy as np
import json
import os

class RockPaperScissorsWorld:
    def __init__(self):
        # Initialize MediaPipe
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.3
        )
        self.mp_draw = mp.solutions.drawing_utils
        
        # Game states
        self.state = "menu"  # menu, countdown, battle, result, options
        
        # Scores
        self.player_wins = 0
        self.ai_wins = 0
        self.ties = 0
        self.total_games = 0
        
        # Game variables
        self.choices = ['rock', 'paper', 'scissors']
        self.player_choice = ""
        self.ai_choice = ""
        self.result = ""
        
        # Countdown variables
        self.countdown_start = 0
        self.countdown_phase = 0  # 0=rock, 1=paper, 2=scissors, 3=shoot
        self.countdown_texts = ["ROCK", "PAPER", "SCISSORS", "SHOOT!"]
        
        # Gesture detection
        self.current_gesture = "none"
        self.confidence = 0
        self.stable_start = 0
        self.last_gesture = "none"
        
        # Menu interaction
        self.finger_pos = (0, 0)
        self.pointing = False
        self.menu_hover = -1
        
        # FPS tracking
        self.fps_count = 0
        self.fps_start = time.time()
        self.fps = 0
        
        # Colors
        self.colors = {
            'red': (0, 0, 255),
            'green': (0, 255, 0),
            'blue': (255, 0, 0),
            'yellow': (0, 255, 255),
            'white': (255, 255, 255),
            'black': (0, 0, 0),
            'skin': (180, 140, 120),
            'dark_skin': (120, 90, 70)
        }
        
        # Load saved data
        self.load_data()
    
    def load_data(self):
        """Load game statistics"""
        try:
            if os.path.exists('rps_stats.json'):
                with open('rps_stats.json', 'r') as f:
                    data = json.load(f)
                    self.player_wins = data.get('player_wins', 0)
                    self.ai_wins = data.get('ai_wins', 0)
                    self.ties = data.get('ties', 0)
                    self.total_games = data.get('total_games', 0)
        except:
            pass
    
    def save_data(self):
        """Save game statistics"""
        try:
            data = {
                'player_wins': self.player_wins,
                'ai_wins': self.ai_wins,
                'ties': self.ties,
                'total_games': self.total_games
            }
            with open('rps_stats.json', 'w') as f:
                json.dump(data, f)
        except:
            pass
    
    def detect_gesture(self, landmarks):
        """Enhanced gesture detection with better accuracy"""
        if not landmarks:
            return "none", 0
        
        # Get key landmarks
        thumb_tip = landmarks[4]
        thumb_ip = landmarks[3]
        thumb_mcp = landmarks[2]
        index_tip = landmarks[8]
        index_pip = landmarks[6]
        index_mcp = landmarks[5]
        middle_tip = landmarks[12]
        middle_pip = landmarks[10]
        middle_mcp = landmarks[9]
        ring_tip = landmarks[16]
        ring_pip = landmarks[14]
        ring_mcp = landmarks[13]
        pinky_tip = landmarks[20]
        pinky_pip = landmarks[18]
        pinky_mcp = landmarks[17]
        wrist = landmarks[0]
        
        # Store finger position for menu interaction
        self.finger_pos = (int(index_tip.x * 1280), int(index_tip.y * 720))
        
        # More precise finger detection
        fingers = []
        
        # Thumb - improved detection for both hands
        thumb_is_open = False
        if thumb_tip.x > wrist.x:  # Right hand
            thumb_is_open = thumb_tip.x > thumb_ip.x + 0.03
        else:  # Left hand
            thumb_is_open = thumb_tip.x < thumb_ip.x - 0.03
        fingers.append(thumb_is_open)
        
        # Index finger - more sensitive
        index_is_open = index_tip.y < index_pip.y - 0.03
        fingers.append(index_is_open)
        
        # Middle finger - more sensitive
        middle_is_open = middle_tip.y < middle_pip.y - 0.03
        fingers.append(middle_is_open)
        
        # Ring finger - more sensitive
        ring_is_open = ring_tip.y < ring_pip.y - 0.03
        fingers.append(ring_is_open)
        
        # Pinky finger - more sensitive
        pinky_is_open = pinky_tip.y < pinky_pip.y - 0.03
        fingers.append(pinky_is_open)
        
        finger_count = sum(fingers)
        
        # PRIORITY 1: Special gestures (thumbs up/down, pointing)
        
        # Thumbs up - thumb up, others down, proper orientation
        thumb_vertical_up = (thumb_tip.y < thumb_ip.y - 0.06) and (thumb_tip.y < thumb_mcp.y - 0.08)
        other_fingers_closed = not any(fingers[1:4])  # Index, middle, ring, pinky closed
        
        if thumb_vertical_up and other_fingers_closed:
            return "thumbs_up", 0.95
        
        # Thumbs down - improved detection with better positioning
        thumb_vertical_down = (thumb_tip.y > thumb_ip.y + 0.04) and (thumb_tip.y > thumb_mcp.y + 0.06)
        thumb_pointing_down = thumb_tip.y > wrist.y + 0.05  # Thumb clearly below wrist
        
        if thumb_vertical_down and thumb_pointing_down and other_fingers_closed:
            return "thumbs_down", 0.95
        
        # Pointing - only index finger extended
        only_index_up = fingers[1] and not fingers[0] and not fingers[2] and not fingers[3] and not fingers[4]
        
        if only_index_up:
            self.pointing = True
            return "pointing", 0.95
        else:
            self.pointing = False
        
        # PRIORITY 2: Rock Paper Scissors gestures
        
        # Scissors - IMPROVED: exactly index and middle up, others down
        scissors_pattern = (fingers[1] and fingers[2] and 
                           not fingers[0] and not fingers[3] and not fingers[4])
        
        # Additional check: ensure index and middle are well separated
        index_middle_separation = abs(index_tip.x - middle_tip.x) > 0.08
        both_fingers_high = (index_tip.y < index_mcp.y - 0.05) and (middle_tip.y < middle_mcp.y - 0.05)
        
        if scissors_pattern and index_middle_separation and both_fingers_high:
            return "scissors", 0.92
        
        # Rock - no fingers or only thumb slightly up
        if finger_count == 0 or (finger_count == 1 and fingers[0]):
            return "rock", 0.9
        
        # Paper - 4 or 5 fingers up (excluding thumb sometimes)
        if finger_count >= 4:
            return "paper", 0.9
        
        # If we have 2-3 fingers but not scissors pattern, check for partial gestures
        if finger_count == 2:
            # Could be partial scissors or other gesture
            if fingers[1] and fingers[2]:  # Index and middle up
                return "scissors", 0.7  # Lower confidence
            else:
                return "rock", 0.6  # Probably transitioning to rock
        
        if finger_count == 3:
            # Probably transitioning to paper
            return "paper", 0.6
        
        return "none", 0.3
    
    def check_menu_hover(self):
        """Improved menu hover detection with back button support"""
        if not self.pointing:
            self.menu_hover = -1
            return
        
        x, y = self.finger_pos
        
        if self.state == "menu":
            # Main menu button areas (larger for easier selection)
            buttons = [
                (300, 215, 980, 285),  # Start - bigger area
                (300, 295, 980, 365),  # Options - bigger area  
                (300, 375, 980, 445)   # Exit - bigger area
            ]
            
            self.menu_hover = -1
            for i, (x1, y1, x2, y2) in enumerate(buttons):
                if x1 <= x <= x2 and y1 <= y <= y2:
                    self.menu_hover = i
                    break
        
        elif self.state == "options":
            # Back button area in options screen
            if 100 <= x <= 300 and (720 - 120) <= y <= (720 - 70):  # Back button
                self.menu_hover = 0  # Use 0 for back button
            else:
                self.menu_hover = -1
    
    def update_fps(self):
        """Update FPS counter"""
        self.fps_count += 1
        current_time = time.time()
        
        if current_time - self.fps_start >= 1.0:
            self.fps = self.fps_count / (current_time - self.fps_start)
            self.fps_count = 0
            self.fps_start = current_time
    
    def draw_menu(self, frame):
        """Draw main menu"""
        h, w = frame.shape[:2]
        
        # Semi-transparent overlay
        overlay = frame.copy()
        cv2.rectangle(overlay, (0, 0), (w, h), self.colors['black'], -1)
        cv2.addWeighted(overlay, 0.5, frame, 0.5, 0, frame)
        
        # FPS counter
        cv2.rectangle(frame, (10, 10), (120, 50), self.colors['black'], -1)
        cv2.putText(frame, f"FPS: {self.fps:.1f}", (20, 35), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, self.colors['green'], 2)
        
        # Gesture info with better visual feedback
        cv2.rectangle(frame, (w-220, 10), (w-10, 100), self.colors['black'], -1)
        color = self.colors['green'] if self.confidence > 0.8 else self.colors['yellow'] if self.confidence > 0.5 else self.colors['red']
        
        cv2.putText(frame, f"Gesture: {self.current_gesture}", (w-210, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
        cv2.putText(frame, f"Conf: {self.confidence:.2f}", (w-210, 50), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
        
        # Show stability indicator
        if hasattr(self, 'stable_start') and self.stable_start > 0:
            stability = min(1.0, (time.time() - self.stable_start) / 0.8)
            cv2.putText(frame, f"Stable: {stability:.1f}", (w-210, 70), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.colors['green'] if stability > 0.7 else self.colors['yellow'], 1)
        
        # Show gesture history for debugging
        if hasattr(self, 'gesture_history') and len(self.gesture_history) > 0:
            recent = "->".join(self.gesture_history[-3:])
            cv2.putText(frame, f"History: {recent}", (w-210, 90), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.4, self.colors['white'], 1)
        
        # Title
        title = "ROCK PAPER SCISSORS WORLD"
        title_size = cv2.getTextSize(title, cv2.FONT_HERSHEY_SIMPLEX, 1.5, 3)[0]
        title_x = (w - title_size[0]) // 2
        
        # Title with glow
        for i in range(3):
            glow = (50 + i*30, 50 + i*30, 100 + i*40)
            cv2.putText(frame, title, (title_x - i, 100 + i), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1.5, glow, 3 + i)
        
        cv2.putText(frame, title, (title_x, 100), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1.5, self.colors['yellow'], 3)
        
        # Menu buttons
        options = ["START THE WAR", "OPTIONS", "EXIT"]
        y_positions = [250, 330, 410]
        
        for i, (option, y) in enumerate(zip(options, y_positions)):
            # Button color
            if i == self.menu_hover:
                btn_color = self.colors['green']
            else:
                btn_color = self.colors['blue']
            
            # Draw button
            cv2.rectangle(frame, (350, y - 25), (930, y + 25), btn_color, -1)
            cv2.rectangle(frame, (350, y - 25), (930, y + 25), self.colors['white'], 2)
            
            # Button text
            text_size = cv2.getTextSize(option, cv2.FONT_HERSHEY_SIMPLEX, 0.8, 2)[0]
            text_x = (w - text_size[0]) // 2
            cv2.putText(frame, option, (text_x, y + 8), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.8, self.colors['white'], 2)
        
        # Instructions
        instructions = [
            "👍 Thumbs UP = Start Game",
            "👎 Thumbs DOWN = Exit",
            "👉 Point = Select Menu"
        ]
        
        for i, instruction in enumerate(instructions):
            cv2.putText(frame, instruction, (50, h - 100 + i * 25), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, self.colors['white'], 2)
        
        # Stats
        stats = f"Wins: {self.player_wins} | Losses: {self.ai_wins} | Ties: {self.ties}"
        cv2.putText(frame, stats, (50, h - 20), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, self.colors['yellow'], 2)
    
    def draw_countdown(self, frame):
        """Draw countdown animation"""
        h, w = frame.shape[:2]
        
        if self.countdown_phase < len(self.countdown_texts):
            text = self.countdown_texts[self.countdown_phase]
            colors = [self.colors['red'], self.colors['green'], 
                     self.colors['blue'], self.colors['yellow']]
            color = colors[self.countdown_phase]
            
            # Animated size
            elapsed = time.time() - self.countdown_start
            scale = 3 + np.sin(elapsed * 10) * 0.5
            
            text_size = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, scale, 8)[0]
            text_x = (w - text_size[0]) // 2
            text_y = (h + text_size[1]) // 2
            
            # Shadow
            cv2.putText(frame, text, (text_x + 5, text_y + 5), 
                       cv2.FONT_HERSHEY_SIMPLEX, scale, self.colors['black'], 8)
            
            # Main text
            cv2.putText(frame, text, (text_x, text_y), 
                       cv2.FONT_HERSHEY_SIMPLEX, scale, color, 8)
    
    def draw_battle(self, frame):
        """Draw battle arena"""
        h, w = frame.shape[:2]
        
        # Split screen
        cv2.line(frame, (w//2, 0), (w//2, h), self.colors['white'], 3)
        
        # Labels
        cv2.putText(frame, "YOU", (w//4 - 50, 50), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1.5, self.colors['green'], 3)
        cv2.putText(frame, "AI", (3*w//4 - 30, 50), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1.5, self.colors['red'], 3)
        
        # Draw AI hand
        self.draw_ai_hand(frame, 3*w//4, h//2)
        
        # Show result if battle over
        if self.state == "result":
            cv2.putText(frame, f"You: {self.player_choice.upper()}", (50, h - 100), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, self.colors['white'], 2)
            cv2.putText(frame, f"AI: {self.ai_choice.upper()}", (w//2 + 50, h - 100), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, self.colors['white'], 2)
            
            # Result
            if "WIN" in self.result:
                result_color = self.colors['green']
            elif "LOSE" in self.result:
                result_color = self.colors['red']
            else:
                result_color = self.colors['yellow']
            
            result_size = cv2.getTextSize(self.result, cv2.FONT_HERSHEY_SIMPLEX, 2, 4)[0]
            result_x = (w - result_size[0]) // 2
            cv2.putText(frame, self.result, (result_x, 150), 
                       cv2.FONT_HERSHEY_SIMPLEX, 2, result_color, 4)
    
    def draw_ai_hand(self, frame, cx, cy):
        """Draw realistic AI hand"""
        skin = self.colors['skin']
        dark = self.colors['dark_skin']
        
        if self.ai_choice == "rock":
            # Fist
            cv2.ellipse(frame, (cx, cy), (45, 35), 0, 0, 360, skin, -1)
            cv2.ellipse(frame, (cx, cy), (45, 35), 0, 0, 360, dark, 3)
            
            # Knuckles
            knuckles = [(cx-25, cy-10), (cx-8, cy-15), (cx+8, cy-15), (cx+25, cy-10)]
            for kx, ky in knuckles:
                cv2.circle(frame, (kx, ky), 8, skin, -1)
                cv2.circle(frame, (kx, ky), 8, dark, 2)
            
            # Thumb
            cv2.ellipse(frame, (cx-35, cy+5), (12, 20), 45, 0, 360, skin, -1)
            cv2.ellipse(frame, (cx-35, cy+5), (12, 20), 45, 0, 360, dark, 2)
        
        elif self.ai_choice == "paper":
            # Palm
            cv2.ellipse(frame, (cx, cy+15), (35, 45), 0, 0, 360, skin, -1)
            cv2.ellipse(frame, (cx, cy+15), (35, 45), 0, 0, 360, dark, 3)
            
            # Fingers
            fingers = [
                (cx-25, cy-30, 12, 40),  # Pinky
                (cx-8, cy-40, 14, 50),   # Ring
                (cx+8, cy-42, 14, 52),   # Middle
                (cx+25, cy-35, 13, 45),  # Index
            ]
            
            for fx, fy, fw, fh in fingers:
                cv2.ellipse(frame, (fx, fy), (fw//2, fh//2), 0, 0, 360, skin, -1)
                cv2.ellipse(frame, (fx, fy), (fw//2, fh//2), 0, 0, 360, dark, 2)
                
                # Joints
                cv2.circle(frame, (fx, fy-fh//4), 3, dark, -1)
                cv2.circle(frame, (fx, fy+fh//4), 3, dark, -1)
            
            # Thumb
            cv2.ellipse(frame, (cx-45, cy-5), (15, 25), 30, 0, 360, skin, -1)
            cv2.ellipse(frame, (cx-45, cy-5), (15, 25), 30, 0, 360, dark, 2)
        
        elif self.ai_choice == "scissors":
            # Palm
            cv2.ellipse(frame, (cx, cy+20), (30, 35), 0, 0, 360, skin, -1)
            cv2.ellipse(frame, (cx, cy+20), (30, 35), 0, 0, 360, dark, 3)
            
            # Index finger
            cv2.ellipse(frame, (cx-15, cy-25), (8, 30), -15, 0, 360, skin, -1)
            cv2.ellipse(frame, (cx-15, cy-25), (8, 30), -15, 0, 360, dark, 2)
            cv2.circle(frame, (cx-12, cy-35), 3, dark, -1)
            
            # Middle finger
            cv2.ellipse(frame, (cx+15, cy-25), (8, 30), 15, 0, 360, skin, -1)
            cv2.ellipse(frame, (cx+15, cy-25), (8, 30), 15, 0, 360, dark, 2)
            cv2.circle(frame, (cx+12, cy-35), 3, dark, -1)
            
            # Folded fingers
            cv2.ellipse(frame, (cx+25, cy+5), (6, 15), 45, 0, 360, skin, -1)
            cv2.ellipse(frame, (cx+30, cy+15), (5, 12), 60, 0, 360, skin, -1)
            
            # Thumb
            cv2.ellipse(frame, (cx-35, cy+10), (12, 20), 45, 0, 360, skin, -1)
            cv2.ellipse(frame, (cx-35, cy+10), (12, 20), 45, 0, 360, dark, 2)
    
    def draw_options(self, frame):
        """Draw options screen with back button"""
        h, w = frame.shape[:2]
        
        # Semi-transparent overlay
        overlay = frame.copy()
        cv2.rectangle(overlay, (0, 0), (w, h), self.colors['black'], -1)
        cv2.addWeighted(overlay, 0.6, frame, 0.4, 0, frame)
        
        # Title
        cv2.putText(frame, "STATISTICS", (w//2 - 150, 100), 
                   cv2.FONT_HERSHEY_SIMPLEX, 2, self.colors['yellow'], 4)
        
        # Stats
        stats = [
            f"Total Games: {self.total_games}",
            f"Your Wins: {self.player_wins}",
            f"AI Wins: {self.ai_wins}",
            f"Ties: {self.ties}",
            f"Win Rate: {(self.player_wins/max(1, self.total_games)*100):.1f}%"
        ]
        
        for i, stat in enumerate(stats):
            cv2.putText(frame, stat, (100, 200 + i * 50), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, self.colors['white'], 2)
        
        # Back button for finger navigation
        back_color = self.colors['green'] if self.menu_hover == 0 else self.colors['blue']
        cv2.rectangle(frame, (100, h - 120), (300, h - 70), back_color, -1)
        cv2.rectangle(frame, (100, h - 120), (300, h - 70), self.colors['white'], 2)
        
        cv2.putText(frame, "← BACK", (150, h - 85), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, self.colors['white'], 2)
        
        # Instructions
        cv2.putText(frame, "👎 Thumbs DOWN to go back", (400, h - 50), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, self.colors['yellow'], 2)
        cv2.putText(frame, "👉 Point at BACK button", (400, h - 20), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, self.colors['yellow'], 2)
    
    def update_game(self):
        """Update game logic"""
        current_time = time.time()
        
        # Stable gesture detection
        if self.current_gesture == self.last_gesture and self.current_gesture != "none":
            if self.stable_start == 0:
                self.stable_start = current_time
        else:
            self.stable_start = 0
        
        # Gesture smoothing and filtering
        self.gesture_history = getattr(self, 'gesture_history', [])
        self.gesture_history.append(self.current_gesture)
        
        # Keep only last 5 gestures for smoothing
        if len(self.gesture_history) > 5:
            self.gesture_history.pop(0)
        
        # Use most common gesture from recent history for stability
        if len(self.gesture_history) >= 3:
            gesture_counts = {}
            for g in self.gesture_history[-3:]:  # Last 3 gestures
                gesture_counts[g] = gesture_counts.get(g, 0) + 1
            
            # Get most frequent gesture
            smoothed_gesture = max(gesture_counts, key=gesture_counts.get)
            
            # Only update if confidence is high enough or gesture is consistent
            if gesture_counts[smoothed_gesture] >= 2:  # Appears at least twice
                self.current_gesture = smoothed_gesture
        
        # Stable gesture detection with different thresholds for different states
        if self.current_gesture == self.last_gesture and self.current_gesture != "none":
            if self.stable_start == 0:
                self.stable_start = current_time
        else:
            self.stable_start = 0
        
        stable_time = current_time - self.stable_start if self.stable_start > 0 else 0
        
        # Different stability requirements for different gestures
        if self.state == "menu":
            required_stability = {
                "thumbs_up": 0.6,
                "thumbs_down": 0.6, 
                "pointing": 0.3  # Faster response for pointing
            }
        elif self.state == "options":
            required_stability = {
                "thumbs_down": 0.5,  # Faster thumbs down in options
                "pointing": 0.3
            }
        else:
            required_stability = {
                "rock": 0.4,
                "paper": 0.4,
                "scissors": 0.5  # Slightly longer for scissors accuracy
            }
        
        min_stable_time = required_stability.get(self.current_gesture, 0.8)
        
        # Menu logic with improved responsiveness
        if self.state == "menu":
            self.check_menu_hover()
            
            if self.current_gesture == "thumbs_up" and stable_time > min_stable_time:
                self.start_game()
                self.stable_start = 0
            elif self.current_gesture == "thumbs_down" and stable_time > min_stable_time:
                return False
            elif self.current_gesture == "pointing" and self.menu_hover >= 0 and stable_time > min_stable_time:
                if self.menu_hover == 0:
                    self.start_game()
                elif self.menu_hover == 1:
                    self.state = "options"
                elif self.menu_hover == 2:
                    return False
                self.stable_start = 0
        
        # Options logic with improved back navigation
        elif self.state == "options":
            self.check_menu_hover()  # Check for back button hover
            
            if self.current_gesture == "thumbs_down" and stable_time > min_stable_time:
                self.state = "menu"
                self.stable_start = 0
            elif self.current_gesture == "pointing" and self.menu_hover == 0 and stable_time > min_stable_time:
                # Back button clicked with finger
                self.state = "menu"
                self.stable_start = 0
        
        # Countdown logic
        elif self.state == "countdown":
            elapsed = current_time - self.countdown_start
            
            if elapsed >= 1.0:
                self.countdown_phase += 1
                self.countdown_start = current_time
                
                if self.countdown_phase >= 4:
                    self.execute_battle()
        
        # Result logic
        elif self.state == "result":
            if current_time - self.countdown_start >= 3.0:
                self.state = "menu"
        
        self.last_gesture = self.current_gesture
        return True
    
    def start_game(self):
        """Start new game"""
        self.state = "countdown"
        self.countdown_phase = 0
        self.countdown_start = time.time()
        self.ai_choice = random.choice(self.choices)
    
    def execute_battle(self):
        """Execute battle and determine winner"""
        if self.current_gesture in self.choices:
            self.player_choice = self.current_gesture
        else:
            self.player_choice = "rock"
        
        # Determine winner
        if self.player_choice == self.ai_choice:
            self.result = "TIE!"
            self.ties += 1
        elif ((self.player_choice == "rock" and self.ai_choice == "scissors") or
              (self.player_choice == "paper" and self.ai_choice == "rock") or
              (self.player_choice == "scissors" and self.ai_choice == "paper")):
            self.result = "YOU WIN!"
            self.player_wins += 1
        else:
            self.result = "YOU LOSE!"
            self.ai_wins += 1
        
        self.total_games += 1
        self.save_data()
        
        self.state = "result"
        self.countdown_start = time.time()
    
    def run(self):
        """Main game loop"""
        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        
        print("🎮 Welcome to Rock Paper Scissors World! 🎮")
        print("👍 Thumbs UP = Start | 👎 Thumbs DOWN = Exit | 👉 Point = Select")
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            # Flip frame
            frame = cv2.flip(frame, 1)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Hand detection
            results = self.hands.process(rgb_frame)
            
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    # Draw landmarks
                    self.mp_draw.draw_landmarks(frame, hand_landmarks, 
                                               self.mp_hands.HAND_CONNECTIONS)
                    
                    # Detect gesture
                    gesture, confidence = self.detect_gesture(hand_landmarks.landmark)
                    self.current_gesture = gesture
                    self.confidence = confidence
            else:
                self.current_gesture = "none"
                self.confidence = 0
                self.pointing = False
            
            # Update FPS
            self.update_fps()
            
            # Update game
            if not self.update_game():
                break
            
            # Draw screens
            if self.state == "menu":
                self.draw_menu(frame)
            elif self.state == "countdown":
                self.draw_countdown(frame)
            elif self.state in ["battle", "result"]:
                self.draw_battle(frame)
            elif self.state == "options":
                self.draw_options(frame)
            
            # Show finger pointer in menu and options
            if self.pointing and self.state in ["menu", "options"]:
                cv2.circle(frame, self.finger_pos, 15, self.colors['yellow'], -1)
                cv2.circle(frame, self.finger_pos, 15, self.colors['white'], 3)
            
            # Display
            cv2.imshow('Rock Paper Scissors World', frame)
            
            # Exit on 'q'
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    game = RockPaperScissorsWorld()
    game.run()