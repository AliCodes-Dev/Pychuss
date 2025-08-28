<p align="center">
  <img src="https://upload.wikimedia.org/wikipedia/commons/4/45/Chess_plt45.svg" width="80" alt="Chess Pawn"/>
</p>

<h1 align="center">♜ PyChuss – Python Chess Game (Pygame)</h1>

<p align="center">
  <b>A structured, feature-rich chess game written in Python with Pygame.<br>
  Built to explore chess logic, game loops, and modular UI design.</b>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-blue?logo=python" />
  <img src="https://img.shields.io/badge/Pygame-2.x-green?logo=pygame" />
  <img src="https://img.shields.io/badge/License-MIT-yellow.svg" />
  <img src="https://img.shields.io/badge/Status-Playable-brightgreen" />
</p>

---

## 🧠 About PyChuss

**PyChuss** is an object-oriented chess game built in **Python** with **Pygame**.  
It supports the full chess ruleset (minus en passant, coming soon) and a basic UI framework with menus and in-game panels.

Great for learning:

- Chess rule implementation (check, checkmate, castling, promotion, etc.)
- Modular UI with scenes and reusable components
- Turn-based game design in Python
- Event-driven programming with Pygame

---

## 🧱 Features

- ✅ Interactive chessboard with mouse-driven moves
- ✅ Accurate piece movement (all standard rules except en passant)
- ✅ Capturing, castling, and pawn promotion (defaults to queen)
- ✅ Check and checkmate detection
- ✅ Turn-based play (White vs Black)
- ✅ Scene-based UI system:
  - Main menu
  - Game scene
  - Pause menu
- ✅ Custom font + pixel-art style pieces
- ✅ Modular, OOP-driven codebase for easy extension

---

## 🚧 Roadmap

- ♚ En passant rule support
- ✨ Stalemate and draw conditions
- 🎨 Improved UI polish (win screen, restart menu, animations)
- 📸 Gameplay GIFs/screenshots

---

## 🛠 Tech Stack

| Tool      | Purpose                   |
| --------- | ------------------------- |
| 🐍 Python | Main programming language |
| 🎮 Pygame | Rendering, input handling |
| 🌀 Git    | Source control            |
| rich      | Debugging                 |

---

## 📂 Project Structure

```
PyChuss/
├── assets/ # Piece sprites, font, UI images
│ ├── black/
│ ├── white/
│ ├── font/
│ └── move.png
├── Scenes/ # Menu & game scenes
│ ├── game_scene.py
│ ├── main_menu.py
│ ├── pause_menu.py
│ └── scene.py
├── UI/ # Reusable UI components
│ ├── button.py
│ ├── label.py
│ └── panel.py
├── board.py # Core chessboard logic
├── pieces.py # Piece movement + rules
├── player.py # Player/turn management
├── settings.py # Config/settings
├── main.py # Entry point – game loop
├── icon.png # Game icon
├── readme.md # This file
└── description.md # Extra project notes
```

---

## 🚀 Getting Started

1. **Install dependencies:**

   ```bash
   pip install pygame,rich
   ```

2. **Run the game:**

   ```bash
   python main.py
   ```

> **Note:** Works best with Python 3.10+.  
> Ensure your assets are in place for sprites to load correctly.


## 🎮 Screenshots

<p align="center">
  <img src="assets/screenshots/main_menu.png" alt="Main Menu" width="300"/>
  <br/><em>Main Menu</em>
</p>

<p align="center">
  <img src="assets/screenshots/game.png" alt="Chess Board" width="350"/>
  <img src="assets/screenshots/game_play.png" alt="Gameplay" width="350"/>
  <br/><em>Board & Gameplay</em>
</p>

<p align="center">
  <img src="assets/screenshots/Gameplay%20-%20Castle.gif" alt="Castle Move" width="400"/>
  <img src="assets/screenshots/output.gif" alt="Output Test" width="400"/>
  <br/><em>Castling & Move Outputs</em>
</p>


## ⚖️ License

MIT License.  
Feel free to use, modify, and learn from this project. Please don’t claim it as your own for resale.
