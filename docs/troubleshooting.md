# Troubleshooting

## `ssh: Could not resolve hostname raspberrypi.local`

Some networks don't support `.local` names. Connect with the Pi's IP address instead, for example `ssh you@192.168.1.42`. Your router or phone hotspot lists the address among the connected devices.

## SSH says `Connection refused`

SSH isn't turned on. Write the card again with SSH turned on in Raspberry Pi Imager's settings. If you have a monitor and keyboard, you can instead run `sudo raspi-config` and turn on SSH under **Interface Options**.

## The LED doesn't light

- Check the LED's direction: the long leg goes to the resistor and GPIO17.
- Check that the wire is on physical **pin 11**, which is GPIO17, not on pin 17.
- Check that the resistor and the LED sit in different breadboard rows, so the current flows through both.

## One button press toggles the LED twice

That's switch bounce: the contacts chatter for a few milliseconds. `button.py` ignores repeat presses within 50 ms. If it still happens, raise the limit:

```bash
python3 demos/button.py --bounce-time 0.1
```

## The distance is stuck at about 100 cm

gpiozero reports its maximum range, 100 cm, when no echo comes back. Check the TRIG wire (pin 16), the ECHO wire (pin 18) and the 1 kΩ / 2 kΩ divider, and make sure VCC is on 5 V (pin 2).

## A `PWMSoftwareFallback` warning appears

It's harmless. gpiozero is suggesting the pigpio library for more precise timing, and the demo works without it.

## The phone can't open the web page

- The phone and the Pi must be on the same network. Campus Wi-Fi often blocks traffic between devices, so put both on your phone's hotspot.
- Use the Pi's address from `hostname -I` with port 5000, for example `http://192.168.1.42:5000/`.
- Check that `web.py` is still running in the terminal.

## `lgpio.error: 'GPIO busy'`

Another program is still using the pin, often a demo left running in another terminal. Stop it with `Ctrl+C`, then try again.

## `error: externally-managed-environment` from pip

Raspberry Pi OS manages Python packages with `apt`. Install the demo packages with `sudo apt install python3-gpiozero python3-flask`, or use a virtual environment as described in [setup.md](setup.md#optional-use-a-virtual-environment).
