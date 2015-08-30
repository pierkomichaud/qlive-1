from constants import *

QLiveVariables = dict()

QLiveVariables["currentProject"] = ""
QLiveVariables["projectFolder"] = ""
QLiveVariables["MainWindow"] = None
QLiveVariables["ControlPanel"] = None
QLiveVariables["CuesPanel"] = None
QLiveVariables["CurrentCueWindow"] = None
QLiveVariables["FxTracks"] = None
QLiveVariables["AudioMixer"] = None
QLiveVariables["AudioServer"] = None
QLiveVariables["MidiServer"] = None
QLiveVariables["MixerPanel"] = None
QLiveVariables["Soundfiles"] = None
QLiveVariables["FxViews"] = []
QLiveVariables["CanProcessCueKeys"] = True

# QLiveVariables which will be loaded/saved in prefs file go here:
PREFS_TO_SAVE = {"useTooltips": False,
                "audioHostAPI": "portaudio",
                "bufferSize": "64"}

def readQLivePrefsFromFile():
    if not os.path.isfile(PREFERENCES_PATH):
        with open(PREFERENCES_PATH, "w") as f:
            f.write(str(PREFS_TO_SAVE))
            prefs = PREFS_TO_SAVE
    else:
        with open(PREFERENCES_PATH, "r") as f:
            prefs = eval(f.read())
            # Load prefs which are not in the prefs file
            for p in PREFS_TO_SAVE:
                if p not in prefs:
                    prefs[p] = PREFS_TO_SAVE[p]

    QLiveVariables.update(prefs)

def writeQLivePrefsToFile():
    try:
        file = open(PREFERENCES_PATH,"wt")
    except IOError:
        print("Unable to open the preferences file.\n")
        return

    save_tmp = {}
    for key in QLiveVariables:
        if key in PREFS_TO_SAVE:
            save_tmp[key] = QLiveVariables[key]

    with open(PREFERENCES_PATH, "w") as f:
        f.write(str(save_tmp))

    file.close()
