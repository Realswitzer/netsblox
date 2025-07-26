# netsblox code and stuff

note: eNBy is a package that handles netsblox roboscape stuff, since thats poorly documented and hard to interact with.
part of this information is derived from the course materials, others from testing, and a bit from reviewing the NetsBlox source.

# How to use
Easiest way to start is by copying the code below. This has the fundamentals, like making the Client and RoboScape, which are probably necessary if interacting with a RoboScape anyways.

1. Install necessary packages
```sh
pip install netsblox
# Optional depending on scripts/own usage
pip install mido keyboard pygame_gui pygame
# mido is for midis, keyboard, pygame, and pygame_gui are all useful for making a GUI.
```

2. Make client and start using `enby`
```py
import eNBy, netsblox

Client = netsblox.Client(project_name='testclient')
RoboScape = netsblox.RoboScape(client=Client)
print("Initialized RoboScape")
enby = eNBy.enby(Client, RoboScape, "ffff")
# ending of mac address, some things work with it and some dont. easier to just put full mac there but whatever
```

Other common imports
```py
import threading, time, random, typing
```

## GUI
For the GUI in some of the scripts, `pygame` and `pygame_gui` are used.

## Music
While there is the code to play MIDIs, realistically, due to limitations of the robots themselves, they will not be able to play MIDIs. Reasons for this include the following: limitations in the `beep` command (1000ms limit), network delay, slow response time (even with ideal delay, the buzzer will still sometimes not work), the buzzer only being able to play one tone at a time, and quite simply, these robots are intended for education -- not playing `megalovania3.mid`.

Even if you slow it to half speed (`duration*2`) it will still be too fast on some notes, thus skipping them, or too slow on other notes, preventing the full note from being played. Maybe if you take all of the robots, you can try to have each robot play a different MIDI track, though that sounds like a lot more work, and I don't have 12 robots.

## Bugs
While I do not have access to a robot to confirm anything working, I still want to provide what little support I can give. This will likely include rewriting functions (i.e. `encrypt` and `encrypt++`), which should not require a robot.

Listening is broken due to a server-side bug in NetsBlox/services where the server does not send messages to an external client's `ws`.

Using async will break API/RPC calls, this is an upstream problem (either in PyBlox or NetsBlox)

Not everything has been thoroughly tested, UAYOR. This includes setting keys, encryption, etc.

References:
- [NetsBlox/services#270](https://github.com/NetsBlox/services/issues/270)
- [dragazo/PyBlox#2](https://github.com/dragazo/PyBlox/issues/2)