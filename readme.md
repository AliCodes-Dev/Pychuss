<p align="center">
  <img src="https://upload.wikimedia.org/wikipedia/commons/4/45/Chess_plt45.svg" width="80" alt="Chess Pawn"/>
</p>

<h1 align="center">♟️ PyChuss – A Python Chess Game with Pygame</h1>

<p align="center">
  <i>Chess, but make it code. Built from scratch with Python and Pygame, featuring clean architecture, piece logic, and good vibes.</i>
</p>

---

## 🧠 Overview

**PyChuss** is a chess game coded in Python using Pygame. It’s fully playable with click-based movement, accurate piece rules, and capturing logic. Ideal if you wanna learn game logic, object-oriented design, or just flex your Python skills in something real.

---

## 🚩 Features

- ✅ Full 8x8 board setup
- ✅ All standard pieces with correct movement
- ✅ Piece capturing logic
- ✅ Turn-based system (White vs Black)
- ✅ Mouse-based input — click to play
- ✅ Modular codebase (OOP, clean structure)
- ✅ Git-tracked and public repo (source control FTW)

---

## 🔧 In Progress

- ⏳ Check and Checkmate detection
- ⏳ Draw / Stalemate conditions
- ⏳ Move highlighting (show valid moves)
- ⏳ GUI polishing (menu, restart, etc.)

---

## 🧩 File Structure

.
├── main.py # Main game loop
├── board.py # Board class + logic
├── pieces/ # Folder for individual piece classes
│ ├── bishop.py
│ ├── king.py
│ ├── knight.py
│ ├── pawn.py
│ ├── queen.py
│ ├── rook.py
│ └── init.py
├── assets/ # Sprites and visual stuff
│ └── (piece images)
├── README.md

---

## 🛠️ Tech Stack

- 🐍 **Python** 3.10+
- 🎮 **Pygame** (for rendering + input)
- 🌀 **Git** (source control and commits)

---

## ⚡ How to Run

```bash
# Install pygame if you haven't
pip install pygame

# Run the game
python main.py


License
MIT License – Use it, mod it, share it, no strings attached.
```
