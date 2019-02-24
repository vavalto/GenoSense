from src.utils import log_creator


class Chromosome(object):
    def __init__(self,
                 configuration_dict=None,
                 designator=None,
                 sequences=None):
        self.configuration_dict = configuration_dict
        self.logger = None
        self.designator = designator
        self.sequences = sequences
        self.position_start = 0
        self.position_end = None
        self.create_logger()

    def create_logger(self):
        self.logger = log_creator.create_logger(name=self.designator,
                                                logging_configuration=self.configuration_dict)
