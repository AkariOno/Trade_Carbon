import numpy as np
import pandas as pd
import math
import copy


class onesector():
    def __init__(self,
                # Metadata
                year, # year of the data
                countries, # list of ISO3 codes 
                
                #Equilibrium outcome
                X, # trade flow (NxN ndarrary)
                wL, # labor compensation
                ##rK, # rental payment

                # Fundamental parameters
                theta = 4, #trade elastisity (in this model, this is sigma - 1)
                nu = 1,

                # Deep parameter
                #tau = None, # tech. parameter
                #beta_L = None, # labor intensity
                #beta_K = None, # capital intensity
                #L = None, # labor endowment
                #K = None, # capital endowment
                #D = None, # trade deficit
            ):
            
            # Set country list and year and model
            self.year, self.countries = year, countries
            self.N = len(countries) # length in R

            # Set parameters
            self.theta = theta
            self.nu = nu
            self.X = X
            self.wL = wL
            #self.rK = rK

            # Set data
            # Calculate absorption, production, trade deficit
            self.Xm = np.sum(X, axis=(0))
            self.Ym = np.sum(X, axis=(1))
            self.D = self.Xm - self.Ym 

    @staticmethod #skip above
    def from_static_parameters(
        # Metadata
        countries, # list of ISO3 codes: list(N)
        year, # year of the data we use: int

        # Elasticity
        theta, # trade elasticity: ndarrary(S)
        nu, # Intertemporal substitution

        # Deep parameters
        tau, # tech. parameter: ndarrary(S)
        beta_L, # cost share on labor: ndarrary(N)
        #beta_K, # cost share on capital:  ndarrary(N)
        L, # labor endowment: ndarrary(N)
        #K, # capital endowment: ndarrary(N)
        D,
    ):
        # Set sum convergence parameter
        phi = 0.1 # convergence speed
        tol = 0.00001 # convergence tolerance
        dif = 1 # initial convergence criterion

        # Start solving
        N = len(countries)
        w = np.ones(N)
        #r = np.ones(N)

        # Normalization
        w = w / np.sum(w*L)
        #r = r / np.sum(w*L + r*K)

        while dif > tol:
            # Updata w and r
            w_old = np.copy(w)
            #r_old = np.copy(r)

            # Calculate price
            p = np.zeros((N,N))
            for OR, DE in np. ndindex((N,N)):
                p[OR, DE] = w[OR]**beta_L[OR]*tau[OR, DE] # definition of p_ij

            # Calculate pi
            pi_num = np.zeros((N,N)) # p_ij(^theta)
            pi_den = np.zeros((N)) # sum of p_ij
            pi = np.zeros((N,N))
            for OR, DE in np.ndindex((N,N)):
                pi_num[OR, DE] = p[OR, DE]**(-theta)
                pi_den[DE] += pi_num[OR, DE]
            for OR, DE in np.ndindex((N,N)):
                pi[OR, DE] = pi_num[OR,DE] / pi_den[DE]
            
            # Calculate price index
            P = pi_den**(-1/theta)

            # Caluculate excess factor demand
            wLS = w*L
            #rKS = r*K
            Xm = wLS + D

            wLD = np.zeros((N))
            #rKD = np.zeros((N))
            for OR, DE in np.ndindex((N,N)):
                wLD[OR] += beta_L[OR]*pi[OR, DE]*Xm[DE]
                #rKD[OR] += beta_K[OR]*pi[OR, DE]*Xm[DE]
            ZL = (wLD - wLS)/w
            #ZK = (rKD -rKS)/r

            w = w*(1 + phi/L*ZL)
            #r = r*(1 + phi/K*ZK)

            #dif = max(np.max(np.abs(w - w_old)))
            dif = np.max(np.abs(ZL))

        # Define economic size
        WGDP = np.sum(w*L) #WGDP = np.sum(w*L + r*K)            
        w = w/WGDP
        # r = r/WGDP
        Xm = w*L + D
        X = np.zeros((N,N))
        for OR, DE in np.ndindex((N,N)):
            X[OR, DE] = pi[OR, DE]*Xm[DE]
        wL = w*L
        #rK = r*K
        return onesector(year=year, countries=countries, theta=theta, nu=nu, X=X, wL=wL)
    

    # Exaxt hat algebra -----------------------
    def exacthatalgebra(self, tauhat):
        # Set convergence parameter
        phi = 0.1 # convergence speed
        tol = 0.00001 # convergence tolerance
        
        # Start solving
        N = self.N
        w = np.ones(N)
        theta = self.theta

        # Setting boxes
        X1 = np.zeros((N,N))

        # Initial Exacthat
        what = np.ones(N)

        # Normalization
        WGDP = np.sum(what*self.wL) #WGDP = np.sum(w*L + r*K)            
        what = what/WGDP

        dif = 1

        # Calculate beta_L
        beta_L = np.ones((N))

        # Calculate pi
        pi = np.zeros((N,N))
        for OR, DE in np.ndindex((N,N)):
            pi[OR, DE] = self.X[OR, DE]/self.Xm[DE]

        while dif > tol:
            # Updata w and r
            what_old = np.copy(what)

            # Calculate price (phat) and price index (Phat)
            phat = np.zeros((N,N))
            Phat = np.zeros((N))
            for OR, DE in np.ndindex((N,N)):
                phat[OR, DE] = what[OR]**beta_L[OR]*tauhat[OR, DE]
                Phat[DE] += pi[OR, DE]*phat[OR, DE]**(-theta)
            Phat = Phat**(-1/theta)

            # Calculate pi
            pihat = np.zeros((N,N))
            for OR, DE in np.ndindex((N,N)):
                pihat[OR, DE] = phat[OR, DE]**(-theta) / Phat[DE]**(-theta)

            # Caluculate excess factor demand and supply
            wLS1 = what*(self.wL)
            wLD1 = np.zeros((N))
            Xm1 = wLS1 + self.D

            for OR, DE in np.ndindex((N,N)):
                wLD1[OR] += pi[OR, DE]*pihat[OR, DE]*Xm1[DE]
            ZL = (wLD1 - wLS1)/what

            what = what*(1 + phi/self.wL*ZL)

            #dif = max(np.max(np.abs(w - w_old)))
            dif = np.max(np.abs(ZL))

        # Define economic size
        X1 = np.zeros((N,N))
        for OR, DE in np.ndindex((N,N)):
            X1[OR, DE] = pi[OR, DE]*pihat[OR, DE]*Xm1[DE]

        hatmodel = onesector(year=self.year, countries=self.countries, X=X1,
                             wL=what*self.wL, theta=self.theta, nu=self.nu)
        rwhat = what/Phat
        rexphat = Xm1 / self.Xm / Phat 
        return hatmodel, rwhat, rexphat       

    # log_linear ---------------------------
    def log_linearization(self, dlntau):
        # Set convergence parameter
        phi = 0.1 # convergence speed
        tol = 0.0001 # convergence tolerance 

        # Start solving
        N = self.N
        theta = self.theta
        
        # Setting boxes
        X2 = np.zeros((N,N))

        # Initial dlnw
        dlnw = np.zeros((N))

        # Normalization
        dlnWGDP = np.sum(dlnw * self.wL) #WGDP = np.sum(w*L + r*K)          
        dlnw = dlnw - dlnWGDP
        #dlnw = dlnw - dlnw[0]

        # Calculate pi, s dlns
        pi = np.zeros((N,N))
        s = np.zeros((N,N))

        for OR, DE in np.ndindex((N,N)):
            pi[OR, DE] = self.X[OR, DE]/self.Xm[DE]
            s[OR,DE] = self.X[OR,DE] /self.Ym[OR]
        
        dif = 1

        # Calculate beta_L
        # beta_L = np.ones((N))

        while dif > tol:
            # Updata w and r
            dlnw_old = np.copy(dlnw)

            # Calculate price (phat) and price index (Phat)
            dlnp = np.zeros((N,N))
            dlnP = np.zeros((N))
            for OR, DE in np.ndindex((N,N)):
                dlnp[OR, DE] = dlnw[OR] + dlntau[OR, DE]
                dlnP[DE] += pi[OR, DE]*dlnp[OR, DE]

            # Calculate pi
            dlnpi = np.zeros((N,N))
            for OR, DE in np.ndindex((N,N)):
                dlnpi[OR, DE] = (-theta)*dlnp[OR, DE] + theta*dlnP[DE]
                       
            # Calculate dlnw (update)
            dlnw = np.zeros((N))
            for OR, DE in np.ndindex((N,N)):
                dlnw[OR] += s[OR, DE] * (dlnw_old[DE] + phi*dlnpi[OR,DE])

            # Normalizetion
            dlnWGDP = np.sum(dlnw * self.wL)
            dlnw = dlnw - dlnWGDP
            #dlnw = dlnw - dlnw[0]
            #dlnw = dlnw / 2 + dlnw_old / 2

            dif = np.max(np.abs(dlnw - dlnw_old))

            # Caluculate excsess factor demand and supply
            #Xm2 = dlnw * self.D
            wLS2 = (1+dlnw)*(self.wL)
            Xm2 = wLS2 + self.D
            
            for OR, DE in np.ndindex((N,N)):
                #dlnP[DE] += dlnp[OR, DE]*(theta)
                dlnP[DE] += pi[OR, DE]*dlnp[OR, DE]

            #dlns[OR, DE] = theta*dlnp[OR, DE] - dlnP[DE]
            #s[OR, DE] = math.exp(dlns[OR, DE])


        # Define economic size
        X2 = np.zeros((N,N))
        for OR, DE in np.ndindex((N,N)):
            X2[OR, DE] = (1 + dlnpi[OR, DE]) * pi[OR,DE] * Xm2[DE]
            #X2[OR, DE] = s[OR, DE] + Xm2[DE] 

        logmodel = onesector(year=self.year, countries=self.countries, X=X2,
                                 wL=(1+dlnw)*self.wL, theta=self.theta, nu=self.nu)
        dlnr = dlnw - dlnP
        dlnrexp = Xm2 - self.Xm - dlnP 
        return logmodel, dlnr, dlnrexp  

