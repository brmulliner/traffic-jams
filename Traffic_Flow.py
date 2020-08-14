'''FIRST FILE - SINGLE LANE'''
import numpy as np
import collections
import matplotlib.pyplot as plt
#from matplotlib import colors
from matplotlib.colors import ListedColormap



"""
start_pos returns an array x indicating the positions of N cars on a road of 
length L with initial velocity v, ensuring no two cars are assigned to the 
same position. Any empty space on the road is displayed as a -1 in the array x
"""
def start_pos(L,N):
    x = -np.ones([L])           # array of -1s of length L
    while  np.count_nonzero(x) > L-N:    # check for duplicates
        x[np.random.randint(0,L)] = 0 # generate new random positioning
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
if the velocity of a car is such that in the next time iteration it will
progress beyond the current position of any other car in front, the velocity
is decreased so that it will be one less than the distance between the two cars
"""    
def avoid_crash(x):
    for i in range(len(x)):
        if x[i] != -1:
            xv = int(x[i])
            for j in range(1,xv+1):
                if i+j < len(x):
                    if x[i+j] != -1:
                        xv = j-1
                        break
                else:
                    if x[i+j-len(x)] != -1:
                        xv = j-1
                        break
            x[i] = xv
    return x
 
       
"""
there is a random probability p of a car slowing down at every time step
"""
def random_slow(x,p):
    r = np.random.uniform(0,1,len(x))
    r = np.where( r < p, - 1 , 0 )
    x = np.where(x > 0, x+r, x)
    return x


"""
cars of velocity v move forward by v steps
"""
def move_forward(x,f):
    z = -np.ones([len(x)])
    for i in range(len(x)):
        if x[i] != -1:
            a = int(x[i])
            if (i+a) >= len(x):
                a_ = a -len(x)
                z[i+a_] = a
                f= f+1
            else:
                z[i+a] = a
    return z ,f

"""
progresses 1 time step by performing the 3 speed change conditions in order
then move forwards.
"""
def time_step(x,v_max,p,f):
    x = speed_up(x,v_max)
    x = avoid_crash(x)
    x = random_slow(x,p)
    x, f = move_forward(x,f)
    return x ,f

"""
Returns the average speed of N cars on a road x with max speed v_max
"""
def analyse_cars(x,N,v_max): #,cc):
    #c = collections.Counter(x)
    #for i in range(v_max+1):
    #    cc[i] = cc[i] + c[i]
    tot_array = sum(x)      # sum of all entries in array x
    empties = -1*(len(x)-N) # sum of all empty values in x
    tot_cars = tot_array - empties # sum of all non -1 entries
    av = tot_cars / N       # total speed divided by no. of cars
    #print("average speed = ",av)
    return av



'''Flow Rate against Density'''
L = 267
V = 5
pp = np.array([0,0.05,0.1,0.15,0.2,0.25]) # probability of an unexpected slow down
t = 5000

for p in pp:
    flow_count = 0.
    CC = np.arange(0,200,5)
    flow_rate = np.zeros(len(CC))
    for i,C in enumerate(CC):
        flow_count = 0.
        road = start_pos(L,C)
        for j in range(t):
            road, flow_count = time_step(road,V,p,flow_count)
        #print("i = ",i,flow_count/t)
        flow_rate[i] = flow_count/t
    plt.plot(CC/(250*7.5*10**-3),flow_rate, label = ('p = %.2f'%p))
    #print(flow_rate) 


plt.ylabel('Flow Rate (cars per s)')
plt.xlabel('Density (cars per km)')
plt.legend()
plt.show()
 
      
'''AVERAGE SPEED AGAINST DECELERATION'''
t = 100000                     # total time sample to be taken for
length = 267                # road of length L
cars =  80                       #_array = np.arange(0,150,5)                  # number of cars on road
v_max = 5                   # max speed of a car
pp = np.linspace(0,1,50)                    # probability of an unexpected slow down
#cc = np.zeros(v_max+1)
pos_init = start_pos(length,cars)   # set out initial layout for array
av_speed = np.empty(len(pp))
flow_rate = np.empty(len(pp))
for i in range(len(pp)):
    p = pp[i]
    arrays = np.empty((t,length))
    av = np.empty((t,length))
    road = pos_init                     # name array 'road'
    flow_count=0
    for _ in range(t):
        road,flow_count = time_step(road, v_max, p, flow_count) # perform a sample of time length t
        arrays[_] = road
        av[_] = analyse_cars(road,cars,v_max)
    av_speed[i] = (np.mean(av)*27)
    flow_rate[i] = (flow_count/t)
#print(flow_count/t)
#    cc = analyse_cars(road, cars, v_max, cc)
plt.plot(pp,av_speed)
plt.title('Average car speed against Deceleration Probability')
plt.ylabel('Car Speed ($kmh-1$)')
plt.xlabel('Deceleration Probability')
plt.show()


'''VIZUALIZER'''
t = 100                     # total time sample to be taken for
length = 267                # road of length L
cars =  80                       #_array = np.arange(0,150,5)                  # number of cars on road
v_max = 3                   # max speed of a car
p=0.1                    # probability of an unexpected slow down
#cc = np.zeros(v_max+1)
pos_init = start_pos(length,cars)   # set out initial layout for array
#av_speed = np.empty(len(pp))
#flow_rate = np.empty(len(pp))
p = 0.1
arrays = np.empty((t,length))
av = np.empty((t,length))
road = pos_init                     # name array 'road'
flow_count=0
for _ in range(t):
    road,flow_count = time_step(road, v_max, p, flow_count) # perform a sample of time length t
    arrays[_] = road
    av[_] = analyse_cars(road,cars,v_max)
    #av_speed[i] = (np.mean(av)*27)
    #flow_rate[i] = (flow_count/t)
#print(flow_count/t)
#    cc = analyse_cars(road, cars, v_max, cc)
colors = ["w","#e50000","#fd411e","#f97306","#ffff14","#c0fb2d","#01ff07"]
cmap = ListedColormap(colors)
#create 5000 Random points distributed within the circle radius 100
n = length
m = t
a = np.linspace(0, 2 * np.pi, n)
rad = np.linspace(0, m, m)
print(len(a),len(rad))
r, theta = np.meshgrid(rad, a)
print(r.shape,theta.shape,arrays.shape)
#z = np.random.uniform(0, 5, (m,n))
#Create a polar projection
plt.subplot(projection="polar")
#plt.scatter(theta,r, c= arrays.T, cmap = cmap, vmin = -1, vmax = 5)
plt.pcolormesh(theta, r, arrays.T, cmap = cmap, vmin = -1, vmax = v_max)
plt.grid()
plt.colorbar()
plt.show()





"""
speed_dist = np.array([  0,  27,  54,  81, 108, 135]) 
    
