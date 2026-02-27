from numba import jit
import numpy as np
import matplotlib.pyplot as plt
import math
from numba.typed import List
import json
import time


filename=input("Enter the file name")

noe=200
noex=80
noey=30
vol=noex*noey
E=200000
mu=0.3
l=1
h=1
x=[]
y=[]

k=0
fixedbeam=[]
propedcantiliver=[]
cantiliver=[]
topfixed=[]
bottomfixed=[]
for i in range(noey+1):
    nodelist=[]
    j=0#for support condition
    for j in range(0,(noex+1)*2):
        k=k+1
        j=j+1
        if(j==1 or j==2 or j==(noex+1)*2 or j==(noex+1)*2-1):
            fixedbeam.append(k)
        if(j==1 or j==2 or j==(noex+1)*2):
            propedcantiliver.append(k)
        if(j==1 or j==2):
            cantiliver.append(k)
        if(i==0):
            bottomfixed.append(k)
        if(i==noey):
            topfixed.append(k)
        nodelist.append(k)
    print(nodelist)

    
#constrain=cantiliver
constrain=[]
"""for i in range(6):
    constrain.append(cantiliver[i]);constrain.append(cantiliver[-i-1])"""
constrain=[1,2,3,4,159,160,161,162]
constrain=list(set(constrain))
constrain.sort()
#print(constrain)
#for i in range(3,(nomember+1)*4+1):
for i in range(1,((noex+1)*2*(noey+1))+1):
    x.append(i)
    y.append(0)

force=y[:len(y)]
#force[4962-1]=-10
#force[202-1]=-10
#force[5152-1]=-10
force[82-1]=-10
"""for i in bottomfixed:
    if(i%2==0):
        force[i-1]=-10"""
#print(force)
print(constrain)

constrainsort=sorted(constrain,reverse=True)
for i in constrain:
    x.remove(i)

gc=x+constrain
gr1=x

for i in constrainsort:
    force.pop(i-1)

intensity=List()
for i in range(noey):
    list1=List()
    for i in range(noex):
        list1.append(1)
    intensity.append(list1)
    
