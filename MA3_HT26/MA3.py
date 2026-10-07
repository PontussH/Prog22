""" MA3.py

Student: Pontus Härkegård
Mail: pontusharkegard@gmail.com
Reviewed by:
Date reviewed:

"""
import random
import matplotlib.pyplot as plt
import math as m
import concurrent.futures as future
from statistics import mean 
from time import perf_counter as pc
from numba import njit
import concurrent.futures as future

# Exc1
def approximate_pi(n):
    x = [random.uniform(-1,1) for i in range(n)]
    y = [random.uniform(-1,1) for i in range(n)]
    inside = 0
    for i in range(n):
        if x[i]**2 + y[i]**2 <= 1:
            inside += 1
            plt.scatter(x[i], y[i], s=0.1, c='b')
        else:
            plt.scatter(x[i], y[i], s=0.1, c='r')
    plt.savefig(f'Pisim{n}.png')
    pi = 4*inside / n
    return pi


    # n is the number of points

    # Write your code here
    return

# Exc2, approximation
def sphere_volume(n, d): 
    # n is the number of points
    all_points = [[random.uniform(-1, 1) for i in range(d)] for k in range(n)]
    def inside(p):
        return sum(map(lambda x: x**2, p)) <= 1

    inside_points = list(filter(inside, all_points))
    return len(inside_points) / n * 2**d


#Exc2, real value
def hypersphere_exact(n, d):
    # n is the number of points
    return m.pi ** (d/2) / (m.gamma(d/2 + 1))
    # d is the number of dimensions of the sphere 
    

#Exc3: numba version
@njit
def sphere_volume_numba(n:int, d:int)->float:
    all_points = [[random.uniform(-1, 1) for i in range(d)] for k in range(n)]
    def inside(p):
        tot = 0
        for v in p:
            tot += v**2
        if tot <=1:
            return True
        else: return False

    tot = 0
    for i in range(n):
        if inside(all_points[i]):
            tot += 1
    return tot / n * 2**d


def runner(n, d):
    # n is the number of points
    all_points = [[random.uniform(-1, 1) for i in range(d)] for k in range(n)]
    def inside(p):
        return sum(map(lambda x: x**2, p)) <= 1

    return len(list(filter(inside, all_points))) #Returns the amount of points in the circle 

#Exc4: parallel code - parallelize actual computations by splitting data
def sphere_volume_parallel(n, d, np=10):

    with future.ProcessPoolExecutor() as ex:
        p = [n // np for i in range(np)]
        d_list = [d for i in range(np)]
        results = ex.map(runner, p, d_list)
        n_c = 0
        for r in results:
            n_c += r
        
    return n_c / n * 2**d

    
    # n is the number of points
    # d is the number of dimensions of the sphere
    # np is the number of processes
     
    
def main():
    # Exc1
    dots = [1000, 10000, 100000]
    for n in dots:
        pi = approximate_pi(n)
        print(f'The approximated value of pi is {pi} when n = {n}')
    # Exc2
    n = 10000
    d = 2
    print(sphere_volume(n, d))
    print(f"Actual volume of {d} dimentional sphere = {hypersphere_exact(n,d)}")

    n = 100000
    d = 11
    print(sphere_volume(n, d))
    print(f"Actual volume of {d} dimentional sphere = {hypersphere_exact(n,d)}")

    # Exc3
    n = 1000000
    d = 11
    for i in range(3):
        start = pc()
        sphere_volume(n, d)
        stop = pc()
        print(f"Exc3: Sequential time of {d} and {n}: {stop-start}")

    for i in range(3):
        start = pc()
        sphere_volume_numba(n, d)
        stop = pc()
        print(f"Exc3: Numba time of {d} and {n}: {stop-start}")

    # Exc4
    n = 1000000
    d = 11
    start = pc()
    print(sphere_volume(n, d))
    stop = pc()
    print(f"Exc4: Sequential time of {d} and {n}: {stop-start}")

    start = pc()
    print(sphere_volume_parallel(n, d))
    stop = pc()
    print(f"Exc4: Parallell time of {d} and {n}: {stop-start}")

    

if __name__ == '__main__':
	main()
