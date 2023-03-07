# Python 3 Blue Box DTMF Tone Generator
===================

Modernized python bluebox

## How it works

You can run this in interactive mode, or from a file, pipe, stdin, etc.

## Installation

```
git clone https://github.com/zeyus/Python3BlueBox.git
cd PythonBlueBox
pip install -r requirements.txt
```

### Requirements

- Python 3 (tested on 3.9 - 3.11)

## Usage

### CLI

```
python ./bluebox.py -h
```

Output:

```
usage: bluebox.py [-h] [-l LENGTH] [-p PAUSE] [-a AMPLITUDE] [-s SAMPLE_RATE] [-m MF] [-d] [-b BACKEND] [-r PAD_PAUSE_DURATION] [-f FILE] [-P PIPE] [-S] [-i] [-v] [sequence]

Generate tone sequences.

positional arguments:
  sequence              The sequence of tones to generate.

options:
  -h, --help            show this help message and exit
  -l LENGTH, --length LENGTH
                        The length of each tone in milliseconds.
  -p PAUSE, --pause PAUSE
                        The length of the pause between tones in milliseconds.
  -a AMPLITUDE, --amplitude AMPLITUDE
                        The combined amplitude of the waveforms.
  -s SAMPLE_RATE, --sample-rate SAMPLE_RATE
                        The sample rate of the waveforms.
  -m MF, --mf MF        The MF to use e.g. dtmf, mf.
  -d, --debug           Enable debug logging.
  -b BACKEND, --backend BACKEND
                        The backend to use for playing the waveforms.
  -r PAD_PAUSE_DURATION, --pad-pause-duration PAD_PAUSE_DURATION
                        The duration (ms) of the pause before/after sequence.
  -f FILE, --file FILE  The file to read the sequence from.
  -P PIPE, --pipe PIPE  Read the sequence from a pipe.
  -S, --stdin           Read the sequence from stdin.
  -i, --interactive     Enter interactive mode.
  -v, --version         show program's version number and exit
```

**Examples**

```
python ./bluebox.py -i
```

```
python ./bluebox.py 123456789
```

### API

You mainly need an `BaseMF` subclass instance and a `Sequencer` instance.

```python
from bluebox import DTMF
from bluebox.box import Sequencer

mf = DTMF()
seq = Sequencer(mf = mf)

seq('12345')
```


## Development

Development of different MF implementations and audio backends is extremely easy now.  Just create a new class that inherits from the MF class, and register it.
Same thing for audio backends.

Currently there are two MF implementations (DTMF and MF), and two audio backends (PyAudio and Dummy).


