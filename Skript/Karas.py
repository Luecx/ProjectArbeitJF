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
def printProgressBar(iteration, total, label, length=100, fill='#'):  # Progress Bar
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
        rho=0.00796,  # [kg/cm^3]                   #Dichte der Platte
        E_p=2.2 * 1e06,  # [kg/cm^2]                #E-Modul
        nue_p=0.3,  # [-]                           #Poissonzahl

        # Kugelmaterial
        # rho_g=0.00796, # [kg/cm^3]
        E_g=2.2 * 1e06,  # [kg/cm^2]                #E-Modul
        nue_g=0.3,  # [-]                           #Poissonzahl

        # Platte
        a=50.0,  # [cm]                             #Laenge der Platte
        b=50.0,  # [cm]                             #Breite der Platte
        h=1.0,  # [cm]                              #Hoehe der Platte

        # Kugel
        r=1.0,  # [cm]                              #Radius des Impaktors
        # m_g = 0.1, # [kg]

        mass_ratio=2,  # [-]                        #Massenverhältnis [Impaktormasse/Plattenmasse]
        v_0=440.0,  # [cm/sek]                      #Auftreffgeschwindigkeit

        # Impakt
        xi=25.0,  # [cm]                            #Auftreffstelle
        eta=25.0,  # [cm]                           #Auftreffstelle
        c=1.6 * 1e06,  # [kg/cm^3/2]                #Konstante aus der Hertz'schen Pressung

        # Auswertung
        x=25.0,  # [cm]                             #Auswertungsstelle
        y=25.0,  # [cm]                             #Auswertungsstelle

        stop_computation_after_first_impact=False,  # Berechnung nach dem ersten Aufschlag abbrechen
        iterations=1000,                            # Anzahl der Zeitschritte
        cosPreset=None,                             # Cosinusberechnung
        printLoadingBar=True                        # Anzeigen des Fortschritts

):

    # Konstanten

    # Masse des Impaktors ausgerechnet durch das Massenverhaeltnis und die Masse der Platte
    m_g = mass_ratio * a * b * h * rho

    # Material Konstante aus der Hertz'schen Pressung
    mat = 2 * ((((1 - nue_g ** 2) / E_g) + ((1 - nue_p ** 2) / E_p)) ** (-1))

    # Pressungskonstante
    c = np.sqrt((4 * r) / 9) * mat

    # Gravitationskonstante
    g = 981  # [cm/sek^2]

    # Vorfaktor nach Karas
    a_quer = np.sqrt((E_p * h ** 2 * g) / (12 * rho * (1 - nue_p ** 2)))

    # Faktor für die Berechnung der Auslenkung
    w_pre = 4 / ((np.pi ** 4) * (a_quer ** 2) * rho * h * a * b)


    # Zeitkonstanten

    # Anzahl der Intervalle
    num_inter = iterations
    # Schwingungsdauer der Platte
    Tg = 2 * np.pi / (np.pi ** 2 * a_quer * (1 / a ** 2 + 1 / b ** 2))
    # Schrittweite
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
            if (printLoadingBar):
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
    # 1. Naeherung
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

    # 2. Naeherung
    P[1] = c * z[1] ** (3 / 2) * g
    # P1 hier in [kg*cm/sek^2] einsetzen
    u[1] = v_0 * 1 * tau - (1 / m_g) * P[1] / 2 * 0.5 * tau ** 2

    w[1] = 0
    # P1 hier in [kg] einsetzen:
    w[1] += w_pre * P[1] / 2 * (cos[0] - cos[1])

    z[1] = u[1] - w[1]
    P[1] = c * z[1] ** (3 / 2) * g
    time[1] = tau

    # ------------------------------------------------------------------------------
    # A U S R E C H N E N   V O N   P_i

    for j in range(2, num_inter):

        if (printLoadingBar):
            printProgressBar(j, num_inter, "simulation")

        # 1. Naeherung
        # P_hilf[j-1]=P[j-1]/2
        P_hilf[j - 1] = (P[j - 1] + P[j - 2]) / 2
        P_hilf[j] = P[j - 1]

        u[j] = u[j - 1] + v[j - 1] * tau - (1 / m_g) * P_hilf[j] * 0.5 * tau ** 2
        for i in range(1, j + 1):
            w[j] += w_pre * P_hilf[i] * (cos[j - i] - cos[j - (i - 1)])
        z[j] = u[j] - w[j]
        if z[j] < 0:
            z[j] = 0

        # 2. Naeherung
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

            if (stop_computation_after_first_impact):
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

    P /= 100
    return time, j, tau, w, P, u, cos