# newtau = tau*(1 + dln_tau)

def test():
    print("Okie, we start tessting")

    countries = ["USA", "JPN", "TWN"]
    N = len(countries)
    tau = np.random.rand(N,N)/2 + 1
    L = np.ones((N))
    beta_L = np.ones((N))
    D = np.zeros((N))
    tempmodel = onesector.from_static_parameters(countries, year=2023, theta=4, nu=0.5,
                                                  tau=tau, beta_L=beta_L, L=L, D=D)
    
    tauhat = np.random.rand(N,N)/2 + 0.5
    #tauhat = np.ones((N,N))
    hatmodel, rwhat, rexphat = tempmodel.exacthatalgebra(tauhat=tauhat)
    print("How's exact hat algebra going?")
    tau1 = tau*tauhat
    resolvemodel = onesector.from_static_parameters(countries, year=2023, theta=4, nu=0.5,
                                                                tau=tau1, beta_L=beta_L, L=L, D=D)
    print(hatmodel.X/resolvemodel.X)

    #dlntau = (1 + np.random.rand(N,N)/2 + 0.5) ##
    dlntau = np.random.rand(N,N)/100 
    #dlntau = np.zeros((N,N))
    logmodel, dlnr, dlnrexp = tempmodel.log_linearization(dlntau=dlntau)
    print("How's log linearization going?")
    tau2 = tau * (1 + dlntau)
    resolvemodel2 = onesector.from_static_parameters(countries, year=2023, theta=4, nu=0.5,
                                                                tau=tau2, beta_L=beta_L, L=L, D=D)
    print(logmodel.X/resolvemodel2.X)
    print("Done?")
    


if __name__ == '__main__' :
    test()