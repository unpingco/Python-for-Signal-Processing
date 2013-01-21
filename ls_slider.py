import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider 

fig, ax = plt.subplots()
#fig.set_size_inches(5,5)

plt.subplots_adjust(left=0.25, 
                    bottom=0.30,
#                     right=1,
                    )

x = np.linspace(0,2,50)
y = 1+x + 2*x**2 + 0*np.sin(2*np.pi*x) + np.random.randn(len(x))

V = np.matrix(np.vstack([np.ones(x.shape),x,x**2]).T)
Q = np.matrix(np.eye(V.shape[0]))
i,j =np.diag_indices_from(Q)
#Q[i[:20],j[:20]]=100
R = np.matrix(np.diag([1,1,1]))*.01

Pv = V*np.linalg.inv(V.T*Q*V+R)*V.T*Q
p=np.polyfit(x,y,2)

#d_line,=ax.plot(x,y,'o',label='data',alpha=0.3)
d=[ (ax.plot(i,j,'ob',alpha=0.8))[0] for i,j in zip(x,y) ]

ax.set_title('err^2=%3.2f'%(np.linalg.norm(y)**2 - np.linalg.norm(np.dot(Pv,y))**2 ))
ls_line,=ax.plot(x,np.dot(Pv,y).flat,label='projection')
ax.plot(x,np.polyval(p,x),'-',label='polyfit',alpha=0.3)
ax.legend(loc=0)
ax.grid()

axw0 = plt.axes([0.25, 0.2, 0.65, 0.03] )
sw0  = Slider(axw0, 'w0', 0.1, 30.0, valinit = 1)
axw1 = plt.axes([0.25, 0.15, 0.65, 0.03] )
sw1  = Slider(axw1, 'w1', 0.1, 30.0, valinit = 1)
axw2 = plt.axes([0.25, 0.10, 0.65, 0.03] )
sw2  = Slider(axw2, 'w2', 0.1, 30.0, valinit = 1)
scale_factor = 1.
##DEBUG scale_factor = np.mean(np.array(np.dot(Pv,y)).flatten()**2)
print scale_factor

def update_w0(val):
   w = sw0.val
   R[0,0]=w
   Pv = V*np.linalg.inv(V.T*Q*V+R)*V.T*Q
   err = np.array(np.dot(Pv,y)-y).flatten()**2
   err_scaled=err/scale_factor
   for i,j in zip(d,err_scaled) :
      i.set_color(plt.cm.gray(j))
   i=np.argsort(np.array(np.dot(Pv,y)-y).flatten()**2)
   ls_line.set_ydata(np.dot(Pv,y).flat)
   ax.set_title('err=%3.2f'%(err_scaled.mean()))
   print np.linalg.inv(V.T*Q*V+R)*V.T*Q
   plt.draw()
sw0.on_changed(update_w0)

def update_w1(val):
   w = sw1.val
   R[1,1]=w
   Pv = V*np.linalg.inv(V.T*Q*V+R)*V.T*Q
   err = np.array(np.dot(Pv,y)-y).flatten()**2
   err_scaled=err/scale_factor
   for i,j in zip(d,err_scaled) :
      i.set_color(plt.cm.gray(j))
   ls_line.set_ydata(np.dot(Pv,y).flat)
   ax.set_title('err=%3.2f'%(err_scaled.mean()))
   plt.draw()
sw1.on_changed(update_w1)

def update_w2(val):
   w = sw2.val
   R[2,2]=w
   Pv = V*np.linalg.inv(V.T*Q*V+R)*V.T*Q
   err = np.array(np.dot(Pv,y)-y).flatten()**2
   err_scaled=err/scale_factor
   for i,j in zip(d,err_scaled) :
      i.set_color(plt.cm.gray(j))
   ls_line.set_ydata(np.dot(Pv,y).flat)
   ax.set_title('err=%3.2f'%(err_scaled.mean()))
   plt.draw()
sw2.on_changed(update_w2)

plt.show()

