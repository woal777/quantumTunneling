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
    bo = True
    while e < len(arr[:, 0]) - 50 and bo:
        f = 0
        g = 1
        while arr[e + f][1] == arr[e][1]:
            g = arr[e + f][0] if arr[e + f][0] < g else g
            f += 1
        if arr[e + f][1] < 0:
            if eff_m[-2][1] > g:
                bo = False
        if bo:
            eff_m.append([arr[e + f - 1][1], g])
        e += f
    eff_m = np.array(eff_m)
    eff_m = np.flip(eff_m, axis=0)
    new_arr = []
    for i in range(1, eff_m.shape[0]):
        if eff_m[i, 1] > eff_m[i - 1, 1]:
            break
        else:
            new_arr.append(eff_m[i])

    new_arr = np.array(new_arr)
    new_arr[:, 0] -= new_arr[-1, 0]
    new_arr = np.abs(new_arr)
    new_arr = np.flip(new_arr, axis=0)
    new_arr[:, 0] += round(np.polyfit(new_arr[:2, 0], new_arr[:2, 1], deg=1)[1], 2)
    energy = np.array(new_arr[:, 0])
    k = np.array(new_arr[:, 1])
    k = k / (2 * np.pi) * c
    mass = k ** 2 / energy * hbar_c ** 2 / mcs
    eff_m_dict = dict()
    for i in range(len(mass)):
        eff_m_dict[round(energy[i], 2)] = mass[i]
    return eff_m_dict


if __name__ == '__main__':
    mass = get_eff('hf.im', 5.03)
    import matplotlib.pyplot as plt
    print(mass)
    plt.plot(mass.keys(), mass.values())
    plt.show()
