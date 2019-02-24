from pybedtools import BedTool
import numpy as np
import os
from functools import reduce
import timeit


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
                # For each single interval fragment range
                for frag2 in frag_range2:
                    range_tuple_list = []
                    min_frag1 = frag1[0] + gap_min
                    min_frag2 = frag2[0] + gap_min
                    max_frag1 = frag1[1] + gap_min + 1 # Adding one for inclusive intersection
                    max_frag2 = frag2[1] + gap_min + 1 # Adding one for inclusive intersection
                    # Find intersection of fragment intervals
                    intersect = np.intersect1d(range(min_frag1, max_frag1), range(min_frag2, max_frag2))
                    # If there is any intersections
                    if intersect.any() and overlap_min >= 1:
                        # Increment unique ID
                        intersect_loop = intersect_loop + 1
                        # Create intersection interval
                        range_tuple = (min(intersect), max(intersect))
                        # Find the length of the intersection
                        len_intersect = len_intersect_limit(range_tuple, overlap_min)
                        # Create "grandparent" fragment of intersection
                        gp_dict = {'grand_parent': (frag2[0], frag2[1]+1)}
                        # Create "parent" fragment of intersection
                        parent_dict = {'parent': (frag1[0], frag1[1]+1)}
                        intersect_dict = {'intersect': range_tuple}
                        # Save length of interval
                        length_dict = {'length': len_intersect}
                        range_tuple_list.append(gp_dict)
                        range_tuple_list.append(parent_dict)
                        range_tuple_list.append(intersect_dict)
                        range_tuple_list.append(length_dict)
                        # If chromosone is already in the output
                        if chrom1 in bed_dict:
                            bed_dict[chrom1].update({intersect_loop: range_tuple_list})
                        else:
                            # Intialize output
                            bed_dict.update({chrom1: {intersect_loop: range_tuple_list}})
    return bed_dict


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


parent_dir = os.getcwd()
BED_file_directory = os.path.join(parent_dir)

Ex1 = os.path.join(BED_file_directory, 'Example1.bed')
Ex2 = os.path.join(BED_file_directory, 'Example2.bed')
Ex3 = os.path.join(BED_file_directory, 'Example3.bed')

REP1 = os.path.join(BED_file_directory, 'iCellNeuron_HTTLOC_CAPCxHTT_REP1.bed')
REP2 = os.path.join(BED_file_directory, 'iCellNeuron_HTTLOC_CAPCxHTT_REP2.bed')

# Example input list of files
file_list = []
file_list.append(Ex1)
file_list.append(Ex2)
#file_list.append(Ex3)


#sect_bed = run_intersect(file_list, 50, 0, multi_bed=2, multi_frag=3)
#print(sect_bed)

class Bed_File:
    def __init__(self, filelist):
        self.filelist = filelist
        total_files_dict = {}
        for single_files in filelist:
            genome = Genome(single_files)
            total_files_dict.update({single_files:genome})
        self.total_files_dict = total_files_dict
   
class Genome:
    def __init__(self, bed_dict):
        self.bed_list = get_file_lines(bed_dict)
        self.bed_dict = get_file_bed_dict(self.bed_list)

class Chromosome:
    def __init__(self, genome_dict):
        self.chromo_num = chromo_num

class Chromo_Range:
    def __init__(self, overlap_min, gap_min, range_of_chromo=(), intersections={}):
        self.overlap_min = overlap_min
        self.gap_min = gap_min
        self.range_of_chromo = range_of_chromo
        self.intersections = intersections

        start = range_of_chromo[0]
        end = range_of_chromo[1]
        
        self.start = start
        self.end = end




test_class_Bed_File = Bed_File(file_list)

print(test_class_Bed_File.total_files_dict)