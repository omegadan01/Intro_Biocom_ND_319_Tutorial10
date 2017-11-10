#Load packages
import pandas
import scipy
import scipy.integrate as si
from plotnine import *

# function
def SIR (y,t0,beta,gamma):
    S = y[0]
    I = y[1]
    R = y[2]
    dS = -1*(beta*I*S)
    dI = (beta*I*S)-(gamma*I)
    dR = (gamma*I)
    return dS, dI, dR

# initial conditions
times = range(0,500)
NO = [999, 1, 0]

# dataframe of gamma and beta values
data = [{'beta' : .0005, 'gamma' : .05},
        {'beta': .005, 'gamma': .5},
        {'beta': .0001, 'gamma': .1},
        {'beta': .00005, 'gamma': .1},
        {'beta': .0001, 'gamma': .05},
        {'beta': .0002, 'gamma': .05},
        {'beta': .0001, 'gamma': .06}]
my_data = pandas.DataFrame(data)

# make lists to hold the results
mdi = []
mdp = []
pa = []
ro = []
b = []
g = []

# start big for loop here
for line in range(0,len(my_data),):
    q = my_data.iloc[line]['beta']
    p = my_data.iloc[line]['gamma']
    params = (q, p)

    b.append(params[0])
    g.append(params[1])

    infection = pandas.DataFrame({"time":times,"S":0,"I":0,"R":0})

    # sim
    sim = si.odeint(func=SIR, y0=NO, t=times, args=params)

    # fill dataframe
    infection.iloc[:,2]=sim[:,0]
    infection.iloc[:,0]=sim[:,1]
    infection.iloc[:,1]=sim[:,2]

    # calc max daily incidence
    daily_incidence = []
    for i in range(0,len(infection),):
        if infection.time[i]==0:
            continue
        else:
            I = infection.iloc[i]['I']
            Iold = infection.iloc[i-1]['I']
            incidence = I-Iold
            daily_incidence.append(incidence)
    max_daily_incidence = max(daily_incidence)
    mdi.append(max_daily_incidence)

    # calc max daily prevalence
    daily_prev = []
    for i in range(0,len(infection),):
        I = infection.iloc[i]['I']
        R = infection.iloc[i]['R']
        S = infection.iloc[i]['S']
        prev = I/(S+I+R)
        daily_prev.append(prev)
    max_daily_prev = max(daily_prev)
    mdp.append(max_daily_prev)

    #calc percent affected over simulation- use last time step (499)
    I= infection.iloc[499]['I']
    R= infection.iloc[499]['R']
    S= infection.iloc[499]['S']
    percent_affected = (I+R)/(S+I+R)
    pa.append(percent_affected)

    # basic reproduction number initial SIR
    beta = params[0]
    gamma = params[1]
    I= infection.iloc[0]['I']
    R= infection.iloc[0]['R']
    S= infection.iloc[0]['S']
    repo_number = (beta*(S+I+R))/gamma
    ro.append(repo_number)


results = pandas.DataFrame(
    {'beta' : b,
     'gamma' : g,
     'max_daily_incide' : mdi,
     'max_daily_prev' : mdp,
     'percent_affect' : pa,
     'repo_num' : ro})


print results
#need these to fill into a list or a dataframe
# need to put all this intoa bigger loop





