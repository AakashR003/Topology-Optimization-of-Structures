import numpy as np
import matplotlib.pyplot as plt
import json

#plt.axis([0, 10, 0, 1])

try:
    with open("sbb301802.txt") as f:
            lines = f.read()
            allintensity=(json.loads(lines))[0]
            strainenergy=(json.loads(lines))[1]
            check=(json.loads(lines))[2]

    x=[]
    for i in range(len(strainenergy)):
        x.append(i)
    plt.plot(x,strainenergy)
    plt.show()

    x=[]
    for i in range(len(check)):
        x.append(i)
    plt.plot(x,check)
    plt.show()

    for i in range(3):
            intensityplot2=allintensity[len(allintensity)-1]
            for i in range(len(intensityplot2)):
                for j in range(len(intensityplot2[i])):
                    if(i<2 or j<2):
                        lf=(allintensity[len(allintensity)-1][i][j])
                    else:
                        try:
                                lf1=allintensity[len(allintensity)-1][i][j]*1
                                lf2=((allintensity[len(allintensity)-1][i][j-1]+allintensity[len(allintensity)-1][i][j+1]+allintensity[len(allintensity)-1][i+1][j]+allintensity[len(allintensity)-1][i-1][j])*1+(allintensity[len(allintensity)-1][i+1][j+1]+allintensity[len(allintensity)-1][i+1][j-1]+allintensity[len(allintensity)-1][i-1][j+1]+allintensity[len(allintensity)-1][i-1][j-1])*1)/8*1
                                lf=(lf1+lf2)/2
                        except:
                            lf=(allintensity[len(allintensity)-1][i][j])
                    newshade=lf
                    intensityplot2[i][j]=newshade
            allintensity.append(intensityplot2)
            print(len(allintensity))
            
    for plot in range(len(allintensity)):
        print(plot)
        plt.imshow(allintensity[plot],cmap ='Greys',vmin=0, vmax = 1)
        plt.pause(0.1)
        #plt.axis('off')
    plt.show()

except :
    with open("cb17.txt") as f:
            lines = f.read()
            allintensity=(json.loads(lines))[0]
            strainenergy=(json.loads(lines))[1]

    x=[]
    for i in range(len(strainenergy)):
        x.append(i)
    plt.plot(x,strainenergy)
    plt.show()

    for i in range(10):
            intensityplot2=allintensity[len(allintensity)-1]
            for i in range(len(intensityplot2)):
                for j in range(len(intensityplot2[i])):
                    if(i<2 or j<2):
                        lf=(allintensity[len(allintensity)-1][i][j])
                    else:
                        try:
                                lf1=allintensity[len(allintensity)-1][i][j]*1
                                lf2=((allintensity[len(allintensity)-1][i][j-1]+allintensity[len(allintensity)-1][i][j+1]+allintensity[len(allintensity)-1][i+1][j]+allintensity[len(allintensity)-1][i-1][j])*1+(allintensity[len(allintensity)-1][i+1][j+1]+allintensity[len(allintensity)-1][i+1][j-1]+allintensity[len(allintensity)-1][i-1][j+1]+allintensity[len(allintensity)-1][i-1][j-1])*1)/8*1
                                lf=(lf1+lf2)/2
                        except:
                            lf=(allintensity[len(allintensity)-1][i][j])
                    newshade=lf
                    allintensity[len(allintensity)-1][i][j]=newshade
            allintensity.append(intensityplot2)

    for plot in range(len(allintensity)):
        print(plot)
        plt.imshow(allintensity[plot],cmap ='Greys',vmin=0, vmax = 1)
        plt.pause(0.1)
        plt.axis('off')
        
    plt.show()
else:
    with open("bridge1.txt") as f:
            lines = f.read()
            allintensity=(json.loads(lines))
    for plot in range(len(allintensity)):
        print(plot)
        plt.imshow(allintensity[plot],cmap ='Greys')
        plt.pause(0.5)
        
    plt.show()


