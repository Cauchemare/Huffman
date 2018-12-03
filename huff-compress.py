# -*- coding: utf-8 -*-
"""
Created on Sun Dec  2 12:48:44 2018

@author: luyao.li
"""

import struct
import pickle
import os
import argparse
import re
from collections import Counter

 
 
class Node:
    def __init__(self,frequency,value=None,left=None,right=None,code=''):
        self.value = value
        self.left = left
        self.right = right
        self.frequency = frequency
        self.code = code
 
 
def change_value_to_key(huffmap):
    return  {  v:k  for k,v in huffmap.items()}
 

def give_code(node):
    if node.left:
        node.left.code = '%s%s' % (node.code, '0')
        give_code(node.left)
    if node.right:
        node.right.code = '%s%s' % (node.code, '1')
        give_code(node.right)
 
 
 
def save_code(huff_map, node):
    if not node.left and not node.right:
        huff_map[node.value] = node.code
    if node.left:
        save_code(huff_map, node.left)
    if node.right:
        save_code(huff_map, node.right)



if  __name__=='__main__':
    from MyOutils import Timer
    timer=Timer()
    
    
    parser=argparse.ArgumentParser()
    parser.add_argument("-s", "--symbolmodel", help="specify character- or word-based Huffman encoding -- default is character",
                    choices=["char","word"])
    parser.add_argument("infile", help="pass infile to huff-compress/decompress for compression/decompression")
    args=parser.parse_args()
    (r,_)=os.path.splitext(args.infile)

 
    with open(args.infile) as f:
        if args.symbolmodel =='char':
                origindata =f.read()
        else:
            origindata=re.findall(r'[+-]?\w+',f.read())
    lettermap=Counter(origindata)
    
    nodelist = [  Node(value=k,frequency=v)   for k,v in lettermap.items()  ]
    
    
    nodelist.sort(key=lambda n:n.frequency,reverse= True)
  
    for i in range(len(nodelist) - 1):  #merge  len(nodelist)-1 times
        node1 = nodelist.pop()
        node2 = nodelist.pop()
        node = Node(left=node1,right=node2,frequency=node1.frequency + node2.frequency)
        nodelist.append(node)
        nodelist.sort(key=lambda n:n.frequency,reverse=True)
    
    root = nodelist[0] 
    give_code(root)

    huffman_map = {}
    save_code(huffman_map, root)

    pickle.dump(huffman_map,open(r +'-symbol-model.pkl', 'wb'))
   
    code_data = ''.join(huffman_map[l] for l in origindata)
 
   
    huffman_map_bytes = pickle.dumps(huffman_map)
    symbol_mode_bytes=pickle.dumps(args.symbolmodel)
    

    with open(r+'.bin', 'wb') as f:
        f.write(struct.pack('I', len(symbol_mode_bytes)))
        f.write(struct.pack('%ds' % len(symbol_mode_bytes), symbol_mode_bytes))
        
        f.write(struct.pack('I', len(huffman_map_bytes)))
        f.write(struct.pack('%ds' % len(huffman_map_bytes), huffman_map_bytes))
       
        f.write(struct.pack('B', len(code_data) % 8))
        for i in range(0, len(code_data), 8):
            if i + 8 < len(code_data):
                f.write(struct.pack('B', int(code_data[i:i + 8], 2)))  #max( int(code_data[i:i+8],2)) =255 <= B
            else:
                f.write(struct.pack('B', int(code_data[i:], 2)))

 

 



