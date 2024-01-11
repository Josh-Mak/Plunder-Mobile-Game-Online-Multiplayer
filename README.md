# Plunder-Mobile-Game-Online-Multiplayer
This is a game demo for a mobile game called Plunder. It contains both the client and network/server to run online multiplayer.

![image](https://github.com/Josh-Mak/Plunder-Mobile-Game-Online-Multiplayer/assets/152421096/34ada16e-c978-4a10-a2e7-40706106929a)
![image](https://github.com/Josh-Mak/Plunder-Mobile-Game-Online-Multiplayer/assets/152421096/1912a941-6638-490d-9dac-050a21571b33)


**Intro**: This game was made as a concept/demo for a game developer who wanted to see how their board game would fair as a mobile game. As such it heavily focuses on functionality over appeearance.

**Important Note**: Game assets (such as images) have been removed from this GitHub repository. In order for the code to work you would need to add these images, or placeholders for them, back in.

**Technical Overview**: Plunder uses Pygame as a base for building the game, and a custom built server/network to connect clients. Here's how it works:
  1. Important information about the state of the game is stored in the Game class.
  2. Each players important information (eg. actions taken) is sent from individual clients to the server using strings and the network class. 
  3. The server runs different functions depending on the incoming string, and updates the Game class accordingly.
  4. The server sends the Game object to each client using Pickle and the network to update the releveant information on both players client's.
