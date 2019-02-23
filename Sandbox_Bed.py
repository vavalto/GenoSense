from pybedtools import BedTool
import numpy as np
import os

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
        range_tuple = [int(values[1]), int(values[2])]
        range_tuple_list.append(range_tuple)
        if chromosome in bed_dict:
            bed_dict[chromosome].append(range_tuple)
        else:
            bed_dict.update({chromosome: range_tuple_list})
    return bed_dict

def intersect_bed(bed_dict1, bed_dict2):
    for chrom1, frag_range1 in bed_dict1.items():
        for chrom2, frag_range2 in bed_dict2.items():
            for frag1 in frag_range1:
                for frag2 in frag_range2:
                    print(frag1)
                    print(frag2)
                    intersect = set(frag1).intersection(frag2)
                    print(intersect)

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

intersect_bed(BED_file_dict_1, BED_file_dict_2)


# a = [[0, 2], [5, 10], [13, 23], [24, 25]]
# b = [[1, 5], [8, 12], [15, 18], [20, 24]]
#
# def get_intersection(x, y):
#     x_spread = [item for sublist in [list(range(l[0],l[1]+1)) for l in x] for item in sublist]
#     y_spread = [item for sublist in [list(range(l[0],l[1]+1)) for l in y] for item in sublist]
#     print(x_spread)
#     print(y_spread)
#     flat_intersect_list = list(set(x_spread).intersection(y_spread))
#     print(flat_intersect_list)
#
# get_intersection(a, b)

#def overlap_constrain(file_list, min_overlap==100, n==3, k==2)

#sect_file = REP1.intersect(REP2)
#print(sect_file)

# Handling the n==# module
#n = 2
#num_of_files = range(0, len(file_list))
#combo_files = pd.Series(list(it.combinations(np.unique(num_of_files),n)))
#print(combo_files)

# Handling the min_overlap
#for item in sect_file:
#    if abs(len(item)) >= 100:
#        print(item.chrom, item.start, item.end, len(item))
