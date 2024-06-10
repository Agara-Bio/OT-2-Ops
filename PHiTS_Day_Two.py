from opentrons import protocol_api

# Metadata
metadata = {
    'protocolName': 'Host Bacteria Removal and Well Plate Preparation',
    'author': 'Your Name <your.email@example.com>',
    'description': 'Transfer samples to a filter plate, centrifuge, and prepare a new well plate with reagents.',
    'apiLevel': '2.13'
}

# Protocol run function
def run(protocol: protocol_api.ProtocolContext):
    
    # Labware
    deep_well_plate = protocol.load_labware('nest_96_wellplate_2ml_deep', 1)
    filter_plate = protocol.load_labware('millipore_96_wellplate_0.45um', 2)
    well_plate_2 = protocol.load_labware('nunc_96_wellplate_200ul', 3)
    well_plate_3 = protocol.load_labware('nunc_96_wellplate_200ul', 4)
    tiprack_200ul = protocol.load_labware('opentrons_96_tiprack_300ul', 5)
    reservoir = protocol.load_labware('usascientific_12_reservoir_22ml', 6)
    
    # Pipettes
    p300 = protocol.load_instrument('p300_multi', 'left', tip_racks=[tiprack_200ul])
    p20 = protocol.load_instrument('p20_multi_gen2', 'right', tip_racks=[tiprack_200ul])
    
    # Reagents
    host_medium = reservoir.wells_by_name()['A1']
    host_culture = reservoir.wells_by_name()['A2']
    cacl2_mgcl2 = reservoir.wells_by_name()['A3']
    
    # Step 1: Transfer 200 μL from each well of deep-well plate to filter plate, pipetting up and down to mix
    p300.pick_up_tip()
    for source, dest in zip(deep_well_plate.wells(), filter_plate.wells()):
        p300.aspirate(200, source)
        p300.dispense(200, dest)
        p300.mix(3, 150, dest)  # Mix by pipetting up and down 3 times
    p300.drop_tip()
    
    # Simulate centrifugation
    protocol.pause("Centrifuge the filter plate on top of a new well plate at 900 x g for 2 minutes. Then add pierceable sealing tape to well plate no. 2. Discard the filter plate.")
    
    # Step 2: Prepare well plate no. 3 with host medium, host culture, and CaCl2/MgCl2
    p300.pick_up_tip()
    for well in well_plate_3.wells():
        p300.aspirate(180, host_medium)
        p300.dispense(180, well)
    p300.drop_tip()
    
    p20.pick_up_tip()
    for well in well_plate_3.wells():
        p20.aspirate(10, host_culture)
        p20.dispense(10, well)
        p20.aspirate(10, cacl2_mgcl2)
        p20.dispense(10, well)
    p20.drop_tip()
    
    # Step 3: Use 96-pin replicator to transfer ~1 μL from well plate no. 2 to well plate no. 3
    protocol.pause("Use the 96-pin replicator to transfer ~1 μL from each lysate in well plate no. 2 to each well in well plate no. 3. Then close well plate no. 3 and incubate ON on a shaker at 200 rpm.")
    
    # Step 4: Inoculate ON host culture in 10 mL liquid medium
    liquid_medium_tube = protocol.load_labware('opentrons_15_tuberack_falcon_15ml_conical', 7).wells_by_name()['A1']
    p300.pick_up_tip()
    p300.aspirate(10, host_culture)
    p300.dispense(10, liquid_medium_tube)
    p300.drop_tip()
    
    protocol.comment("Inoculate the ON host culture in 10 mL liquid medium for the next day.")

# Run the protocol
run(protocol_api.ProtocolContext())