# -----------------------------------------------------------------------------------------------------------
# A U S W E R T U N G S H I L F S M I T T E L

# Methode zur Berechnung der Aufschlaege
def countHits(F):
    c = 0
    for i in range(1, len(F)):
        if F[i] == 0.0 and F[i - 1] > 0:
            c += 1
    return c


# Methode zur Berechnung der maximalen Auslenkung
def maxW(W):
    return max(W)


# Methode zur Berechnung der maximalen Kraft
def maxP(Kraft):
    return max(Kraft)


# -----------------------------------------------------------------------------------------------------------
# P A R A M E T E R S T U D I E
#
# Schleifen der verschiedenen Parameter

# ----------------------------
# Geschwindigkeit

for v_0 in np.arange(100, 1010, 10):

    time, j, tau, w, P, u, cosPre = compute(mass_ratio=1, iterations=1000, printLoadingBar=False)
    for mr in np.arange(0.01, 2.51, 0.01):
        time, j, tau, w, P, u, cosPre = compute(v_0=v_0, mass_ratio=mr, iterations=1000, cosPreset=cosPre,
                                                printLoadingBar=False)
        with open("SpeedNeu.txt", "a") as myfile:
            myfile.write(str.format("%10f %10f %10f %10f %10f \n" % (v_0, mr, countHits(P), maxW(w), maxP(P))))
        with open("SpeedAuslenkung.txt", "a") as myfile:
            myfile.write(str.format("%10f %10f %10f \n" % (v_0, mr, maxW(w))))
        with open("SpeedKraft.txt", "a") as myfile:
            myfile.write(str.format("%10f %10f %10f \n" % (v_0, mr, maxP(P))))
        print("%10f %10f %10f %10f %10f" % (v_0, mr, countHits(P), maxW(w), maxP(P)))

# ----------------------------
# Hoehe

# for h in np.arange(0.5, 2.52, 0.02):
#
#     time, j, tau, w, P, u, cosPre = compute(h=h, mass_ratio=1, iterations=1000, printLoadingBar=False)
#     for mr in np.arange(0.01, 2.51, 0.01):
#         time, j, tau, w, P, u, cosPre = compute(h=h, mass_ratio=mr, iterations=1000, cosPreset=cosPre, printLoadingBar=False)
#         with open("HoeheNeu.dat", "a") as myfile:
#          myfile.write(str.format("%10f %10f %10f %10f %10f \n" % (h,mr,countHits(P),maxW(w),maxP(P))))
#         print("%10f %10f %10f %10f %10f" % (h,mr,countHits(P),maxW(w),maxP(P)))

# ----------------------------
# Impaktorradius

# for r in np.arange(0.5, 10.1, 0.1):
#
#     time, j, tau, w, P, u, cosPre = compute(r=r, mass_ratio=1, iterations=1000, printLoadingBar=False)
#     for mr in np.arange(0.01, 2.51, 0.01):
#         time, j, tau, w, P, u, cosPre = compute(r=r, mass_ratio=mr, iterations=1000, cosPreset=cosPre, printLoadingBar=False)
#         with open("Radius.txt", "a") as myfile:
#          myfile.write(str.format("%10f %10f %10f \n" % (r,mr,countHits(P))))
#         with open("RadiusAuslenkung.dat", "a") as myfile:
#          myfile.write(str.format("%10f %10f %10f \n" % (r,mr, maxW(w))))
#         with open("RadiusKraft.dat", "a") as myfile:
#          myfile.write(str.format("%10f %10f %10f \n" % (r,mr, maxP(P))))
#         print("%10f %10f %10f" % (r,mr,countHits(P)))

# ----------------------------
# Seitenverhaeltnis

# for sv in np.arange(1, 2.5, 0.05):
#
#     f = 2500
#     # sv = 2.5
#     b = (f / sv) ** 0.5
#     a = f / b
#
#     # time, j, tau, w, P, u, cosPre = compute(a=a, b=b, mass_ratio=2)
#
#     time, j, tau, w, P, u, cosPre = compute(a=a, b=b, mass_ratio=1, iterations=1000, xi=a / 2, eta=b / 2, printLoadingBar=True)
#     for mr in np.arange(2.5, 2.51, 0.01):
#         time, j, tau, w, P, u, cosPre = compute(a=a, b=b, mass_ratio=mr, iterations=1000, xi=a / 2, eta=b / 2, cosPreset=cosPre, printLoadingBar=True)
#         # with open("svmr.dat", "a") as myfile:
#         #     myfile.write(str.format("%10f %10f %10f %10f %10f \n" % (sv, mr, countHits(P), maxW(w), maxP(P))))
#     print(str((sv-1) / 4 * 100) + "%")
#
# sv = 2.3

