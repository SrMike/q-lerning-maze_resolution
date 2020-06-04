import pygame, sys, time, random
from pygame.locals import *

import numpy as np
from matplotlib import pyplot as plt
import random
import pygame, sys,time
from pygame.locals import *
multi = 50
tam = 8
def qiteraciones(est_act,R,est,A,gamma,n):
    Q = np.copy(A)
    if n == 1:
        act_select = random.choice(np.where(R[est_act,:]>=0)[0])
    else:
        act_select = random.choice(np.where(Q[est_act,:]==np.max(Q[est_act,:]))[0])
    act_fut_pos = np.where(R[act_select,:]>=0)[0]
    Q_futuras = []
    for i in range(act_fut_pos.shape[0]):
        
        Q_futuras.append(Q[act_select,act_fut_pos[i]])
    
    Q[est_act,act_select] = R[est_act, act_select]+gamma*max(Q_futuras)
    # if est_act == 52:
    #     print('R[est_act,act_select] = ',R[est_act, act_select] )
    #     print('Q[est_act,act_select] = ',Q[est_act, act_select] )
    #     print('Estado actual: ',est_act)
    #     print('Estado siguiente',act_select)
    #     print('Q_futuras',Q_futuras)
    #     print('max(Q_futuras) = ',max(Q_futuras))
    #     print('np.where(R[act_select,:]>=0) = ', np.where(R[act_select,:]>=0))
    #     print('act_fut_pos = ',act_fut_pos)
    est_act = act_select
    return est_act,Q



# Declaro las iteraciones oficialmente inauguradas

pygame.init()

play_surface = pygame.display.set_mode((tam*multi, tam*multi))
fps = pygame.time.Clock()



def main():
    multi = 50
    #_________________________________________________________________________
    tam = 8
    
    pasos = 0
    mesa = np.array([[-1., -1., -1., -1., -1., -1., -1., -1.],
           [-1.,  0.,  0., -1.,  0.,  0.,  0., -1.],
           [-1., -1.,  0.,  0.,  0., -1.,  0., -1.],
           [-1.,  0.,  0., -1.,  0., -1.,  0., -1.],
           [-1.,  0., -1., -1.,  0., -1.,  0., -1.],
           [-1.,  0.,  0., -1.,  0., -1., -1., -1.],
           [-1.,  0., -1., -1.,  0.,  0., 100., -1.],
           [-1., -1., -1., -1., -1., -1., -1., -1.]])
    
    
    est = np.zeros(mesa.shape)
    cuenta = 0
    for i in range(tam):
        for j in range(tam):
            est[i,j] = cuenta
            cuenta = cuenta+1
    est = np.int32(est)
    
    tam2 = mesa.shape[0]*mesa.shape[1]
    
    
    R = np.ones([tam2,tam2])*-1 
    
    for fil in range(tam):
        for col in range(tam):
            estado = est[fil,col]
            if not(fil == 0):
                p1 = est[fil-1,col]
                R[estado,p1] = mesa[fil-1,col]
            if not(col == 0):
                p2 = est[fil, col-1]
                R[estado,p2] = mesa[fil,col-1]
            if not(fil == tam-1):
                p3 = est[fil+1,col]
                R[estado,p3] = mesa[fil+1,col]
            if not(col == tam-1):
                p4 = est[fil,col+1]
                R[estado,p4] = mesa[fil,col+1]
    R[54,53] = 10000
    Q = np.zeros(R.shape)
    gamma = 0.7
    est_act = 9

    #________________________________________________________________________
    
    est_act = 9
   
    score = 0

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run= False

        for i in range(tam):
            for j in range(tam):
                u = mesa[i,j]
                if u == -1: 
                    color = (255,0,0)
                elif u == 0:
                    color = (0,255,0)
                elif u > 0:
                    color = (0,0,255)
                pygame.draw.rect(play_surface,color,pygame.Rect(j*multi, i*multi, multi, multi))
        if score > 100:
            est_act,Q = qiteraciones(est_act,R,est,Q,gamma,0)
        else:
            est_act,Q = qiteraciones(est_act,R,est,Q,gamma,1)
        
        fil = np.where(est == est_act)[0][0]
        col = np.where(est == est_act)[1][0]
        pygame.draw.rect(play_surface,(100,100,100),pygame.Rect(col*multi, fil*multi,multi, multi))   
        pygame.display.flip()
        pasos = pasos +1
        if est_act == 54:
            score = score +1
            print('______________llega a la meta______________ ',score,pasos)
            plt.imshow(Q)
            plt.show()
            pasos = 0
            
            est_act = 9
        fps.tick(10000)

main()
pygame.quit()
