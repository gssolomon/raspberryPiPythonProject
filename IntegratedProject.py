# -*- coding: utf-8 -*-

#Created on Tue Jan  9 19:09:20 2018

#@author: glenn
#student no: 040908930


import tkinter as tk
from sense_hat import SenseHat
from datetime import datetime
import time
import os
from tkinter import filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

class measureTempHumid:
    def __init__(self, top):
        self.tempList = []
        self.humidList = []
        self.currTime = []
        
        self.startButton = tk.Button(top, text = "Start Reading", command = lambda: self.startTempHumid(top))
        self.startButton.grid(row = 2, column = 2, columnspan = 3, pady = 15)
                     
        self.selectFile = tk.Label(top, text = "Select File for Graphical Report: ")
        self.selectFile.grid(row = 5, column = 2, columnspan = 4, sticky = tk.E + tk.W, pady = 5)
        
        self.fileEntry = tk.Entry(top, validate = "focusout", validatecommand = self.callBack)
        self.fileEntry.grid(row = 6, column = 2, sticky = tk.E + tk.W, pady = 5, columnspan = 2)
        
        self.browseFile = tk.Button(top, text = "Browse", command = lambda: self.browseOpen())
        self.browseFile.grid(row = 6, column = 4, pady = 5)
        
        self.graphButton = tk.Button(top, text = "Generate Graph", command = lambda: self.generateGraph(top))
        self.graphButton.grid(row = 7, column = 2, pady = 15, columnspan = 4)
        
    def callBack(self):
        self.inFile = self.fileEntry.get()
        
    def browseOpen(self):
        currentDir = os.getcwd() #assigning current working directory
        self.tempFile = filedialog.askopenfilename(initialdir = currentDir, filetypes = (("Text Files", "*.txt"), ("All Files", "*.*"))) #which file to open
        
        if len(self.tempFile) > 0: #to display in entrybox the file-destination
            print("%s file chosen" %self.tempFile)
            
            self.inFile = self.tempFile
            self.fileEntry.delete(0,tk.END)
            self.fileEntry.insert(0,self.tempFile)
            
        
    def startTempHumid(self, top):
        
        
        
            
        self.sense = SenseHat()
        self.sense.clear()
        
        q = 1
        while (q < 10):
                
            
            self.temp = self.sense.get_temperature()
            #self.temp = round(self.temp,2)
                
            self.humid = self.sense.get_humidity()
            #self.humid = round(self.humid,2)
            
            #self.dt = datetime.now().strftime("%H:%M:%S")
            #self.dt2 = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.dt = time.time()
            
            self.tempList.append(self.temp)
            self.humidList.append(self.humid)
            self.currTime.append(self.dt)
            
            q += 1
            #time.sleep(1)
        self.startLabel = tk.Label(top, text = "The Temperature and Humidity Readings finished and written")
        self.startLabel.grid(row = 3, column = 2, columnspan = 3, padx = 10, pady = 10)
            
        
        with open("ReadindsTemp.txt", "w") as f:
            f.write("Building no: E" + "\tRoom: 212" + "\tCollection Device: RPI \n")
            x = 1
            for i in self.tempList, self.currTime:
                f.write(str(self.tempList[x]) + "," + str(self.currTime[x]) + "\n")
                x = x + 1
                
        
        with open("ReadingsHumid.txt", "w") as f2:
            f2.write("Building no: E" + "\tRoom: 212" + "\tCollection Device: RPI \n")
            y = 1
            for j in self.humidList, self.currTime:
                f2.write(str(self.humidList[y]) + "," + str(self.currTime[y]) + "\n")
                y = y + 1
            
            
    def generateGraph(self, top):
        self.inFile = self.fileEntry.get()
        
        if self.fileEntry.get() == "":
            self.browseOpen()
        
        if self.fileEntry.get() == "":
            return
        
        self.x = []
        self.y = []
        
        with open(self.inFile, "r") as f3:
            f3.readline()
            self.lines = f3.read().splitlines()
            
            for i in self.lines:
                self.a, self.b = i.split(",")
                self.x.append(float(self.a))
                self.y.append(float(self.b))
        
        fig = Figure(figsize=(6,6))
        a = fig.add_subplot(111)
        a.scatter(self.x,self.y,color='red')
        a.plot(self.x,self.y,color='blue')

        a.set_title ("Graph", fontsize=16)
        a.set_ylabel("Temp/Humid", fontsize=14)
        a.set_xlabel("Time", fontsize=14)
        canvas = FigureCanvasTkAgg(fig, master = top)
        canvas.get_tk_widget().grid(row = 10, column = 2, columnspan = 4)        
        canvas.draw()
            
            
def main():
    root = tk.Tk()
    root.resizable(width = False, height = False)
    root.title("Weather & Humidity Analysis")
    begin = measureTempHumid(root)
    root.mainloop()
    
if __name__=="__main__": main()