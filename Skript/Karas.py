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
# V A R I A B L E N D E K L A R A T I O N


def compute(
        # Material
        rho=0.00796,  # [kg/cm^3]
        E=2.2 * 1e06,  # [kg/cm^2]
        nue=0.3,  # [-]

        # Platte
        a=40,  # [cm]
        b=40,  # [cm]
        h=0.8,  # [cm]

        # Kugel
        #r=1,  # [cm]
        m_g = 1, # [kg]
        v_0=100,  # [cm/sek]

        # Stoß
        xi=20,  # [cm]
        eta=20,  # [cm]
        c=1.6 * 1e06,  # [kg/cm^3/2]

        # Auswertung
        x=20,  # [cm]
        y=20,  # [cm]

):
    # Konstanten
    g = 981  # [cm/sek^2]
    #m_g = (4 / 3) * np.pi * r ** 3 * rho
    a_quer = np.sqrt((E * h ** 2 * g) / (12 * rho * (1 - nue ** 2)))
    w_pre = 4 * g / ((np.pi ** 4) * (a_quer ** 2) * rho * h * a * b)

    # Zeitkonstanten

    num_inter = 100  # Anzahl der Intervalle
    Tg = 2 * np.pi / (np.pi ** 2 * a_quer * (1 / a ** 2 + 1 / b ** 2))
    tau = Tg / (2 * 720)  # [sek]

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
    for j in range(0, num_inter + 1):
        for m in range(1, 45, 1):
            for n in range(1, 45, 1):
                cos[j] += \
                    np.sin(m * np.pi * x / a) * np.sin(n * np.pi * y / b) * \
                    np.sin(m * np.pi * xi / a) * np.sin(n * np.pi * eta / b) * \
                    np.cos(((m ** 2 / a ** 2) + (n ** 2 / b ** 2)) * np.pi ** 2 * a_quer * (j) * tau) / \
                    (m ** 2 / a ** 2 + n ** 2 / b ** 2) ** 2

    # ------------------------------------------------------------------------------
    # A U S R E C H N E N   V O N   P 1
    # j=1, da nur erstes Intervall betrachtet wird
    # 1. Näherung
    z[1] = v_0 * tau
    P[1] = c * z[1] ** (3 / 2)
    P1 = P[1] / 2
    # P1 hier in [kg*cm/sek^2] einsetzen
    u_P1 = v_0 * 1 * tau - (1 / m_g) * P1 * g * 0.5 * tau ** 2
    w_P1 = 0
    # P1 hier in [kg] einsetzen:
    for m in range(1, 45, 1):
        for n in range(1, 45, 1):
            w_P1 += w_pre * P1 * (
                    np.cos(((m ** 2 / a ** 2) + (n ** 2 / b ** 2)) * np.pi ** 2 * a_quer * (1 - 1) * tau) - np.cos(
                ((m ** 2 / a ** 2) + (n ** 2 / b ** 2)) * np.pi ** 2 * a_quer * 1 * tau)) / (
                            m ** 2 / a ** 2 + n ** 2 / b ** 2) ** 2
    z[1] = u_P1 - w_P1
    v[1] = v_0 - (P[1] / 2 * g / m_g) * tau

    # 2. Näherung
    P[1] = c * z[1] ** (3 / 2)
    # P1 hier in [kg*cm/sek^2] einsetzen
    u[1] = v_0 * 1 * tau - (1 / m_g) * P[1] / 2 * g * 0.5 * tau ** 2
    w[1] = 0
    # P1 hier in [kg] einsetzen:
    for m in range(1, 45, 1):
        for n in range(1, 45, 1):
            w[1] += w_pre * P[1] / 2 * (
                    np.cos(((m ** 2 / a ** 2) + (n ** 2 / b ** 2)) * np.pi ** 2 * a_quer * (1 - 1) * tau) - np.cos(
                ((m ** 2 / a ** 2) + (n ** 2 / b ** 2)) * np.pi ** 2 * a_quer * 1 * tau)) / (
                            m ** 2 / a ** 2 + n ** 2 / b ** 2) ** 2
    z[1] = u[1] - w[1]
    P[1] = c * z[1] ** (3 / 2)
    time[1] = tau

    # ------------------------------------------------------------------------------
    # A U S R E C H N E N   V O N   P_i

    for j in range(2, num_inter):
        # 1. Näherung
        # P_hilf[j-1]=P[j-1]/2
        P_hilf[j - 1] = (P[j - 1] + P[j - 2]) / 2
        P_hilf[j] = P[j - 1]

        u[j] = u[j - 1] + v[j - 1] * tau - (1 / m_g) * P_hilf[j] * g * 0.5 * tau ** 2
        for i in range(1, j + 1):
            w[j] += w_pre * P_hilf[i] * (cos[j - i] - cos[j - (i - 1)])
        z[j] = u[j] - w[j]
        if z[j] < 0:
            z[j] = 0

        # 2. Näherung
        P[j] = c * z[j] ** (3 / 2)
        v[j] = v[j - 1] - (P_hilf[j] * g / m_g) * tau

        w[j] = 0
        u[j] = 0
        z[j] = 0

        P_hilf[j] = (P[j - 1] + P[j]) / 2

        u[j] = u[j - 1] + v[j - 1] * tau - (1 / m_g) * P_hilf[j] * g * 0.5 * tau ** 2

        for i in range(1, j + 1):
            w[j] += w_pre * P_hilf[i] * (cos[j - i] - cos[j - (i - 1)])
        z[j] = u[j] - w[j]

        if z[j] < 0:
            z[j] = 0
            P = P[:j]
            w = w[:j]
            z = z[:j]
            u = u[:j]
            time = time[:j]
            break

        # Bestimmung P und v
        P[j] = c * z[j] ** (3 / 2)
        v[j] = v[j - 1] - (P_hilf[j] * g / m_g) * tau
        time[j] = j * tau

        # if np.isnan(z[j]):

    #     z[j]=0
    #   P[j]=0

    return time, j, tau, w, P,


