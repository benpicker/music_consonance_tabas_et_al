import numpy as np
import matplotlib.pyplot as plt

def loadParameters():
    # Replace with your actual parameter loading logic
    return {
        'est': {
            'dur': 200,
            'type': 'IRN',
            'f': 160,
            'nOfIts': 16,
            'noiseOff': 0,
            'bandpass': [800, 3200],
            'tuning': 'just',
            'notes': []
        },
        'sigma': 0,
        'Cei': np.ones((30, 30)) * 0.5,  # Dummy connectivity, replace as needed
        'Cie': np.ones((30, 30)) * 0.5
    }

def tdoch(pars):
    # Dummy implementation for demonstration
    s = {
        'p': {'He': np.random.rand(300, 30)},
        'q': {'He': np.random.rand(300, 30)}
    }
    r = {'A': np.random.rand(300, 30)}
    lagSpace = np.linspace(1, 30, 30)
    timeSpace = np.linspace(0, 300, 300)
    return s, r, lagSpace, timeSpace

# Fig 1 -- Model's diagram
delays = np.arange(4, 13, 4)  # [4, 8, 12]

pars = loadParameters()
pars['est']['dur'] = 300
pars['est']['type'] = 'IRN'
pars['est']['nOfIts'] = 16
pars['est']['noiseOff'] = 0
pars['est']['bandpass'] = [800, 3200]
pars['sigma'] = 0  # No cortical noise for the examples -> clearer plots

He = []
Ac = []
por = []

for i, delay in enumerate(delays):
    print(i + 1)
    pars['est']['f'] = 1000.0 / delay
    s, r, lagSpace, timeSpace = tdoch(pars)
    He.append(np.mean(s['q']['He'][250:], axis=0))
    Ac.append(np.mean(r['A'][250:], axis=0))
    por.append(np.mean(s['p']['He'], axis=1))

por = np.stack(por, axis=1)

fig0, axs0 = plt.subplots(1, len(delays), figsize=(20, 2))
l = [4.1, 3.1, 2.9]
for i in range(len(delays)):
    axs0[i].plot(np.arange(1, por.shape[0] + 1), por[:, i], 'k')
    axs0[i].set_ylabel('excitatory activity in the decoder network (Hz)')
    axs0[i].set_xlabel('time after tone onset (ms)')
    axs0[i].set_xlim([0, 300])
    axs0[i].set_ylim([0, l[i]])
    axs0[i].invert_yaxis()
fig0.tight_layout()
fig0.savefig('fig1-0.svg', format='svg')
plt.close(fig0)

fig, axs = plt.subplots(4, 3, figsize=(8, 11))
for i in range(len(delays)):
    ax = axs[i // 3, i % 3]
    ax.plot(lagSpace, He[i], 'k')
    ax.set_title(f'perceived pitch: {1000 / delays[i]:.0f}ms')
    ax.set_xlabel('characteristic period of the population (ms)')
    ax.set_ylabel('average firing rate (Hz)')
    ax.set_xlim([0, 30])
    ax.set_ylim([0, 80])

im1 = axs[1, 2].imshow(pars['Cei'], extent=[lagSpace[0], lagSpace[-1], lagSpace[0], lagSpace[-1]], aspect='auto', cmap='viridis', vmin=0, vmax=1)
axs[1, 2].set_title('decoder exc-to-inh')
axs[1, 2].set_xticks(np.arange(5, 31, 5))
fig.colorbar(im1, ax=axs[1, 2])

im2 = axs[2, 2].imshow(pars['Cie'], extent=[lagSpace[0], lagSpace[-1], lagSpace[0], lagSpace[-1]], aspect='auto', cmap='viridis', vmin=0, vmax=1)
axs[2, 2].set_title('decoder inh-to-exc')
axs[2, 2].set_xticks(np.arange(5, 31, 5))
fig.colorbar(im2, ax=axs[2, 2])

for i in range(len(delays)):
    ax = axs[3, i]
    ax.plot(lagSpace, Ac[i], 'k')
    ax.set_xlabel('characteristic period of the population (ms)')
    ax.set_ylabel('average firing rate (Hz)')
    ax.set_xlim([0, 30])
    ax.set_ylim([0, 80])

fig.tight_layout()
fig.savefig('fig1-1.svg', format='svg')
plt.close(fig)