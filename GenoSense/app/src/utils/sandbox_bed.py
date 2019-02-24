# from pybedtools import BedTool
import numpy as np
import os
from functools import reduce
# import timeit
# from multiprocessing import Pool
import pickle

result_list = []
def log_result(result):
    # This is called whenever foo_pool(i) returns a result.
    # result_list is modified only by the main process, not the pool workers.
    result_list.append(result)

def run_intersect(file_list, overlap_min=1, gap_min=0, multi_bed=2, multi_frag=3):

    # File 1
    BED_file_lines_1 = get_file_lines(abs_file_name=file_list[0])
    BED_file_dict_1 = get_file_bed_dict(lines=BED_file_lines_1)
    # File 2
    BED_file_lines_2 = get_file_lines(abs_file_name=file_list[1])
    BED_file_dict_2 = get_file_bed_dict(lines=BED_file_lines_2)
    sect_bed = intersect_bed(BED_file_dict_1, BED_file_dict_2, overlap_min, gap_min)
    return sect_bed

def get_file_lines(abs_file_name=None):
    with open(abs_file_name,'r') as file:
        lines = file.readlines()
    return lines


def get_file_range_set(lines=None):
    file_range_set = set()
    for line in lines:
        values = line.split()
        value_range = range(int(values[1]), int(values[2]))
        file_range_set.add(value_range)
    return file_range_set


def get_file_bed_dict(lines=None):
    bed_dict = {}
    for line in lines:
        range_tuple_list = []
        values = line.split()
        #print(values)
        chromosome = values[0]
        range_tuple = (int(values[1]), int(values[2]))
        range_tuple_list.append(range_tuple)
        if chromosome in bed_dict:
            bed_dict[chromosome].append(range_tuple)
        else:
            bed_dict.update({chromosome: range_tuple_list})
    return bed_dict

def intersect_bed(bed_dict1, bed_dict2, overlap_min, gap_min):
    '''
    Compares BED dictionaries given a overlap minnimum and gap minnimum

    Input Arguments:
        bed_dict1: dictionary of bed file created by get_file_bed_dict
        bed_dict2: dictionary of bed file created by get_file_bed_dict

    Output Arguments:
        bed_dict:
            {'chromosome:'
                {'Unique ID for intersections':
                    list(
                            {'grand_parent': (start, end)}
                            {'parent':       (start, end)}
                            {'intersect':    (start, end)}
                            {'length':       value}
                        )
                }
            }
    '''
    # Intialize bed_dict
    bed_dict = {}
    # Intialize unique intersect ID
    intersect_loop = 0
    for chrom1, frag_range1 in bed_dict1.items():
        if chrom1 in bed_dict1:
            frag_range2 = bed_dict2[chrom1]
            # For each single interval fragment range
            for frag1 in frag_range1:
                min_frag1 = frag1[0] + gap_min
                max_frag1 = frag1[1] + gap_min# Adding one for inclusive intersection
                if overlap_min >= (max_frag1-min_frag1):
                    continue
                # For each single interval fragment range
                for frag2 in frag_range2:
                    range_tuple_list = []
                    max_frag2 = frag2[1] + gap_min # Adding one for inclusive intersection
                    min_frag2 = frag2[0] + gap_min
                    if max_frag1 <= min_frag1:
                        continue
                    # Find intersection of fragment intervals
                    intersect = intersect_min_max(min_frag1, max_frag1, min_frag2, max_frag2)
                    # If there is any intersections
                    if intersect and overlap_min >= 1:
                        # Increment unique ID
                        intersect_loop = intersect_loop + 1
                        # Create intersection interval
                        range_tuple = (intersect)
                        # Find the length of the intersection
                        #len_intersect = len_intersect_limit(range_tuple, overlap_min)
                        # Create "grandparent" fragment of intersection
                        gp_dict = {'grand_parent': (frag2[0], frag2[1])}
                        # Create "parent" fragment of intersection
                        parent_dict = {'parent': (frag1[0], frag1[1])}
                        intersect_dict = {'intersect': range_tuple}
                        # Save length of interval
                        #length_dict = {'length': len_intersect}
                        range_tuple_list.append(gp_dict)
                        range_tuple_list.append(parent_dict)
                        range_tuple_list.append(intersect_dict)
                        #range_tuple_list.append(length_dict)
                        # If chromosone is already in the output
                        if chrom1 in bed_dict:
                            bed_dict[chrom1].update({intersect_loop: range_tuple_list})
                        else:
                            # Intialize output
                            bed_dict.update({chrom1: {intersect_loop: range_tuple_list}})
                    else:
                        continue
    return bed_dict

