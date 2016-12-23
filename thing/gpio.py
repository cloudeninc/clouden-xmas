from RPi import GPIO
import time

GPIO_RED = 18
GPIO_GREEN = 24
GPIO_BLUE = 2
FLASH_DELAY = 0.2
FLASH_DURATION = 0.2
FLASH_REPETITIONS = 3

colors = ('red', 'green', 'blue')

gpio_pins = {
    'red': GPIO_RED,
    'green': GPIO_GREEN,
    'blue': GPIO_BLUE,
}

led_states = {
    'red': {
        'busy': False,
        'repetitions': 0,
        'delay': 0,
        'duration': 0,
        'next_time': 0,
        'next_state': 0,
    },
    'green': {
        'busy': False,
        'repetitions': 0,
        'delay': 0,
        'duration': 0,
        'next_time': 0,
        'next_state': 0,
    },
    'blue': {
        'busy': False,
        'repetitions':0,
        'delay': 0,
        'duration': 0,
        'next_time': 0,
        'next_state': 0,
    },
}

def tick():
    now = time.time()
    for color in colors:
        if led_states[color]['busy']:
            if now >= led_states[color]['next_time']:
                # State change
                if led_states[color]['next_state'] == 'on':
                    # Turn led on and start duration timer
                    GPIO.output(gpio_pins[color], GPIO.HIGH)
                    led_states[color]['next_time'] = now + led_states[color]['duration']
                    led_states[color]['next_state'] = 'off'
                else:
                    # Turn led off and start delay timer
                    GPIO.output(gpio_pins[color], GPIO.LOW)
                    led_states[color]['repetitions'] -= 1
                    if led_states[color]['repetitions'] > 0:
                        # Next round
                        led_states[color]['next_time'] = now + led_states[color]['delay']
                        led_states[color]['next_state'] = 'on'
                    else:
                        # Finished
                        led_states[color]['busy'] = False

def flash(color, repetitions=0, delay=0, duration=0):
    now = time.time()
    if not color in led_states:
        # Unknown
        return
    if led_states[color]['busy']:
        # Already flashing
        return
    led_states[color]['busy'] = True
    led_states[color]['repetitions'] = repetitions or FLASH_REPETITIONS
    led_states[color]['delay'] = delay or FLASH_DELAY
    led_states[color]['duration'] = duration or FLASH_DURATION
    led_states[color]['next_time'] = now + (delay or FLASH_DELAY)
    led_states[color]['next_state'] = 'on'

def init():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(GPIO_RED, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(GPIO_BLUE, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(GPIO_GREEN, GPIO.OUT, initial=GPIO.LOW)

def uninit():
    for color in colors:
        GPIO.output(gpio_pins[color], GPIO.LOW)

def handle_message(msg):
    for key, value in msg.items():
        if key in colors:
            print('Flashing %s' % key)
            flash(key, value)
