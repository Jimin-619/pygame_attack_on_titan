# pygame_attack_on_titan

A 2D obstacle-avoiding game inspired by **Subway Surfer**, implemented in Python using the `pygame` library. Players must navigate through stages, avoid obstacles, and battle bosses while maintaining their health.

![Game Preview]("C:\Users\jimin\OneDrive\사진\스크린샷\스크린샷 2024-12-24 001244.png") 

## Table of Contents
- [Features](#features)
- [Gameplay](#gameplay)
- [Installation](#installation)
- [How to Play](#how-to-play)
- [Assets](#assets)
- [Future Enhancements](#future-enhancements)

---

## Features
- **Dynamic Gameplay:** 
  - Increasing difficulty across three stages with unique challenges.
  - Mid-stage and final boss fights with health and attack mechanics.
- **Visual Effects:**
  - Particle effects for impacts and collisions.
- **Audio Experience:**
  - Background music and sound effects for immersive gameplay.
- **Health Management:**
  - Player health bar and fail mechanics.
- **Interactive Obstacles:**
  - Regular obstacles, mid-bosses, and final boss attacks.

---

## Gameplay
1. Navigate through the game world using arrow keys to avoid or attack obstacles.
2. Clear stages by defeating a set number of obstacles or bosses.
3. Survive boss attacks and avoid rocks to maintain your health.

Stages:
- **Stage 1:** Regular obstacles with low difficulty.
- **Stage 2:** Includes mid-bosses with unique appearances and attacks.
- **Stage 3:** Final boss with special attack patterns.

Game ends when:
- Player defeats the final boss (*Victory*).
- Player health drops to 0 (*Game Over*).

---

## Installation
1. Ensure you have Python 3.9+ installed.
2. Install the required dependencies:
   ```bash
   pip install pygame
