
# ####################### Scrambler and Descrambler ############################
 
#                             Hadis Abolfathi
#                                 9803134
 
# ##############################################################################
import numpy as np
 
# __________________ PARAMETERS _____________________
 
HEADER_LEN = 4 + 1 + 12 + 1 + 6
#HEADER_LEN = 5
TAIL_LEN = 6
 
NUM_DATA_BIT_PER_SYMBOL = 24  # for BPSK modulation
NUM_SYMBOL = 50
SERVICE_LEN = 16
#DATA_LEN  = SERVICE_LEN + NUM_SYMBOL*NUM_DATA_BIT_PER_SYMBOL
DATA_LEN = 1000
 
SCRAMBLER_LEN = 7
# __________________Scrambler Core __________________
 
def scrambler_core(inp_vec, Initial_Vec):
  vec_len = len(inp_vec)
  out_vec = np.zeros(vec_len,dtype=np.int8)
 
  scrambler_vec = Initial_Vec; # initializing the scrambler
 
  for i in range(vec_len):
    temp = np.bitwise_xor(scrambler_vec[3] , scrambler_vec[6])
    scrambler_vec[1:] = scrambler_vec[0:6]
    scrambler_vec[0] = temp
    out_vec[i] = np.bitwise_xor(scrambler_vec[0] , inp_vec[i])
 
  return out_vec
 
# __________________Scrambler unit __________________
 
def scrambler (inp_vec, Initial_Vec, header_len, service_len, tail_len):
  vec_len = len(inp_vec)
  out_vec = np.zeros(vec_len,dtype=np.int8)
  
  # Scrambler does not scramble the header and service; therefore, the header and service do not change
  out_vec[0:header_len] = inp_vec[0:header_len]
 
  # We know that SERVICE is 16 bits zero. The first 7 bits to be sent into the Scrambler 
  # are the beginning of the SERVICE parameter. These 7 bits are re-written with the 
  # initial state of the Scrambler so descrambling can be done in the receiver.
  out_vec[header_len:header_len+7] = Initial_Vec
 
  out_vec[header_len+service_len:] = scrambler_core(inp_vec[header_len+service_len:],Initial_Vec)
 
  # Scrambler replaces the trailing scrambled zero bits with nonscrambled zero bits
  # to reset the Convolutional Encoder for the next message
  out_vec[vec_len-tail_len:] = 0
 
  return out_vec
 
# __________________Decrambler unit __________________
 
def descrambler (inp_vec, service_len):
  # According to the standard scrambler_len = 7
 
  # We know that SERVICE is 16 bits zero. The first 7 bits to be sent into the Scrambler 
  # are the beginning of the SERVICE parameter. These 7 bits are re-written with the 
  # initial state of the Scrambler so descrambling can be done in the receiver.
  descrambler_init = inp_vec[0:7]
 
  vec_len = len(inp_vec)
  out_vec = np.zeros(vec_len,dtype=np.int8)
  out_vec[0:service_len] = inp_vec[0:service_len]
  out_vec[service_len:] = scrambler_core(inp_vec[service_len:],descrambler_init)
  return out_vec
 
 
# __________________Testting the scrambler and descrambler ______________________
 
 
# test setting: If we inital the scrambler with 1111111, the pattern provided in
# standard will be generated. In order to accomplish this task, we can set the initial
# vector as [1 1 1 1 1 1 1] and the input vector as all zeros. In this case, the given pattern
# will be generated.
 
#Initial_Vec = np.ones(SCRAMBLER_LEN,dtype=np.int8) # only for test
#Inp_vec = np.zeros(127,dtype=np.int8) # only for test
#Out_vec = scrambler_core(Inp_vec,Initial_Vec)
#print(Out_vec)
 
# Initializing the scrambler
Initial_Vec = np.random.randint(2, size=SCRAMBLER_LEN)
 
# Generating the input test vector. Note: The 16 bits of SERVICE all are zero
Scrambler_Inp_vec = np.random.randint(2, size=DATA_LEN)
Scrambler_Inp_vec[HEADER_LEN:HEADER_LEN+SERVICE_LEN] = 0
 
# Scrambler Unit
Scrambler_Out_vec = scrambler(Scrambler_Inp_vec, Initial_Vec, HEADER_LEN, SERVICE_LEN, TAIL_LEN)
 
# Important Notes: The header part is not fed to the descrambler. Therefore, this part
# is eliminated and other parts are fed to the descrambler. In addition, The TAIL_LEN bits
# remain in the convolutional encoder. 
 
# Descrambler Unit
Descrambler_Inp_vec = Scrambler_Out_vec[HEADER_LEN:DATA_LEN-TAIL_LEN]
Descrambler_Out_vec = descrambler(Descrambler_Inp_vec, SERVICE_LEN)
 
