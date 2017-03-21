# coding: utf-8

import itertools
import random

#======================== исходные данные =======================
"""
# P1 - матрица времены операций (симметричная относительно главной диагонали)
D = [ [0,  15, 20, 17, 10],
      [15, 0,  33, 12, 5],
      [20, 33, 0,  9,  7],
      [17, 12, 9,  0,  12],
      [10, 5,  7,  12, 0] ]
# создаем матрицу n, обратную расстояниям Nij = 1 / Dij
n1 = [[0 if y == 0 else 1.0/y for y in x] for x in D]
t1 = [ [0, 1, 1, 1, 1],
       [1, 0, 1, 1, 1],
       [1, 1, 0, 1, 1],
       [1, 1, 1, 0, 1],
       [1, 1, 1, 1, 0] ]   
alfa1 = 1.0
beta1 = 3.0 

# P2 - матрица доступности оборудования (1-загрузка станка; 2-соотношение габаритов заготовки и рабочей зоны; 3-удобство)
n2 = [0.8, 0.9, 0.2, 0.5, 0.6]

# P3 - матрица доступности инструмента
n3 = [0.4, 0.5, 0.8, 0.8, 0.9]

# P4 - матрица "традиционности" использования операций (накопление опыта)
n4 = [0.6, 0.7, 0.8, 0.8, 0.9]

# f-коэф. "испарения опыта", Q - интенсивность "добавления опыта", dt - прирост интесивности
f = 1.0
Q = 100.0

# матрица переходов: фиксация строго последовательных переходов (например, невозможность выбора резьбонарезания без предварительного сверления). Ориентированный граф
sequences = [ [0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0],
              [0, 1, 0, 0, 0],
              [0, 0, 1, 0, 0],
              [1, 0, 0, 0, 0] ]      
"""
#======================== random input date's =======================
N = 10
D = [ [random.randint(0, 100) for j in range(N)] for i in range(N)]
n1 = [[0 if y == 0 else 1.0/y for y in x] for x in D]
t1 = [ [1 for j in range(N)] for i in range(N)] 
sequences = [ [0 for j in range(N)] for i in range(N)] 
n2 = [random.random() for i in range(N)]
n3 = [random.random() for i in range(N)]
n4 = [random.random() for i in range(N)]
alfa1 = 1.0
beta1 = 3.0 
f = 1.0
Q = 100.0

#======================== ant colony optimization algorithm =======================

# список номеров вершин графа 
vertex_list = range(len(D))

for vertex in vertex_list:
    # обнуление промежуточных переменных/массивов
    min_path = []
    Lmax = 100000

    G = 0
        
    iteration_count = 0
    while iteration_count < 10:
        G += 1

        # задаем начальную вершину для старта алгоритма
        current = vertex
        path = [current]

        # проходим по всем вершинам (до тех пор пока будут альтернтивы)
        while True:
        
            # расчет вершин, потенциально пригодных для перехода k ним
            potentioal_points = list(set(vertex_list).difference(path))
            # удаляем те вершины графа (операции), которые должны выполняться строго последовательно
            for i in vertex_list:
                if (sequences[i] == 1) and (i in potentioal_points):
                    potentioal_points.pop(i)

            
            # если осталась только одна вершина, то расчет пути закончен
            if len(potentioal_points) == 1:
                path.append(potentioal_points[0])
                break
                
            # нормирование (расчет вероятностей по каждому ребру графа: p1+p2+p3+....=100%)
            # Pij = n1i*t1i*n2i*.../ sum(n1i*t1i*n2i*... + n2i*t2i*n2i*...)
            #  1) общий знаменатель для всех составляющих
            k = 0
            for i in potentioal_points:
                k1 = (n1[current][i] ** alfa1) * (t1[current][i] ** beta1)
                k2 = n2[i]
                k3 = n3[i]
                k4 = n4[i]
                k += k1 * k2 * k3 * k4
            #  2)  массив вероятностей 
            probability = []
            for i in potentioal_points:
                k1 = (n1[current][i] ** alfa1) * (t1[current][i] ** beta1)
                k2 = n2[i]
                k3 = n3[i]
                k4 = n4[i]
                probability.append((k1 * k2 * k3 * k4) / k)

            # расчет инетрвалов - каждый i-й элемент interval является суммой всех предыдущих элементов
            interval = list(itertools.accumulate(probability)) #only python3

            # генератор случайного числа на инетравле [0]..[max]
            rand = random.uniform(0, interval[-1])

            # определение номера вершины, с учетом вероятности перехода и случайного числа
            number = 0
            while rand > interval[number]: number += 1
            # добавляем в список пройденного пути вершину
            current = potentioal_points[number]
            path.append(current)
            
        # суммируем длинну пути
        L = 0
        for i in range(len(path)-1):
            L += D[path[i]][path[i+1]]
        
        # перевычесляем матрицу t 
        if L < Lmax:
            dt = Q / L
            for i in range(len(path)-1):
                t1[path[i]][path[i+1]] = f * t1[path[i]][path[i+1]] + dt
            Lmax = L
            min_path = path
            iteration_count = 0
        else:
            iteration_count += 1

    #print("path=", min_path, "  total time=", Lmax)
    print (G)

