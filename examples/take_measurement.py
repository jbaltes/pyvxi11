#!/usr/bin/env python

# example to take measurements periodicly after trigger occured
# calculate simple statistics modes to the measurement values
# works with tektronix tds series

import sys
import time
import pyvxi11
import datetime

HOST = sys.argv[0]

def main():
    dev = pyvxi11.Vxi11(HOST)
    dev.open()
    dev.io_timeout = 10

    count = 4
    sum = 0
    square_sum = 0
    cube_sum = 0
    quad_sum = 0
    min = 0
    max = 0
    mean = 0
    rms = 0
    skewness = 0
    ekurtosis = 0

    print datetime.datetime.now().strftime('screen_%y-%m-%d_%Hh%Mm%S.png')
    start_second = int(datetime.datetime.now().strftime("%s"))
    dev.write('ACQUIRE:STATE ON')

    while True:
        state = dev.ask(':ACQ?').split(';')[1]
        if state == "STATE 0":
            # capture screenshot
            value = float(dev.ask('MEASUREMENT:MEAS1:VALUE?').split(' ')[1])
            count += 1
            if value > max:
                max = value
            if value < min:
                min = value
            sum += value
            square_sum += pow(value, 2)
            cube_sum += pow(value, 3)
            quad_sum += pow(value, 4)
            mean = sum / count
            rms = pow((square_sum - pow(sum, 2)/count) / (count-1), 0.5)
            skewness = cube_sum / pow(rms, 3) * count / (count-1) / (count-2)
            ekurtosis = ( quad_sum / pow(rms, 4) * \
                (count+1) / (count-1) - 3 * count ) * \
                count / (count-2) / (count-3)
            print "%i, %e, %e, %e, %e, %e, %e, %e" % \
                (count, value, min, max, mean, rms, skewness, ekurtosis)

            # reenable single shot
            dev.write('ACQUIRE:STATE ON')

    dev.close()

if __name__ == '__main__':
    main()
