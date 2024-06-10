from opentrons import protocol_api

# Metadata
metadata = {
    'protocolName': 'Host Bacteria Removal and Soft-Agar Overlay Plate Preparation',
    'author': 'Your Name <your.email@example.com>',
    'description': 'Filter host bacteria, prepare soft-agar overlay plates, and transfer lysates in a chequered pattern.',
    'apiLevel': '2.13'
}

# Protocol run function
def run(protocol: protocol_api.ProtocolContext):
    
    # Labware
    deep_well_plate = protocol.load_labware('nest_96_wellplate_2ml_deep', 1)
    filter_plate = protocol.load_labware('millipore_96_wellplate_0.45um', 2)
    well_plate_A = protocol.load_labware('nunc_96_wellplate_200ul', 3)
    well_plate_B = protocol.load_labware('nunc_96_wellplate_200ul', 4)
    tiprack_200ul = protocol.load_labware('opentrons_96_tiprack_300ul', 5)
    reservoir = protocol.load_labware('usascientific_12_reservoir_22ml', 6)
    
    # Pipettes
    p300 = protocol.load_instrument('p300_multi', 'left', tip_racks=[tiprack_200ul])
    p20 = protocol.load_instrument('p20_multi_gen2', 'right', tip_racks=[tiprack_200ul])
    
    # Reagents
    cacl2_mgcl2 = reservoir.wells_by_name()['A1']
    host_culture = reservoir.wells_by_name()['A2']
    
    # Step 1: Transfer 200 μL from each well of deep-well plate to filter plate, pipetting up and down to mix
    p300.pick_up_tip()
    for source, dest in zip(deep_well_plate.wells(), filter_plate.wells()):
        p300.aspirate(200, source)
        p300.dispense(200, dest)
        p300.mix(3, 150, dest)  # Mix by pipetting up and down 3 times
    p300.drop_tip()
    
    # Simulate centrifugation
    protocol.pause("Centrifuge the filter plate on top of a new well plate at 900 x g for 2 minutes. Then add pierceable sealing tape to well plate no. 2. Discard the filter plate.")
    
    # Step 2: Prepare two large soft-agar overlay plates with CaCl2, MgCl2, and host culture
    protocol.pause("Prepare two large soft-agar overlay plates with 0.5% agarose, CaCl2 and MgCl2 (final concentration 10 mM), and host culture (final concentration 2.5-5%). Allow the plates to solidify.")
    
    # Step 3: Remove every second row of pipette tips in a box of 200 μL pipette tips
    protocol.pause("Remove every second row of pipette tips in a box of 200 μL pipette tips to facilitate the transfer of lysate in a chequered pattern.")
    
    # Step 4: Transfer lysates in a chequered pattern to two new microtiter plates
    # Transfer lysates from deep-well plate to well plate A (no. 4) and well plate B (no. 5)
    p300.pick_up_tip()
    for i in range(0, 96, 2):
        p300.transfer(200, filter_plate.wells()[i], well_plate_A.wells()[i], new_tip='never')
        p300.transfer(200, filter_plate.wells()[i], well_plate_B.wells()[i], new_tip='never')
    p300.drop_tip()
    
    # Step 5: Use the 96-pin replicator to transfer lysates to soft-agar overlay plates
    protocol.pause("Use the 96-pin replicator to carefully transfer ~1 μL of lysates from well plate A (no. 4) to the soft-agar overlay plate A. Clean the 96-pin replicator with ethanol and flame, then repeat the procedure with well plate B (no. 5) and soft-agar overlay plate B.")
    
    # Step 6: Incubate soft-agar overlay plates and store well plates
    protocol.pause("Incubate the soft-agar overlay plates upside down overnight. Seal well plates A (no. 4) and B (no. 5) and store them at 4°C.")
    
    protocol.comment("Protocol complete.")

# Run the protocol
run(protocol_api.ProtocolContext())
