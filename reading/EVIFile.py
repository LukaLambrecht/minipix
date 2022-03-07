# Tools for reading XCounter EVI files into numpy arrays for plotting and processing
# Originally based on here: https://github.com/wangzhentian/EVI_reader/blob/master/EVIFile.py

# imports
import os
import sys
import numpy as np
import matplotlib.pyplot as plt

class EVIFile():
    ### Class for handling XCounter EVI file format 
    # note: follows the naming convention of the ImageJ Java plugin
    
    # initializations
    headers = {} # dictionary for EVI headers
    data = [] # image data
    width = 0 # width of one image in number of pixels
    height = 0 # height in one image in number of pixels
    nimages = 0 # number of frames
    intelByteOrder = True
    tds = False
    tdsTruncate = False
    TE = True 
    TC = 1
    numberOfBoards = 1
    numberOfRows = 1
    sequenceHeaderBytes = 0 # number of bytes reserved for the file header (including first frame header)
    frameHeaderBytes = 0 # number of bytes reserved for the header for each frame
    is32bit = False # data format (32-bit or 16-bit unsigned integers)

    def __init__(self, filename=None):
        ### initiate with a filename
        if filename is None: pass
        else: self.read(filename)

    def read(self, filename):
        ### read an EVI file
        
        # check file
        if not os.path.exists(filename):
            msg = 'ERROR in EVIFile.read: file {} does not exist.'.format(filename)
            print(msg)
            return
        fileextension = os.path.splitext(filename)[1]
        if fileextension.upper()!='.EVI':
            msg = 'WARNING in EVIFile.read: unexpected file extension {}'.format(fileextension)
            print(msg)
        try: fp = open(filename, encoding='latin-1')
        except:
            msg = 'ERROR in EVIFile.read: error while trying to open file {}.'.format(filename)
            print(msg)
            return
        
        # read the headers
        for i in range(0, 76): 
            # note: 76 lines of file header, not completely sure how stable this number is
            line = fp.readline()
            name, var = line.partition(" ")[::2]
            self.headers[name.strip()] = var
            
        # set some important headers as instance attributes
        image_type   = self.headers["Image_Type"]
        self.is32bit = (image_type == "Single") or (image_type == "32-bit Real")
        self.width   = int(self.headers["Width"])
        self.height  = int(self.headers["Height"])
        self.nimages = int(self.headers["Scan_Frame_Count"])
        self.frameHeaderBytes = int(self.headers["Gap_between_iamges_in_bytes"])
        self.intelByteOrder = self.headers["Endianness"] == "Little-endian byte order"
        self.TC = int(self.headers["HV_TC"])
        self.sequenceHeaderBytes = int(self.headers["Offset_To_First_Image"])
        self.tds = self.headers["Tds"].lower() == "true"
        if "Tds_Truncate_to_015" in self.headers:
            self.tdsTruncate = self.headers["Tds_Truncate_to_015"].lower() == "true"
        else:
            self.TE = self.headers["Energy_type"].lower() == "TOTAL_ENERGY" 
            if self.TE:
                self.tdsTruncate = self.headers["Tds_Truncate_to_015_TE"].lower() == "true"
            else:
                self.tdsTruncate = self.headers["Tds_Truncate_to_015_HE"].lower() == "true"
        if "Number_of_boards" in self.headers:
            self.numberOfBoards = int(self.headers["Number_of_boards"])
        if "Number_of_board_rows" in self.headers:
            self.numberOfRows = int(self.headers["Number_of_board_rows"])

        self.data = np.zeros((self.height, self.width, self.nimages),dtype=np.uint16)

        # read the image data
        fp.seek(0) # go back to the begining of the file
        fp.read(self.sequenceHeaderBytes-self.frameHeaderBytes) # skip file header
        for i in range(0, self.nimages):
            fp.read(self.frameHeaderBytes) # skip frame header
            if self.is32bit:
                tmp = np.fromfile(fp,dtype=np.uint32,count=self.width*self.height).astype(np.uint16)
            else:
                tmp = np.fromfile(fp,dtype=np.uint16,count=self.width*self.height)
            self.data[:,:,i] = np.reshape(tmp, (self.height, self.width))
        fp.close()

    def print_header(self):
        ### print the full header of the EVI file
        for i in self.headers:
            print("{} : {}".format(i, self.headers[i]))

    def show(self, frame_inds=None):
        ### show the EVI image
        if frame_inds is None:
            frame_inds = np.arange(self.nimages)
        for i in frame_inds:
            plt.figure()
            plt.imshow(self.data[:,:,i], cmap='gray')
            plt.show(block=False)

    def get_data(self):
        ### return the numpy array of the raw data
        return self.data

    def get_header(self):
        ### return the header dictionary
        return self.headers

    def shape(self):
        ### show the dimension of the image
        print("(H, W, frames) = ", [self.height, self.width, self.nimages])
        return (self.height, self.width, self.nimages)


def EVIRead(filename):
    ### utility function to read the EVI data and header directly"
    evi = EVIFile(filename)
    return evi