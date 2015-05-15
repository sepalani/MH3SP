# MH3 Server Project

The goal of this project is to reverse the game in order to make private servers.


Current Status
--------------
The project isn't yet functionnal. Todo:
 * **Loading bar:** 85%
- [x] Bypass Nintendo Servers
- [x] DNS Redirection
- [x] Create SSL connection (tcp port: 8200)
- [ ] Find/Send expected data
- [ ] *What's next?*
 * **Capcom ID selection:** No
- [ ] Reverse the Capcom ID selection protocol format 
 * **Server selection:** No
- [ ] Reverse the Server selection protocol format
 * **Gate selection:** No
- [ ] Reverse the Gate selection protocol format
 * **Time system:** No
- [ ] Reverse the Time system protocol format
 * **City creation:** No
- [ ] Reverse the City creation protocol format
 * **Join a city:** No
- [ ] Reverse the City joining protocol format
 * **Search a city:** No
- [ ] Reverse the Research protocol format
 * **Submit a quest:** No
- [ ] Reverse the Quest submitting protocol format
 * **Join a quest:** No
- [ ] Reverse the Quest joining protocol format
 * **Start a quest:** No
- [ ] Reverse the Quest starting protocol format
 * **Chat implemented:** No
- [ ] Reverse the Chat protocol format
 * **Event Quest:** No
- [ ] Reverse the Event Quest protocol format
 * **Arena Quest:** No
- [ ] Reverse the Arena Quest protocol format
 * **Sandstorm:** No
- [ ] Reverse the Sandstorm event protocol format


Prerequisites
-------------
 * Softmodded Wii or Dolphin Emulator
 * Monster Hunter 3 (~tri) w/ Nintendo servers patch
 * DNS server (will be optional in the future)
 * Python 2.7 or above (Python3 not supported)


Monster Hunter 3 (~tri)
-----------------------
In order to use custom servers on Monster Hunter Tri you first need to patch the game to bypass the Nintendo servers. Their servers are blocking the game and prevent it to connect to Capcom servers. I personally use Wiimmfi for that, any other alternative should work as well.
[Link to Wiimmfi instruction](http://wiki.tockdom.com/wiki/MKWii_Network_Protocol/Server/Wiimmfi-Patcher).

1. **Patch the game on the fly**
   * Download the **autowiimmfipatcher** from the "*Playing from a real disc*" section
   * Copy the *apps* folder into your SD card **root directory**
   * Launch the **Homebrew Channel**
   * Run the MrBean35000vr **Wiimmfi Patcher**
   * Insert your **game disc**
2. **Permanent patch**
   * Download the **wiimmfi-patcher** from the "*How-To*" section
   * Carefully **read** the patcher's *README*
   * **Run the patcher** corresponding to your OS
   * Launch your **patched game**


DNS Server
----------
TODO
