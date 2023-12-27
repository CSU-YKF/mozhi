import os
import pickle
import struct
import torch
import numpy as np
from torch.utils.data import Dataset


class HWDB1(Dataset):
    def __init__(self, gnt_directory, transform=None, mapping_file=None):
        """
        Initialize the dataset with the directory of gnt files and optional transform.
        Args:
        - gnt_directory (str): The directory containing the .gnt files.
        - transform (callable, optional): Optional transform to be applied on a sample.
        - mapping_file (str, optional): Path to save the mapping file.
        """
        self.gnt_directory = gnt_directory
        self.transform = transform
        self.code_to_index = {}  # Mapping from GBK code to index
        self.index_to_code = []  # List to store GBK codes in order of their index
        self.samples = self._load_samples()

        if mapping_file:
            self._save_mapping(mapping_file)

    def _load_samples(self):
        """
        Load samples from gnt files and create a list of tuples (image, index).
        """
        samples = []
        for filename in os.listdir(self.gnt_directory):
            if filename.endswith('.gnt'):
                file_path = os.path.join(self.gnt_directory, filename)
                for image, packed_tag_code in self.read_gnt_file(file_path):
                    tag_code = struct.unpack('<H', packed_tag_code)[0]  # GBK code as integer
                    if tag_code not in self.code_to_index:
                        # Assign a new index to the new GBK code
                        self.code_to_index[tag_code] = len(self.index_to_code)
                        self.index_to_code.append(tag_code)
                    samples.append((image, self.code_to_index[tag_code]))
        return samples

    def _save_mapping(self, mapping_file):
        """
        Save the code_to_index and index_to_code mappings to a file.
        """
        with open(mapping_file, 'wb') as f:
            pickle.dump({'code_to_index': self.code_to_index, 'index_to_code': self.index_to_code}, f)

    @staticmethod
    def read_gnt_file(gnt_file_path):
        """
        Read a GNT file, yield ndarray-type image and source gdk code.
        """
        with open(gnt_file_path, 'rb') as file:
            while True:
                # Read the header part
                packed_length = file.read(4)
                if len(packed_length) != 4:
                    break  # End of file
                length = struct.unpack('<I', packed_length)[0]

                # Read the tag code
                packed_tag_code = file.read(2)
                if len(packed_tag_code) != 2:
                    break  # End of file or corrupt file
                # tag_code = packed_tag_code.decode('gbk')

                # Read the width and height of the image
                width, height = struct.unpack('<HH', file.read(4))

                # Read the image
                image_data = file.read(width * height)
                if len(image_data) != width * height:
                    break  # End of file or corrupt file
                image = np.frombuffer(image_data, dtype=np.uint8).reshape((height, width))

                yield image, packed_tag_code
    
    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        image, label_index = self.samples[idx]
        if self.transform:
            image = self.transform(image)
        # image_tensor = torch.from_numpy(image).float()
        label_tensor = torch.tensor(label_index, dtype=torch.long)
        return image, label_tensor
    

# dataset = HWDB1(gnt_directory='/', transform=transform, mapping_file='mapping.pkl')
