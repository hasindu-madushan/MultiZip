#!python3

#======================================================================
# Author : Hasindu Madushan
# Date   : 08 sep 2020
# Module : multizip
# File   : multizipcore.py
# version: 0.9v
#======================================================================

from zipfile import ZipFile
import zlib
import os

_end_of_central_directory_header_signature = b'PK\x05\x06'
_central_directory_header_signature = b'PK\x01\x02'
_local_file_header_signature = b'PK\x03\x04'

class _EndCentralDirectoryRecord:
    def __init__(self, b, offset):
        self.this_disk = int.from_bytes(b[offset + 4:offset + 6], 'little')
        self.central_dir_disk = int.from_bytes(b[offset + 6:offset + 8], 'little')
        self.offset_central_dir = int.from_bytes(b[offset + 16:offset + 20], 'little')
        self.n_entries_this_disk = int.from_bytes(b[offset + 8:offset + 10], 'little')
    

class _CentralDirectoryHeader:
    def __init__(self, b, offset):
        self.offset_local_header = int.from_bytes(b[offset + 42:offset + 46], 'little')
        self.local_header_disk = int.from_bytes(b[offset + 34:offset + 36], 'little')
        self.file_name_len = int.from_bytes(b[offset + 28:offset + 30], 'little')
        exf_len = int.from_bytes(b[offset + 30:offset + 32], 'little')
        com_len = int.from_bytes(b[offset + 32:offset + 34], 'little')
        self.len = 46 + self.file_name_len  + exf_len + com_len
        self.file_name = b[offset + 46:offset + 46 + self.file_name_len].decode()
        

class _LocalFileHeader:
    def __init__(self, b, offset):
        self.compressed_size = int.from_bytes(b[offset + 18:offset + 22], 'little')
        self.file_name_len = int.from_bytes(b[offset + 26:offset + 28], 'little')
        self.file_name = b[offset + 30:offset+30 + self.file_name_len].decode()
        self.extra_len = int.from_bytes(b[offset + 28:offset + 30], 'little')
        self.offset_file_data = offset + 30 + self.file_name_len + self.extra_len
        self.crc32 = b[offset + 12:offset + 16]
 
       
class _Disk:    
    main_disk_id = 0
    main_disk = None
    def __init__( self, file_name, disk_id = 0 ):
        with open(file_name, 'rb') as f:
            self.file_name = file_name
            self.content = f.read()
            self.disk_id = disk_id
            self.size = len(self.content)
            

    def load( self, disk_id ):  
        
        
        if disk_id == _Disk.main_disk_id:
            return _Disk.main_disk
        
        file_name = self.file_name[:-3]
        
        if disk_id < 10:
            file_name += 'z0' + str(disk_id + 1)
        else:
            file_name += 'z' + str(disk_id + 1)
                
        return _Disk(file_name, disk_id)
    

        
        
        
        
        
        
        