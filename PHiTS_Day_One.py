import math, opentrons

# metadata
metadata = {
    'protocolName': 'Complete PCR Workflow with Thermocycler',
    'author': 'Your Name <your.email@example.com>',
    'description': 'Distribute CaCl2, MgCl2, O/N host culture, and host medium to a deep-well plate and incubate.',
    'apiLevel': '2.13'
}
""" 
Phage amplification (day 1) 
a. Distribute a maximum of 94 samples (1.5 mL) in a deep-well plate (no. 1) with pierceable sealing tape (e.g., Z722529-50EA; Excel Scientific, Victorville, CA). 
To each of the 96 wells add:
    90uL CaCl2 (0.25 M) and MgCl2 (0.25 M), final concentration 10 mM.
    110uL ON host culture, final concentration 5% v/v.
    500uL host medium (concentration · 4.4), final concentration · 1. During addition of medium, carefully pipette up and down a few times to mix.
Sterilized water (1.5 mL) is added as negative amplification controls to wells D6 and E6.
If a sample volume <1.5 mL is used, then adjust volume and concentration of host medium accordingly.

Close the well plate and incubate ON on a shaker (200 rpm).
"""

# Protocol run function
def run(PHiTS_1: protocol_api.ProtocolContext):
    
    # Labware
    deep_well_plate = protocol.load_labware('nest_96_wellplate_2ml_deep', 1)
    tiprack_200ul = protocol.load_labware('opentrons_96_tiprack_300ul', 2)
    tiprack_20ul = protocol.load_labware('opentrons_96_tiprack_20ul', 3)
    reservoir = protocol.load_labware('usascientific_12_reservoir_22ml', 4)
    
    # Pipettes
    p300 = protocol.load_instrument('p300_single_gen2', 'right', tip_racks=[tiprack_200ul])
    p20 = protocol.load_instrument('p20_single_gen2', 'left', tip_racks=[tiprack_20ul])
    
    # Reagents
    cacl2_mgcl2 = reservoir.wells_by_name()['A1']
    on_host_culture = reservoir.wells_by_name()['A2']
    host_medium = reservoir.wells_by_name()['A3']
    
    # Step 1: Add 90uL CaCl2 and MgCl2 to each well
    p300.pick_up_tip()
    for well in deep_well_plate.wells():
        p300.aspirate(90, cacl2_mgcl2)
        p300.dispense(90, well)
    p300.drop_tip()
    
    # Step 2: Add 110uL ON host culture to each well
    p300.pick_up_tip()
    for well in deep_well_plate.wells():
        p300.aspirate(110, on_host_culture)
        p300.dispense(110, well)
    p300.drop_tip()
    
    # Step 3: Add 500uL host medium to each well, mixing in the process
    p1000.pick_up_tip()
    for well in deep_well_plate.wells():
        p1000.aspirate(500, host_medium)
        p1000.dispense(500, well)
        p1000.mix(3, 300, well)  # Mix by pipetting up and down 3 times
    p1000.drop_tip()
    
    # Incubation step (simulated)
    protocol.comment('Incubate the well plate ON on a shaker at 200 rpm.')

# Run the protocol
run(protocol_api.ProtocolContext())
