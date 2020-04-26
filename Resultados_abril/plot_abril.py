# -*- coding: utf-8 -*-
"""
Editor de Spyder

Este es un archivo temporal.
"""

import numpy as np
import matplotlib.pyplot as plot

#Load Data
data_0320 = np.loadtxt("resultados_0320.txt", delimiter ='\t')
data_0327 = np.loadtxt("resultados_0327.txt", delimiter ='\t')
data_0401_1 = np.loadtxt("resultados_0401_1.txt", delimiter ='\t')
data_0401_2 = np.loadtxt("resultados_0401_2.txt", delimiter ='\t')

plot.style.use("seaborn-deep")
figure = plot.figure(constrained_layout = True)
grid = figure.add_gridspec(4,4)

ax_mu = figure.add_subplot(grid[2:,:])
ax_OD = figure.add_subplot(grid[0:2,:],sharex = ax_mu)

plot.setp(ax_OD.get_xticklabels(), visible = False)

ln1, = ax_OD.plot(data_0320[:,0],data_0320[:,2], label = '$1^{ra}$')
ln2, = ax_OD.plot(data_0327[:,0],data_0327[:,1], label = '$2^{da}$')
ln3, = ax_OD.plot(data_0401_1[:,0],data_0401_1[:,1], label = '$3^{ra}$')
ln4, = ax_OD.plot(data_0401_2[:,0],data_0401_2[:,1], label = '$4^{ta}$')
ax_OD.set_yscale("log")
ax_OD.set_yticks([0.2,0.4,0.6,0.8,0.9,1])
ax_OD.set_yticklabels([0.2,0.4,0.6,1])
ax_OD.set_ylim(0, 1.2)
ax_OD.set_ylabel("$D.O._{600nm}$")
ax_OD.legend()

ln5, = ax_mu.plot(data_0320[:, 0], data_0320[:, 3])
ln6, = ax_mu.plot(data_0327[:, 0], data_0327[:, 2])
ln7, = ax_mu.plot(data_0401_1[:, 0], data_0401_1[:, 2])
ln8, = ax_mu.plot(data_0401_2[:, 0], data_0401_2[:, 2])
ax_mu.set_ylabel("$ \mu (h^{⁻1})$")
ax_mu.set_xlabel("Tiempo (h)")
ax_mu.set_xlim(0)
figure2, ax_sg = plot.subplots()
ln9, = ax_sg.plot(data_0320[:,0], data_0320[:,1], label = "Sin Filtro")
ln10, = ax_sg.plot(data_0320[:,0], data_0320[:,2], label = "Filtro Savitzky-Golay")
ax_sg.legend()
ax_sg.set_xlabel("Tiempo (h)")
ax_sg.set_ylabel("$D.O._{600nm}$")
ax_sg.set_yscale("log")
ax_sg.set_yticks([0.2,0.4,0.6,0.8,0.9,1])
ax_sg.set_yticklabels([0.2,0.4,0.6,0.8,0.9,1])
ax_sg.set_xlim(0)
plot.tight_layout()

figure.savefig('cineticas_abril.png')
figure2.savefig('ejemplo_filtro_sg.png')

plot.show()
