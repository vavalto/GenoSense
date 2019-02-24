import json
import multiprocessing
import pprint

from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter.filedialog import askopenfilename

from src.utils import log_creator
from src.utils import bed_handler
from src.utils import sandbox_bed


class Manager(object):
    def __init__(self):
        self.configuration_file = r'./config/configuration.json'
        self.configuration_dict = None
        self.logger = None
        self.ui = None
        self.ui_height = None
        self.ui_width = None

        #  ui widgets
        self.selection_frame = None
        # self.start_here_label = None
        # self.move_forward_1 = None
        self.add_files_button = None
        self.add_files_image = None
        self.move_forward_2 = None
        self.select_files_label = None
        self.select_files_image = None
        self.move_forward_3 = None
        self.display_files_button = None
        self.display_files_image = None
        self.move_forward_4 = None
        self.analyze_files_button = None
        self.analyze_files_image = None

        self.file_listbox = None

        self.canvas_frame = None
        self.display_canvas = None
        self.canvas_scrollbar = None
        self.display_bar_height = 15
        self.display_bar_colors = []

        self.bed_file_list = []
        self.bed_handlers = {}
        self.currently_selected_files = None
        self.pre_logger_messages = []
        self.pre_logger_messages.append('manager called')

        #  startup functions
        self.read_config_file()
        self.create_logger()
        self.create_ui()
        self.start_ui()

    def read_config_file(self):
        with open(self.configuration_file, 'r') as config_file:
            config_json = config_file.read()
            config_dict = json.loads(config_json)
        self.configuration_dict = config_dict
        self.pre_logger_messages.append('manager read configuration file')

    def create_logger(self):
        self.logger = log_creator.create_logger(name='manager',
                                                logging_configuration=self.configuration_dict)
        for message in self.pre_logger_messages:
            self.logger.info(message)

    def create_ui(self):
        self.ui = Tk()
        self.ui_height = self.ui.winfo_screenheight()
        self.ui_width = self.ui.winfo_screenwidth()
        self.logger.info(f'screen width: {self.ui_width}, screen height: {self.ui_height}')

        self.ui.title('GenoSense')
        root_img = PhotoImage(file=r'./images/GenoSense.png')
        self.ui.tk.call('wm', 'iconphoto', self.ui._w, root_img)

        #  button frame and child widgets
        self.selection_frame = Frame(self.ui)
        self.selection_frame.grid(column=0, row=0)

        # self.start_here_label = Label(self.selection_frame,
        #                               text='Start Here')
        # self.start_here_label.grid(column=0, row=0)
        #
        # self.move_forward_1 = Label(self.selection_frame,
        #                             text='>>')
        # self.move_forward_1.grid(column=1, row=0)

        self.add_files_image = PhotoImage(file=r'./images/add-files.png')
        self.add_files_button = Button(self.selection_frame,
                                       text='Add Files',
                                       command=lambda: self.add_files())
        self.add_files_button.config(image=self.add_files_image)
        self.add_files_button.grid(column=2, row=0)

        self.move_forward_2 = Label(self.selection_frame,
                                    text='>>')
        self.move_forward_2.grid(column=3, row=0)

        self.select_files_image = PhotoImage(file=r'./images/select.png')
        self.select_files_label = Label(self.selection_frame,
                                        text='Select Files Below')
        self.select_files_label.config(image=self.select_files_image)
        self.select_files_label.grid(column=4, row=0)

        self.move_forward_3 = Label(self.selection_frame,
                                    text='>>')
        self.move_forward_3.grid(column=5, row=0)

        self.display_files_image = PhotoImage(file=r'./images/display.png')
        self.display_files_button = Button(self.selection_frame,
                                           text='Display Selected Files',
                                           command=lambda: self.display_selected_files())
        self.display_files_button.config(image=self.display_files_image)
        self.display_files_button.grid(column=6, row=0)

        self.move_forward_4 = Label(self.selection_frame,
                                    text='>>')
        self.move_forward_4.grid(column=7, row=0)

        self.analyze_files_image = PhotoImage(file=r'./images/analyze.png')
        self.analyze_files_button = Button(self.selection_frame,
                                           text='Analyze Selected Files',
                                           command=lambda: self.analyze_selected_files())
        self.analyze_files_button.config(image=self.analyze_files_image)
        self.analyze_files_button.grid(column=8, row=0)

        self.file_listbox = Listbox(self.selection_frame, width=50, height=32, selectmode=MULTIPLE)
        self.file_listbox.grid(column=4, row=1)
        self.ui.update()

        self.canvas_frame = Frame(self.selection_frame)
        self.canvas_frame.grid(column=6, row=1, columnspan=3)

        self.display_canvas = Canvas(self.canvas_frame,
                                     height=self.file_listbox.winfo_height(),
                                     width=1000,
                                     bg='white')
                                     # scrollregion=(0, 0, 1000, 1000))
        self.display_canvas.grid(column=0, row=0)

        # self.canvas_scrollbar = Scrollbar(self.canvas_frame,
        #                                   orient=HORIZONTAL)
        # self.canvas_scrollbar.grid(column=0, row=1, columnspan=3)
        # self.canvas_scrollbar.config(command=self.display_canvas.xview)

    def start_ui(self):
        self.ui.state('zoomed')
        self.ui.mainloop()

    def add_files(self):
        file_name = askopenfilename(initialdir=r'../BED_files',
                                    filetypes=(('BED File', '*.bed'), ('All Files', '*.*')),
                                    title='Choose a file.')
        if file_name not in self.bed_file_list:
            if file_name:
                self.bed_file_list.append(file_name)
                file_directory_path_breakdown = file_name.split(r'/')
                self.file_listbox.insert(END, file_directory_path_breakdown[-1])
            else:
                messagebox.showwarning('Duplicate File',
                                       'This file has already been selected. Please select another file.')

    def display_selected_files(self):
        self.create_bed_handlers()
        start_height = 0
        for bed_handler in self.bed_handlers:
            handler = self.bed_handlers[bed_handler]
            handler.convert_chromo_dict()
            for sequence in handler.converted_chromo_dict['chr1']:
                #  canvas.create_rectangle(x1, y1, x2, y2)
                self.display_canvas.create_rectangle(sequence[0],               #  x1
                                                     start_height,              #  y1
                                                     sequence[1],               #  x2
                                                     start_height + self.display_bar_height,
                                                     fill='black')              #  y2
            start_height += self.display_bar_height + 2

    def create_bed_handlers(self):
        # self.file_listbox.curselection() provides a tuple of indexes for the selected items.
        self.currently_selected_files = self.file_listbox.curselection()
        if self.currently_selected_files:
            self.logger.debug(f'currently selected file indexes in listbox: {self.currently_selected_files}')
            for index in self.currently_selected_files:
                if index not in self.bed_handlers:
                    file_path = self.bed_file_list[index]
                    file_name = file_path.split(r'/')[-1]
                    handler = bed_handler.BED_Handler(file_path=file_path,
                                                      file_name=file_name,
                                                      configuration_dict=self.configuration_dict)
                    self.bed_handlers.update({index: handler})
            self.logger.debug(f'bed handlers that exist: {self.bed_handlers}')

    def analyze_selected_files(self):
        bed_1_chromo = self.bed_handlers[0].chromo_dict
        # print(f'bed_1_chromo: {bed_1_chromo}')

        bed_2_chromo = self.bed_handlers[1].chromo_dict
        # print(f'bed_2_chromo: {bed_2_chromo}')
        # chromo_1 = self.bed_handlers['chr1']
        combo_magic_dict = sandbox_bed.intersect_bed(bed_1_chromo, bed_2_chromo, 1, 0)
        # print(f'combo_magic_dict: {combo_magic_dict}')

        gp_values = []
        p_values = []
        intersect_values = []
        for sequence_id in combo_magic_dict:
            list_of_dicts = combo_magic_dict[sequence_id]
            for dictionary in list_of_dicts:
                things = list_of_dicts[dictionary]
                for something in things:
                    if 'grand_parent' in something:
                        # print('yay')
                        value = something['grand_parent']
                        gp_values.append(value)
                    elif 'parent' in something:
                        value = something['parent']
                        p_values.append(value)
                    elif 'intersect' in something:
                        value = something['intersect']
                        intersect_values.append(value)

        # for value in gp_values:
        #     bed_handler.convert_range(old_value=)






