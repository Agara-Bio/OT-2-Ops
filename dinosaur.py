# Used to get arguments from user for non-coding modification of protocol
#def get_values(*names):
#            import json
#            _all_values = json.loads("""{"p300_mount":"right","tip_type":"opentrons_96_tiprack_300ul","plate_type":"corning_96_wellplate_360ul_flat","protocol_filename":"dinosaur"}""")
#            return [_all_values[n] for n in names]

import opentrons

metadata = {
    "protocolName": "Dinosaur",
    "author": "Rishi Wahi <>",
    "description": "Draw a picture of a dinosaur",
    "apiLevel": "2.9",
}

def run(ctx):
    magnetic_module = ctx.load_module(module_name="magnetic module gen2", location=4)
    thermocycler_module = ctx.load_module(module_name="thermocycler module")
    [p20_mount, tip_type, plate_type] = ["left", "opentrons_96_tiprack_20ul", "corning_96_wellplate_360ul_flat"]
    tiprack = ctx.load_labware(tip_type, 1)
    plate = ctx.load_labware(plate_type, 3)
    tuberack = ctx.load_labware("opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap", 2)
    p20 = ctx.load_instrument("p20_single_gen2", p20_mount, tip_racks=[tiprack])
    green = tuberack["A2"]
    blue = tuberack["B2"]
    green_wells = list(
        plate.wells(
            "E1",
            "D2",
            "E2",
            "D3",
            "E3",
            "F3",
            "G3",
            "H3",
            "C4",
            "D4",
            "E4",
            "F4",
            "G4",
            "H4",
            "C5",
            "D5",
            "E5",
            "F5",
            "G5",
            "C6",
            "D6",
            "E6",
            "F6",
            "G6",
            "C7",
            "D7",
            "E7",
            "F7",
            "G7",
            "D8",
            "E8",
            "F8",
            "G8",
            "H8",
            "E9",
            "F9",
            "G9",
            "H9",
            "F10",
            "G11",
            "H12",
        )
    )
    blue_wells = list(
        plate.wells("C3", "B4", "A5", "B5", "B6", "A7", "B7", "C8", "C9", "D9", "E10", "E11", "F11", "G12")
    )
    p20.distribute(20, green, green_wells, disposal_vol=0, blow_out=True)
    p20.distribute(20, blue, blue_wells, disposal_vol=0, blow_out=True)
