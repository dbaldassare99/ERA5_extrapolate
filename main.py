import xarray as xr
import numpy as np
import os
import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as st
import statsmodels.api as sm
import seaborn as sns
import hc

uf = #Location of zonal mean uas data
vf = #Location of zonal mean va data

lat = xr.open_dataset(vf)['lat'][:].values
lev = xr.open_dataset(vf)['level'][:].values
time = xr.open_dataset(vf)['time'][:].values.astype('datetime64[Y]')

vt = xr.open_dataset(vf)
vt = vt['v'][:].values
v = np.transpose(vt, (0,2,1))

ut = xr.open_dataset(uf)
ut = ut['u10'][:].values
u = ut

us,un = hc.uas(u)
sfs,sfn = hc.sf(v)

nd = {}
nd['UAS'] = un
nd['va'] = sfn

sd = {}
sd['UAS'] = us
sd['va'] = sfs

dm = dict.fromkeys(['NH','SH'])
di = dict.fromkeys(['NH','SH'])
dil = dict.fromkeys(['NH','SH'])
dih = dict.fromkeys(['NH','SH'])
dtl = dict.fromkeys(['NH','SH'])
dth = dict.fromkeys(['NH','SH'])
dt = dict.fromkeys(['NH','SH'])
nvd = dict.fromkeys(['NH','SH'])

for hem,dic in zip(['NH','SH'],[nd,sd]):
    m = dict.fromkeys(['UAS','va'])
    il = dict.fromkeys(['UAS','va'])
    ih = dict.fromkeys(['UAS','va'])
    tl = dict.fromkeys(['UAS','va'])
    th = dict.fromkeys(['UAS','va'])
    vd = dict.fromkeys(['UAS','va'])
    i = dict.fromkeys(['UAS','va'])
    t = dict.fromkeys(['UAS','va'])
    for meth in ['UAS','va']:
        y = dic[meth]
        x = np.arange(len(time))
        fit = st.linregress(x,y)
        yHat = fit.intercept + fit.slope*x
        mstd = np.std(y-yHat)
        m[meth] = np.mean(y[:-11])
        vd[meth] = mstd
        mod = sm.OLS(y, sm.add_constant(x))
        res = mod.fit()
        alpha = 0.05
        ci = res.conf_int(alpha)
        il[meth] = ci[0,0]
        ih[meth] = ci[0,1]
        tl[meth] = ci[1,0]
        th[meth] = ci[1,1]
        i[meth] = res.params[0]
        t[meth] = res.params[1]
    dm[hem] = m
    di[hem] = i
    dil[hem] = il
    dih[hem] = ih
    dtl[hem] = tl
    dth[hem] = th
    nvd[hem] = vd
    dt[hem] = t

#Plots of SF derived future HC width

lw = 2
for hem in ['NH','SH']:
    plt.subplots()
    for method in ['UAS','va']:
        x = np.arange(1979,2100,1)-1979
        yl = dil[hem][method] + dtl[hem][method]*x - dm[hem][method]
        yh = dih[hem][method] + dth[hem][method]*x - dm[hem][method]
        yf = di[hem][method] + dt[hem][method]*x - dm[hem][method]
        
        if method == 'va':
            plt.fill_between(x,yl,yh,color='blue',alpha=0.1,label='Ψ')
            plt.plot(x,yf,color='blue',linewidth=3)
        else:
            plt.fill_between(x,yl,yh,color='red',alpha=0.1,label='UAS')
            plt.plot(x,yf,color='red',linewidth=3)
        plt.xticks(x[1::20],np.arange(1979,2100,1)[1::20])
        plt.xlim([0,len(x)])
    plt.axhline(y=nvd[hem]['va']*2,linewidth=lw,linestyle='dashed',color='red')
    plt.axhline(y=nvd[hem]['UAS']*2,linewidth=lw,linestyle='dashed',color='blue')
    plt.axhline(y=nvd[hem]['va']*-2,linewidth=lw,linestyle='dashed',color='red')
    plt.axhline(y=nvd[hem]['UAS']*-2,linewidth=lw,linestyle='dashed',color='blue')
    plt.legend()

#Plots of uas derived future HC width
yll = []
yhl = []
yml = []
for hem in ['NH','SH']:
    plt.subplots()
    for method in ['UAS','va']:
        x = np.arange(1979,2100,1)-1979
        yl = dil[hem][method] + dtl[hem][method]*x - dm[hem][method]
        yh = dih[hem][method] + dth[hem][method]*x - dm[hem][method]
        yf = di[hem][method] + dt[hem][method]*x - dm[hem][method]
        
        if method == 'UAS':
            plt.fill_between(x,yl,yh,color='red',alpha=0.1,label='UAS')
            plt.plot(x,yf,color='red',linewidth=3)
            yll.append(yl)
            yhl.append(yh)
            yml.append(yf)
        plt.xticks(x[1::20],np.arange(1979,2100,1)[1::20])
        plt.xlim([0,len(x)])
    plt.axhline(y=nvd[hem]['UAS']*2,linewidth=lw,linestyle='dashed',color='blue')
    plt.axhline(y=nvd[hem]['UAS']*-2,linewidth=lw,linestyle='dashed',color='blue')
    plt.legend()
    
yls = yll[0]-yll[1]
yhs = yhl[0]-yhl[1]
yms = yml[0]-yml[1]
plt.subplots()
plt.fill_between(x,yls,yhs,color='red',alpha=0.1,label='UAS')
plt.plot(x,yms,color='red',linewidth=3)
plt.xticks(x[1::20],np.arange(1979,2100,1)[1::20])
plt.xlim([0,len(x)])
plt.legend()
plt.axhline(y=nvd['NH']['UAS']*2+nvd['SH']['UAS']*2,linewidth=lw,linestyle='dashed',color='blue')