zeros =speed_dist -7.5
ones = speed_dist -4.5
twos = speed_dist -1.5
threes = speed_dist + 1.5
fours = speed_dist +4.5
fives = speed_dist +7.5

#fig, axs = plt.subplots(1, 6, sharey=True)
# Remove horizontal space between axes
#fig.subplots_adjust(hspace=0)



plt.title('Distribution of car speeds at peak flow rate')
plt.ylabel('Frequency')
plt.xlabel('Car Speed ($kmh^{-1})$')
plt.xticks([  0,  27,  54,  81, 108, 135])
plt.bar(zeros,cc0, width = 3, label= "p=0.00")
plt.bar(ones,cc05, width = 3, label= "p=0.05")
plt.bar(twos,cc1, width = 3, label= "p=0.10")
plt.bar(threes,cc15, width = 3, label= "p=0.15")
plt.bar(fours,cc2, width = 3, label= "p=0.20")
plt.bar(fives,cc25, width = 3, label= "p=0.25")
plt.legend()



plt.plot(cars_array,flow_count_0, label= "p=0.00")
plt.plot(cars_array,flow_count_05, label= "p=0.05" )
plt.plot(cars_array,flow_count_1, label= "p=0.10" )
plt.plot(cars_array,flow_count_15, label= "p=0.15")
plt.plot(cars_array,flow_count_2, label= "p=0.20")
plt.plot(cars_array,flow_count_25, label= "p=0.25")
plt.xlabel("Density (cars per kilometer)")
plt.ylabel("Flow Rate (cars per s)")
plt.title("Graph to show Flow Rate against Road Density")
plt.legend()
plt.show()

#print(road)                         # print final layout
"""

'''SECOND FILE - TWO LANE'''
import numpy as np
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

    