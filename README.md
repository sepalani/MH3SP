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
To redirect requests the game sends to Capcom servers, you need to setup a **DNS server**. This server will **redirect the traffic** to Monster Hunter Tri private servers. You need to setup **Address Records** (a.k.a. *A Record*) with **Capcom's domain names** pointing to your servers' IP. FTM, I don't propose any DNS server so you have to **find and install one yourself**. Nonetheless, I'm planing to make one to automate this task and make it easier for everyone.

[MHTrIDA](https://github.com/sepalani/MHTrIDA/tree/master/server/dns) has lots of details about the **domain names** you may set for you DNS server and other data concerning the game as well.

**NB for Dolphin Users:** Rather than using a DNS server, edit the **hosts file** also work.
 * **Windows** Location: ```%SystemRoot%\system32\drivers\etc\hosts```
 * **Mac OS X** Location: ```/private/etc/hosts```
 * **Linux** Location: ```/etc/hosts```



SSL Certificates
----------------
OpenSSL can be used to generate your own private key/certificate to use with MH3SP servers. Then check with a notepad the server.py file and edit the path for the private key/certificate if needed.



TCP Servers
-----------
Mainly developed in **Python 2.7**, a python interpreter is needed to run MH3SP's servers. **Python3 isn't supported yet**, so a Python2 interpreter has to be used FTM. Then, you only need to **run server.py** python executable to start the server. A usage will be printed if it requires parameters. Servers **may print details** when a client is connected and doing something, **they'll be quiet** otherwise.

1. **Port 8200**
 * This server isn't complete, a **python prompt** is available to send data (string) to the client
