import io
import math
import struct
import sys
import random

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
    sample = sample + hard*random.random()

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
  
esamples = samples[9000:30000]

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