# ------------------------------------------------------------------------------
# L E A S T   S Q U A R E S - F I T
def test_P(x, P0, P1, P2, P3):
    return P0 * np.sin(x * P1 + P2) + P3


def test_w(x, w0, w1, w2, w3):
    return w0 * np.sin(x * w1 + w2) + w3


time, j, tau,  w, P = compute()

paramp, paramp_covariance = optimize.curve_fit(test_P, time, P, maxfev=100000, p0=[100, 1/time[j - 1], 0, 20])
paramw, paramw_covariance = optimize.curve_fit(test_w, time, w, maxfev=100000)

P_fit = np.zeros(j)
w_fit = np.zeros(j)
for i in range(0, j):
    P_fit[i] = test_P(time[i], paramp[0], paramp[1], paramp[2], paramp[3])
    w_fit[i] = test_w(time[i], paramw[0], paramw[1], paramw[2], paramw[3])
print('R^2 P:  ', r2_score(P, P_fit))
print('R^2 w:  ', r2_score(w, w_fit))

# ------------------------------------------------------------------------------
# P L O T T E N   D E R   E R G E B N I S S E

fig, ax1 = plt.subplots()
ax1.set_xlabel('time[s]')
ax1.set_ylabel('Power [kg]')
l1, = ax1.plot(time, P, 'r.', label='P')
l2, = ax1.plot(time, test_P(time, paramp[0], paramp[1], paramp[2], paramp[3]), 'r-', label='P_fit')
ax1.tick_params(axis='y', colors='r')

ax2 = ax1.twinx()
ax2.set_ylabel('w,z [cm]')
l3, = ax2.plot(time, w, 'b.', label='w')
l4, = ax2.plot(time, test_w(time, paramw[0], paramw[1], paramw[2], paramw[3]), 'b-', label='w_fit')
# ax2.plot(time,z,color='tab:cyan',label='z')
ax2.tick_params(axis='y', colors='b')

lines = [l1, l2, l3, l4]
plt.legend(lines, ["P", "P_fit", "w", "w_fit"])
fig.tight_layout()
plt.show()

# ------------------------------------------------------------------------------
# A U S W E R T U N G   M A X I M A L W E R T E

maxw = np.where(w_fit == np.amax(w_fit))
maxP = np.where(P_fit == np.amax(P_fit))

print(np.amax(P_fit))

DeltaT = np.absolute(maxw[0] - maxP[0]) * tau
