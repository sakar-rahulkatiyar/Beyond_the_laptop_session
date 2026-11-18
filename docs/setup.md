# Set up the Raspberry Pi

This guide gets a Raspberry Pi running Raspberry Pi OS and reachable over SSH from your laptop, with no monitor, keyboard or mouse. This is called a *headless* setup, and it's how most robots and servers run.

## You need

- A Raspberry Pi 4 Model B or Raspberry Pi 5, its power supply and a microSD card of 16 GB or more.
- A laptop on the same network the Pi will join. A phone hotspot works well and avoids campus networks that block traffic between devices.

## 1. Flash the card

1. Install [Raspberry Pi Imager](https://www.raspberrypi.com/software/) on your laptop.
2. Insert the microSD card.
3. In Imager, choose your **device** (for example, Raspberry Pi 4), the **operating system** (Raspberry Pi OS, 64-bit) and the **storage** (your microSD card).

## 2. Customise before writing

When Imager offers to customise the OS, set:

- **Hostname**, for example `raspberrypi`.
- **Username and password.** The examples in this repo use the username `you`.
- **Wi-Fi** name, password and country.
- **SSH: turn it on.** A password is fine for a workshop; a public key is safer for a Pi you keep.

This is the step people skip. Without it, you need a monitor and keyboard to finish the setup.

## 3. Write and boot

Write the card, put it in the Pi and connect the power. The first boot takes a minute or two.

## 4. Connect over SSH

From your laptop's terminal (Terminal on macOS or Linux, PowerShell on Windows):

```bash
ssh you@raspberrypi.local
```

Type `yes` to trust the Pi the first time, then enter your password. The prompt changes to `you@raspberrypi:~ $`: everything you type now runs on the Pi.

If `raspberrypi.local` isn't found, use the Pi's IP address instead, for example `ssh you@192.168.1.42`. Your router or phone hotspot lists it among the connected devices.

## 5. Update and install the tools

```bash
sudo apt update
sudo apt full-upgrade -y
sudo apt install -y git htop python3-gpiozero python3-flask
```

The last command is safe to run even if some of these are already installed.

## 6. Get the code

```bash
git clone https://github.com/sakar-rahulkatiyar/Beyond_the_laptop_session.git
cd Beyond_the_laptop_session
```

## 7. Check that everything works

```bash
pinout                  # prints the GPIO map for your board
vcgencmd measure_temp   # prints the CPU temperature, for example temp=48.3'C
```

Then wire the circuit as shown in the [wiring guide](wiring.md) and run the demos from the [README](../README.md#quick-start).

## Optional: use a virtual environment

Raspberry Pi OS manages Python packages with `apt`, so `pip install` outside a virtual environment stops with an `externally-managed-environment` error. To use pip, create a virtual environment that can still see the system packages, because gpiozero needs the GPIO libraries that `apt` installs:

```bash
python3 -m venv --system-site-packages .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Shut down safely

Shut down before you unplug the power or change the wiring:

```bash
sudo shutdown now
```

Wait until the green activity light stops flashing, then unplug the power.
