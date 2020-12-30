# Python LoRa Playground

For messing around with LoRa, specifically peer-to-peer connections with the RAK811 module (using pyrak811).

## Installation

1. Clone this repository to the device doing the communicating.
2. Set up a virtualenv in the repository directory with `python3 -m virtualenv venv`.
3. Activate the venv with `source venv/bin/activate`.
4. Install dependencies (there's only one) with `pip install -r requirements.txt`.

## Usage

Everytime your device boots, hard-reset the module using `python3 utils/hard\_reset.py`.
The first time you use the module or whenever you change the config from the values in `utils/write\_config.py`, you'll need to write the config to the module's EEPROM using `python3 utils/write\_config.py`.

Then, do all the talking between devices on the same configs!
See `p2p/p2p.py`.