# We know the output of the descrambler must be equal to the input of the scrambler. In order to evaluate
# the functionality of these functions, we compare the input of the sracambler with the output of the descrambler
 
Err = 0
for i in range(DATA_LEN-HEADER_LEN-SERVICE_LEN-TAIL_LEN):   # for i in range (len(Descrambler_Out_vec))
   if (Descrambler_Out_vec[i+SERVICE_LEN] != Scrambler_Inp_vec[i+HEADER_LEN+SERVICE_LEN]):
     Err += 1
 
#print(Descrambler_Out_vec[SERVICE_LEN:])  
#print(Scrambler_Inp_vec[HEADER_LEN+SERVICE_LEN:])
if (Err==0):
  print("Congratulation! Both of the scrambler and descrambler work correctly")
else:
  print("Scrambler and descrambler don't work correctly")

"""The following part is the code for the Interleaver and Deinterleaver."""

# #################### interleaver and Deinterleaver ##########################
 
#                             Hadis Abolfathi
#                                 9803134
  
# ##############################################################################
import numpy as np
import math

N_CBPS = 48
N_BPSC = 1
NUM_SYMBOL = 4
TOT_BITS = N_CBPS * NUM_SYMBOL

# __________________Interleaver unit __________________
def interleaver_Core (inp_vec, N_CBPS, N_BPSC):
  s = max(N_BPSC/2,1)

  inner_vec = np.ones(N_CBPS,dtype=np.int8)
  for cnt in range(N_CBPS):
    i = (N_CBPS/16) * (cnt % 16) + math.floor(cnt/16)
    inner_vec[int(i)] = inp_vec[cnt]
  
  outp_vec = np.ones(N_CBPS,dtype=np.int8)
  for cnt in range(N_CBPS):
    j = (s * math.floor(cnt/s)) + ((cnt + N_CBPS - math.floor(16*cnt/N_CBPS)) % s)
    outp_vec[int(j)] = inner_vec[cnt]

  return outp_vec

def Interleaver(inp_vec, N_CBPS, N_BPSC):
  inp_len = len(inp_vec)
  iteration = inp_len/N_CBPS

  outp_vec = np.ones(inp_len,dtype=np.int8)
  for cnt in range(int(iteration)):
    vec = inp_vec[N_CBPS*cnt:N_CBPS*(cnt+1)]
    outp_vec[N_CBPS*cnt:N_CBPS*(cnt+1)] = interleaver_Core(vec, N_CBPS, N_BPSC)
  
  return outp_vec


# __________________Deinterleaver unit __________________
def deinterleaver_Core (inp_vec, N_CBPS, N_BPSC):
  s = max(N_BPSC/2,1)

  inner_vec = np.zeros(N_CBPS,dtype=np.int8)
  for cnt in range(N_CBPS):
    i = (s * math.floor(cnt/s)) + ((cnt + math.floor(16*cnt/N_CBPS)) % s)
    inner_vec[int(i)] = inp_vec[cnt]
  
  outp_vec = np.zeros(N_CBPS,dtype=np.int8)
  for cnt in range(N_CBPS):
    k = 16 * cnt - (N_CBPS-1) * math.floor(16*cnt/N_CBPS)
    outp_vec[int(k)] = inner_vec[cnt]

  return outp_vec

def Deinterleaver(inp_vec, N_CBPS, N_BPSC):

  inp_len = len(inp_vec)
  iteration = inp_len/N_CBPS

  outp_vec = np.ones(inp_len,dtype=np.int8)
  for cnt in range(int(iteration)):
    vec = inp_vec[N_CBPS*cnt:N_CBPS*(cnt+1)]
    outp_vec[N_CBPS*cnt:N_CBPS*(cnt+1)] = deinterleaver_Core(vec, N_CBPS, N_BPSC)

  return outp_vec

# ________________Testting the Interleaver and Deinterleaver ________________

Interleaver_Inp_vec = np.random.randint(2, size=TOT_BITS)

#Interleaver_outp_vec = interleaver_Core(Interleaver_Inp_vec,N_CBPS,N_BPSC)
#Deinterleaver_outp_vec = deinterleaver_Core(Interleaver_outp_vec,N_CBPS,N_BPSC)

Interleaver_outp_vec = Interleaver(Interleaver_Inp_vec,N_CBPS,N_BPSC)
Deinterleaver_outp_vec = Deinterleaver(Interleaver_outp_vec,N_CBPS,N_BPSC)

#print(Interleaver_Inp_vec)
#print(Interleaver_outp_vec)
#print(Deinterleaver_outp_vec)

Err = 0
for i in range(TOT_BITS):   
   if (Interleaver_Inp_vec[i] != Deinterleaver_outp_vec[i]):
     Err += 1

if (Err==0):
  print("Congratulation! Both of the Interleaver and Deinterleaver work correctly")
else:
  print("Interleaver and Deinterleaver don't work correctly")
