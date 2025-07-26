# eNBy - a NetsBlox (specifically RoboScape) wrapper with ease of use in mind. Kinda.
# Author: Sylvyon <sylvyon@disroot.org>

from typing import List
import netsblox
import json
from . import ciphers


    
def decrypt(text: str, shift: int):
    return ciphers.caesar.encrypt(text, -shift)

def clamp(val: int, min: int, max: int):
    if val >= min and val <= max:
        return val
    if val > max:
        return max
    return min


class this:
    def __init__(self, id: str, enby):
        self.id = id
        self.enby = enby

    def beep(self, duration: int, frequency: int):
        return self.enby.beep(self.id, duration, frequency)

    def setSpeed(self, left: int = None, right: int = None):
        return self.enby.setSpeed(self.id, left, right)

    def stop(self):
        return self.enby.setSpeed(self.id, 0, 0)

    def connected(self):
        return self.enby.connected(self.id)
    
    def send(self, command: str):
        return self.enby.roboscape.send(self.id, command)


class music:
    def __init__(self, enby):
        self.enby = enby

    def midi_to_freq(self, note: int) -> float:
        return 440.0 * (2 ** ((note - 69) / 12))

class message:
    robotMessage = 'robot message'
    robotCommand = 'robot command'

class enby:
    def __init__(
        self,
        client: netsblox.Client,
        roboscape: netsblox.RoboScape,
        roboscape_id: str = "",
    ):
        self.client: netsblox.Client = client
        self.roboscape: netsblox.RoboScape = roboscape
        self.roboscape_id: str = roboscape_id
        self.this: this = this(self.roboscape_id, self)
        self.speedLeft: int = 0
        self.speedRight: int = 0
        self.encryptBot = {}
        self.key = ''
        self.music: music = music(self)
        self.message: message = message()
        self.Proxy = None

    def beep(self, robot: str, duration: int, frequency: int) -> None:
        return self.roboscape.send(robot, f"beep {duration} {frequency}")

    def setSpeed(self, robot: str, left: int = None, right: int = None):

        if left is not None:
            left = clamp(left, -127, 127)
            self.speedLeft = left
        else:
            left = self.speedLeft

        if right is not None:
            right = clamp(right, -127, 127)
            self.speedRight = right
        else:
            right = self.speedRight

        return self.roboscape.send(robot, f"set speed {left} {right}")

    def stop(self, robot: str):
        return self.setSpeed(robot, 0, 0)

    def getRobots(self) -> List[str]:
        return (
            self.roboscape.get_robots()
        )  # since i know im going to get lazy and just type getrobots

    def getOthers(self) -> List[str]:
        robots = self.roboscape.get_robots()
        for robot in robots:
            if robot.endswith(self.roboscape_id):
                robots.remove(robot)
        return robots

    def connected(self, id: str) -> bool:
        robots = self.roboscape.get_robots()
        for robot in robots:
            if robot.endswith(id):
                return True
        return False

    def setKey(self, id: str, key: str) -> bool:
        self.roboscape.send(id, "set key " + key)

    """
    name: str = 'speck' | 'caesar'
    """

    def setEncryption(self, id: str, name: str, key: str | int):
        self.roboscape.send(id, f"set encryption {name} {key}")

    def kill(self, id: str):
        self.roboscape.send(id, "set client rate 1 1")

    def loadCrypt(self):
        with open("./encryptBot.json") as data:
            self.encryptBot = json.loads(data.read())
            data.close()

    def saveCrypt(self):
        with open("./encryptBot.json", "w") as data:
            data.write(json.dumps(self.encryptBot))
            data.close()

    def sendCrypt(self, robot: str, command: str):
        data = self.encryptBot.get(robot, None)
        if data is not None:
            mode = data.get("mode")
            if mode.lower() != "caesar":
                raise Warning('Mode is present but not caesar. Unsupported, sending in plain text.')
            value = data.get("value")
            self.roboscape.send(robot, ciphers.caesar.encrypt(command, value))
        self.roboscape.send(robot, command)
    
    def listenAll(self):
        # robots = self.getOthers()
        # self.roboscape.listen(" ".join(robots))
        pass
