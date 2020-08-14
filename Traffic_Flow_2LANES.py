import numpy as np
import collections
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap



"""
start_pos returns an array x indicating the positions of N cars on a road of
2 lanes olength L with initial velocity v, ensuring no two cars are assigned
to the same position. Any empty space on the road is displayed as a -1 in the
array x
"""
def start_pos(L,N):
    x = -np.ones([2,L])           # array of -1s of dimensions Lx3
    while  np.count_nonzero(x) > 2*L-N:    # check for duplicates
        x[np.random.randint(0,2),np.random.randint(0,L)] = 0 # generate new random positioning
    return x


"""
if a car is not travelling at the maximum speed, it will increase by one
"""
def speed_up(x,v_max):
    x = np.where(x == -1 , -1, np.where(x < v_max , x+1 , x))
    return x # array indicating new provisional velocities, before movement


"""
returns an array where each values is the position of a car on the road in order
"""
def map_positions(x):
    y = np.array([])
    for i in range(len(x)):
        if x[i] != -1:
            y = np.append(y,i)
    return y


"""
def overtake_start(i,j,x,xv,L):
    if i%L < i+xv+1%L:
        if all( i == -1 for i in x[1,i%L:(i+xv+1)%L]) and x[0,(i+j)%L] < xv:     #if there is space in lane 1 and the car ahead in lane 0 is moing slow
            x[1,i] = int(x[0,i])     #change lane
            xv = -1
        else:
            xv = j-1            #slow down
    else:
        if all( i == -1 for i in x[1,(i+xv+1)%L:i%L]) and x[0,(i+j)%L] < xv:     #if there is space in lane 1 and the car ahead in lane 0 is moing slow
            x[1,i] = int(x[0,i])     #change lane
            xv = -1
        else:
            xv = j-1            #slow down


def overtake_finish(i,j,x,xv,v,L):
    if (i-v)%L < (i+xv+1)%L:
        if all( i == -1 for i in x[0,(i-v)%L:(i+xv+1)%L]):
            x[0,i] = int(x[1,i])
            xv= -1
        else:
            xv = j-1
        if all( i == -1 for i in x[0,(i+xv+1)%L:(i-v)%L]):
            x[0,i] = int(x[1,i])
            xv= -1
        else:
            xv = j-1
"""

            
"""
if the velocity of a car is such that in the next time iteration it will
progress beyond the current position of any other car in front, the velocity
is decreased so that it will be one less than the distance between the two cars
"""    
def avoid_collision_slowlane(x,L):
    for i in range(L):          #go through entire road
        if x[0,i] != -1:        #check for car
            xv = int(x[0,i])    #xv is car's speed
            for j in range(1,xv+1):     #go through range of car's speed
                if x[0,(i+j)%L] != -1:  # if a car is in the way
                    if i%L < i+xv+1%L:
                        if all( i == -1 for i in x[1,i%L:(i+xv+1)%L]) and x[0,(i+j)%L] < xv:     #if there is space in lane 1 and the car ahead in lane 0 is moing slow
                            x[1,i] = int(x[0,i])     #change lane
                            xv = -1
                            break
                        else:
                            xv = j-1            #slow down
                            break
                    else:
                        if all( i == -1 for i in x[1,(i+xv+1)%L:i%L]) and x[0,(i+j)%L] < xv:     #if there is space in lane 1 and the car ahead in lane 0 is moing slow
                            x[1,i] = int(x[0,i])     #change lane
                            xv = -1
                            break
                        else:
                            xv = j-1            #slow down
                            break
            x[0,i] = xv
    return x

"""
If there is enough space in the slow lane, a car in the fast lane will change
lane. if the velocity of a car is such that in the next time iteration it will
progress beyond the current position of any other car in front, the velocity
is decreased so that it will be one less than the distance between the two cars
"""
def avoid_collision_fastlane(x,L,v):
    for i in range(L):
        if x[1,i] != -1:
            xv = int(x[1,i])
            for j in range(1,xv+1):
                if x[1,(i+j)%L] != -1:
                    if (i-v)%L < (i+xv+1)%L:
                        if all( i == -1 for i in x[0,(i-v)%L:(i+xv+1)%L]):
                            x[0,i] = int(x[1,i])
                            xv= -1
                            break
                        else:
                            xv = j-1
                            break
                    else:
                        if all( i == -1 for i in x[0,(i+xv+1)%L:(i-v)%L]):
                            x[0,i] = int(x[1,i])
                            xv= -1
                            break
                        else:
                            xv = j-1
                            break
            x[1,i] = xv
    return x
                    
            
                

       
"""
there is a random probability p of a car slowing down at every time step
"""
def random_slow(x,p):
    r = np.random.uniform(0,1,x.shape)
    r = np.where( r < p, 1 , 0 )
    x = np.where(x > 0, x-r, x)
    return x

"""
a car of speed v in the slow lane will change lane if its velocity is greater
than the car ahead's, and there is appropriate space in the other lane

def start_overtake():
    return
"""



"""
cars of velocity v move forward by v steps
"""
def move_forward(x,f,L):
    z = -np.ones(x.shape)
    for j in range(2):
        for i in range(L):
            if x[j,i] != -1:
                a = int(x[j,i])
                if (i+a) >= L:
                    a_ = a -L
                    z[j,i+a_] = a
                    f= f+1
                else:
                    z[j,i+a] = a
    return z ,f

"""
progresses 1 time step by performing the 3 speed change conditions in order
then move forwards.
"""
def time_step(x,L,v_max,p,f):
    x = speed_up(x,v_max)
    #print("sped up")
    #print(x)
    x = avoid_collision_slowlane(x,L)
    #print("slow lane")
    #print(x)
    x = avoid_collision_fastlane(x,L,v_max)
    #print("fast lane")
    #print(x)
    x = random_slow(x,p)
    #print("slow")
    #print(x)
    x, f = move_forward(x,f,L)
    #print("move")
    #print(x)
    return x ,f

"""
Returns the average speed of N cars on a road x with max speed v_max
"""
def analyse_cars(x,N,v_max): #,cc):
    cc = np.zeros(v_max+1)
    c = collections.Counter(x)
    for i in range(v_max+1):
        cc[i] = cc[i] + c[i]
    #tot_array = sum(x)      # sum of all entries in array x
    #empties = -1*(len(x)-N) # sum of all empty values in x
    #tot_cars = tot_array - empties # sum of all non -1 entries
    #av = tot_cars / N       # total speed divided by no. of cars
    #print("average speed = ",av)
    return cc
 
L = 250
C = 150
V = 5
flow_count = 0.
p= 0.15
t = 1000

'''
flow_count = 0
road = start_pos(L,C)
for _ in range(t):
    road, flow_count = time_step(road,L,V,p,flow_count)
flow_rate = flow_count / t
#print(road)
print(flow_rate)


'''

CC = np.arange(0,200,5)
flow_rate = np.zeros(len(CC))
for i,C in enumerate(CC):
    flow_count = 0.
    road = start_pos(L,C)
    for j in range(t):
        road, flow_count = time_step(road,L,V,p,flow_count)
    print("i = ",i,flow_count/t)
    flow_rate[i] = flow_count/t
print(flow_rate)

plt.plot(CC/(250*7.5*10**-3),flow_rate)
plt.ylabel('Flow Rate (cars per s)')
plt.xlabel('Density (cars per km)')
plt.show()


#colors = ["w","#e50000","#fd411e","#f97306","#ffff14","#c0fb2d","#01ff07"]
#cmap = ListedColormap(colors)

    