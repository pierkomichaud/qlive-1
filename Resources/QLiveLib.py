# encoding: utf-8
"""
Copyright 2016 (Pierre Michaud, Olivier Belanger, Tiago Bortoletto Vaz)

This file is part of QLive, a cues-based software to help the 
creation of mixed music.

QLive is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

QLive is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public
License along with QLive.  If not, see <http://www.gnu.org/licenses/>.

"""
import os
import codecs
from pyo import pa_get_input_devices, pa_get_default_input
from pyo import pa_get_output_devices, pa_get_default_output
from pyo import pm_get_input_devices, pm_get_default_input
from constants import *
import variables as vars

def getRecentFiles():
    recentFiles = []
    filename = ensureNFD(OPEN_RECENT_PATH)
    if os.path.isfile(filename):
        f = codecs.open(filename, "r", encoding="utf-8")
        for line in f.readlines():
            fname = line.replace("\n", "")
            if os.path.isfile(fname):
                recentFiles.append(fname)
        f.close()
    return recentFiles

def getAvailableAudioMidiDrivers():
    inDefault = pa_get_default_input()
    inDriverList, inDriverIndexes = pa_get_input_devices()
    if inDefault in inDriverIndexes:
        defaultInputDriver = inDriverList[inDriverIndexes.index(inDefault)]
    else:
        defaultInputDriver = ""
    outDriverList, outDriverIndexes = pa_get_output_devices()
    outDefault = pa_get_default_output()
    if outDefault in outDriverIndexes:
        defaultOutputDriver = outDriverList[outDriverIndexes.index(outDefault)]
    else:
        defaultOutputDriver = ""
    midiDefault = pm_get_default_input()
    midiDriverList, midiDriverIndexes = pm_get_input_devices()
    if midiDefault in midiDriverIndexes:
        defaultMidiDriver = midiDriverList[midiDriverIndexes.index(midiDefault)]
    else:
        defaultMidiDriver = ""
    return (inDriverList, inDriverIndexes, defaultInputDriver,
            outDriverList, outDriverIndexes, defaultOutputDriver,
            midiDriverList, midiDriverIndexes, defaultMidiDriver)

# getter/setter for global variables defined at runtime (see variables.py)
def getVar(var, default=None):
    return vars.QLiveVariables.get(var, default)

def setVar(var, value):
    vars.QLiveVariables[var] = value

def saveVars():
    vars.writeQLivePrefsToFile()

def loadVars():
    vars.readQLivePrefsFromFile()

def getBackgroundColour():
    if getVar("locked"):
        return BACKGROUND_COLOUR_LOCKED
    else:
        return BACKGROUND_COLOUR

def saveMEI(path):
    if PYMEI:
        import MEI
        MEI.saveMEI(path)
    else:
        pass

def loadMEI():
    MEI.loadMEI()

def queryAudioMidiDrivers():
    driverInfos = getAvailableAudioMidiDrivers()
    inputs = driverInfos[0]
    inputIndexes = driverInfos[1]
    defaultInput = driverInfos[2]
    outputs = driverInfos[3]
    outputIndexes = driverInfos[4]
    defaultOutput = driverInfos[5]
    midiInputs = driverInfos[6]
    midiInputIndexes = driverInfos[7]
    defaultMidiInput = driverInfos[8]

    setVar("availableAudioOutputs",  outputs)
    setVar("availableAudioOutputIndexes",  outputIndexes)
    if getVar("audioOutput") not in outputs:
        setVar("audioOutput", defaultOutput)

    setVar("availableAudioInputs", inputs)
    setVar("availableAudioInputIndexes", inputIndexes)
    if getVar("audioInput") not in inputs:
        setVar("audioInput", defaultInput)

    if midiInputs == []:
        setVar("useMidi", 0)
    else:
        setVar("useMidi", 1)
    setVar("availableMidiInputs", midiInputs)
    setVar("availableMidiInputIndexes", midiInputIndexes)
    if getVar("midiDeviceIn") not in midiInputs:
        setVar("midiDeviceIn", defaultMidiInput)

# PRINT() should be used instead of print statement to enable/disable printing.
def PRINT(*args):
    if DEBUG:
        for arg in args:
            print arg,
        print

def ensureNFD(unistr):
    "Converts a string to unicode."
    if unistr is None:
        return None
    if PLATFORM == 'win32' or PLATFORM.startswith("linux"):
        encodings = [DEFAULT_ENCODING, SYSTEM_ENCODING,
                     'cp1252', 'iso-8859-1', 'utf-16']
        format = 'NFC'
    else:
        encodings = [DEFAULT_ENCODING, SYSTEM_ENCODING,
                     'macroman', 'iso-8859-1', 'utf-16']
        format = 'NFC'
    decstr = unistr
    if type(decstr) != unicode:
        for encoding in encodings:
            try:
                decstr = decstr.decode(encoding)
                break
            except UnicodeDecodeError:
                continue
            except:
                decstr = "UnableToDecodeString"
                print("Unicode encoding not in a recognized format...")
                break
    if decstr == "UnableToDecodeString":
        return unistr
    else:
        return unicodedata.normalize(format, decstr)

def toSysEncoding(unistr):
    "Converts a unicode string to the current system encoding."
    try:
        if PLATFORM == "win32":
            unistr = unistr.encode(SYSTEM_ENCODING)
        else:
            unistr = unicode(unistr)
    except:
        pass
    return unistr