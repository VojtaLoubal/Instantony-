import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation,  PillowWriter

#Graf klasického řešení v dvojjámovém potenciálu při přítomnosti regulátoru e^{-i\alpha}

lmb, eta, tau_c = (1,1,0)
size, res = (100,10000) # velikost x-ové osy pro čas a počet bodů na vykreslení
tau = np.linspace(-size,size,res)
    
omega = np.sqrt(8*lmb*eta**2)

fig, (ax1,ax2) = plt.subplots(1,2, figsize = (10,5))

#Graf Re X(t), Im X(t)
line_re, = ax1.plot([],[], label = "Re X")
line_im, = ax1.plot([],[],label = "Im X")
ax1.set_xlim(-10,10) 
ax1.set_ylim(-2,2)
ax1.set_xlabel("$\\tau$")
ax1.set_ylabel("$X(\\tau)$")
ax1.legend()

line2, = ax2.plot([],[])
ax2.set_xlim(-3,3)
ax2.set_ylim(-3,3)
ax2.set_xlabel("Re X")
ax2.set_ylabel("Im X")

def x(tau,alpha):
    phase = np.e**(-1j*(alpha- np.pi/2))
    arg = (omega/2)*(tau-tau_c)*phase
    return eta*np.tanh(arg)

def update(frames):
    x_values = x(tau,frames)

    x_im = x_values.imag
    x_re = x_values.real
    line_re.set_data(tau,x_re)
    line_im.set_data(tau,x_im)
    line2.set_data(x_re,x_im)
    fig.suptitle(f"$\\alpha$ = {frames} \n $\\lambda$ = {lmb}, $\\eta$ = {eta}, $\\tau_c$ = {tau_c}, $\\tau \\in$ {(-size,size)}")
    return line_re,line_im,line2

ani = FuncAnimation(
    fig,
    update,
    frames = np.linspace(np.pi/2,0,100), #meze alfy - začíná v pi/2, končí v 0 a udělá se 100 snímků
    interval = 100 #rychlost snímků - jeden snímek co 100 ms
)

#Pokud chcete pouze graf a ne animaci, položte počet snímků v "frames" výše jako 1 a počáteční a koncový stav položte stejný

plt.show()

#Odstranit komentář, pokud chcete uložit jako gif pro dané parametry do daného adresáře
"""writer = PillowWriter(fps=30)
ani.save("C:/Users/vojta/Desktop/animation.gif", writer="pillow")"""