allintensity=[]
allstrainenergy=[]
checklist=[]
for iteration in range(1,60):
    gr=gc
    @jit(nopython=True)
    def fast(gc,intensity):
        C3=[[(3-mu)/6,(1+mu)/8,-(3+mu)/12,(-1+3*mu)/8,(-3+mu)/12,-(1+mu)/8,mu/6,(1-3*mu)/8],
           [(1+mu)/8,(3-mu)/6,(1-3*mu)/8,mu/6,-(1+mu)/8,(-3+mu)/12,(-1+3*mu)/8,-(3+mu)/12],
           [-(3+mu)/12,(1-3*mu)/8,(3-mu)/6,-(1+mu)/8,mu/6,(-1+3*mu)/8,(-3+mu)/12,(1+mu)/8],
           [(-1+3*mu)/8,mu/6,-(1+mu)/8,(3-mu)/6,(1-3*mu)/8,-(3+mu)/12,(1+mu)/8,(-3+mu)/12],
           [(-3+mu)/12,-(1+mu)/8,mu/6,(1-3*mu)/8,(3-mu)/6,(1+mu)/8,-(3+mu)/12,(-1+3*mu)/8],
           [-(1+mu)/8,-(3-mu)/12,(-1+3*mu)/8,-(3+mu)/12,(1+mu)/8,(3-mu)/6,(1-3*mu)/8,mu/6],
           [mu/6,(-1+3*mu)/8,(-3+mu)/12,(1+mu)/8,-(3+mu)/12,(1-3*mu)/8,(3-mu)/6,-(1+mu)/8],
           [(1-3*mu)/8,-(3+mu)/12,(1+mu)/8,(-3+mu)/12,(-1+3*mu)/8,mu/6,-(1+mu)/8,(3-mu)/6]]
        nnn=[1,2,3,4,7,8,5,6]
        C2=[]
        for i in nnn:
            emptylist1=[]
            for j in nnn:
                emptylist1.append(C3[i-1][j-1]*E/(1-mu**2))
            C2.append(emptylist1)
        GSM=[]
        for i in range(1,noey+1):
            for j in range(noex):
                C3 = [[y * intensity[i-1][j] for y in x] for x in C2]
                LSM=C3+[[float(((noex+1)*(i-1)*2)+(j*2)+1),float(((noex+1)*(i-1)*2)+(j*2)+2),float(((noex+1)*(i-1)*2)+(j*2)+3),float(((noex+1)*(i-1)*2)+(j*2)+4),
                         float(((noex+1)*i*2)+(j*2)+1),float(((noex+1)*i*2)+(j*2)+2),float(((noex+1)*i*2)+(j*2)+3),float(((noex+1)*i*2)+(j*2)+4)]]
                GSM.append(LSM)
                
        C1=[]
        for Mc in gc:
            R1=[]
            cc=Mc
            for Mr in gc:
                y=0
                if(cc%2==0):
                    cc=cc-1
                if(Mr==cc or Mr==cc+1 or Mr==cc+2 or Mr==cc+3 or Mr==cc-1 or Mr==cc-2
                   or Mr==cc+((noex+1)*2) or Mr==cc+((noex+1)*2)+1 or Mr==cc+((noex+1)*2) +2 or Mr==cc+((noex+1)*2)+3 or Mr==cc+((noex+1)*2)-1 or Mr==cc+((noex+1)*2)-2
                   or Mr==cc-((noex+1)*2) or Mr==cc-((noex+1)*2)+1 or Mr==cc-((noex+1)*2) +2 or Mr==cc-((noex+1)*2)+3 or Mr==cc-((noex+1)*2)-1 or Mr==cc-((noex+1)*2)-2):
                    
                    elementno1=math.ceil((Mr-(Mr//((noex+1)*2))*2)/2)-1-1
                    elementno2=math.ceil((Mr-(Mr//((noex+1)*2))*2)/2)-1
                    elementno3=math.ceil((Mr-(Mr//((noex+1)*2))*2)/2)-1-noex-1
                    elementno4=math.ceil((Mr-(Mr//((noex+1)*2))*2)/2)-1-noex
                    if(elementno1>=noex*noey ):#or elementno1< -noex*noey
                        elementno1=0
                    if(elementno2>=noex*noey ):
                        elementno2=0
                    if(elementno3>=noex*noey ):
                        elementno3=0
                    if(elementno4>=noex*noey ):
                        elementno4=0
                    nearelementlist=[elementno1,elementno2,elementno3,elementno4]
                    #nearelementlist=set(nearelementlist)
                    for mn in nearelementlist:
                        for mr in range(0,8):
                            if(GSM[mn][8][mr]==Mr):
                                for mc in range(0,8):
                                    if(GSM[mn][8][mc]==Mc):
                                        x=GSM[mn][mc][mr]
                                        y=y+x
                R1.append(y)
            C1.append(R1)
        return C1
    
    C1=fast(gc,intensity)
    print("Loop finished")
    start_time = time.time()
    multmat=[]
    for i in C1:
            multmat.append(i[0:len(gr1)])
    multmat=multmat[0:len(gr1)]
    u=np.dot((np.linalg.inv(multmat)),force)
    u=list(u)
    for i in constrain:
        u.insert(i-1,0)

    ux=[];uy=[]
    for i in range(len(u)):
        if(i%2==0):
            ux.append(u[i])
        else:
            uy.append(u[i])
    ux= np.array_split(ux, noey+1)
    uy= np.array_split(uy, noey+1)

    for i in ux:
        for j in range(len(i)):
            i[j]=i[j]+j*l
    k=0
    for i in uy:
        for j in range(len(i)):
            i[j]=i[j]+k*h
        k=k+1

    """for i in range(len(ux)):
        plt.plot(ux[i],uy[i])
    plt.show()"""
    
    #finding average y displacement in each line
    xyavgstrain=[]
    for i in range(noey):
        chumma1=[]
        for j in range(noex):
            avgstrain=((((-ux[i][j]+ux[i][j+1])+(-ux[i+1][j]+ux[i+1][j+1]))/2-l)  +  (((-uy[i][j]+uy[i+1][j])+(-uy[i][j+1]+uy[i+1][j+1]))/2-h))/2
            chumma1.append(avgstrain)
        xyavgstrain.append(chumma1)
    xyavgstrainplot=list(reversed(xyavgstrain))
    umax=np.max(xyavgstrain)
    umin=np.min(xyavgstrain)
    if(umax > abs(umin)):
        gumax=umax
        gumin=-umax
    else:
        gumax=-umin
        gumin=umin  
    print("--- %s seconds ---" % (time.time() - start_time))

        
    plt.imshow(xyavgstrainplot,cmap ='RdBu_r',vmax=gumax/3,vmin=gumin/3)
    print(xyavgstrainplot)
    plt.show()
    absxyavgstrain=[]
    for i in range(len(xyavgstrain)):
        chumma=[]
        for j in range(len(xyavgstrain[i])):
            chumma.append(abs(xyavgstrain[i][j]))
        absxyavgstrain.append(chumma)
    strainenergy=0
    for se in absxyavgstrain:
        strainenergysum1= sum(map(lambda st : st * st*E, se))
        strainenergy=strainenergysum1+strainenergy
    allstrainenergy.append(strainenergy)

    intensity=list(intensity)
    for i in range(len(intensity)):
        intensity[i]=list(intensity[i])
        

    #optimality criteria method
    lambdaa=0
    power=(1-iteration/100)**7
    if(power<0.1):
        power=0.1
    for j in range(len(absxyavgstrain)):
        for i in range(len(absxyavgstrain[0])):
            if(i==0):
                    lambdaa=lambdaa+intensity[j][i]*(E*((absxyavgstrain[j][i]))**2)**power
            else:
                    lambdaa=lambdaa+intensity[j][i]*(E*((absxyavgstrain[j][i]))**2)**power
    lambdaa=((lambdaa)/(vol))**(1/power)
    check=0
    for j in range(len(absxyavgstrain)):
        for i in range(len(absxyavgstrain[0])):
            if(i==0):
                    shade=intensity[j][i]*(E*((absxyavgstrain[j][i]))**2/lambdaa)**power
            else:
                    shade=intensity[j][i]*(E*((absxyavgstrain[j][i]))**2/lambdaa)**power
                    if(((E*((absxyavgstrain[j][i]))**2/lambdaa))>0.9 and ((E*((absxyavgstrain[j][i]))**2/lambdaa))<1.1):
                        check=1+check
            if(shade<.001):
                shade=.001
            intensity[j][i]=shade
    print(power,lambdaa,iteration,check)
    #filter
    """intensity2=intensity
    for i in range(len(intensity2)):
        for j in range(len(intensity2[i])):
            if(i<2 or j<2):
                lf=(intensity[i][j])
            else:
                try:
                    if((iteration<20 or iteration%4==0)):
                        lf1=intensity[i][j]*3
                        lf2=((intensity[i][j-1]+intensity[i][j+1]+intensity[i+1][j]+intensity[i-1][j])*1+(intensity[i+1][j+1]+intensity[i+1][j-1]+intensity[i-1][j+1]+intensity[i-1][j-1])*1)/8*1
                        lf=(lf1+lf2)/4
                    else:
                        lf=(intensity[i][j])
                except:
                    lf=(intensity[i][j])
            newshade=lf
            intensity[i][j]=newshade"""
    
    intensityplot=list(reversed(intensity))

    """#moderization
    if(iteration==49):
        for i in range(15):
            intensityplot2=intensityplot
            for i in range(len(intensityplot2)):
                for j in range(len(intensityplot2[i])):
                    if(i<2 or j<2):
                        lf=(intensityplot[i][j])
                    else:
                        try:
                                lf1=intensityplot[i][j]*1.2
                                lf2=((intensityplot[i][j-1]+intensityplot[i][j+1]+intensityplot[i+1][j]+intensityplot[i-1][j])*1+(intensityplot[i+1][j+1]+intensityplot[i+1][j-1]+intensityplot[i-1][j+1]+intensityplot[i-1][j-1])*1)/8*1
                                lf=(lf1+lf2)/2.2
                        except:
                            lf=(intensityplot[i][j])
                    newshade=lf
                    intensityplot[i][j]=newshade
                allintensity.append(intensityplot)"""
    #plt.imshow(intensityplot,cmap ='Greys')
    #plt.show()
    
    allintensity.append(intensityplot)
    print(intensityplot)

    intensity1=intensity
    intensity=List()
    for x in intensity1:
        s=List()
        for y in x:
            s.append(y)
        intensity.append(s)
    checklist.append(check)
outputlist=[allintensity,allstrainenergy,checklist]
out_file = open(str(filename)+".txt", "w")
json.dump(outputlist, out_file,indent =0)
out_file.close()
        
for plot in range(len(allintensity)):
    plt.imshow(allintensity[plot],cmap ='Greys')
    plt.pause(0.05)
plt.show()


            
