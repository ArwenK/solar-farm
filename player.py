import numpy as np
import os
from numpy.random import randint

class Player:

    def __init__(self):
        self.dt = 0.5
        self.efficiency=0.95
        self.sun=[]
        self.bill = np.zeros(48) # prix de vente de l'électricité
        self.load= np.zeros(48) # chargement de la batterie (li)
        self.battery_stock = np.zeros(49) #a(t)
        self.capacity = 100
        self.max_load = 70
        self.prices = {"internal" : [],"external_purchase" : [],"external_sale" : []}
        self.imbalance=[]

    def take_decision(self, time):

            # TO DO:
            # implement your policy here to return the load charged / discharged in the battery
            # below is a simple example
            
                        if time==0:
                return 0 
                    
            elif time>=12 and time<=44:
                return -min(self.battery_stock[time-1],self.max_load*self.dt)
                
            else:
                return 0.5*self.sun[time-1]*self.dt

    def update_battery_stock(self, time,load):
            if abs(load) > self.max_load:
                load = self.max_load*np.sign(load) #saturation au maximum de la batterie
            
            new_stock = self.battery_stock[time] + (self.efficiency*max(0,load) - 1/self.efficiency * max(0,-load))*self.dt
            
            #On rétablit les conditions si le joueur ne les respecte pas :
            
            if new_stock < 0: #impossible, le min est 0, on calcule le load correspondant
                load = - self.battery_stock[time] / (self.efficiency*self.dt)
                new_stock = 0
    
            elif new_stock > self.capacity:
                load = (self.capacity - self.battery_stock[time]) / (self.efficiency*self.dt)
                new_stock = self.capacity
    
            self.battery_stock[time+1] = new_stock
            
            
            return load
        
    def compute_load(self,time,sun):
        load_player = self.take_decision(time)
        load_battery=self.update_battery_stock(time,load_player)
        self.load[time]=load_battery - sun
        
        return self.load[time]
    
    def observe(self, t, sun, price, imbalance):
        self.sun.append(sun)
        
        self.prices["internal"].append(price["internal"])
        self.prices["external_sale"].append(price["external_sale"])
        self.prices["external_purchase"].append(price["external_purchase"])
        
        self.imbalance.append(imbalance)
        
    
    def reset(self):
        self.load= np.zeros(48)
        self.bill = np.zeros(48)
        
        last_bat = self.battery_stock[-1]
        self.battery_stock = np.zeros(49)
        self.battery_stock[0] = last_bat
        
        self.sun=[]
        self.prices = {"internal" : [],"external_purchase" : [],"external_sale" : []}
        self.imbalance=[]
