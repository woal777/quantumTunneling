try:
    from quantum_mach import solve2
except ImportError:
    import solve2
import numpy as np

if __name__ == "__main__":
    Solving_problem = solve2.SolvingProblem
    plt = solve2.plt
    s = Solving_problem(4.6e-09, 1e-4, 0.2, 1.45, 0.22)
    x, y = s.main(-.45, .45)
    with open('APL_Mater_r.dat', 'w') as f:
        for i, j in zip(x, y):
            f.write('%f\t%f\n' % (-i, -j))
    plt.plot(-x, -y, 'r')
    s = Solving_problem(4.6e-09, 1e-4, 0.2, 1.67, .205)
    x, y = s.main(-.45, .45)
    with open('APL_Mater_o.dat', 'w') as f:
        for i, j in zip(x, y):
            f.write('%f\t%f\n' % (-i, -j))
    plt.plot(-x, -y, '#FF8C00')
    s = Solving_problem(4.6e-09, 1e-4, 0.2, 2.05, .205)
    x, y = s.main(-.45, .45)
    with open('APL_Mater_g.dat', 'w') as f:
        for i, j in zip(x, y):
            f.write('%f\t%f\n' % (-i, -j))
    plt.plot(-x, -y, 'g')
    s = Solving_problem(4.6e-09, 1e-4, 0.2, 2.84, .16)
    x, y = s.main(-.45, .45)
    with open('APL_Mater_b.dat', 'w') as f:
        for i, j in zip(x, y):
            f.write('%f\t%f\n' % (-i, -j))
    plt.plot(-x, -y, 'b')
    plt.xlim(-.55, 0.55)
    plt.ylim(-20, 10)
    plt.xticks(np.arange(-.55, .55, 0.2))
    plt.minorticks_off()
    plt.show()
    # x, y = s.main(1., 3.)
    # plt.semilogy(x, y, 'r')
    #    x, y, y2, y3 = s.main(0.48, 0.96, 10e-09, 20e-09, 1000)
    #    yf = [k1 + k2 + k3 for k1, k2, k3 in zip(y, y2, y3)]
    #    plt.semilogy(x, yf, 'g')
    # plt.semilogy(x, y, 'r', x, y2, 'g', x, y3, 'b')
    plt.show()
