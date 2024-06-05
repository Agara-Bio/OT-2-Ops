import math, opentrons

# metadata
metadata = {
    'protocolName': 'Complete PCR Workflow with Thermocycler',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.0'
}
""" 
Phage amplification (day 1) 
Sterilized water (1.5 mL) is added as negative amplification controls to wells D6 and E6.
If a sample volume <1.5 mL is used, then adjust volume and concentration of host medium accordingly.
"""

def run():
##a. Distribute a maximum of 94 samples (1.5 mL) in a deep-well plate (no. 1) with pierceable sealing tape (e.g., Z722529-50EA; Excel Scientific, Victorville, CA). 
## To each of the 96 wells add: 90uL CaCl2 (0.25 M) and MgCl2 (0.25 M), final concentration 10 mM.
## 110uL ON host culture, final concentration 5% v/v. 500uL host medium (concentration · 4.4), final concentration · 1. During addition of medium, carefully pipette up and down a few times to mix.


## Close the well plate and incubate ON on a shaker (200 rpm).