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

# Plattengeometrie
a = 400                 # [mm]
b = 400                 # [mm]
h = 8                   # [mm]

# Plattenmaterial
E = 2.2 * 1e08          # [N / mm^2]
nu = 0.3                # [-]
rho_p = 0.00000795      # [kg / mm^3]

# Kugeleigenschaft
r = 10                  # [mm]
rho_g = 0.000795      # [kg / mm^3]
v_0 = 1000              # [mm / sek]

# Erdbeschleunigung
g = 9810                # [mm / sek^2]

# Impaktpunkt
xi = 0.5
eta = 0.5

# Auswertung
x = xi
y = eta


# ------------------------------------------------------------------------------
# K O E F F Z I E N T N


# Kugelmasse
m_g = (4/3) * np.pi * r ** 3 * rho_g


# Koeffizient
a_quer = np.sqrt((E * h ** 2) / (12 * rho_p * (1 - nu ** 2)))



#Koeffizient für Herzsche Pressung
c = 1.6 * 1e04  # [kg/mm^3/2]

# Anzahl der Intervalle
num_inter = 1000

# Schwingdauer
Tg = 2 * np.pi / (np.pi ** 2 * a_quer * (1 / a ** 2 + 1 / b ** 2))

# Zeitkonstante
tau = Tg / 180  # [sek]

# # Annäherung
w_pre = 4 / ((np.pi ** 4) * (a_quer ** 2) * h * a * b)



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
S = np.zeros(num_inter + 1)
for k in range(0, num_inter + 1):
    for m in range(1, 45, 2):
        for n in range(1, 45, 2):
            S[k] += \
                np.sin((m * np.pi * x)/a)**2 * \
                np.sin((m * np.pi * y)/b)**2 * \
                np.cos(((m ** 2 / a ** 2) + (n ** 2 / b ** 2)) * np.pi ** 2 * a_quer * k * tau) / \
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
for m in range(1, 45, 2):
    for n in range(1, 45, 2):
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


#exit(-1)

# ------------------------------------------------------------------------------
# A U S R E C H N E N   V O N   P_i

for j in range(2, num_inter):
    # 1. Näherung
    # P_hilf[j-1]=P[j-1]/2
    P_hilf[j - 1] = (P[j - 1] + P[j - 2]) / 2
    P_hilf[j] = P[j - 1]

    u[j] = u[j - 1] + v[j - 1] * tau - (1 / m_g) * P_hilf[j] * g * 0.5 * tau ** 2
    for i in range(1, j + 1):
        w[j] += w_pre * P_hilf[i] * (S[j - i] - S[j - (i - 1)])
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
        w[j] += w_pre * P_hilf[i] * (S[j - i] - S[j - (i - 1)])
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

# ------------------------------------------------------------------------------
# L E A S T   S Q U A R E S - F I T
def test_P(x, P0, P1):
    return P0 * np.sin(x * P1)


def test_w(x, w0, w1):
    return w0 * np.sin(x * w1)


print(time, P)

paramp, paramp_covariance = optimize.curve_fit(test_P, time, P, maxfev=2000)
paramw, paramw_covariance = optimize.curve_fit(test_w, time, w, maxfev=2000)
P_fit = np.zeros(j)
w_fit = np.zeros(j)
for i in range(0, j):
    P_fit[i] = test_P(time[i], paramp[0], paramp[1])
    w_fit[i] = test_w(time[i], paramw[0], paramw[1])
print('R^2 P:  ', r2_score(P, P_fit))
print('R^2 w:  ', r2_score(w, w_fit))

# ------------------------------------------------------------------------------
# P L O T T E N   D E R   E R G E B N I S S E

fig, ax1 = plt.subplots()
ax1.set_xlabel('time[s]')
ax1.set_ylabel('Power [kg]')
l1, = ax1.plot(time, P, 'r.', label='P')
l2, = ax1.plot(time, test_P(time, paramp[0], paramp[1]), 'r-', label='P_fit')
ax1.tick_params(axis='y', colors='r')

ax2 = ax1.twinx()
ax2.set_ylabel('w,z [cm]')
l3, = ax2.plot(time, w, 'b.', label='w')
l4, = ax2.plot(time, test_w(time, paramw[0], paramw[1]), 'b-', label='w_fit')
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

DeltaT = np.absolute(maxw[0] - maxP[0]) * tau


