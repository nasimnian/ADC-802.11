

## Modules


import numpy as np
import math
import matplotlib.pyplot as plt
from numpy import fft

    
## Initialization

bpsk_6 = {
        "rate": 6,
        "coding rate": 1/2,
        "Nbpsc": 1,
        "Ncbps": 48,
        "Ndbps": 24,
        "RATE": [1, 1, 0, 1],
    }
bpsk_9 = {
        "rate": 9,
        "coding rate": 3/4,
        "Nbpsc": 1,
        "Ncbps": 48,
        "Ndbps": 36,
        "RATE": [1, 1, 1, 1],
    }
qpsk_12 = {
        "rate": 12,
        "coding rate": 1/2,
        "Nbpsc": 2,
        "Ncbps": 96,
        "Ndbps": 48,
        "RATE": [0, 1, 0, 1],
    }
qpsk_18 = {
        "rate": 18,
        "coding rate": 3/4,
        "Nbpsc": 2,
        "Ncbps": 96,
        "Ndbps": 72,
        "RATE": [0, 1, 1, 1],
    }
qam16_24 = {
        "rate": 24,
        "coding rate": 1/2,
        "Nbpsc": 4,
        "Ncbps": 192,
        "Ndbps": 96,
        "RATE": [1, 0, 0, 1],
    }
qam16_36 = {
        "rate": 36,
        "coding rate": 3/4,
        "Nbpsc": 4,
        "Ncbps": 192,
        "Ndbps": 144,
        "RATE": [1, 0, 1, 1],
    }
qam64_48 = {
        "rate": 48,
        "coding rate": 2/3,
        "Nbpsc": 6,
        "Ncbps": 288,
        "Ndbps": 192,
        "RATE": [0, 0, 0, 1],
    }
qam64_54 = {
        "rate": 54,
        "coding rate": 3/4,
        "Nbpsc": 6,
        "Ncbps": 288,
        "Ndbps": 216,
        "RATE": [0, 0, 1, 1],
    }


mod = qam16_36
tail = np.zeros(6, dtype=int)
service = np.zeros(16, dtype=int)
s_initialization = np.array([0, 0, 0, 0, 0, 0, 0], dtype=int)          ##  Scrambler Initialization
nfft = 64          # fft size
cplen = 16
ndcps = 48          # number of data carriers per OFDM symbol
ndspp = 4095          # number of data symbols per packet
ndsppps = 4096          # number of data symbols per packet plus SIGNAL
pl = 4100          # packet length
st = 400         # silence time
ntspdp = (nfft+cplen)*ndspp          # number of time sample per data packet
ntspdpps = (nfft+cplen)*ndsppps         # number of time sample per data packet plus SIGNAL  
ntspp = (nfft+cplen)*pl          # number of time sample per packet
ndbpp = (mod['Ndbps']*ndspp)         # number of data bit per packet
ndbps = mod['Ndbps']          # number of data bit per symbol
ndbppts = ndbpp - len(tail) - len(service)  ##ndbpp -len(tail) -len(service)


def test_encoder(inputd, rate):     
    L = len(inputd)
    if rate == 1/2:
        codbit = np.zeros(L)
    elif rate == 2/3:
        codbit = np.zeros(int(L/2))
    elif rate == 3/4:
        codbit = np.zeros(int(L/3))
    outputd = np.hstack((inputd,codbit))
    return outputd

def test_decoder(inputd,rate):
    L = len(inputd)
    if rate == 1/2:
        codbit = np.delete(inputd,range(int(L/2),L))
    elif rate == 2/3:
        codbit = np.delete(inputd,range(int((2*L)/3),L))
    elif rate == 3/4:
        codbit = np.delete(inputd,range(int((3*L)/4),L))
    
    return codbit


def choose_packet(data,nop,iteration,ndbpp):
    complet_packet = data[i*ndbpp:(i+1)*ndbpp]
    last_paacket = data[(nop-1)*ndbpp:]
    if iteration<nop-1:
        output = complet_packet
    elif iteration==nop-1:
        output = last_paacket
    return output

def make_packet(chosen_packet, mod_type):
    en_data = test_encoder(chosen_packet, mod_type["coding rate"])
    return en_data


def extract_packet(time_signal, mod_type):
    de_data = test_decoder(time_signal, mod_type["coding rate"])
    return de_data


source = np.random.randint(0, high=2, size=200000)
sourcehat = []
nop = math.ceil(len(source)/(ndbppts))          # number of packets


for i in range(nop):
    ch_data = choose_packet(source,nop,i,ndbppts)       ## chosen packet   (bit)
    t_signal = make_packet(ch_data, mod)
    ex_data = extract_packet(t_signal, mod)
    sourcehat = np.append(sourcehat,ex_data)    

for i in range(len(sourcehat))
    if sourcehat[i]!=source[i]:
        print('false')
