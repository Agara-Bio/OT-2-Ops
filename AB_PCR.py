# Used to get arguments from user for non-coding modification of protocol
# def get_values(*names):
#    import json
#    _all_values = json.loads("""{"number_of_samples":96,"dna_volume":1,"mastermix_volume":24,"master_mix_csv":"Reagent,Well,Volume\\nBuffer,A2,3\\nMgCl,A3,40\\ndNTPs,A2,90\\nWater,A3,248\\nprimer 1,A4,25\\nprimer 2,A5,25\\n","tuberack_type":"opentrons_24_aluminumblock_nest_1.5ml_screwcap","single_channel_type":"p1000_single_gen2","single_channel_mount":"right","pipette_2_type":"p1000_single_gen2","pipette_2_mount":"left","lid_temp":105,"init_temp":96,"init_time":30,"d_temp":96,"d_time":15,"a_temp":60,"a_time":30,"e_temp":74,"e_time":30,"num_cycles":30,"fe_temp":74,"fe_time":30,"final_temp":4}""")
#    return [_all_values[n] for n in names]


import math, opentrons

# metadata
metadata = {
    'protocolName': 'Complete PCR Workflow with Thermocycler',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.0'
}


def run(ctx):

    [number_of_samples, dna_volume, mastermix_volume, master_mix_csv,
     tuberack_type, pipette_1_type, pipette_1_mount,
     pipette_2_type, pipette_2_mount, lid_temp, init_temp, init_time, d_temp,
     d_time, a_temp, a_time, e_temp, e_time, num_cycles, fe_temp, fe_time,
     final_temp] =[
        '8', '1', '500', 'master_mix_csv',
        'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap', 'p20_single_gen2',
        'left', 'p300_single_gen2', 'right',
        'lid_temp', 'init_temp', 'init_time', 'd_temp', 'd_time', 'a_temp',
        'a_time', 'e_temp', 'e_time', '15', 'fe_temp', 'fe_time',
        'final_temp']
    
    #pipette Setup
    tipracks1 = ctx.load_labware('opentrons_96_tiprack_20_ul', 6)
    p1 = ctx.load_instrument(pipette_1_type, pipette_1_mount, tip_racks=tipracks1)
    tipracks2 = ctx.load_labware('opentrons_96_tiprack_300_ul', 3)
    p2 = ctx.load_instrument(pipette_2_type, pipette_2_mount, tip_racks=tipracks2)

    # labware setup
    magnetic_module = ctx.load_module(module_name="magnetic module gen2", location=4)
    tc = ctx.load_module('thermocycler')
    tc_plate = tc.load_labware('nest_96_wellplate_100ul_pcr_full_skirt', 'thermocycler plate')
    if tc.lid_position != 'open':
        tc.open_lid()
    tc.set_lid_temperature(lid_temp)
    tuberack = ctx.load_labware(tuberack_type, '1', 'rack for mastermix reagents')
    dna_plate = ctx.load_labware('nest_96_wellplate_360ul_flat', '5', 'DNA plate')
    mix_rack = ctx.load_labware("opentrons_15_tuberack_falcon_15ml_conical",2,'mastermix_rack')

    # reagent setup
    mm_tube = tuberack.wells()[0]
    num_cols = math.ceil(number_of_samples/8)

    #pipette overruns
    pip_counts = {p1: 0, p2: 0}
    p1_max = len(tipracks1)*96
    p2_max = len(tipracks2)*96
    pip_maxs = {p1: p1_max, p2: p2_max}

    def pick_up(pip):
        if pip_counts[pip] == pip_maxs[pip]:
            ctx.pause('Replace empty tipracks before resuming.')
            pip.reset_tipracks()
            pip_counts[pip] = 0
        pip.pick_up_tip()
        pip_counts[pip] += 1

    # determine which pipette has the smaller volume range
    #if int(range1) <= int(range2):
    pip_s, pip_l = p1, p2
    #else:
    #    pip_s, pip_l = p2, p1

    # destination
    mastermix_dest = tuberack.wells()[0]

    info_list = [
        [cell.strip() for cell in line.split(',')]
        for line in master_mix_csv.splitlines()[1:] if line
    ]

    """ create mastermix """
    for line in info_list[1:]:
        source = tuberack.wells(line[1].upper())
        vol = float(line[2])
        pip = pip_s if vol <= pip_s.max_volume else pip_l
        pick_up(pip)
        pip.transfer(vol, source, mastermix_dest, new_tip='never')
        pip.drop_tip()

    """ distribute mastermix and transfer sample """
    if tc.lid_position != 'open':
        tc.open_lid()
    
    mm_source = mm_tube
    mm_dests = tc_plate.wells()[:number_of_samples]
    pip_mm = pip_s if mastermix_volume <= pip_s.max_volume else pip_l

    for d in mm_dests:
        pick_up(pip_mm)
        pip_mm.transfer(mastermix_volume, mm_source, d, new_tip='never')
        pip_mm.drop_tip()

    # transfer DNA to corresponding well
    dna_sources = dna_plate.wells()[:number_of_samples]
    dna_dests = tc_plate.wells()[:number_of_samples]
    pip_dna = pip_s if dna_volume <= pip_s.max_volume else pip_l

    for s, d in zip(dna_sources, dna_dests):
        pick_up(pip_dna)
        pip_dna.transfer(
            dna_volume, s, d, mix_after=(5, 0.8*mastermix_volume + dna_volume),
            new_tip='never')
        pip_dna.drop_tip()

    """ run PCR profile on thermocycler """

    # Close lid
    if tc.lid_position != 'closed':
        tc.close_lid()

    # lid temperature set
    tc.set_lid_temperature(lid_temp)

    # initialization
    well_vol = mastermix_volume + dna_volume
    tc.set_block_temperature(
        init_temp, hold_time_seconds=init_time, block_max_volume=well_vol)

    # run profile
    profile = [
        {'temperature': d_temp, 'hold_time_seconds': d_time},
        {'temperature': a_temp, 'hold_time_seconds': a_temp},
        {'temperature': e_temp, 'hold_time_seconds': e_time}
    ]

    tc.execute_profile(
        steps=profile, repetitions=num_cycles, block_max_volume=well_vol)

    # final elongation
    tc.set_block_temperature(
        fe_temp, hold_time_seconds=fe_time, block_max_volume=well_vol)

    # final hold
    tc.deactivate_lid()
    tc.set_block_temperature(final_temp)