#
# time, j, tau, w, P, u, cosPre = compute(a=a, b=b, mass_ratio=2.7, iterations=1000, xi=a / 2, eta=b / 2, printLoadingBar=True)


#      with open("Speed.txt", "a") as myfile:
#           myfile.write(str.format("%10f %10f %10f %10f %10f \n" % (sv, mr, countHits(P), maxW(w), maxP(P))))
#    print(str((sv-1) / 4 * 100) + "%")


# ----------------------------
# Auftreffstelle

# for xi_rel in np.arange(0.5,1,0.01):
#     for eta_rel in np.arange(0.5,xi_rel, 0.01):
#         time, j, tau, w, P, u, cosPre = compute(xi=xi_rel * 50, eta=eta_rel * 50, iterations=1000,
#                                                 printLoadingBar=False)
#         with open("xieta.txt", "a") as myfile:
#             myfile.write(str.format("%-10f %10f %10f %10f %10f \n" % (xi_rel, eta_rel, countHits(P), maxW(w), maxP(P))))
#             myfile.write(str.format("%-10f %10f %10f %10f %10f \n" % (eta_rel, xi_rel, countHits(P), maxW(w), maxP(P))))
#
#         print("%-10f %10f %10f %10f %10f \n" % (xi_rel, eta_rel, countHits(P), maxW(w), maxP(P)))
#
#
#     time, j, tau, w, P, u, cosPre = compute(xi=xi_rel * 50, eta=xi_rel * 50, iterations=1000,
#                                             printLoadingBar=False)
#     with open("xieta.txt", "a") as myfile:
#         myfile.write(str.format("%-10f %10f %10f %10f %10f \n" % (xi_rel, xi_rel, countHits(P), maxW(w), maxP(P))))
#
#     print("%-10f %10f %10f %10f %10f \n" % (xi_rel, xi_rel, countHits(P), maxW(w), maxP(P)))



# ------------------------------------------------------------------------------
# P L O T T E N   D E R   E R G E B N I S S E
#
fig, ax1 = plt.subplots()
ax1.set_xlabel('time[s]')
ax1.set_ylabel('Force [N]')
l1, = ax1.plot(time, P, 'r.', label='P')
ax1.tick_params(axis='y', colors='r')

ax2 = ax1.twinx()
ax2.set_ylabel('w,z [cm]')
l3, = ax2.plot(time, w, 'b.', label='w')
ax2.tick_params(axis='y', colors='b')

l4, = ax2.plot(time, u, "g.", label="u")

lines = [l1, l3]
plt.legend(lines, ["P", "w", "u"])
fig.tight_layout()
plt.show()


# ---------------------------------------------------------------------------------
# G I F    D A T A    C R E A T I O N
#
#
#
# dx = 2
# timesteps = 500
# a = 50
# b = 50
#
#
# dataCount = 0
# for x in range(int(a/2),a+dx,dx):
#     dataCount += 1
#
#
# data = np.zeros((dataCount, dataCount, timesteps))
#
# xIndex = 0
# for x in range(50,a +1,dx):
#     yIndex = 0
#     for y in range(int(b/2),b+1,dx):
#         time, j, tau, w, P, u, cosPre = compute(x=x,y=y,a=a,b=b,xi=a/2,eta=b/2,mass_ratio=0.1, iterations=timesteps, printLoadingBar=False)
#         # data[xIndex][yIndex] = np.asarray(w)
#         print(x,y)
#
#         with open("gifdata.dat", "a") as myfile:
#              myfile.write(str.format("%-10f %10f %10s\n" % (x, y, ' '.join(np.char.mod('%f', w)))))
#              myfile.write(str.format("%-10f %10f %10s\n" % (a-x, y, ' '.join(np.char.mod('%f', w)))))
#              myfile.write(str.format("%-10f %10f %10s\n" % (x, b-y, ' '.join(np.char.mod('%f', w)))))
#              myfile.write(str.format("%-10f %10f %10s\n" % (a-x, b-y, ' '.join(np.char.mod('%f', w)))))
#         yIndex += 1
#     xIndex += 1




# print(data)