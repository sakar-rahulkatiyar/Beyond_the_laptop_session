# Command cheat sheet

The commands from the terminal demo. Press `Tab` to complete names, `↑` to bring back your last command and `Ctrl+C` to stop a running program.

## Navigate and manage files

| Command | What it does |
| --- | --- |
| `pwd` | Show where you are |
| `ls -la` | List everything here, including hidden files |
| `cd folder` | Change folder: `cd /` goes to the top, `cd ~` goes home |
| `mkdir name` | Make a folder |
| `cp a b` | Copy `a` to `b` |
| `mv a b` | Move or rename `a` to `b` |
| `rm file` | Delete a file. There is no recycle bin and no undo. |
| `cat file` | Print a file |
| `nano file` | Edit a file: `Ctrl+O` then `Enter` saves, `Ctrl+X` exits |

## System and hardware

| Command | What it does |
| --- | --- |
| `whoami` | Show which user you are |
| `hostname` | Show which machine you are on; `hostname -I` shows its IP address |
| `sudo command` | Run one command as the administrator |
| `sudo apt update` | Refresh the list of available software |
| `sudo apt install name` | Install software |
| `htop` | Show live CPU, memory and processes; `q` quits |
| `systemctl status name` | Check a background service, for example `ssh` |
| `ssh user@host` | Log in to another machine |
| `chmod +x file` | Make a file runnable |
| `pinout` | Show the GPIO map for your board |
| `vcgencmd measure_temp` | Show the CPU temperature |
| `sudo shutdown now` | Shut down safely |

## Reading permissions

`ls -l` starts each line with a string such as `-rwxr-xr-x`:

- The first character is the type: `-` for a file, `d` for a folder.
- Then come three groups of three letters, for the **owner**, the **group** and **everyone else**.
- `r` means read, `w` means write and `x` means execute. A `-` means that permission is missing.

So `-rwxr-xr-x` is a file that its owner can read, change and run, and that everyone else can read and run.

## The Linux filesystem

Linux has one tree with one root, `/`. There is no `C:` drive; even a USB stick appears inside the tree, usually under `/media`.

| Folder | What it holds |
| --- | --- |
| `/home` | Your files and projects |
| `/etc` | System settings, as plain text files |
| `/boot` | Startup files and firmware |
| `/dev` | Devices, as files |
| `/usr` | Installed programs |
| `/var` | Logs and data that change |
| `/tmp` | Temporary files |

## Hardware as files

Linux shows hardware as files, so the same tools work for both:

```bash
cat /sys/class/thermal/thermal_zone0/temp   # 48312 means 48.3 °C
ls /dev                                     # video0 is a camera, ttyUSB0 a USB serial device, sda1 a USB drive
```
