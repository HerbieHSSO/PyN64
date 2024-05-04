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

Running CPULW.N64 test from [PeterLemon-N64]([https://github.com/PeterLemon/N64/](https://github.com/PeterLemon/N64/tree/master/CPUTest/CPU/LOADSTORE/LW))
![image](https://github.com/HerbieHSSO/PyN64/assets/54962184/0669077d-3c31-4a76-b909-920263ecf410)
Running HelloWorldCPU.N64 test from [PeterLemon-N64]([https://github.com/PeterLemon/N64/](https://github.com/PeterLemon/N64/tree/master/HelloWorld/32BPP))
![image](https://github.com/HerbieHSSO/PyN64/assets/54962184/a562fd13-2d0d-4940-bbcb-5555a04ec370)
