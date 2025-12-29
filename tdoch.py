import numpy as np
import scipy.io
import os
import string
import random
from loadParameters import loadParameters
from tdochCortex import tdochCortex

def binSpace(pars):
    """
    Replicates the MATLAB binSpace function:
        lagMin = 1000 / pars.freqInterval[1]
        lagMax = 1000 / pars.freqInterval[0]
        lagSpace = np.linspace(lagMax, lagMin, pars.N)
    """
    lagMin = 1000. / pars.freqInterval[1]
    lagMax = 1000. / pars.freqInterval[0]
    lagSpace = np.linspace(lagMax, lagMin, pars.N)
    return lagSpace

def parseThalamic(parsing):
    pyparse = scipy.io.loadmat(parsing)
    timeSpace = pyparse['timeSpace'].squeeze()
    A = pyparse['A']
    n = pyparse['n']
    b = pyparse['b']
    return timeSpace, A, n, b

def pyThalamic(lagSpace, pars):
    # parse filename is randomized to allow parallel computations
    chart = string.ascii_letters + string.digits
    parseID = 'pyparse' + ''.join(random.choices(chart, k=4))
    parseIn = parseID + 'In.mat'
    parseOut = parseID + 'Out.mat'
    scipy.io.savemat(parseIn, {'pars': pars, 'lagSpace': lagSpace})

    # You may need to adjust the python command for your system
    python_cmd = 'python'
    os.system(f'{python_cmd} subthalamic.py {parseID}')

    timeSpace, A, n, b = parseThalamic(parseOut)
    os.remove(parseOut)
    return timeSpace, A, n, b

def tdoch(pars=None, parsing=0):
    """
    Python version of tdoch.m
    Args:
        pars: parameters dictionary or object
        parsing: 0 (default) or string for parsing file
    Returns:
        s, r, lagSpace, timeSpace
    """
    if pars is None:
        pars = loadParameters()
    if parsing is None:
        parsing = 0

    r = {}
    r['lagSpace'] = binSpace(pars)
    r['freqSpace'] = 1000. / r['lagSpace']

    if isinstance(parsing, str) and parsing:
        timeSpace, r['A'], r['n'], r['b'] = parseThalamic(parsing)
    else:
        timeSpace, r['A'], r['n'], r['b'] = pyThalamic(r['lagSpace'], pars)

    r['timeSpace'] = timeSpace * 1000  # convert to ms

    if not getattr(pars, 'onlySubcort', False):
        s = tdochCortex(r, pars)
    else:
        s = 0

    return s, r, r['lagSpace'], r['timeSpace']


