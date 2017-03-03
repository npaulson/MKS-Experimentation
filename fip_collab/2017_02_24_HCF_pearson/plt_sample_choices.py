import matplotlib.pyplot as plt
import numpy as np
import matplotlib.cm as cm


fig = plt.figure(figsize=[6, 3.5])

x = np.linspace(-1, 1, 101)
y1 = np.zeros(x.shape)
y2 = np.zeros(x.shape)
y2[:50] = np.linspace(0, 1, 51)[:-1]
y2[50:] = np.linspace(1, 0, 51)

plt.plot(x, y2, color=cm.viridis(0.7), linewidth=3, label='upper bound')
plt.plot(x, y1, color=cm.viridis(0.9), linewidth=3, label='lower bound')

plt.xticks([-1.0, 0.0, 1.0], [r'$-s_o$', '0', r'$s_o$'], fontsize=20)
plt.yticks([0.0, 1.0], [r'$c_2 s_o$', r'$s_o \left(c_2 + c_3\right)$'], fontsize=20)

plt.axis([-1.1, 1.1, -0.1, 1.3])

plt.xlabel(r'$m_t$', fontsize=20)
plt.ylabel(r'$s_t$', fontsize=25)

# plt.grid(linestyle='-', alpha=0.15)
plt.legend(loc='upper center', shadow=False, fontsize=13, ncol=2)

plt.tight_layout()

plt.show()
