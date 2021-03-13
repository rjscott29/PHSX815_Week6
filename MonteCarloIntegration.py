#! /usr/bin/env python

# imports of external packages to use in our code
import sys
import numpy as np
import matplotlib.pyplot as plt
import random   

def XYFunction(x):
    y = x**2
    return x,y

def Trapezoidal(f,a,b,N):
    # get x and y components of f
    f_x = f[0]
    f_y = f[1]
    # prefactor of the trapezoidal method uses x values and number of bins
    T_prefactor = (f_x[N-1]-f_x[0])/(2*N)
    # sum all y values of g, and get f(a) + 2*f(a+1)... + 2*f(b-1) + f(b)
    T_sum = sum(f_y)
    T_sum = 2*T_sum - f_y[99] - f_y[0]
    # multiply to get trapezoidal equation for uniform grid
    # this will be exact for linear equations of y and x
    T = round(T_prefactor*T_sum, 3)
    return T

# takes tuples to compare data from two functions (x,y)
    # These are our for loops determining if we are above or below the curve
    # We take each data point and compare it with the curve equations given
    # Look at the y and z values for any x and calculate the difference.
    # +/- reveals acceptance
def MonteCarlo(function1,function2):
    yesxValues = []
    yesyValues = []
    noxValues = []
    noyValues = []
    nTotal = 0
    nAccept = 0
    for x_i, y_i in function1:
        for x_j, y_j in function2:
            if x_i == x_j:
                ydiff = y_j-y_i
                nTotal += 1
                if ydiff >= 0:
                    nAccept += 1
                    yesxValues.append(x_i)
                    yesyValues.append(y_i)
                else:
                    noxValues.append(x_i)
                    noyValues.append(y_i)
    return yesxValues, yesyValues, noxValues, noyValues, nAccept, nTotal

# iterates our MonteCarlo method with set values of nPoints to return array
def MCIteration(dataspacing,maximum):
    nPoints = np.linspace(10,maximum,dataspacing)
    nRatio = []
    Tvalue = []
    for n in nPoints:
        # establishing data and preparing [x,y] for data comparison
        x = np.linspace(0,1,101)    
        y = XYFunction(x)
        y = y[1]
        x = np.around(x,2)
        y = np.around(y,2)
        # convert data to tuple
        f = list(zip(x,y))
        
        # establish random numbers for scatter plot
        xValues = []
        yValues = []
        for xs in range(0,int(n)):
            xValues.append(random.uniform(0,1))
        for ys in range(0,int(n)):
            yValues.append(random.uniform(0,1))
            # rounding values for a direct comparison with the precision of x
        xValues = np.around(xValues, 2)
        yValues = np.around(yValues, 2) 
        # another tuple for comparison
        g = list(zip(xValues, yValues))
        
        M = MonteCarlo(g,f)
        nAccept = M[4]
        nTotal = M[5]
        nRatio.append(nAccept/nTotal)
    print(nRatio)
    return nPoints, nRatio, Tvalue
        
    

# main function for our coin toss Python code
if __name__ == "__main__":
       
    # default number of points for analysis
    nPoints = 1000
    
    # determines significant digits. This will prove useful for comparing
    # random values with generated points.
    # when we have 2 decimal places, we want 100 x values between 0 and 1
    # 3 decimals takes too long to calculate and search in our tuples
    decimals = 2
    precision = 1*10**decimals
    
    # do not rotate unless commanded
    rotate = 0
    
    # set initial values to 0
    nAccept = 0
    nTotal = 0
    
    # default to 2D plot
    dims = 2
    
    # default shows both accepted and rejected items
    show = 0
    
    # default bounds [a,b] for x
    a = 0
    b = 1
        
    # available options for user input
    if '-nPoints' in sys.argv:
        p = sys.argv.index('-nPoints')
        npo = int(sys.argv[p+1])
        if npo >= 0:
            nPoints = npo
    if '-rotate' in sys.argv:
        p = sys.argv.index('-rotate')
        rotate = 1
    if '-ThreeDee' in sys.argv:
        p = sys.argv.index('-ThreeDee')
        dims = 3
    if '-show' in sys.argv:
        p = sys.argv.index('-show')
        sh = int(sys.argv[p+1])
        if sh >= 0 and sh <= 2:
            show = sh
        else:
            show == 0
    # if the user includes the flag -h or --help print the options
    if '-h' in sys.argv or '--help' in sys.argv:
        print ("Usage: %s [options]" % sys.argv[0])
        print ("  options:")
        print ("   --help(-h)             print options")
        print ("   -nPoints [number]      number of data points to find volume")
        print ("   -ThreeDee              show a 3D plot")
        print ("   -rotate                rotates 3D plot (Use at own risk!)")
        print ("   -show [number 0,1,2]   determines what data is visualized")
        sys.exit(1)

# establishing data and preparing [x,y] for data comparison
    adjpts = (b-a)*(precision+1)
    x = np.linspace(a,b,adjpts)    
    y = XYFunction(x)
    y = y[1]
    x = np.around(x,decimals)
    y = np.around(y,decimals)
    ymax = max(y)
    # convert data to tuple
    f = list(zip(x,y))
    
# establish random numbers for scatter plot
    xValues = []
    yValues = []
    for xs in range(0,nPoints):
        xValues.append(random.uniform(a,b))
    for ys in range(0,nPoints):
        yValues.append(random.uniform(0,ymax))
    
# rounding values for a direct comparison with the precision of x
    xValues = np.around(xValues, decimals)
    yValues = np.around(yValues, decimals) 
# another tuple for comparison
    g = list(zip(xValues, yValues))

    M = MonteCarlo(g,f)
    yesxValues = M[0]
    yesyValues = M[1]
    noxValues = M[2]
    noyValues = M[3]
    nAccept = M[4]
    nTotal = M[5]
                    
    print("Accepted points: " + str(nAccept))
    print("Total points: " + str(nTotal))
    area = nAccept/nTotal
    
    MCI = MCIteration(100, 10000)
    MCIx = MCI[0]
    MCIy = MCI[1]
    MCIt = MCI[2]
    
    T = Trapezoidal(XYFunction(x),a,b,101)
    print("Area calculated by Trapezoidal method: " + str(T))
                      
# Creating our plot
    title = "Plotting with " + str(nPoints) + " data points. Calculated area = " + str("%.3f" % area) + " per unit area"                

# 2D plotting of data
    plt.figure()
    plt.plot(x,y, color = 'black')
    plt.scatter(yesxValues, yesyValues, color = 'lawngreen')
    plt.scatter(noxValues, noyValues, color = 'firebrick')
    
    plt.xlabel('X axis')
    plt.ylabel('Y axis')
    
    plt.title(title)
    plt.grid(True)
    
    plt.show()
    
# Plotting data relative to actual value:
    plt.figure()
    plt.plot(MCIx, MCIy, color = 'black')
    plt.hlines(.333, 0, 10000, color = 'red')
    plt.plot(MCIt,MCIy, color = 'blue')
    
    plt.xlabel('nPoints')
    plt.ylabel('Area')
    
    plt.grid(True)
    
    plt.show()