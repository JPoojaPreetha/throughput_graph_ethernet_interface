import copy
import re
import datetime
import copy
import configuration as conf
import re

import matplotlib.dates as md
import matplotlib.pyplot as plt
from datetime import datetime
import math
import time
import copy
def graph(dates,oput,title,stfile):
    plt.subplots_adjust(bottom=0.3)
    plt.xticks( rotation=30, horizontalalignment='right' )
    
    ax=plt.gca()
    xfmt = md.DateFormatter('%Y-%m-%d %H:%M:%S')
    ax.xaxis.set_major_formatter(xfmt)
    plt.plot(dates,oput)
    plt.title(title)
    plt.xlabel('Time')
    plt.ylabel('Mbps')
    plt.savefig(stfile)
    plt.show()

def throughputeth(fname,thl):
    print(" Throughput Graphs \n") 
    infile=open(fname,"r")
    lines=infile.readlines()

    txfile=open("txfile.txt","w+")
    rxfile=open("rxfile.txt","w+")
    ttfile=open("tmp3.txt","w+")
    tmp=open("tmp2.txt","w+")
    ttt=open("ttt.txt","w+")
    ttr=open("ttr.txt","w+")
    
    c=False
    j=0
    prev=""
    txb=[]
    txt=[]
    rxb=[]
    rxt=[]
    l1=[]
    l2=[]
    #group first instance
    for k in thl:
            for i in range(len(lines)) :
                lines[i]=lines[i].strip()
                if re.match(r"^"+k+" .*",lines[i]):
                    l1.append(k)
                    break
                elif k in lines[i] and not re.match(r"^"+k+" .*",lines[i]):
                    l2.append(k)
                    break

    infile=open(fname,"r")
    lines=infile.readlines()           
    for k in l1:
            print("\n\nThroughput graph for "+k)
            for i in range(len(lines)) :
                lines[i]=lines[i].strip()
                
                if re.match(r"^"+k+" .*",lines[i]) and "no wireless extensions." not  in lines[i]:
                        for j in range(i,len(lines)):
                        
                            if re.match(r"^RX bytes.*",lines[j]):
                                txb.append(lines[j].split("TX bytes:")[1].split(' ')[0])
                                rxb.append(lines[j].split('RX bytes:')[1].split(' ')[0])
                                txt.append(lines[j].split("|")[1].split('.')[0])
                                rxt.append(lines[j].split("|")[1].split('.')[0])
                                break
                
   
            
            tdelb=[]
            txt1=copy.deepcopy(txt)  
            txb = [int(i) for i in txb]
            txt = [datetime.strptime(x,'%Y-%m-%d %H:%M:%S') for x in txt]
            ndata=0
            for i in range(1,len(txb)):
                if txb[i]<txb[i-1]:
                    ndata=4294967295-txb[i-1]+txb[i]
                    #x=ndata-txb[i-1]
                    tdelb.append(ndata)
                    #print(i)
                    
                else:
                    x = txb[i] - txb[i-1]
                    tdelb.append(x)
                    
 
            
            #tdelb = [txb[i+1]-txb[i] for i in range(len(txb)-1) ]
            tdelt = [(txt[i + 1] - txt[i]).total_seconds() for i in range(len(txt)-1)]
          
            
            tput=[((tdelb[i])*8)/(tdelt[i]*math.pow(10,6)) for i in range(0,len(tdelb))]
            
            
            txt1 = [datetime.strptime(txt1[x],'%Y-%m-%d %H:%M:%S') for x in range(len(txt1)-1)]
                
            dates = md.date2num(txt1)
            graph(dates,tput,"Througput graph for tx databytes","txtput_1.png")
    



        
            rdelb=[]
            rdata=0
            rxt1=copy.deepcopy(rxt)  
            rxb = [int(i) for i in rxb]
            rxt = [datetime.strptime(x,'%Y-%m-%d %H:%M:%S') for x in rxt]
            for i in range(1,len(rxb)):
                if rxb[i]<rxb[i-1]:
                    rdata=4294967295-rxb[i-1]+rxb[i]
                    #x=rdata-rxb[i-1]
                    rdelb.append(rdata)
                    #rdelb.append(x)
                    
                else:
                    x = rxb[i] - rxb[i-1]
                    rdelb.append(x)

          
            rdelt = [(rxt[i + 1] - rxt[i]).total_seconds() for i in range(len(rxt)-1)]

            rtput=[((rdelb[i])*8)/(rdelt[i]*math.pow(10,6)) for i in range(0,len(rdelb))]
            
            
            ttput=[(tput[i]+rtput[i]) for i in range(len(tput))] 

            

            rxt1 = [datetime.strptime(rxt1[x],'%Y-%m-%d %H:%M:%S') for x in range(len(rxt1)-1)]
                
            dates = md.date2num(rxt1)
            graph(dates,rtput,"Througput graph for rx databytes","rxtput_1.png")
            graph(dates,ttput,"Througput graph for tx+rx databytes","tot_throughput_1.png")
    
      
            txb=[]
            txt=[]
            rxb=[]
            rxt=[]

    for i in l2:
        print("\n\n"+i+" is not a valid interface")
    
