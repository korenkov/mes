# coding: utf-8

import itertools
import random

#======================== �������� ������ =======================
"""
# P1 - ������� ������� �������� (������������ ������������ ������� ���������)
D = [ [0,  15, 20, 17, 10],
      [15, 0,  33, 12, 5],
      [20, 33, 0,  9,  7],
      [17, 12, 9,  0,  12],
      [10, 5,  7,  12, 0] ]
# ������� ������� n, �������� ����������� Nij = 1 / Dij
n1 = [[0 if y == 0 else 1.0/y for y in x] for x in D]
t1 = [ [0, 1, 1, 1, 1],
       [1, 0, 1, 1, 1],
       [1, 1, 0, 1, 1],
       [1, 1, 1, 0, 1],
       [1, 1, 1, 1, 0] ]   
alfa1 = 1.0
beta1 = 3.0 

# P2 - ������� ����������� ������������ (1-�������� ������; 2-����������� ��������� ��������� � ������� ����; 3-��������)
n2 = [0.8, 0.9, 0.2, 0.5, 0.6]

# P3 - ������� ����������� �����������
n3 = [0.4, 0.5, 0.8, 0.8, 0.9]

# P4 - ������� "��������������" ������������� �������� (���������� �����)
n4 = [0.6, 0.7, 0.8, 0.8, 0.9]

# f-����. "��������� �����", Q - ������������� "���������� �����", dt - ������� ������������
f = 1.0
Q = 100.0

# ������� ���������: �������� ������ ���������������� ��������� (��������, ������������� ������ ��������������� ��� ���������������� ���������). ��������������� ����
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

# ������ ������� ������ ����� 
vertex_list = range(len(D))

for vertex in vertex_list:
    # ��������� ������������� ����������/��������
    min_path = []
    Lmax = 100000

    G = 0
        
    iteration_count = 0
    while iteration_count < 10:
        G += 1

        # ������ ��������� ������� ��� ������ ���������
        current = vertex
        path = [current]

        # �������� �� ���� �������� (�� ��� ��� ���� ����� �����������)
        while True:
        
            # ������ ������, ������������ ��������� ��� �������� k ���
            potentioal_points = list(set(vertex_list).difference(path))
            # ������� �� ������� ����� (��������), ������� ������ ����������� ������ ���������������
            for i in vertex_list:
                if (sequences[i] == 1) and (i in potentioal_points):
                    potentioal_points.pop(i)

            
            # ���� �������� ������ ���� �������, �� ������ ���� ��������
            if len(potentioal_points) == 1:
                path.append(potentioal_points[0])
                break
                
            # ������������ (������ ������������ �� ������� ����� �����: p1+p2+p3+....=100%)
            # Pij = n1i*t1i*n2i*.../ sum(n1i*t1i*n2i*... + n2i*t2i*n2i*...)
            #  1) ����� ����������� ��� ���� ������������
            k = 0
            for i in potentioal_points:
                k1 = (n1[current][i] ** alfa1) * (t1[current][i] ** beta1)
                k2 = n2[i]
                k3 = n3[i]
                k4 = n4[i]
                k += k1 * k2 * k3 * k4
            #  2)  ������ ������������ 
            probability = []
            for i in potentioal_points:
                k1 = (n1[current][i] ** alfa1) * (t1[current][i] ** beta1)
                k2 = n2[i]
                k3 = n3[i]
                k4 = n4[i]
                probability.append((k1 * k2 * k3 * k4) / k)

            # ������ ���������� - ������ i-� ������� interval �������� ������ ���� ���������� ���������
            interval = list(itertools.accumulate(probability)) #only python3

            # ��������� ���������� ����� �� ��������� [0]..[max]
            rand = random.uniform(0, interval[-1])

            # ����������� ������ �������, � ������ ����������� �������� � ���������� �����
            number = 0
            while rand > interval[number]: number += 1
            # ��������� � ������ ����������� ���� �������
            current = potentioal_points[number]
            path.append(current)
            
        # ��������� ������ ����
        L = 0
        for i in range(len(path)-1):
            L += D[path[i]][path[i+1]]
        
        # ������������� ������� t 
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

