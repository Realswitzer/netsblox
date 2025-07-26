# View the other versions in the `demo.ipynb` notebook.
import netsblox
import time
import eNBy
import mido

Client = netsblox.Client()
RoboScape = netsblox.RoboScape(client=Client)
print("Initialized RoboScape")
enby = eNBy.enby(Client, RoboScape, "37ac")

mid = mido.MidiFile('midi/untitled2.mid')
note_events = []
for msg in mid:
    if msg.type == 'note_on' and msg.velocity > 0:
        freq = enby.music.midi_to_freq(msg.note)
        duration = msg.time  # usually in seconds
        if duration < 0.1: continue
        note_events.append((freq, duration * 2))

while not enby.this.connected():
    time.sleep(1)
input('r')
for freq, dur in note_events:
    enby.this.beep(int(dur * 1000), int(freq))
