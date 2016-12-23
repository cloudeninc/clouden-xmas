import time
import rtmidi

midiout = None

midi_channels = {
    'red': 5,
    'green': 10,
    'blue': 6,
}

active_channels = {
}

def init():
    global midiout
    print('Initializing MIDI...')
    midiout = rtmidi.MidiOut()
    midiout.open_port(1)

def uninit():
    global midiout
    print('Uninitializing MIDI...')
    del midiout
    midiout = None

def stop_midi(color):
    channel = midi_channels[color]
    note_off = [0x80 | (channel-1), 60, 0]
    print('Sending NOTE OFF to %s channel %s: %s' % (color, channel, note_off))
    midiout.send_message(note_off)
    del active_channels[color]

def play_midi(color, repetitions):
    if not repetitions:
        repetitions = 5
    if repetitions > 10:
        repetitions = 10
    channel = midi_channels[color]
    now = time.time()
    note_on = [0x90 | (channel-1), 60, 127] # channel 1, middle C, velocity 112
    print('Sending NOTE ON to %s channel %s: %s' % (color, channel, note_on))
    midiout.send_message(note_on)
    active_channels[color] = now + 0.1 * repetitions

def tick():
    now = time.time()
    for color, end_time in active_channels.items():
        if end_time <= now:
            stop_midi(color)

def handle_message(msg):
    for key, value in msg.items():
        if key in midi_channels:
            if not key in active_channels:
                play_midi(key, value)
            else:
                print('Already playing channel %s' % key)
        else:
            print('Unknown MIDI channel %s' % key)
