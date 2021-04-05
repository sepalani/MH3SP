# MH3 Server Project

The goal of this project is to reverse the game in order to make private servers and custom event/arena quests.

## Current Status
The project isn't yet functionnal.

![Progress](https://github.com/sepalani/MH3SP/blob/master/progress.png)

## Progress
- [ ] Nintendo servers implementation
  - [x] Authentication server (altwfc/wiimmfi)
  - [ ] Shop server and `gpatch.rso` (japan only?)
  - [ ] Are other Nintendo servers used?
- [ ] Capcom servers
  - [ ] Terms/Announce/Maintenance message 
  - [ ] Dummy Capcom ID profile
  - [ ] Create/retrieve Capcom ID profiles
  - [ ] Cheat detection system
- [ ] Server selection
  - [ ] Server type selection
  - [ ] Gate selection
  - [ ] HR restriction
  - [ ] Population count
  - [ ] Backend to report statistics
- [ ] Server events
  - [ ] Day/night cycle
  - [ ] Market event
  - [ ] Sandstorm event  
- [ ] Gate server
  - [ ] Spawning at the gate
  - [ ] Chat system
  - [ ] City search
  - [ ] City selection
- [ ] City
  - [ ] Create a city
  - [ ] Join a city
  - [ ] Set city maximum capacity
  - [ ] (...)
- [ ] Chat
  - [ ] Server message
  - [ ] Player message
  - [ ] Quest message 
  - [ ] Private message
  - [ ] WiiSpeak
- [ ] Quest
  - [ ] Create a quest
  - [ ] Join a quest
  - [ ] Start a quest
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
