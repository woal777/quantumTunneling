import os
try:
    from quantum_mach import solve2
except ImportError:
    import solve2

if __name__ == "__main__":
    Solving_problem = solve2.SolvingProblem
    plt = solve2.plt
    directory = 'output'
    if not os.path.exists(directory):
        os.makedirs(directory)
    xmin = -0.1
    xmax = 0.15
    Effective_mass = 1.
    area = 2e-12
    unit = 1e+9
    s = Solving_problem(3e-09, area * unit, 0.24, 0.92, Effective_mass)
    x, y = s.main(xmin, xmax)
    with open(directory+'\\Nat_com_Au_down.dat', 'w') as f:
        for i, j in zip(x, y):
            f.write('%f\t%f\n' % (i, j))
    plt.plot(x, y, 'b')
    TER = y
    s = Solving_problem(3e-09, area * unit, 0.26, 0.78, Effective_mass)
    x, y = s.main(xmin, xmax)
    with open(directory+'\\Nat_com_Au_up.dat', 'w') as f:
        for i, j in zip(x, y):
            f.write('%f\t%f\n' % (i, j))
    plt.plot(x, y, 'r')
    TER = [s / r - 1 for r, s in zip(TER, y)]
    plt.grid(True)
    plt.minorticks_off()
    plt.ylim([-1, 3.5])
#    plt.show()

    s = Solving_problem(3e-09, area * unit, 0.30, 0.61, Effective_mass)
    x, y = s.main(xmin, xmax)
    with open(directory+'\\Nat_com_Cu_down.dat', 'w') as f:
        for i, j in zip(x, y):
            f.write('%f\t%f\n' % (i, j))
    plt.plot(x, y, 'r')
    TER = y
    s = Solving_problem(3e-09, area * unit, 0.37, 0.76, Effective_mass)
    x, y = s.main(xmin, xmax)
    with open(directory+'\\Nat_com_Cu_up.dat', 'w') as f:
        for i, j in zip(x, y):
            f.write('%f\t%f\n' % (i, j))
    plt.plot(x, y, 'b')
    TER = [s / r - 1 for r, s in zip(TER, y)]
    plt.ylim([-1, 3.5])
    plt.minorticks_off()
    plt.grid(True)
    plt.show()
