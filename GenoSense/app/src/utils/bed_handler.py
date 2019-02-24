import multiprocessing
import threading
import time
import pprint

from src.utils import log_creator
from src.utils import chromosome


class BED_Handler(object):  #(multiprocessing.Process):
    def __init__(self,
                 file_path=None,
                 file_name=None,
                 configuration_dict=None):
                 # message_q=None):
        # multiprocessing.Process.__init__(self)
        self.file_path = file_path
        # print(f'bed handler file path: {self.file_path}')
        self.file_name = file_name
        self.configuration_dict = configuration_dict
        self.logger = None
        self.create_logger()

        # self.message_q = message_q
        self.lines = None
        self.chromo_dict = None
        self.converted_chromo_dict = {}
        self.largest_chromo_end = 0

        #  start up functions
        self.logger.info(f'BED Handler using file: {self.file_name} at {self.file_path}')
        self.get_file_lines()
        self.get_file_chromo_dict()
        # self.monitor_q_thread = None
        # self.commands = {'test': self.test}

    # def run(self):
    #     print('bed manipulator started')
    #     self.monitor_q_thread = threading.Thread(target=self.monitor_message_q)
    #     self.monitor_q_thread.start()

    def create_logger(self):
        self.logger = log_creator.create_logger(name=self.file_name,
                                                logging_configuration=self.configuration_dict)

    @staticmethod
    def convert_range(old_value=None,
                      old_max=None,
                      old_min=None,
                      new_max=None,
                      new_min=None):
        old_range = (old_max - old_min)
        new_range = (new_max - new_min)
        new_value = (((old_value - old_min) * new_range) / old_range) + new_min
        return new_value

    def find_largest_chromo_end(self, chromo=None):
        for chromo in self.chromo_dict:
            chromo_sequences = self.chromo_dict[chromo]
            chromo_end = chromo_sequences[-1][1]
            if chromo_end < self.largest_chromo_end:
                self.largest_chromo_end = chromo_end

    def convert_chromo_dict(self):
        chromo_end = 248586827
        for chromo in self.chromo_dict:
            chromo_sequences = self.chromo_dict[chromo]
            # chromo_end = chromo_sequences[-1][1]

            # if chromo_end < self.largest_chromo_end:
            #     self.largest_chromo_end = chromo_end
            converted_sequences = []
            for sequence in chromo_sequences:
                converted_start = self.convert_range(old_value=sequence[0],
                                                     old_max=chromo_end,
                                                     old_min=0,
                                                     new_max=1000,
                                                     new_min=0)
                converted_end = self.convert_range(old_value=sequence[1],
                                                   old_max=chromo_end,
                                                   old_min=0,
                                                   new_max=1000,
                                                   new_min=0)
                converted_sequences.append((converted_start, converted_end))
            self.converted_chromo_dict.update({chromo: converted_sequences})

    def get_file_lines(self):
        with open(f'{self.file_path}', 'r') as file:
            lines = file.readlines()
        self.lines = lines

    def get_file_range_set(self):
        file_range_set = set()
        for line in self.lines:
            values = line.split()
            value_range = range(int(values[1]), int(values[2]))
            file_range_set.add(value_range)
        return file_range_set

    def get_file_chromo_dict(self):
        chromo_dict = {}
        for line in self.lines:
            range_tuple_list = []
            values = line.split()
            # print(f'values: {values}')
            chromosome = values[0]
            range_tuple = (int(values[1]), int(values[2]))
            range_tuple_list.append(range_tuple)
            if chromosome in chromo_dict:
                chromo_dict[chromosome].append(range_tuple)
            else:
                chromo_dict.update({chromosome: range_tuple_list})
        self.chromo_dict = chromo_dict
        self.logger.debug(f'chromo dict: {pprint.pformat(chromo_dict)}')

    # def monitor_message_q(self):
    #     while not self.message_q.empty():
    #         message = self.message_q.get()
    #         print(message)
    #         self.commands[message]()
    #     time.sleep(0.1)















