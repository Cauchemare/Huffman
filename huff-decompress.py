# -*- coding: utf-8 -*-
"""
Created on Sun Dec  2 13:40:35 2018

@author: luyao.li
"""
import argparse
import os
import struct
def change_value_to_key(huffmap):
    return  {  v:k  for k,v in huffmap.items()}

if __name__=="__main__":
    import pickle
    
    parser=argparse.ArgumentParser()
    parser.add_argument("infile", help="pass infile to huff-compress/decompress for compression/decompression")
    args=parser.parse_args()
    (r,_)=os.path.splitext(args.infile)
    
    with open(args.infile, 'rb') as f:
        symbol_size = struct.unpack('I', f.read(4))[0]
        symbol_mode = pickle.loads(f.read(symbol_size))
    
        
        size = struct.unpack('I', f.read(4))[0]
        huffman_map = pickle.loads(f.read(size))
        left = struct.unpack('B', f.read(1))[0]
        data = f.read()
        if data:
            datalist = ['{:0>8}'.format(bin(i)[2:])  for  i in data]
    datalist[-1]=datalist[-1][8-left:]
    #Important
    encode_data = ''.join(datalist)

    huffman_map_reversed = change_value_to_key(huffman_map)
    suffixe=""
    if symbol_mode =='word':
        suffixe=" "
        
    current_code = ''

    with open(r+'-decompressed.txt', 'w') as f:
        for l in encode_data:
            current_code += l
            if current_code in huffman_map_reversed:
                f.write(huffman_map_reversed[current_code]+suffixe)    
                current_code = ''
