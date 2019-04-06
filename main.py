import temp
import time

for i in range(5):
    print("Press CTRL-C to interupt within %s seconds" % (5 - i))
    time.sleep(1)

temp.main()
