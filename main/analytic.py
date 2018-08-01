from cmath import exp, sqrt, sinh, pi

m0 = 0.511 * 1e+6 / 299792458 ** 2  # eV * (s / m) ** 2
h = 4.135667662 * 1e-15  # eV * s
h_ = 6.582119514e-16  # ev s
e = 1.602e-19  # C
q = e
k = 8.617343e-5  # eV / K
rich = 4 * pi * m0 * e * k ** 2 / h ** 3


def di(d, v, p1, p2, mr):
    m = mr * m0
    C = - (4 * e * m) / (9 * pi ** 2 * h_ ** 3)
    alpha = (4 * d * (2 * m) ** .5) / (3 * h_ * (p1 + v - p2))
    term_sinh: complex = 1.5 * alpha * (sqrt(p2 - v / 2) - sqrt(p1 + v / 2)) * v / 2
    term_exp: complex = alpha * (sqrt(p2 - v / 2) ** 3 - sqrt(p1 + v / 2) ** 3)
    term_rec: complex = (alpha ** 2 * (sqrt(p2 - v / 2) - sqrt(p1 + v / 2)) ** 2)
    return (C * exp(term_exp) * sinh(term_sinh) / term_rec).real


def fn(d, v, p1, p2, mr):
    m = mr * m0
    E = - v / (e * d) + (p2 - p1) / (e * d)
    C = e ** 3 * m0 / (16 * pi ** 2 * h_ * m)
    p = p2
    if v > 0:
        C = C
    else:
        C = -C
    try:
        return (C * E ** 2 / p * exp(-4 * (2 * m) ** 0.5 * p ** 1.5 / (3 * h_ * e * E))).real
    except OverflowError:
        print('over')


### sze ch8. TUNNEL DEVICES

def mis(temp, d, phi_t, shb, eta, v, mr):
    alpha = 2 * sqrt(2 * e * mr) / h
    return rich * temp ** 2 * exp(-alpha * d * sqrt(e * phi_t) - e * shb / k / temp) * (exp(e * v / eta / k / temp) - 1)


def dt_sze(d, phi0, v, mr):
    j0 = q ** 2 / (2 * pi * h * d ** 2)
    c = 4 * pi * d * sqrt(2 * mr * q) / h
    return j0 * (phi0 - v / 2) * exp(-c * sqrt(phi0 - v / 2)) - (phi0 + v / 2) * exp(-c * sqrt(phi0 + v / 2))


def fn_sze(phi0, ep, v, mr):
    ep0 = 8 * pi / 3 / h * sqrt(2 * mr * q) * phi0 ** 1.5
    j0 = q ** 2 * pow(e, 2) / (4 * pi * h * phi0) * (
            exp(-ep0 / ep) - (1 + 2 * v / phi0) * exp(-ep0 / ep * sqrt(1 + (2 * v / phi0))))


def simmon_low(phi, V, d):
    j0 = 3 * sqrt(2 * m0 * phi) / 2 / d * pow(e / h, 2)
    term_exp = -4 * pi * d / h * sqrt(2 * m0 * phi)
    return j0 * V * exp(term_exp)