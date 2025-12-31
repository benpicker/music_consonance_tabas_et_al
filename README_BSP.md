1. Run `python -m venv venv`
2. Run `source venv/Scripts/activate` from Git bash 
3. Run `python -m pip install --upgrade pip` 
4. Run `python -m pip install -r requirements.txt`






## `loadParameters.py`

The file `loadParameters.py` defines and manages parameters for the neural simulations. In particular, it does the following  
* Defines a Parameters class to hold all model parameters.
* Provides functions to:    
    - Define stimulus properties (defineStimulus), such as type, frequency, duration, and other sound features.
    - Generate and plot connectivity matrices between neural populations (connectivities, plot_connectivities).
    - Set up all model parameters, including neural population sizes, time constants, synaptic strengths, delays, and noise (loadParameters).

## `moch.py` 

- Uses the cochlea package to simulate auditory nerve responses to sound (peripheralSpikes and peripheral functions).


FOR SAVING THE FILES WITHIN DOCKER 
1. Make sure `COPY . /workspace` is uncommented in `Dockerfile`. 
2. Open Docker Desktop 
3. Build the image by running `docker build -t cochlea-min .` 
4. Run `docker run --rm -it cochlea-min bash`


FOR RUNNIG DOCKER WHILE HAVING THE FILES LOCALLY 

1. Make sure `COPY . /workspace` is commented out in `Dockerfile`. 
2. Open Docker Desktop 
3. Build the image by running `docker build -t cochlea-min .` 
4. Then run `docker run -it -v C:/Users/benpi/Documents/my_repos/music_consonance_tabas_et_al:/workspace cochlea-min` to mount it. 