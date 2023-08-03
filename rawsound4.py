import io
import math
import struct
import sys
import random

import rawsound_handclap

def filter_enclose():
#http://jaggedplanet.com/iir/iir-explorer.asp
#chebyshev
#low-pass
#order = 2
#fs  =44100
#cutoff = 1000
#ripple = 0.1

  NPOLE = 2
  NZERO = 2
  ac = [0.8403838701730075,-1.824007818250394,1]
  bc =[1,2,1]
  gain=247.0067692744004
  xv = [0,0,0]
  yv = [0,0,0]

  '''  
#chebyshev
#band-pass
#order = 2
#fs  =44100
#cutoff = 6000
#ripple = 0.1
#width = 1000

  NPOLE=4
  NZERO=4
  ac=[0.8399557427681004,-2.305225002040346,3.4096106527408647,-2.5158421933802773,1]
  bc=[1,0,-2,0,1]
  gain=245.5284638846673
  xv=[0,0,0,0,0]
  yv=[0,0,0,0,0]

#band-pass
#order = 4
#fs  =44100
#cutoff = 4000
#ripple = 0.1
#width = 1000
  NPOLE = 8
  NZERO = 8
  ac =  [0.8077759712003454,-5.590283701780115,17.91167575505413,-34.40852161929764,43.214553172503194,-36.295619142575816,19.930151118211555,-6.561265254086744,1]
  bc = [1,0,-4,0,6,0,-4,0,1]
  gain = 110357.91104134671
  xv = [0,0,0,0,0,0,0,0,0]
  yv = [0,0,0,0,0,0,0,0,0]
  '''

  def applyfilter(v):
    out = 0.0

    for i in range(NZERO):
      xv[i] = xv[i+1]
    xv[NZERO] = v/gain
  
    for i in range(NPOLE):
      yv[i] = yv[i+1]

    for i in range(NZERO):
      out += xv[i] * bc[i]
    
    for i in range(NPOLE):
      out -= yv[i] * ac[i]

    #feedback 
    yv[NPOLE] = out

    return out

  return applyfilter

#noise is generated at 100kHz?
def pn_enclose():
  pn = 0xf
  def pn909():
    nonlocal pn
    b0 = 0x01 & (pn >> 12)
    b1 = 0x01 & (pn >> 30)
    xb = 0x01 & (b0+b1)
  
    pn = pn<<1
    pn = pn | xb

    ob = ((pn>>35) & 0x01)
    if ob==0:
      ob = -1
    else:
      ob = 1 
    return ob
  return pn909

pn909 = pn_enclose() 
filter1000 = filter_enclose()

def scaled_noise(n,s): 
  noise = []
  for i in range(n):
    noise.append(pn909() * s)

  return noise

print(scaled_noise(200,32))

file_path = "bass.raw"

# Maximum value for a signed integer with one byte.
# Assuming 1 byte (8 bits), 2 ^ (8 - 1) - 1 == 127.
amplitude = 32
# In Hz (44.1 KHz: CD quality)
sampling_rate = 44100
channels = 1
# Desired duration for the audio, in seconds
duration = 2

# Size of the array that will store the samples for the wave.
samples_count = duration * sampling_rate * channels

# Chosen frequency for the sound, in Hertz.
frequency = 50
frequency = 60
frequency = 40
vco = 1

env = []
es = 20.0/5000
e = es
sample = 0
i = 0

#envelope 1
for t in range(samples_count):
    sample = sample + es 
    i = i+1
    if i==5000:
      i=0
      sample = es

    env.append(sample)

env=[]
#envelope 2
up = True
w = False
for t in range(samples_count):
    if w == False:
      sample = 1 
      #if up==True:
      #  sample = sample + es
      #else:
      #  sample = sample - es

    else:
      sample = 0

    if i==5000:
      up=False
      w = True

    if i==30000:
      up=True
      sample = 0
      w = False

    if i==35000:
      up=False
      w = True

    if i==60000:
      up==True
      sample = 0
      w = False

    if i==65000:
      up=True
      sample = 0
      w = True

    if i==80000:
      up=False
      w = True

    if i==85000:
      w=False
    i=i+1

    env.append(sample)
 
