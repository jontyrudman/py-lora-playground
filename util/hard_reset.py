from rak811 import Rak811

with Rak811() as lora:
    print('Hard-resetting LoRa Module...')
    lora.hard_reset()
print('Done.')
