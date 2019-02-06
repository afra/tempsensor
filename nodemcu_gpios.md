The cable between D0 <> RST is required for the **deep-sleep**.V

The outcome is the following:

Micropython | Board
0|D3
2|D4 (also Led1 but inverse)*
4|D2
5|D1 (DHT22 pin)
9|SD2
10|SD3
12|D6
13|D7
14|D5
15|D8
16|D0 to RST (also Led2 but inverse)*
RST|RST to 16|D0


DHT22:

P1|3V3
P2|D1 + (10k to 3V3)
P3|NC
P4|GND