env=[]
for i in range(samples_count):

  d=math.floor(i/10000)
  
  attack = 500
  attack = 500
  attack = 200
  attack = 200
  attack = 50
  decay = 1200
  decay = 2000
  decay = 4000
  decay = 1000
  decay = 2000
  decay = 3000
  start = 20000-attack
  if d==1:
    if i>(start):
      sample =1.0 -  math.exp(-(i-start)/(1.0*attack) )
    else:
      sample = 0
  
  elif d==2 or d==3 or d==4 or d==5:
  
    sample = math.exp(-(i-20000)/decay)
  else:
    sample = 0

  env.append(sample)

print(env[29900])
for i in range(100):
  env[29900+i] = 0.0

# Constant part of the equation.
multiplier = 2.0 * math.pi * frequency / sampling_rate

# Generation of values for the sound.
samples = []
for t in range(samples_count):
    #multiplier = multiplier - vco/100000.0
    vco1 = env[t]* 2-vco * (t-18000)/2000.0
    vco1 = env[t]* 2-vco * (t-18000)/20.0
    vco1 = env[t]* 8-vco * (t-18000)/0.1
    vco1 = 0.8*env[t]* 12-vco * (t-18000)/0.1
    #vco1 = env[t]* 24-vco * (t-18000)/0.1
    if vco1<0:
     vco=0

    multiplier = 2.0 * math.pi * (frequency-vco1) / sampling_rate
    sample = 2*math.floor(amplitude * math.sin(multiplier * t) )
    sample = sample + 1*(amplitude/9.0) * math.sin(3*multiplier*t)
    mag5 = 0.01*(amplitude * amplitude / 25.0)
    sample = sample + mag5 * math.sin(5*multiplier*t)
    mag7 = 0.000*(amplitude * amplitude*amplitude / 49.0)
    sample = sample + mag7 * math.sin(7*multiplier*t)
    gain =2
    sample = sample * gain

    limiter = 48
    limiter = 32
    if(sample>limiter):
      sample = limiter

    if(sample<-limiter):
      sample = -limiter

    hard = 6
    hard = 7
    hard = 4 #was 2
    #sample = sample + hard*random.random()
    pn_noise = filter1000(hard*pn909())
    #sample = sample + 8*pn909()
    
    sample = sample + pn_noise

    sample = math.floor(sample * env[t])
    #added gain and limit
    sample=sample*4
    limiter =127
    if(sample>limiter):
      sample = limiter

    if sample<-limiter:
      sample = -limiter
    '''
    limiter = 48
    if(sample>limiter):
      sample = limiter

    if(sample<-limiter):
      sample = -limiter
    '''

    samples.append(sample)


'''
for i in range(900):
  samples[29000+i] = samples[29000+i]-1
  if samples[29000+i]<0:
    samples[29000+i]=0
'''
  
hc = rawsound_handclap.handclap()
sd = rawsound_handclap.snaredrum()

esamples = samples[9000:30000]
esamples.extend(samples[9000:30000])
esamples.extend(samples[9000:30000])
#esamples.extend(hc)
esamples.extend(esamples)
esamples.extend(esamples)
esamples.extend(esamples)
esamples.extend(esamples)
esamples.extend(esamples)
esamples.extend(esamples)
esamples.extend(esamples)
esamples.extend(esamples)
samples = esamples
samples_count = len(samples)

try:
    file = open(file_path, "wb")
    for t in range(samples_count):
        # 1 byte signed int, in LE order.
        file.write(struct.pack("<b", samples[t]))

    file.close()

    print("Sound created successfully.")
except IOError as exception:
    print("Error when trying to create the binary file.", file=sys.stderr)
    print(exception)
except OSError as exception:
    print("Error when trying to create the binary file.", file=sys.stderr)
    print(exception)
