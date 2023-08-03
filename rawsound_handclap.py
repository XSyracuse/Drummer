import math
def filter_enclose():
#http://jaggedplanet.com/iir/iir-explorer.asp
#chebyshev
#band-pass
#order = 2
#fs  =44100
#cutoff = 4000
#ripple = 0.1
#width = 3000

  NPOLE=4
  NZERO=4
  ac=[0.5727745509816272,-2.2186162841794803,3.6581607190661143,-2.9547713839679646,1]
  bc=[1,0,-2,0,1]
  gain=28.254625011083164
  xv=[0,0,0,0,0]
  yv=[0,0,0,0,0]

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
filterhc = filter_enclose()

def scaled_noise(n,s): 
  noise = []
  for i in range(n):
    noise.append(pn909() * s)

  return noise

print(scaled_noise(200,32))

def snaredrum():


  env0 = []
  
  for i in range(2200):
    sample = math.exp((-i*5)/2200)
    env0.append(sample)

  env = []

  env.extend(env0)

  n = scaled_noise(len(env),96)
  
  hc = []
  for i in range(len(env)):
    hc.append(math.floor(n[i]*env[i]))

  return hc



def handclap():


  env0 = []
  
  sample = 0
  t0 = 1500
  m = 1.0/t0
  print(m)
  env0.append(0)
  env0.append(.1)
  env0.append(.2)
  env0.append(.3)
  env0.append(.4)
  env0.append(.5)
  env0.append(.6)
  env0.append(.7)

  for i in range(t0*2):
    sample = math.exp((-i)/t0)
    env0.append(sample)

 



  part = 800
  part = 1000
  env = []
  envp = env0[0:part]

  env.extend(envp)
  env.extend(envp)
  env.extend(envp)
  env.extend(env0)

   #ambiance env
  env1 = []
  for i in range(len(env)):
    sample = 1.0 - math.exp((-i)/2000)
    env1.append(sample)

  n = []
  for i in range(len(env)):
    pn = filterhc(pn909())

    sample =  env1[i]*6*pn + env[i]*pn*96 
    n.append(sample)
    
    
  hc = []
  for i in range(len(n)):
    sample = math.floor(n[i])
    if sample > 127:
      sample = 127
    if sample < -128:
      sample = -128 
    hc.append(sample)

  if(len(hc) > 21000):
      hc = hc[0:21000]
  return hc


