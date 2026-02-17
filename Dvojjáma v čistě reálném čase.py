import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import mpmath as mp

lmb, eta, t_0 = (1,1,0) # parametry
size, resolution = (100,1000) # velikost intervalu -t, t a počet bodů na vykreslení

t = np.linspace(-size,size,resolution)


fig, (ax1,ax2) = plt.subplots(1,2, figsize = (10,5))

#Re(t),Im(t) graf
line_re, = ax1.plot([],[], label = "Re X")
line_im, = ax1.plot([],[],label = "Im X")
ax1.set_xlim(-size,size) # velikost x-ové osy
ax1.set_ylim(-2,2) # velikost y-ové osy
ax1.set_xlabel("$\\tau$")
ax1.set_ylabel("$X(\\tau)$")
ax1.legend()

# Re vs Im graf
line2, = ax2.plot([],[])
ax2.set_xlim(-3,3) #velikost x-ové osy
ax2.set_ylim(-3,3) #velikost y-ové osy
ax2.set_xlabel("Re X")
ax2.set_ylabel("Im X")


def z(c,t):
    Ctilde = np.sqrt(c/(lmb*eta**4))
    a = np.sqrt(1+Ctilde)
    b = np.sqrt(1-Ctilde)
    m = (a/b)**2
    alpha = 1j*np.sqrt(2*lmb)*eta*b

    return eta*a*mp.ellipfun("sn",alpha*(t-t_0),m)


def update(frames):
    z_re = []
    z_im = []
    
    #Energie systému - začíná v 0 + 1i a končí v 0 + 0i
    c = 0 + 1j*frames

    for i in t:
        z_val = z(c,i)
        z_re.append(z_val.real)
        z_im.append(z_val.imag)

    line_re.set_data(t,z_re)
    line_im.set_data(t,z_im)
    line2.set_data(z_re,z_im)
    fig.suptitle(f"c = 0 + {frames}i \n $\\lambda$ = {lmb}, $\\eta$ = {eta}, t_0 = {t_0}, t $\\in$ {(-size,size)}")
    return line_re,line_im,line2

ani = FuncAnimation(
    fig,
    update,
    frames = np.linspace(1,0,100), #energie se mění jako 0 + i*frames, takže začíná pro 0 + 1i, končí pro 0+0i a udělá se 100 snímků - možno měnit
    interval = 1000 #rychlost snímků v ms
)

plt.show()

    
