import numpy as np
name = 'Butterfly-Experimental'
nf = 398
nn = 1642

data = np.loadtxt('VFM_Displacements.txt',skiprows=3,usecols=(1,4,5))
data[:,0] = data[:,0] - 1

for i in range(nf):
    with open('%s_U_%d.csv'%(name,i+1),'w') as f:
        f.write('Node;U;V\n')
        np.savetxt(f,data[nn*i:nn*(i+1),:],fmt='%.14f',delimiter=';')


data = np.zeros((nn,3))
data[:,0] = np.arange(0,nn,1)
data[:,1:] = np.loadtxt('VFM_Coordinates.txt',delimiter=',')
with open('%s_Nodes.csv'%(name),'w') as f:
    f.write('Node;X;Y\n')
    np.savetxt(f,data,fmt='%.10f',delimiter=';')
