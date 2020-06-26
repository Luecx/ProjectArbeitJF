# -*- coding: utf-8 -*-
"""
Stephan Kalapis - 03.04.2020

Skript zur analytischen Berechnung eines Impakts auf eine Kirchhoffsche Platte

Dieses Skript funktioniert mit folgenden Einheiten [cm,sek,kg], kein [N]!!
Dort wo [N] benötigt wird, muss [kg] mit gewichtskonstante [cm/sek**2] verrechnet werden
"""

# ------------------------------------------------------------------------------
# I M P O R T   V O N   M O D U L E N
import numpy as np
import matplotlib.pyplot as plt
from scipy import optimize
from sklearn.metrics import r2_score


# ------------------------------------------------------------------------------
# T O O L S
def printProgressBar(iteration, total, label, length=100, fill='#'):
    percent = ("{0:." + str(3) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% ' % (label, bar, percent), end="", flush=True)
    # Print New Line on Complete
    if iteration == total:
        print()


# ------------------------------------------------------------------------------
# V A R I A B L E N D E K L A R A T I O N


def compute(
        # Plattenmaterial
        rho=0.00796,  # [kg/cm^3]
        E_p=2.2 * 1e06,  # [kg/cm^2]
        nue_p=0.3,  # [-]

        #Kugelmaterial
        #rho_g=0.00796, # [kg/cm^3]
        E_g = 2.2 * 1e06, # [kg/cm^2]
        nue_g = 0.3, # [-]

        # Platte
        a=50.0,  # [cm]
        b=50.0,  # [cm]
        h=1.0,  # [cm]

        # Kugel
        r=1.0,  # [cm]
        # m_g = 0.1, # [kg]

        mass_ratio=0.5,  # [-]
        v_0=500.0,  # [cm/sek]

        # Stoß
        xi=25.0,  # [cm]
        eta=25.0,  # [cm]
        c=1.6 * 1e06,  # [kg/cm^3/2]

        # Auswertung
        x=25.0,  # [cm]
        y=25.0,  # [cm]

        stop_computation_after_first_impact=False,
        iterations=1000,
        cosPreset = None,
        printLoadingBar = True

):
    # Konstanten
    m_g = mass_ratio * a * b * h * rho
    mat = ( ((1 - nue_g ** 2) / E_g) + ((1 - nue_p ** 2) / E_p)) ** (-1)
    c = np.sqrt((4 * r) / 9) * mat
    g = 981  # [cm/sek^2]
    a_quer = np.sqrt((E_p * h ** 2 * g) / (12 * rho * (1 - nue_p ** 2)))
    w_pre = 4 / ((np.pi ** 4) * (a_quer ** 2) * rho * h * a * b)

    # Zeitkonstanten

    num_inter = iterations  # Anzahl der Intervalle
    Tg = 2 * np.pi / (np.pi ** 2 * a_quer * (1 / a ** 2 + 1 / b ** 2))
    tau = Tg / (2 * 180)  # [sek]

    # ------------------------------------------------------------------------------
    # A N L E G E N   V O N   A R R A Y S
    P = np.zeros(num_inter)
    w = np.zeros(num_inter)
    u = np.zeros(num_inter)
    z = np.zeros(num_inter)
    v = np.ones(num_inter) * v_0
    P_hilf = np.zeros(num_inter)
    time = np.zeros(num_inter)

    # ------------------------------------------------------------------------------
    # A U S R E C H N E N   V O N   C O S
    cos = np.zeros(num_inter + 1)
    if cosPreset is None:
        for j in range(0, num_inter + 1):
            if(printLoadingBar):
                printProgressBar(j, num_inter + 1, "generating S(k)")
            for m in range(1, 45, 1):
                for n in range(1, 45, 1):
                    cos[j] += \
                        np.sin(m * np.pi * x / a) * np.sin(n * np.pi * y / b) * \
                        np.sin(m * np.pi * xi / a) * np.sin(n * np.pi * eta / b) * \
                        np.cos(((m ** 2 / a ** 2) + (n ** 2 / b ** 2)) * np.pi ** 2 * a_quer * (j) * tau) / \
                        (m ** 2 / a ** 2 + n ** 2 / b ** 2) ** 2
    else:
        cos = cosPreset
    # ------------------------------------------------------------------------------
    # A U S R E C H N E N   V O N   P 1
    # j=1, da nur erstes Intervall betrachtet wird
    # 1. Näherung
    z[1] = v_0 * tau
    # mit g multiplizieren da sonst kraft in kg gegeben
    P[1] = c * z[1] ** (3 / 2) * g

    P1 = P[1] / 2
    # P1 bereits in [kg*cm/sek^2]
    u_P1 = v_0 * 1 * tau - (1 / m_g) * P1 * 0.5 * tau ** 2
    w_P1 = 0

    # P1 hier in [kg] einsetzen:
    w_P1 += w_pre * P1 * (cos[0] - cos[1])

    z[1] = u_P1 - w_P1
    v[1] = v_0 - (P[1] / 2 / m_g) * tau


    # 2. Näherung
    P[1] = c * z[1] ** (3 / 2) * g
    # P1 hier in [kg*cm/sek^2] einsetzen
    u[1] = v_0 * 1 * tau - (1 / m_g) * P[1] / 2 * 0.5 * tau ** 2

    w[1] = 0
    # P1 hier in [kg] einsetzen:
    w[1] += w_pre * P[1] / 2 * (cos[0]-cos[1])


    z[1] = u[1] - w[1]
    P[1] = c * z[1] ** (3 / 2) * g
    time[1] = tau


    # ------------------------------------------------------------------------------
    # A U S R E C H N E N   V O N   P_i

    for j in range(2, num_inter):

        if (printLoadingBar):
            printProgressBar(j, num_inter, "simulation")

        # 1. Näherung
        # P_hilf[j-1]=P[j-1]/2
        P_hilf[j - 1] = (P[j - 1] + P[j - 2]) / 2
        P_hilf[j] = P[j - 1]

        u[j] = u[j - 1] + v[j - 1] * tau - (1 / m_g) * P_hilf[j] * 0.5 * tau ** 2
        for i in range(1, j + 1):
            w[j] += w_pre * P_hilf[i] * (cos[j - i] - cos[j - (i - 1)])
        z[j] = u[j] - w[j]
        if z[j] < 0:
            z[j] = 0

        # 2. Näherung
        P[j] = c * z[j] ** (3 / 2) * g
        v[j] = v[j - 1] - (P_hilf[j] / m_g) * tau

        w[j] = 0
        u[j] = 0
        z[j] = 0

        P_hilf[j] = (P[j - 1] + P[j]) / 2

        u[j] = u[j - 1] + v[j - 1] * tau - (1 / m_g) * P_hilf[j] * 0.5 * tau ** 2

        for i in range(1, j + 1):
            w[j] += w_pre * P_hilf[i] * (cos[j - i] - cos[j - (i - 1)])
        z[j] = u[j] - w[j]

        if z[j] < 0:
            z[j] = 0

            if(stop_computation_after_first_impact):
                P = P[:j]
                w = w[:j]
                z = z[:j]
                u = u[:j]
                time = time[:j]
                break

        # Bestimmung P und v
        P[j] = c * z[j] ** (3 / 2) * g
        v[j] = v[j - 1] - (P_hilf[j] / m_g) * tau
        time[j] = j * tau

        # if np.isnan(z[j]):

    #     z[j]=0
    #   P[j]=0

    P /= 100
    return time, j, tau, w, P, u, cos


# ------------------------------------------------------------------------------
# L E A S T   S Q U A R E S - F I T
def test_P(x, P0, P1, P2, P3):
    return P0 * np.sin(x * P1 + P2) + P3


def test_w(x, w0, w1, w2, w3):
    return w0 * np.sin(x * w1 + w2) + w3



def countHits(F):
    c = 0
    for i in range(1,len(F)):
        if F[i] == 0.0 and F[i-1] > 0:
            c += 1
    return c

def maxW(W):
    w_max = 0
    for i in range(1, len(W)):
        if abs(W[i]) > abs(W[i-1]):
            w_max = abs(W[i])
    return w_max

def maxP(Kraft):
    f_max = 0
    for i in range(1, len(Kraft)):
        if Kraft[i] > Kraft[i-1]:
            f_max = Kraft[i]
    return f_max







# mr = 1
# time, j, tau, w, P, u, cosPre = compute(a=a, b=b, mass_ratio=mr, iterations=600,xi=a/2, eta=b/2)
# for i in range(40):
#     time, j, tau, w, P, u, cosPre = compute(a=a, b=b, mass_ratio=mr, iterations=600,xi=a/2, eta=b/2, cosPreset=cosPre)
#     if(countHits(P) > 2):
#         mr -= mr/2
#     else:
#         mr += mr/2
#     print(mr, countHits(P))




for r in np.arange(0.5,10.1,0.1):



    time, j, tau, w, P, u, cosPre = compute(r=r, mass_ratio=1, iterations=1000, printLoadingBar=False)
    for mr in np.arange(0.01,2.51,0.01):
        time, j, tau, w, P, u, cosPre = compute(r=r, mass_ratio=mr, iterations=1000, cosPreset=cosPre, printLoadingBar=False)
        with open("Radius.txt", "a") as myfile:
            myfile.write(str.format("%10f %10f %10f \n" % (r,mr,countHits(P))))
        with open("RadiusAuslenkung.txt", "a") as myfile:
            myfile.write(str.format("%10f %10f %10f \n" % (r,mr, maxW(w))))
        with open("RadiusKraft.txt", "a") as myfile:
            myfile.write(str.format("%10f %10f %10f \n" % (r,mr, maxP(P))))
        print("%10f %10f %10f" % (r,mr,countHits(P)))










































# paramp, paramp_covariance = optimize.curve_fit(test_P, time, P, maxfev=100000, p0=[100, 1/time[j - 1], 0, 20])
# paramw, paramw_covariance = optimize.curve_fit(test_w, time, w, maxfev=100000)

# P_fit = np.zeros(j)
# w_fit = np.zeros(j)
# for i in range(0, j):
#     P_fit[i] = test_P(time[i], paramp[0], paramp[1], paramp[2], paramp[3])
#     w_fit[i] = test_w(time[i], paramw[0], paramw[1], paramw[2], paramw[3])
# print('R^2 P:  ', r2_score(P, P_fit))
# print('R^2 w:  ', r2_score(w, w_fit))

# ------------------------------------------------------------------------------
# P L O T T E N   D E R   E R G E B N I S S E

fig, ax1 = plt.subplots()
ax1.set_xlabel('time[s]')
ax1.set_ylabel('Force [N]')
l1, = ax1.plot(time, P, 'r.', label='P')
# l2, = ax1.plot(time, test_P(time, paramp[0], paramp[1], paramp[2], paramp[3]), 'r-', label='P_fit')
ax1.tick_params(axis='y', colors='r')

ax2 = ax1.twinx()
ax2.set_ylabel('w,z [cm]')
l3, = ax2.plot(time, w, 'b.', label='w')
# l4, = ax2.plot(time, test_w(time, paramw[0], paramw[1], paramw[2], paramw[3]), 'b-', label='w_fit')
# ax2.plot(time,z,color='tab:cyan',label='z')
ax2.tick_params(axis='y', colors='b')

#l4, = ax2.plot(time, u, "g.", label="u")


# lines = [l1, l2, l3, l4]
# plt.legend(lines, ["P", "P_fit", "w", "w_fit"])
lines = [l1, l3]
#lines = [l1, l3, l4]
plt.legend(lines, ["P", "w", "u"])
fig.tight_layout()
plt.show()

# ------------------------------------------------------------------------------
# A U S W E R T U N G   M A X I M A L W E R T E

# maxw = np.where(w_fit == np.amax(w_fit))
# maxP = np.where(P_fit == np.amax(P_fit))
#
# print(np.amax(P_fit))

# DeltaT = np.absolute(maxw[0] - maxP[0]) * tau
