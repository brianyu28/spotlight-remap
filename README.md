# Spotlight Remap

Remaps the buttons on a Logitech Spotlight 2 presentation remote to custom key
combinations on macOS.

Logi Options+ by default only allows some button actions to be mapped to custom
key combinations. For maximum flexibility with the presentation remote, this
script supports mapping all buttons and press types (single press, double press,
long press) to custom key combinations.

## Usage

Using `uv`:

```bash
sudo uv run main.py
```

Or install as a tool first with `uv tool install .` and run as:

```bash
sudo spotlight-remap
```

Your terminal (e.g. Terminal, iTerm) and your Python process (e.g. `python3.14`,
likely located in a subdirectory of `.local/share/uv/python/` if using `uv`)
must have "Input Monitoring" permissions in System Settings -> Privacy &
Security -> Input Monitoring.

Additionally, Logi Options+ must not be running (either actively or in the
background), or else it will intercept these events. Check Activity Monitor or
System Settings's App Background Activity to verify that Logi Options+ isn't
running in the background.

### Other Usage

When the program terminates normally, controls should automatically be
un-diverted. In the event of that this does not happen, you can run the
following command to restore diverting statuses to default state:

```bash
sudo uv run src/main.py restore
```

To learn the Control ID (CID) for a particular device input, run:

```bash
sudo uv run src/main.py learn
```

Then provide the device input (e.g. button press) you want to learn and observe
the CID output.

This program assumes Bluetooth device index by default, not a USB slot. If using
USB, to learn which device index corresponds to your Spotlight 2, run:

```bash
sudo uv run src/main.py device
```

## How It Works

The Spotlight 2 remote, like other input devices, is a HID (Human Interface
Device) device. Logitech extends this protocol with HID++, a proprietary
protocol for messages between Logitech's devices. Spotlight 2 uses a Logitech
HID++ feature called "Reprogrammable Controls V4" (0x1b04).

As part of Reprogrammable Controls V4, each physical control or gesture (e.g.
button press, double press, long press, etc.) gets a 16-bit Control ID (CID).
These controls can be "diverted": which tells the device to stop doing its
default behavior, and instead emit a software notification any time the CID is
triggered.

This script listens for these notifications, and when it receives one, maps that
CID to a custom-defined key combination, and emits that key combination to the
system via CGEvent.
