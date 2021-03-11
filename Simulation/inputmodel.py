import numpy


def inspector1():
    data = open('servinsp1.dat').read().splitlines()
    return calculate_pdf_list(data)


def inspector22():
    data = open('servinsp22.dat').read().splitlines()
    return calculate_pdf_list(data)


def inspector23():
    data = open('servinsp23.dat').read().splitlines()
    return calculate_pdf_list(data)


def ws1():
    data = open('ws1.dat').read().splitlines()
    return calculate_pdf_list(data)


def ws2():
    data = open('ws2.dat').read().splitlines()
    return calculate_pdf_list(data)


def ws3():
    data = open('ws3.dat').read().splitlines()
    return calculate_pdf_list(data)


def calculate_pdf_list(data):
    data_placeholder = 0
    for i in range(0, 300):
        data_placeholder += float(data[i])
    mean = data_placeholder / 300
    return numpy.random.exponential(mean, 1)[0]*60


if __name__ == '__main__':
    print('Generate a Service Time: Inspector 1')
    print(inspector1())
    print('Generate Service Time: Inspector 2-2')
    print(inspector22())
    print('Generate Service Time: Inspector 2-3')
    print(inspector23())
    print('Generate Service Time: Workstation 1')
    print(ws1())
    print('Generate Service Time: Workstation 2')
    print(ws2())
    print('Generate Service Time: Workstation 3')
    print(ws3())



