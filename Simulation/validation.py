import inputmodel


def validateIns1Comp1(i):
    actualAvg = 0
    rndAvg = 0
    data = open('servinsp1.dat').read().splitlines()

    for x in range(0, 300):
        actualAvg += float(data[x])
    actualAvg = actualAvg / 300

    for x in range(0, i):
        rndAvg += inputmodel.inspector1()
    rndAvg = rndAvg / i

    print('Inspector 1 Component 1: ')
    printAvg(actualAvg, rndAvg)


def validateIns2Comp2(i):
    actualAvg = 0
    rndAvg = 0
    data = open('servinsp22.dat').read().splitlines()

    for x in range(0, 300):
        actualAvg += float(data[x])
    actualAvg = actualAvg / 300

    for x in range(0, i):
        rndAvg += inputmodel.inspector22()
    rndAvg = rndAvg / i

    print('Inspector 2 Component 2: ')
    printAvg(actualAvg, rndAvg)


def validateIns2Comp3(i):
    actualAvg = 0
    rndAvg = 0
    data = open('servinsp23.dat').read().splitlines()

    for x in range(0, 300):
        actualAvg += float(data[x])
    actualAvg = actualAvg / 300

    for x in range(0, i):
        rndAvg += inputmodel.inspector23()
    rndAvg = rndAvg / i

    print('Inspector 2 Component 3: ')
    printAvg(actualAvg, rndAvg)


def validateWS1(i):
    actualAvg = 0
    rndAvg = 0
    data = open('ws1.dat').read().splitlines()
   
    for x in range(0, 300):
        actualAvg += float(data[x])
    actualAvg = actualAvg / 300

    for x in range(0, i):
        rndAvg += inputmodel.ws1()
    rndAvg = rndAvg / i

    print('Workstation 1: ')
    printAvg(actualAvg, rndAvg)


def validateWS2(i):
    actualAvg = 0
    rndAvg = 0
    data = open('ws2.dat').read().splitlines()

    for x in range(0, 300):
        actualAvg += float(data[x])
    actualAvg = actualAvg / 300

    for x in range(0, i):
        rndAvg += inputmodel.ws2()
    rndAvg = rndAvg / i

    print('Workstation 2: ')
    printAvg(actualAvg, rndAvg)


def validateWS3(i):
    actualAvg = 0
    rndAvg = 0
    data = open('ws3.dat').read().splitlines()

    for x in range(0, 300):
        actualAvg += float(data[x])
    actualAvg = actualAvg / 300

    for x in range(0, i):
        rndAvg += inputmodel.ws3()
    rndAvg = rndAvg / i

    print('Workstation 3: ')
    printAvg(actualAvg, rndAvg)


def printAvg(actualAvg, rndAvg):
    print('Actual Average: ', actualAvg)
    print('Random Average:', rndAvg)
    print('Difference(%): ', (abs(actualAvg-rndAvg)/actualAvg) * 100, '\n')


if __name__ == '__main__':
    #change sample size from 1000 to 10000
    validateIns1Comp1(1000)
    validateIns2Comp2(1000)
    validateIns2Comp3(1000)
    validateWS1(1000)
    validateWS2(1000)
    validateWS3(1000)
