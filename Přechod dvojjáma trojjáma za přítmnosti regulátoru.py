import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter

#Animace klasického řešení při přechodu mezi dvojjámovým a trojjámovým potenciálem za přítomnosti obecné Wickovy rotace s natočením alpha

save = 0 #0 pro animaci, 1 pro uložit na plochu

alpha = np.pi/100 #Zafixujeme alfu

eta, lmb, xi, tau_c = (1,1,1,0)
size, resolution =(100, 10000)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12,9))

#Graf Re X(t), Im X(t)
line_re, = ax1.plot([], [], label="Re X")
line_im, = ax1.plot([], [], label="Im X")
ax1.set_xlim(-10, 10)
ax1.set_ylim(-5, 5)
ax1.set_xlabel("$\\tau$")
ax1.set_ylabel("$X(\\tau)$")
ax1.legend()

#Graf Re X vs Im X
line2, = ax2.plot([], [])
ax2.set_xlim(-5, 5)
ax2.set_ylim(-5, 5)
ax2.set_xlabel("Re X")
ax2.set_ylabel("Im X")

def X(tau, t):
    omega = np.sqrt(8*lmb*eta**2*((1-t)*eta**2+xi**2*t))
    phase = np.exp(-1j * (alpha - np.pi/2))
    u = (omega / 2) * (tau - tau_c) * phase

    threshold = 15  

    tanh_u = np.empty_like(u, dtype=complex)
    sech_sq = np.empty_like(u, dtype=complex)

    #Asymptotika kvůli numerice exponenciály
    large = np.abs(u.real) > threshold
    small = ~large

    tanh_u[small] = np.tanh(u[small])
    sech_sq[small] = 1 / np.cosh(u[small])**2

    tanh_u[large] = np.sign(u.real[large])
    sech_sq[large] = 0.0

    numerator = eta * xi * np.sqrt(t) * tanh_u
    den = np.sqrt(
        xi**2 * t + (1 - t) * eta**2 * sech_sq
    )

    #Konzistentní branch cut jelikož máme odmocninu ve jmenovateli
    for i in range(1, len(den)):
        if np.abs(den[i] - den[i-1]) > np.abs(-den[i] - den[i-1]):
            den[i] = -den[i]

    return numerator / (den + 0j)

tau_grid = np.linspace(-size,size,resolution)

def update(frames):
    X_values = X(tau_grid, frames)

    X_re = X_values.real
    X_im = X_values.imag

    line_re.set_data(tau_grid, X_re)
    line_im.set_data(tau_grid, X_im)

    line2.set_data(X_re, X_im)

    fig.suptitle(f"Přechod mezi dvojjámou a trojjámou v komplexní rovině \n t = {frames}, \n $\\alpha$ = $\\pi$/{round(np.pi/alpha)}, $\\lambda$ = {lmb}, $\\eta$ = {eta}, $\\xi$ = {xi} $\\tau_c$ = {tau_c}, $\\tau \\in$ {(-size,size)}")
    return line_re, line_im, line2

ani = FuncAnimation(
    fig, 
    update, 
    frames=np.linspace(1,0,50), #Bude se animovat t začínající v 1 a končící v 0 a udělá se 50 snímků - možno měnit
    interval=100) # Nový snímek se zobrazí co 100 ms

if save == 0:
    plt.show()

if save == 1:
    writer = PillowWriter(fps=30)
    ani.save("C:/Users/vojta/Desktop/prechod.gif", writer="pillow") #Možno uložit jako gif do daného adresáře, který si můžete zvolit
    print("Uloženo na plochu")