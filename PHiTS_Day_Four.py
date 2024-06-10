from opentrons import protocol_api

# Metadata
metadata = {
    'protocolName': 'Phage Purification and Titering',
    'author': 'Your Name <your.email@example.com>',
    'description': 'Collect clearing zones, dissolve in SM-buffer, filter, and store for future use. Perform titering and dilution series for lysates.',
    'apiLevel': '2.13'
}

# Protocol run function
def run(protocol: protocol_api.ProtocolContext):
    
    # Labware
    agar_plate_A = protocol.load_labware('corning_96_wellplate_360ul_flat', 1)
    agar_plate_B = protocol.load_labware('corning_96_wellplate_360ul_flat', 2)
    well_plate_6 = protocol.load_labware('nunc_96_wellplate_200ul', 3)
    sm_buffer_reservoir = protocol.load_labware('usascientific_12_reservoir_22ml', 4)
    tiprack_200ul = protocol.load_labware('opentrons_96_tiprack_300ul', 5)
    
    # Pipettes
    p300 = protocol.load_instrument('p300_multi', 'left', tip_racks=[tiprack_200ul])
    
    # Reagents
    sm_buffer = sm_buffer_reservoir.wells_by_name()['A1']
    
    # Step 1: Collect clearing zones from agar plates and dissolve in SM-buffer
    protocol.comment('Collecting clearing zones from agar plates A and B.')
    
    for plate in [agar_plate_A, agar_plate_B]:
        for well in plate.wells():
            if some_condition_for_clearing_zone(well):  # Define your condition for clearing zone
                p300.pick_up_tip()
                p300.aspirate(100, sm_buffer)
                p300.dispense(100, well)
                p300.mix(3, 100, well)
                p300.aspirate(100, well)
                # Place collected solution in a storage plate or tube for future use
                p300.dispense(100, some_storage_location)  # Define your storage location
                p300.drop_tip()
    
    protocol.pause("Filter the collected solutions (0.22-0.45 µm) and store for future purification and characterization.")
    
    # Step 2: Optional titering of lysates by making eightfold dilution series
    protocol.comment('Performing eightfold dilution series for titering.')
    
    # Add 180 µL SM-buffer to columns 2-9 in well plate 6
    p300.pick_up_tip()
    for col in range(1, 9):
        for well in well_plate_6.columns()[col]:
            p300.aspirate(180, sm_buffer)
            p300.dispense(180, well)
    p300.drop_tip()
    
    # Transfer 20 µL from column 1 to column 2, mix and repeat for columns 3-9
    p300.pick_up_tip()
    for row in well_plate_6.rows():
        p300.aspirate(20, row[0])
        p300.dispense(20, row[1])
        p300.mix(3, 20, row[1])
        for col in range(1, 8):
            p300.aspirate(20, row[col])
            p300.dispense(20, row[col+1])
            p300.mix(3, 20, row[col+1])
    p300.drop_tip()
    
    protocol.pause("Spot the dilution series on soft-agar overlay plates with a 96-pin replicator or multichannel pipette and incubate overnight. Next day, count plaques or clearing zones for approximate titer. If single plaques are present, perform DPS of single plaques and collect clearing zone for phage storage. If not, plate lysate dilution to get 10-50 plaques for further processing.")
    
    protocol.comment("Protocol complete.")

# Run the protocol
run(protocol_api.ProtocolContext())
