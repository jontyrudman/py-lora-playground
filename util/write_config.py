""" Write the config to EEPROM

This only needs to be done once for the module,
or if the config is reloaded, because it is written
to the EEPROM.
"""
from rak811 import Mode, Rak811

with Rak811() as lora:
    print('Setting mode to LoRaP2P...')
    lora.mode = Mode.LoRaP2P
    print('Setting band to EU868...')
    lora.band = 'EU868'
    print('Setting data rate to 5...')
    lora.dr = 5
print('Done.')
