from pybedtools import BedTool
import numpy as np
import os
from functools import reduce
import timeit

#REP1 = 'iCellNeuron_HTTLOC_CAPCxHTT_REP1.bed';
#REP2 = 'iCellNeuron_HTTLOC_CAPCxHTT_REP2.bed';
#REP3 = 'iCellNeuron_HTTLOC_CAPCxHTT_REP3.bed';

Ex1 = 'Example1.bed';
Ex2 = 'Example2.bed';
Ex3 = 'Example3.bed';

# Example input list of files
file_list = [];
file_list.append(Ex1);
file_list.append(Ex2);
file_list.append(Ex3);
#print(file_list)
#file_list.append(REP3);


def get_file_lines(file_directory=None, file_name=None):
    abs_file = os.path.join(file_directory, file_name)
    with open(abs_file,'r') as file:
        lines = file.readlines()
        #print(lines)
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

def intersect_bed(bed_dict1, bed_dict2):
    # TODO: Make sure on the same chromosome
    bed_dict = {}
    for chrom1, frag_range1 in bed_dict1.items():
        for chrom2, frag_range2 in bed_dict2.items():
            if chrom1 == chrom2:
                for frag1 in frag_range1:
                    for frag2 in frag_range2:
                        range_tuple_list = []
                        intersect = np.intersect1d(range(frag1[0], frag1[1]+1), range(frag2[0], frag2[1]+1))
                        if intersect.any():
                            range_tuple = (min(intersect), max(intersect))
                            range_tuple_list.append(range_tuple)
                            if chrom1 in bed_dict:
                                bed_dict[chrom1].append(range_tuple)
                            else:
                                bed_dict.update({chrom1: range_tuple_list})
    print('Intersect:')
    print(bed_dict)
    return bed_dict

def len_intersect_limit(intersect_bed, overlap_min=100):
    for chrom1, frag_intersect in intersect_bed.items():
        for frag in frag_intersect:
            len_sect = np.abs(np.subtract(frag[0], frag[1]))
            if len_sect >= overlap_min:
                print(len_sect)


parent_dir = os.getcwd()
BED_file_directory = os.path.join(parent_dir)
#print(BED_file_directory)

# File 1
BED_file_lines_1 = get_file_lines(file_directory=BED_file_directory,
                                  file_name=file_list[0])

BED_file_dict_1 = get_file_bed_dict(lines=BED_file_lines_1)
print(BED_file_dict_1)

# File 2
BED_file_lines_2 = get_file_lines(file_directory=BED_file_directory,
                                  file_name=file_list[1])

BED_file_dict_2 = get_file_bed_dict(lines=BED_file_lines_2)
print(BED_file_dict_2)

# File 3
BED_file_lines_3 = get_file_lines(file_directory=BED_file_directory,
                                  file_name=file_list[2])

BED_file_dict_3 = get_file_bed_dict(lines=BED_file_lines_3)
print(BED_file_dict_3)

sect_bed = intersect_bed(BED_file_dict_1, BED_file_dict_2)
len_intersect_limit(sect_bed, 50)
