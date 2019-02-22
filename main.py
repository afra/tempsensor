import temp
import time

print("Press CTRL-C to interupt within 5 seconds")
for _ in range(5):
    print(".")
    time.sleep(1)

temp.main()
