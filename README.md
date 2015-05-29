Python 3 Blue Box DTMF Tone Generator
===================

Really simple, functional tone generator

**How it works**

Just type on a sequence of numbers/commands and press enter, your computer will play it back for you!

**Requirements**

- PyAudio https://people.csail.mit.edu/hubert/pyaudio/

```pip3 install pyaudio```

For OSX you need port audio, which you can install from homebrew:

```brew install portaudio```

For linux or windows, see your package manager, google it or visit here:

http://www.portaudio.com/download.html

**Usage**

```
./PythonBlueBox.py
```

You'll see the '>>>' prompt. 

```>>> U12345O12345```

You can use the 'U' to switch to user tones or 'O' to switch to operator tones

The current tone mapping works as follows:

```python
user_tones = {
    '1',
    '2',
    '3',
    'A',
    '4',
    '5',
    '6',
    'B',
    '7',
    '8',
    '9',
    'C',
    '*',
    '0',
    '#',
    'D',
}
op_tones = {
    '1',
    '2',
    '3',
    '4',
    '5',
    '6',
    '7',
    '8',
    '9',
    '0',  # 0 or "10"
    'A',  # 0 or "10"
    'B',  # 11 or ST3
    'C',  # 12 or ST2
    'D',  # KP
    'E',  # KP2
    'F',  # ST
}
```
