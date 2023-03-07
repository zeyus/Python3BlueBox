Python 3 Blue Box DTMF Tone Generator
===================

Modernized python blue box

**How it works**

You can run this in interactive mode, or from a file, pipe, stdin, etc.

**Requirements**

- Python 3 (tested on 3.9 - 3.11)

**Installation**

```
git clone https://github.com/zeyus/Python3BlueBox.git
cd PythonBlueBox
pip install -r requirements.txt
```

**Usage**

```
./bluebox.py -h
```

**Examples**

```
./bluebox.py -i
```

```
./bluebox.py 123456789
```



**Development**

Development of different MF implementations and audio backends is extremely easy now.  Just create a new class that inherits from the MF class, and register it.
Same thing for audio backends.

Currently there are two MF implementations (DTMF and MF), and two audio backends (PyAudio and Dummy).
