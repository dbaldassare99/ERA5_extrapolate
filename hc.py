import pytropd as pyt

def sf(ar):
    V = ar
    Phi_sf_nh = np.zeros((np.shape(V)[0],)) # latitude of monthly NH Psi zero crossing
    Phi_sf_sh = np.zeros((np.shape(V)[0],)) # latitude of monthly SH Psi zero crossing
    for j in range(np.shape(V)[0]):
        # Default method = 'Psi500'
        Phi_sf_sh[j], Phi_sf_nh[j] = pyt.TropD_Metric_PSI(V[j,:,:], lat, lev) 
    return Phi_sf_sh,Phi_sf_nh

def uas(ar):
    V = ar
    Phi_sf_nh = np.zeros((np.shape(V)[0],)) # latitude of monthly NH Psi zero crossing
    Phi_sf_sh = np.zeros((np.shape(V)[0],)) # latitude of monthly SH Psi zero crossing
    for j in range(np.shape(V)[0]):
        # Default method = 'Psi500'
        Phi_sf_sh[j], Phi_sf_nh[j] = pyt.TropD_Metric_UAS(V[j,:], lat) 
    return Phi_sf_sh,Phi_sf_nh
