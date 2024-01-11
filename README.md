# Python 3 Blue Box DTMF Tone Generator

Modernized python bluebox DTMF tone generator / dialer.

![BlueBox Phreaking](https://github.com/zeyus/Python3BlueBox/assets/75656/32f0c9c7-6c44-4e6e-ba3e-d10595398dcd)


## How it works

In essence, this is a simple utility that creates dual tone multi-frequency sine waves (50/50 mixed, but that can easily be adjusted). What does this mean? Well you know the sounds that you hear if you have the touchpad tones turned on when you dial a number in your phone? That's what this is. It's able to generate the tones that correspond to the number and output it to an audio device or a python `list` (for example).

This tool has a CLI interface which allows you to send a sequence of codes via `stdin`, pipes, files, as an argument, or in an interactive mode.

### Why?

Well, initially this was a fun little python 3 project from 2015, but I thought it would be nice to make it modern and extensible, essentially showcasing it as a framework, but this doesn't have to be limited to DTMF / MF, in theory with ease you could turn this into something that reads in code sequences (`str`) and outputs waves. Also due to issue #3 https://github.com/zeyus/Python3BlueBox/issues/3 it was clear that there were some bugs, so what better way to deal with it than adding tests and a way to decouple things!


## Installation

### PyPI

```
pip install mfbluebox
```

### Development

```
git clone https://github.com/zeyus/Python3BlueBox.git
cd PythonBlueBox
pip install .
```

### Requirements

- Python 3 (tested on 3.9 - 3.11)

## Usage

### CLI

```
python -m bluebox -h
```

Output:

```
usage: __main__.py [-h] [-l LENGTH] [-p PAUSE] [-a AMPLITUDE] [-s SAMPLE_RATE] [-m MF] [-d] [-b BACKEND] [-r PAD_PAUSE_DURATION] [-f FILE] [-P PIPE] [-S] [-i] [-v] [sequence]

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
python -m bluebox -i
```

```
python -m bluebox 123456789
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


