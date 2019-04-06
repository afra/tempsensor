The cable between D0 <> RST is required for the **deep-sleep**.V

| Micropython | Board | connect to |
| ----------- | ----- | ---------- |
| 0           | D3    |            |
| 2           | D4    | *(also Led1 but inverse)* |
| 4           | D2    | BME280 SCL |
| 5           | D1    | DHT22 data pin |
| 9           | D2    |            |
| 10          | D3    |            |
| 12          | D6    | BME280 SDA |
| 13          | D7    |            |
| 14          | D5    |            |
| 15          | D8    |            |
| 16          | D0    | to RST *(also Led2 but inverse)* |
| -           | RST   | conncet to D0 |


DHT22:

| DHT22 | connect to |
| ----- | ---------- |
| P1    | 3V3        |
| P2    | D1 + (10k to 3V3) |
| P3    | NC         |
| P4    | GND        |
