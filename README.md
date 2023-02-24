# MH3 Server Project

The goal of this project is to reverse the game in order to make private servers and custom event/arena quests.

## Current Status
The project is kinda functional, multiplayer isn't supported yet.

![Progress](https://user-images.githubusercontent.com/7890055/132406076-baad3f30-5bce-4417-bd2b-9b32a7873380.png)

## Progress
- [ ] Nintendo servers implementation
  - [x] Authentication server (altwfc/wiimmfi)
  - [ ] Shop server and `gpatch.rso` (japan only?)
  - [ ] Are other Nintendo servers used?
- [ ] Capcom servers
  - [x] Terms/Announce/Maintenance message 
  - [x] Dummy Capcom ID profile
  - [ ] Create/retrieve Capcom ID profiles
  - [ ] Cheat detection system
- [ ] Server selection
  - [x] Server type selection
  - [x] Gate selection
  - [x] HR restriction
  - [x] Population count
  - [ ] Backend to report statistics
- [ ] Server events
  - [x] Day/night cycle
  - [ ] Market event
  - [x] Sandstorm event  
- [ ] Gate server
  - [x] Spawning at the gate
  - [ ] Chat system
  - [ ] City search
  - [x] City selection
- [ ] City
  - [x] Create a city
  - [ ] Join a city
  - [x] Set city maximum capacity
  - [ ] (...)
- [ ] Chat
  - [ ] Server message
  - [ ] Player message
  - [ ] Quest message 
  - [ ] Private message
  - [ ] WiiSpeak
- [ ] Quest
  - [x] Create a quest
  - [ ] Join a quest
  - [x] Start a quest
  - [ ] Event quests
  - [ ] Arena quests
- [ ] Friend system
  - [ ] Friend list
  - [ ] Send a friend request
  - [ ] Receive a friend request
  - [ ] Accept a friend request
  - [ ] Blacklist
 
## Prerequisites
 - Softmodded Wii or Dolphin Emulator
 - Patched game to use Nintendo servers alternatives
   * [AltWFC](https://github.com/polaris-/dwc_network_server_emulator) (prefered)
   * [Wiimmfi](https://wiimmfi.de/)
 - DNS server _(hosts redirection can be used for Dolphin users)_
 - OpenSSL _(or any other tool to generate SSL certificates)_
 - Python 2.7 or Python 3.x

## Setup
You can setup the server by following the guide on the [wiki](https://github.com/sepalani/MH3SP/wiki):
 - **Setup page**: the procedure to setup the server.
 - **Troubleshooting page**: common issues and how to solve them.
 - **Configuration page**: options you can use to change the server behaviour.

## Community
Feel free to join our discord server if you want to discuss MH3SP and 
InusualZ's [MHTriServer](https://github.com/InusualZ/MHTriServer) or if you
need help setting them up:
 - https://discord.gg/4sBmXC55V6

You might find relevant information in the `#faq` and `#help` channels of
the discord server.

## Special thanks
Without them, the project would never have been possible:
 - Nintendo servers emulation projects
   * [Wiimmfi Project](https://wiimmfi.de/)
   * [AltWFC Project](https://github.com/polaris-/dwc_network_server_emulator)
 - [Dolphin Emulator Team](https://dolphin-emu.org/)
 - [InusualZ](https://github.com/InusualZ)
   * For helping me to reverse the game
 - Some people from the video game preservation scene
   * They will recognise themselves ;v)
 - The ones who helped me to improve my reverse and programming skills
