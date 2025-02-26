# Platform Games

A fun and challenging 2D platform game built with Pygame Zero. Jump on enemies, avoid collisions, and try to reach 100% progress!

## Features

- 🎮 Smooth character movement and animations
- 🤖 Smart enemy AI with zone-based patrolling
- ❤️ Lives system with heart display
- 📊 Score and progress tracking
- 🎵 Background music and sound effects
- 🎯 Win condition: Reach 100% progress
- 📱 Interactive menu system

## Screenshots
![platform_games_menu](https://github.com/user-attachments/assets/ce45977c-7c6f-4600-9fa6-5c5eaf5e5d08)

![platform_games](https://github.com/user-attachments/assets/d3551bb0-13c9-4320-a3ea-84a31e0a4589)

![platform_games_game_over](https://github.com/user-attachments/assets/3642f6a7-f96b-44c2-b0e5-bb10e982cd2f)

![platform_games_winner](https://github.com/user-attachments/assets/06ba6475-6043-4346-8ff6-929e544a7cd8)


## Requirements

- Python 3.x
- Pygame Zero

## Installation

1. Make sure you have Python installed on your system
2. Install Pygame Zero:
```bash
pip install pgzero
```

## How to Run

```bash
python platform_game.py
```

## Controls

- Left Arrow: Move left
- Right Arrow: Move right
- Space: Jump
- Click menu buttons to navigate

## Gameplay

- Jump on enemies to defeat them
- Each defeated enemy gives you 50 points and 10% progress
- Avoid side collisions with enemies
- Reach 100% progress to win
- Game over if you collide with enemies

## Project Structure

```
Platform Games/
├── platform_game.py    # Main game file
├── README.md          # Documentation
├── requirements.txt   # Python dependencies
└── images/           # Game assets
    ├── character_*.png
    ├── snake_*.png
    ├── mushroom_*.png
    └── ...
```

## Author

Nurbeniz Yağlı

## License

This project is licensed under the MIT License - see the LICENSE file for details
