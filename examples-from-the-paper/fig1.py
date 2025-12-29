import numpy as np
import matplotlib.pyplot as plt

# Placeholder for the actual loadParameters function
def loadParameters():
    # Implement or import your parameter loading logic here
    pass

# Placeholder for the actual tdoch function
def tdoch(pars):
    # Implement or import your tdoch logic here
    # Should return s, r, lagSpace, timeSpace
    pass

N = 60
notes = np.arange(0, 13, 1)
dyads = ['unison', 'minor second', 'second', 'minor third',
         'third', 'fourth', 'tritone', 'perfect fifth',
         'minor sixth', 'sixth', 'minor seventh', 'seventh', 'octave']
its = 8
dur = 200
f0 = 160
bandpass = [125, 2000]
tuning = 'just'
stimType = 'IRNchordSS'

parbase = loadParameters()
onset = np.full(notes.shape, parbase['subDelayDy'])
onset[0] = parbase['subDelay']
parbase['subDelayDy'] = 0
parbase['subDelay'] = 0
parbase['est']['dur'] = dur
parbase['est']['type'] = stimType
parbase['est']['f'] = f0
parbase['est']['nOfIts'] = its
parbase['est']['bandpass'] = bandpass
parbase['est']['tuning'] = tuning

pars = []
for i in range(len(notes)):
    p = parbase.copy()
    p['est']['notes'] = [0, notes[i]]
    pars.append(p)

# Run tdoch for the first set of parameters to get lagSpace and timeSpace
_, r, lagSpace, timeSpace = tdoch(pars[0])

ACPar = []
DePar = []
DiPar = []
SePar = []
SiPar = []
latPar = []

for i in range(len(notes)):
    print(f' - {i+1} of {len(notes)} ...')
    ac = []
    de = []
    di = []
    se = []
    si = []
    lat = []
    for n in range(N):
        s, r = tdoch(pars[i])
        ac.append(np.mean(r['A'][175:200, :], axis=0))
        de.append(np.mean(s['p']['He'][175:200, :], axis=0))
        di.append(np.mean(s['p']['Hi'][175:200, :], axis=0))
        se.append(np.mean(s['q']['He'][175:200, :], axis=0))
        si.append(np.mean(s['q']['Hi'][175:200, :], axis=0))
        lat.append(np.argmax(np.mean(s['p']['He'], axis=1)))
    ACPar.append(np.array(ac))
    DePar.append(np.array(de))
    DiPar.append(np.array(di))
    SePar.append(np.array(se))
    SiPar.append(np.array(si))
    latPar.append(np.array(lat))
    print('done!')

ACMat = np.stack(ACPar, axis=2)
DeMat = np.stack(DePar, axis=2)
DiMat = np.stack(DiPar, axis=2)
SeMat = np.stack(SePar, axis=2)
SiMat = np.stack(SiPar, axis=2)
lat0 = np.stack(latPar, axis=1)

# Psychoacoustics
fig1 = plt.figure(figsize=(10, 6))

AC = np.mean(ACMat, axis=2)
De = np.mean(DeMat, axis=2)
Di = np.mean(DiMat, axis=2)
Se = np.mean(SeMat, axis=2)
Si = np.mean(SiMat, axis=2)

maximum = 25 * np.ceil(np.max([De, Di, Se]) / 25)

plt.subplot(2, 3, 1)
plt.imshow(AC, aspect='auto', extent=[lagSpace[0], lagSpace[-1], notes[0], notes[-1]])
plt.xlabel('regularised SACF characteristic delay (ms)')
plt.ylabel('stimulus period (ms)')
plt.clim(0, maximum)
plt.title('AC')

plt.subplot(2, 3, 2)
plt.imshow(De, aspect='auto', extent=[lagSpace[0], lagSpace[-1], notes[0], notes[-1]])
plt.xlabel('decoder excitatory characteristic delay (ms)')
plt.ylabel('stimulus period (ms)')
plt.clim(0, maximum)
plt.title('De')

plt.subplot(2, 3, 3)
plt.imshow(Di, aspect='auto', extent=[lagSpace[0], lagSpace[-1], notes[0], notes[-1]])
plt.xlabel('decoder inhibitory characteristic delay (ms)')
plt.ylabel('stimulus period (ms)')
plt.clim(0, maximum)
plt.title('Di')

plt.subplot(2, 3, 4)
plt.imshow(Se, aspect='auto', extent=[lagSpace[0], lagSpace[-1], notes[0], notes[-1]])
plt.xlabel('sustainer excitatory characteristic delay (ms)')
plt.ylabel('stimulus period (ms)')
plt.clim(0, maximum)
plt.title('Se')

plt.subplot(2, 3, 5)
im = plt.imshow(Si, aspect='auto', extent=[lagSpace[0], lagSpace[-1], notes[0], notes[-1]])
plt.clim(0, maximum)
plt.colorbar(im, label='average population activity (Hz)')
plt.title('Si')

plt.tight_layout()
plt.savefig('fig5-0.svg', format='svg')

# POR predictions
fig2 = plt.figure()

lat = lat0 + onset[:, np.newaxis]
latAvg = np.mean(lat, axis=1)
latErr = np.std(lat, axis=1) / np.sqrt(N)

# MEG fields
# You will need to implement the loading of aefs and n1Lats from .mat files
# datapath = '~/Cloud/Projects/TDoCh/Doc/figs/data/'
# aefs = scipy.io.loadmat(datapath + 'aefRes.mat')
# n1Lats = scipy.io.loadmat(datapath + 'n1Lat.mat')
# eLat = n1Lats['n1Lat']
# eNotes = aefs['notes']
# eLatAvg = aefs['n1LatAvg']
# eLatErr = aefs['n1LatErr']

plt.subplot(1, 2, 1)
# plt.errorbar(eNotes, latAvg[eNotes+1], yerr=latErr[eNotes+1])
# plt.errorbar(eNotes, eLatAvg, yerr=eLatErr)
plt.xlabel('notes')
plt.ylabel('latency (ms)')
plt.title('POR predictions')

plt.show()