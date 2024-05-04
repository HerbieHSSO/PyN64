# PyN64
Nintendo 64 emulator written in python

### Compability

 - Executing some instructions;
 - Initial VI, PI, RI, MI support;
 - First Video Emulation;

The emulator doens't convert little-endian to big-endian.
use .Z64 Files Formats or convert .N64(little-endian) to Z64(big-endian)
You can Convert little-endian to big-endian with LEtoBE.py script, python LEtoBE.py [input.n64] [output.z64]

### Performance

Extremely slow, due to a lot of "trash code";
- Print Statements;
- Unnecessary Strings conversions;
- Unoptimized Code in general;

### Usage:
```
python main.py [rom path]
```

## Images

![image](https://user-images.githubusercontent.com/54962184/170876652-eb3c5fb7-ce6d-4191-8a32-4d98476186ed.png)

Running CPULW.N64 test from [PeterLemon-N64](https://github.com/PeterLemon/N64/)

![image](https://github.com/HerbieHSSO/PyN64/assets/54962184/0669077d-3c31-4a76-b909-920263ecf410)
