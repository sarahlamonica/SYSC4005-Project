from simpy.resources import container
import random
import inputmodel
import simpy
import numpy
from scipy import stats
import numpy


class CalculateCI:

    def calculateCI(d, confidence=0.95):

        if not isinstance(d, list):
            return d, 0
        n = len(d)
        if n is 0:
            return 0, 0
        mean, stdev = numpy.mean(d), stats.sem(d)

        result = stdev * stats.t.ppf((1 + confidence) / 2., n - 1)
        return mean, result

    def calculate_statistics(d):
        blockTimes1 = []
        blockTimes2 = []
        blockTimes3 = []
        idleTimes1 = []
        idleTimes2 = []
        idleTimes3 = []
        productsProduced1 = []
        productsProduced2 = []
        productsProduced3 = []

        for var in d:
            blockTimes1.extend(var.BlockTimes[1])
            blockTimes2.extend(var.BlockTimes[2])
            blockTimes3.extend(var.BlockTimes[3])
            idleTimes1.extend(var.IdleTimes[1])
            idleTimes2.extend(var.IdleTimes[2])
            idleTimes3.extend(var.IdleTimes[3])
            productsProduced1.append(var.Products[1])
            productsProduced2.append(var.Products[2])
            productsProduced3.append(var.Products[3])


class Variables:

    def __init__(self):
        self.ServiceTimes = {
            "inspector_1": [],
            "inspector_22": [],
            "inspector_23": [],
            "workstation_1": [],
            "workstation_2": [],
            "workstation_3": [],
        }

        self.Products = {
            1: 0,
            2: 0,
            3: 0,
        }

        self.BlockTimes = {
            1: [],
            2: [],
            3: []
        }

        self.IdleTimes = {
            1: [],
            2: [],
            3: [],
        }

    def AddInsp1_ServiceTime(self, val):
        self.ServiceTimes["inspector_1"].append(val)

    def AddInsp22_ServiceTime(self, val):
        self.ServiceTimes["inspector_22"].append(val)

    def AddInsp23_ServiceTime(self, val):
        self.ServiceTimes["inspector_23"].append(val)

    def AddWs1_ServiceTime(self, val):
        self.ServiceTimes["workstation_1"].append(val)

    def AddWs2_ServiceTime(self, val):
        self.ServiceTimes["workstation_2"].append(val)

    def AddWs3_ServiceTime(self, val):
        self.ServiceTimes["workstation_3"].append(val)

    def AddInsp1_BlockTime(self, val):
        self.BlockTimes[1].append(val)

    def AddInsp22_BlockTime(self, val):
        self.BlockTimes[2].append(val)

    def AddInsp23_BlockTime(self, val):
        self.BlockTimes[3].append(val)

    def AddWs1_IdleTimes(self, val):
        self.IdleTimes[1].append(val)

    def AddWs2_IdleTimes(self, val):
        self.IdleTimes[2].append(val)

    def AddWs3_IdleTimes(self, val):
        self.IdleTimes[3].append(val)

    def AddP1(self):
        self.Products[1] += 1

    def AddP2(self):
        self.Products[2] += 1

    def AddP3(self):
        self.Products[3] += 1


class Inspector1:

    def __init__(self, env, var, ws1, ws2, ws3):
        self.env = env
        self.var = var
        self.action = env.process(self.run())
        self.ws1 = ws1
        self.ws2 = ws2
        self.ws3 = ws3

    def run(self):

        while True:
            stime = inputmodel.inspector1()  # Generate random number for service time
            self.var.AddInsp1_ServiceTime(stime)

            is_alternative = False

            yield self.env.timeout(stime)
            btime = self.env.now
            if not is_alternative:
                # Finds the container with the smallest # of type 1 components
                if self.ws1.self_container.level <= self.ws2.container1.level or \
                        self.ws1.self_container.level <= self.ws3.container1.level:
                    yield self.ws1.self_container.put(1)

                elif self.ws2.container1.level <= self.ws3.container1.level:
                    yield self.ws2.container1.put(1)
                else:
                    yield self.ws3.container1.put(1)
                self.var.AddInsp1_BlockTime(self.env.now - btime)
            else:
                if self.ws3.container1.level <= self.ws2.container1.level or \
                        self.ws3.container1.level <= self.ws1.self_container.level:
                    yield self.ws3.container1.put(1)
                elif self.ws2.container1.level <= self.ws1.self_container.level:
                    yield self.ws2.container1.put(1)
                else:
                    yield self.ws1.self_container.put(1)
                self.var.AddInsp1_BlockTime(self.env.now - btime)


class Inspector2:

    def __init__(self, env, var, ws2, ws3):
        self.env = env
        self.var = var
        self.action = env.process(self.run())
        self.ws2 = ws2
        self.ws3 = ws3

    def run(self):
        while True:
            if bool(random.getrandbits(1)):  # Random for inspector choice
                stime = inputmodel.inspector22()  # Generate duration here
                self.var.AddInsp22_ServiceTime(stime)
                yield self.env.timeout(stime)
                btime = self.env.now
                yield self.ws2.container2.put(1)
                self.var.AddInsp22_BlockTime(self.env.now - btime)
            else:
                stime = inputmodel.inspector23()  # Generate duration here
                self.var.AddInsp23_ServiceTime(stime)
                yield self.env.timeout(stime)
                btime = self.env.now
                yield self.ws3.container3.put(1)
                self.var.AddInsp23_BlockTime(self.env.now - btime)


