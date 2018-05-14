try:
    from quantum_mach import solve2
except ImportError:
    import solve2
import numpy as np
import matplotlib.pyplot as plt
if __name__ == "__main__":
    s = solve2.SolvingProblem(4.8e-09, 4.13e-12 * 1e+6, 0.48, .96, 1.)
    x, y = s.main(-0.3, .3)
    x, y = -x, -y
    with open('Nano-lett_up.dat', 'w') as f:
        for i, j in zip(x, y):
            f.write('%f\t%f\n' % (i, j * 1e+10))
    fig = plt.figure()
    fig.add_subplot(211)
    plt.plot(x, y, 'g')
    s = solve2.SolvingProblem(4.8e-09, 4.13e-12 * 1e+6, 0.24, 1.52, 1.)
    x, y = s.main(-0.3, .3)
    x, y = -x, -y
    fig.add_subplot(212)
    plt.plot(x, y, 'r')
    with open('Nano-lett_down.dat', 'w') as f:
        for i, j in zip(x, y):
            f.write('%f\t%f\n' % (i, j * 1e+10))
    # plt.ylim(-20, 10)
    plt.xticks(np.arange(-.35, .35, 0.1))
    plt.minorticks_off()
    plt.show()
    # x, y = s.main(1., 3.)
    # plt.semilogy(x, y, 'r')
    #    x, y, y2, y3 = s.main(0.48, 0.96, 10e-09, 20e-09, 1000)
    #    yf = [k1 + k2 + k3 for k1, k2, k3 in zip(y, y2, y3)]
    #    plt.semilogy(x, yf, 'g')
    # plt.semilogy(x, y, 'r', x, y2, 'g', x, y3, 'b')