def intersect_min_max(min_frag1, max_frag1, min_frag2, max_frag2):
    # Intialize to empty
    inter_sect = []
    bool_left = (min_frag1 <= min_frag2 and min_frag1 <= max_frag2
                    and max_frag1 >= min_frag2)
    bool_right = (min_frag1 >= min_frag2 and min_frag1 >= max_frag2
                    and max_frag1 >= max_frag2)
    bool_swap_right = (min_frag1 <= max_frag2 and max_frag1 >= min_frag2
                    and max_frag2 <= max_frag1)
    #bool_inside = (min_frag1 <= min_frag2 and max_frag1 <= max_frag2)
    #bool_swap_inside = (min_frag2 <= min_frag1 and max_frag2 <= max_frag1)
    # print(bool_inside)
    # print(bool_swap_inside)
    if bool_left:
        inter_sect = [min_frag2, max_frag1]
    if bool_right:
        inter_sect = [min_frag1, max_frag2]
    if bool_swap_right:
        inter_sect = [min_frag1, max_frag2]
    # if bool_inside:
    #     inter_sect = [min_frag1, max_frag1]
    # if bool_swap_inside:
    #     inter_sect = [min_frag2, max_frag2]
    return inter_sect

def len_intersect_limit(frag_intersect, overlap_min=100):
    '''
    If the length of the interval exists, else return zero

    Input Arguments:
        frag_intersect: fragment intersection

    Output Arguments:
        lenfth of intersection
        boolean
    '''
    len_sect = np.abs(np.subtract(frag_intersect[0], frag_intersect[1]))
    if len_sect >= overlap_min:
        return len_sect
    else:
        return 0

def save_obj(item, name ):
    with open(name + '.pkl', 'wb') as f:
        pickle.dump(item, f, pickle.HIGHEST_PROTOCOL)

if __name__ == "__main__":
    parent_dir = os.getcwd()
    BED_file_directory = os.path.join(parent_dir)

    Ex1 = os.path.join(BED_file_directory, 'Example1.bed');
    Ex2 = os.path.join(BED_file_directory, 'Example2.bed');
    Ex3 = os.path.join(BED_file_directory, 'Example3.bed');

    REP1 = os.path.join(BED_file_directory, 'iCellNeuron_HTTLOC_CAPCxHTT_REP1.bed')
    REP3 = os.path.join(BED_file_directory, 'iCellNeuron_HTTLOC_CAPCxHTT_REP3.bed')

    # Example input list of files
    file_list = [];
    file_list.append(REP1);
    #file_list.append(REP2);
    file_list.append(REP3);
    # file_list.append(Ex1);
    # file_list.append(Ex2);
    import cProfile
    import time
    #run_intersect(file_list, 50, 0, multi_bed=2, multi_frag=3)
    cProfile.run('run_intersect(file_list, 50, 0, multi_bed=2, multi_frag=3)')

    currtime = time.time()
    # po = Pool()
    # po.apply_async(run_intersect, args=file_list, callback = log_result)
    #inter_dict = run_intersect(file_list, 100, 0, multi_bed=2, multi_frag=3)
    #save_obj(inter_dict, 'intersect_overlap100_gap0')
    print('2: parallel: time elapsed:', time.time() - currtime)
    #print(inter_dict)
    file_list.append(Ex1);
    file_list.append(Ex1);
    #file_list.append(Ex3);

    sect_bed = run_intersect(file_list, 50, 0, multi_bed=2, multi_frag=3)
    print(sect_bed)
