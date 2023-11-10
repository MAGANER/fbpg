#!/usr/bin/env python3
import random
import sys
import os
import string
from functools import reduce

#check arguments number
if len(sys.argv) != 3:
    print("fbpg error: incorrect number of arguments!")
    print("fbpg example: fbpg some_root_dir password_len")
    exit(-1)

#check first argument, it should be directory
if not os.path.exists(sys.argv[1]) or not os.path.isdir(sys.argv[1]):
    print("fbpg error: {} doesn't exist or isn't a directory!".format(sys.argv[1]))
    exit(-1)

#check second argument, this string should contain only digit characters
if not sys.argv[2].isdigit():
    print("fbpg error:{} must contain only digital values!".format(sys.argv[2]))
    exit(-1)

if int(sys.argv[2]) < 8:
    print("fbpg error: password length is too small! it should be 8 or higher!")
    exit(-1)
    
j = lambda a,b: os.path.join(a,b) # simple shortcut to concatenate path values

def get_size(f):
    '''avoid window's exeception, if there is no ability to read file'''
    try:
        size = os.path.getsize(j(sys.argv[1],f))
        return size
    except Exception as e:
        return 0

#get files with size above 50
root = sys.argv[1] #script will take random file from this dir
files = [j(root,f) for f in os.listdir(root) if not os.path.isdir(j(root,f)) and get_size(j(f,root)) > 50]
if not files:
    print("fbpg failed: There is no big enough file to choose! Please, try other directory.")
    exit(-1)

file = random.choice(files)

def read_random_bytes(f):
    '''read random bytes from file. amount of bytes equals to key length'''
    key_ken = int(sys.argv[2])
    global file
    size = get_size(file)
    for _ in range(key_ken):
        rand_pos = random.randint(0,size)
        f.seek(rand_pos)
        yield int.from_bytes(f.read(1),byteorder="big")
        
def get_alphabet_codes():
    return [ord(x) for x in string.ascii_lowercase] + [ord(x) for x in string.ascii_uppercase]
def change_element(x):
    '''if passed int value represents ascii character than convert it to char, otherwise do nothing'''
    codes = get_alphabet_codes()
    if x in codes:
        return chr(x)
    else:
        return x

def insert_delimiters(sequence):
    for i,_ in enumerate(sequence):
        if i % 3 == 0 and i != 0:
            sequence[i] = '-'                   
    return sequence

#return positions
def get_numbers_of_3_digits(sequence):
    def check_number(x):
        if isinstance(x,int):
            return x >= 100
        else:
            return False
    return [i for i,x in enumerate(sequence) if check_number(x)]
    
def insert_special_characters(sequence):
    numbers_positions = get_numbers_of_3_digits(sequence)
    
    if not numbers_positions:
        numbers_positions = [random.randint(0,len(sequence)) for _ in range(4)]
    
    chars = list(string.punctuation)
    chars.remove('-')

    for _ in range(int(len(numbers_positions)/2)):
        rand_pos = random.choice(numbers_positions)
        sequence[rand_pos] = random.choice(chars)
    return sequence
def insert_random_letters(sequence):
    numbers_positions = get_numbers_of_3_digits(sequence)

    chars = list(string.ascii_lowercase+string.ascii_uppercase)
    for n in numbers_positions:
        sequence[n] = random.choice(chars)
    return sequence
def check_if_fails(sequence):
    return sequence.count(0)+sequence.count('0') >= len(sequence)/6
try:
    with open(file,"br") as f:
        noise = read_random_bytes(f)
        sequence  = list(map(change_element,noise))
        sequence  = insert_delimiters(sequence)
        sequence  = insert_special_characters(sequence)
        sequence  = insert_random_letters(sequence)
        sequence  = list(map(str,sequence))
        if(check_if_fails(sequence)):
            print("fbpg failed! try again!")
            exit(-1)
            
        print("".join(sequence))
except Exception as e:
    print("fbpg error: failed to read {}! Exception:{}".format(file,str(e)))
    exit(-1)
