import matplotlib.pyplot as plt
import numpy as np
hbar_c = 1970
mcs = .511e+6


def get_slope(arr):
    return (arr[0, 1] - arr[0, 0]) / (arr[1, 1] - arr[1, 0])


def get_eff(filename, c):
    eff_m = list()
    arr = np.genfromtxt(filename)
    arr[:, 0] = np.abs(arr[:, 0])
    e = 0
    while e < arr.shape[0]:
        f = 0
        g = 100
        try:
            while arr[e + f][1] == arr[e][1]:
                g = arr[e + f][0] if arr[e + f][0] < g else g
                f += 1
        except IndexError:
            break
        eff_m.append([arr[e + f - 1][1], g])
        e += f
    eff_m = np.array(eff_m)
    plt.plot(eff_m[:, 0], eff_m[:, 1])
    plt.show()
    num = int(input('select num\n'))
    energy = np.array(eff_m[num:, 0])
    k = np.array(eff_m[num:, 1])
    for i in range(11, k.size):
        if k[i] < k[i - 1]:
            print(i)
            k = k[:i]
            energy = energy[:i]
            break
    energy -= energy[0] + 0.001
    energy = np.abs(energy)
    energy = np.flip(energy)
    k = np.flip(k)
    k = k / (2 * np.pi) * c
    mass = k ** 2 / energy * hbar_c ** 2 / mcs
    eff_m_dict = dict()
    for i in range(len(mass)):
        eff_m_dict[round(energy[i], 2)] = mass[i]
    return eff_m_dict


if __name__ == '__main__':
    mass = get_eff('/home/jinho93/materials/oxides/perobskite/barium-titanate/cond/dense/bto.im', 3.03)
    plt.plot(mass.keys(), mass.values())
    arr = np.zeros((len(mass.keys()), 2))
    arr[:, 0] = list(mass.keys())
    arr[:, 1] = list(mass.values())
    np.savetxt('output', arr)
