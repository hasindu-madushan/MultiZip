#!python3

#======================================================================
# Author : Hasindu Madushan
# Date   : 08 sep 2020
# Module : multizip
# File   : multizip.py
# verison: 0.9v
#======================================================================
import multizipcore as core
import zlib


class Multizip:
    def __init__(self, file_name):   
        self._file_name = file_name
        self._cdhs = []
        self._lfhs = []
         
        self.main_disk = core._Disk(file_name)    # load the main disk       
        offset_encd = self.main_disk.content.find(core._end_of_central_directory_header_signature)    # the offset of the encd
        
        # if no encd found the zip file is not valid
        if offset_encd == -1:
            print("Error: Zip file is not valid")
            exit(-1)
            
        self._encd = core._EndCentralDirectoryRecord( self.main_disk.content, offset_encd )
        self.main_disk_id = self._encd.this_disk
        core._Disk.main_disk_id = self.main_disk_id
        core._Disk.main_disk = self.main_disk
        
        self._loadCentralDirHeaders()

    @staticmethod
    def _loadRange( start_disk, start_offset, length, decompress=False):
        res = b''
        current_size = 0
        disk = start_disk
        offset = start_offset
        
        while True:
            append_size = length - current_size
            if append_size <= disk.size - offset:
                res += disk.content[offset : offset + append_size]
                    
                print(len(res))
                break
            
            current_size += disk.size - offset

            res += disk.content[offset : offset + append_size]
            
            #res += disk.content[offset:]
            disk = disk.load( disk.disk_id + 1 )
            offset = 0
            
        if decompress:
            return zlib.decompress( res, wbits=-15 )
                    
        return res
            
    
    def listFileNames(self):
        names = []
        for cdh in self._cdhs:
            file_name = cdh.file_name.split('/')[-1]
            if file_name != '':
                names.append(file_name)
            
        return names 
    
    
    def extractFile( self , file_name ):
        for cdh in self._cdhs:
            if file_name ==  cdh.file_name.split('/')[-1]:
                
                disk = self.main_disk.load( cdh.local_header_disk )
                lfh = core._LocalFileHeader( disk.content, cdh.offset_local_header) 
                content = Multizip._loadRange( disk, lfh.offset_file_data, lfh.compressed_size , decompress=True)
                
        
                with open( file_name, 'wb+') as f:
                    f.write( content )
                
                return 
        
        print("File not foud: " + file_name)
        
        
    def _loadCentralDirHeaders( self ):                
        self._cdhs.append( core._CentralDirectoryHeader(self.main_disk.content, self._encd.offset_central_dir) )
        
        k = self._cdhs[0].len
        i = 1
        
        #!!! It was assumed that all the central dirs  are in the main disk
        while True:
            offset =  self._encd.offset_central_dir + k
            
            if self.main_disk.content[offset:offset + 4] != core._central_directory_header_signature:
                break
            
            self._cdhs.append( core._CentralDirectoryHeader(self.main_disk.content, offset ) )
            k += self._cdhs[i].len
            
            #print(self._cdhs[i].file_name)
            
            i += 1
                

        
                
           
            
            
        
            
        
