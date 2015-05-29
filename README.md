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

```./PythonBlueBox.py```

You'll see the '>>>' prompt. 

```>>> U12345O12345```

You can use the 'U' to switch to user tones or 'O' to switch to operator tones

The current tone mapping works as follows:

```python
user_tones = {
    '1': (user_freq[0], user_freq[4]),
    '2': (user_freq[0], user_freq[5]),
    '3': (user_freq[0], user_freq[6]),
    'A': (user_freq[0], user_freq[7]),
    '4': (user_freq[1], user_freq[4]),
    '5': (user_freq[1], user_freq[5]),
    '6': (user_freq[1], user_freq[6]),
    'B': (user_freq[1], user_freq[7]),
    '7': (user_freq[2], user_freq[4]),
    '8': (user_freq[2], user_freq[5]),
    '9': (user_freq[2], user_freq[6]),
    'C': (user_freq[2], user_freq[7]),
    '*': (user_freq[3], user_freq[4]),
    '0': (user_freq[3], user_freq[5]),
    '#': (user_freq[3], user_freq[6]),
    'D': (user_freq[3], user_freq[7]),
}

op_tones = {
    '1': (user_freq[0], user_freq[1]),
    '2': (user_freq[0], user_freq[2]),
    '3': (user_freq[1], user_freq[2]),
    '4': (user_freq[0], user_freq[3]),
    '5': (user_freq[1], user_freq[3]),
    '6': (user_freq[2], user_freq[3]),
    '7': (user_freq[0], user_freq[4]),
    '8': (user_freq[1], user_freq[4]),
    '9': (user_freq[2], user_freq[4]),
    '0': (user_freq[3], user_freq[4]),  # 0 or "10"
    'A': (user_freq[3], user_freq[4]),  # 0 or "10"
    'B': (user_freq[0], user_freq[5]),  # 11 or ST3
    'C': (user_freq[1], user_freq[5]),  # 12 or ST2
    'D': (user_freq[2], user_freq[5]),  # KP
    'E': (user_freq[3], user_freq[5]),  # KP2
    'F': (user_freq[4], user_freq[5]),  # ST
}
```