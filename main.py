from nsepy import get_history
import datetime
import numpy as np
import pandas as pd
from datetime import  date
symbols=['INFY','SBIN','RELIANCE']
import math
import scipy.optimize as spo
capital=10000
fd_intrest=6
def normalize_data(df):
    return df / df.iloc[0, :]

def read(symbol,syear,smonth,sday,eyear,emonth,eday):
    df = get_history(symbol=symbol, start=date(syear,smonth,sday), end=date(eyear,emonth,eday))
    df=df['Close']
    return df
def merge(symbols):
    frames=[]
    for symbol in symbols:

        df_temp=read(symbol,2022,1,1,2022,2,1)
        frames.append(df_temp)
        df=pd.concat(frames,axis=1,keys=symbols)
    return df



def final_touches(df,alloc,captial):
    df=df*alloc*captial
    df['Value']=df.sum(axis=1)
    df['Daily returns']=df['Value'].pct_change(1)
    df.fillna(0,inplace=True)
    return df

def cr(df,allocs):
    df = df * allocs * capital
    portfolio_value = df.sum(axis=1)
    return -1*((portfolio_value[-1]/portfolio_value[0])-1)

def shapre_ratio(df,alloc):
    df = df * alloc * capital
    portfolio_value=df.sum(axis=1)

    daily_returns=portfolio_value.pct_change(1)
    fd_daily=math.pow(((fd_intrest/100)+1),1/252)-1
    diff=daily_returns-fd_daily
    s=diff.mean()/daily_returns.std()
    s=math.sqrt(242)*s
    return s*-1
def optimize_shapre_ratio(allocs,df):
    def con(allocs):
        return np.sum(allocs) - 1
    alloc_guess=allocs
    bnds = [(0.0, 1.0), (0.0, 1.0), (0.0, 1.0)]
    cons = ({'type': 'eq', 'fun': con})
    optimizedOutput = spo.minimize(shapre_ratio, alloc_guess, args=(df,),constraints=cons,
                                                                                method='SLSQP',  bounds=bnds,
                                                                                 options={'disp': True})

    optimizedAllocations = optimizedOutput.x

    allocationsApplied = df * optimizedAllocations
    print(allocationsApplied)
    print(allocationsApplied*capital)


def optimize_cum_returns(df,allocs):
    def con(allocs):
        return np.sum(allocs) - 1

    alloc_guess = allocs
    bnds = [(0.0, 1.0), (0.0, 1.0), (0.0, 1.0)]
    cons = ({'type': 'eq', 'fun': con})
    optimizedOutput = spo.minimize(cr, alloc_guess, args=(df,), constraints=cons,
                                   method='SLSQP', bounds=bnds,
                                   options={'disp': True})

    optimizedAllocations = optimizedOutput.x

    allocationsApplied = df * optimizedAllocations
    print(allocationsApplied * capital)

df=merge(symbols)
df=normalize_data(df)


print(shapre_ratio(df,[0.3,0.4,0.3]))
optimize_shapre_ratio([0.4,0.3,0.3],df)
optimize_cum_returns(df,[0.4,0.3,0.3])