class Workstation1:

    def __init__(self, env, var):
        self.env = env
        self.var = var
        self.self_container = container.Container(self.env, 2)
        self.action = env.process(self.run())

    def run(self):
        while True:
            idlestart_time = self.env.now
            yield self.self_container.get(1)
            self.var.AddWs1_IdleTimes(self.env.now - idlestart_time)
            stime = inputmodel.ws1()  # From Random Generation
            self.var.AddWs1_ServiceTime(stime)
            yield self.env.timeout(stime)
            self.var.AddP1()


class Workstation2:

    def __init__(self, env, var):
        self.env = env
        self.var = var
        self.container1 = container.Container(self.env, 2)
        self.container2 = container.Container(self.env, 2)
        self.action = env.process(self.run())

    def run(self):
        while True:
            idlestart_time = self.env.now
            yield self.container1.get(1) & self.container2.get(1)
            self.var.AddWs2_IdleTimes(self.env.now - idlestart_time)
            stime = inputmodel.ws2()  # From Random Generation
            self.var.AddWs2_ServiceTime(stime)
            yield self.env.timeout(stime)
            self.var.AddP2()


class Workstation3:

    def __init__(self, env, var):
        self.env = env
        self.var = var
        self.container1 = container.Container(self.env, 2)
        self.container3 = container.Container(self.env, 2)
        self.action = env.process(self.run())

    def run(self):
        while True:
            idlestart_time = self.env.now
            yield self.container1.get(1) & self.container3.get(1)
            self.var.AddWs3_IdleTimes(self.env.now - idlestart_time)
            stime = inputmodel.ws3()  # From Random Generation
            self.var.AddWs3_ServiceTime(stime)
            yield self.env.timeout(stime)
            self.var.AddP3()


if __name__ == '__main__':

    replications = int(input("Enter Replications: ") or "1000")
    time = int(input("Enter time:  ") or "30000")
    varTemp = []

    for i in range(1, replications + 1):
        print("Starting replication: " + str(i))

        #  Environment setup
        envTemp = simpy.Environment()
        repVariables = Variables()

        # Set all variables
        workstation1 = Workstation1(envTemp, repVariables)
        workstation2 = Workstation2(envTemp, repVariables)
        workstation3 = Workstation3(envTemp, repVariables)
        inspector1 = Inspector1(envTemp, repVariables, workstation1, workstation2, workstation3)
        inspector_2 = Inspector2(envTemp, repVariables, workstation2, workstation3)

        # Run simulation
        envTemp.run(until=time)
        varTemp.append(repVariables)

    results = {
        "inspector_1": [],
        "inspector_22": [],
        "inspector_23": [],
        "workstation_1": [],
        "workstation_2": [],
        "workstation_3": [],

    }

    for i in varTemp:
        for key, value in i.ServiceTimes.items():
            results[key].extend(value)
    for key, value in results.items():
        print("" + key + " Average Service Time: " + str(numpy.mean(value)))

    def calculateCI(d, confidence=0.95):

        if not isinstance(d, list):
            return d, 0
        n = len(d)
        if n is 0:
            return 0, 0
        mean, stdev = numpy.mean(d), stats.sem(d)

        result = stdev * stats.t.ppf((1 + confidence) / 2., n - 1)
        return mean, result

    def calculateCIForEach(d):
        blockTimes1 = []
        blockTimes2 = []
        blockTimes3 = []
        idleTimes1 = []
        idleTimes2 = []
        idleTimes3 = []
        productsProduced1 = []
        productsProduced2 = []
        productsProduced3 = []

        for var in d:
            blockTimes1.extend(var.BlockTimes[1])
            blockTimes2.extend(var.BlockTimes[2])
            blockTimes3.extend(var.BlockTimes[3])
            idleTimes1.extend(var.IdleTimes[1])
            idleTimes2.extend(var.IdleTimes[2])
            idleTimes3.extend(var.IdleTimes[3])
            productsProduced1.append(var.Products[1])
            productsProduced2.append(var.Products[2])
            productsProduced3.append(var.Products[3])

        a, b = calculateCI(blockTimes1)
        print("Confidence Interval: Inspector 1, Block Times: " + str(a) + " ±" + str(b))
        c, d = calculateCI(blockTimes2)
        print("Confidence Interval: Inspector 2, Block Times: " + str(c) + " ±" + str(d))
        e, f = calculateCI(blockTimes3)
        print("Confidence Interval: Inspector 3, Block Times: " + str(e) + " ±" + str(f))
        g, h = calculateCI(idleTimes1)
        print("Confidence Interval: Workstation 1, Idle Times: " + str(g) + " ±" + str(h))
        i, j = calculateCI(idleTimes2)
        print("Confidence Interval: Workstation 2, Idle Times: " + str(i) + " ±" + str(j))
        l, m = calculateCI(idleTimes3)
        print("Confidence Interval: Workstation 3, Idle Times: " + str(l) + " ±" + str(m))
        o, p = calculateCI(productsProduced1)
        print("Confidence Interval: Products Produced 1: " + str(o) + " ±" + str(p))
        q, r = calculateCI(productsProduced2)
        print("Confidence Interval: Products Produced 2: " + str(q) + " ±" + str(r))
        s, t = calculateCI(productsProduced3)
        print("Confidence Interval: Products Produced 3: " + str(s) + " ±" + str(t))


    calculateCIForEach(varTemp)