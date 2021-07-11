#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  4 15:11:27 2019

@author: ermesonandrade
"""

#https://psutil.readthedocs.io/en/latest/

#https://www.thepythoncode.com/article/get-hardware-system-information-python

import psutil 
import time
import datetime
import csv
import argparse

#-----------------------------------------------------------------------

def criarCSV(x, y):
    
    name = "monitoring" + x + "_" + y + ".csv"
    
    f = open(name, 'w')
    
    try:
        writer = csv.writer(f)  
        writer.writerow(('currentTime','core0Usage(%)','core1Usage(%)','core2Usage(%)','core3Usage(%)','totalCpuUsage(%)',
                        'totalMemory', 'availableMemory','usedMemory','percentageMemory(%)',
                         'buffersMemory','cachedMemory',
                        'totalSwap','freeSwap','usedSwap','percentageSwap(%)',
                        'totalExt4Partition','usedExt4Partition','freeExt4Partition','percentageExt4Partition(%)',
                        'totalBootPartition','usedBootPartition','freeBootPartition','percentageBootPartition(%)',
                        'total_IO_read', 'total_IO_write'))
    finally:
        f.close()
        
 
#-----------------------------------------------------------------------
    
def get_size(bytes, suffix="B"):
    """
    Scale bytes to its proper format
    e.g:
        1253656 => '1.20MB'
        1253656678 => '1.17GB'
    """
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor

#-----------------------------------------------------------------------

def executeMonitoring(x, y):
    
    name = "monitoring" + x + "_" + y + ".csv"
    
    f = open(name, 'a')
    
    try:
        writer = csv.writer(f) 
        print('\n')

        #  Current Time
        print("="*20, "Current Time", "="*20)
        currentDT = datetime.datetime.now().time()
        print ("Current time:", str(currentDT))
        
        print('\n')
        
        # let's print CPU information
        print("="*10, "CPU Info", "="*10)
        # number of cores
        print("Physical cores:", psutil.cpu_count(logical=False))
        print("Total cores:", psutil.cpu_count(logical=True))
        # CPU frequencies
        cpufreq = psutil.cpu_freq()
        print(f"Max Frequency: {cpufreq.max:.2f}Mhz")
        print(f"Min Frequency: {cpufreq.min:.2f}Mhz")
        print(f"Current Frequency: {cpufreq.current:.2f}Mhz")

        # CPU usage
        print("CPU Usage Per Core:")
        totalUsage = 0
        cpu_usage = psutil.cpu_percent(percpu=True)
        for i, percentage in enumerate(cpu_usage):
            print(f"Core {i}: {percentage}%")
            #totalUsage = totalUsage + percentage         
        print(f"Total CPU Usage: {psutil.cpu_percent()}%")
        
        print('\n')
    
        # Memory Information
        print("="*10, "Memory Information", "="*10)
        # get the memory details
        svmem = psutil.virtual_memory()
        print(f"Total: {get_size(svmem.total)}")
        print(f"Available: {get_size(svmem.available)}")
        print(f"Used: {get_size(svmem.used)}")
        print(f"Percentage: {svmem.percent}%")
        print(f"Buffers: {get_size(svmem.buffers)}")
        print(f"Cached: {get_size(svmem.cached)}")
        print("="*5, "SWAP", "="*5)
        
        # get the swap memory details (if exists)
        swap = psutil.swap_memory()
        print(f"Total: {get_size(swap.total)}")
        print(f"Free: {get_size(swap.free)}")
        print(f"Used: {get_size(swap.used)}")
        print(f"Percentage: {swap.percent}%")
        
        print('\n')
    
        # Disk Information
        print("="*10, "Disk Information", "="*10)
        print("Partitions and Usage:")
        # get all disk partitions
        partitions = psutil.disk_partitions()
        partition_usage1 = psutil.disk_usage(partitions[0].mountpoint)
        partition_usage2 = psutil.disk_usage(partitions[1].mountpoint)
        #print(partition_usage.total)
        
        for i, partition in enumerate(partitions):
            print(f"=== Device: {partition.device} ===")
            print(f"  Mountpoint: {partition.mountpoint}")
            print(f"  File system type: {partition.fstype}")
            
            partition_usage = psutil.disk_usage(partition.mountpoint)

            if (i==0):
                print(f"  Total Size: {get_size(partition_usage.total)}")
                print(f"  Used: {get_size(partition_usage.used)}")
                print(f"  Free: {get_size(partition_usage.free)}")
                print(f"  Percentage: {partition_usage.percent}%")
            elif (i==1):
                print(f"  Total Size: {get_size(partition_usage.total)}")
                print(f"  Used: {get_size(partition_usage.used)}")
                print(f"  Free: {get_size(partition_usage.free)}")
                print(f"  Percentage: {partition_usage.percent}%")
            
         # get IO statistics since boot
        disk_io = psutil.disk_io_counters()
        print(f"Total read: {get_size(disk_io.read_bytes)}")
        #worksheet.write(linha,22,get_size(disk_io.read_bytes))
        print(f"Total write: {get_size(disk_io.write_bytes)}")
        #worksheet.write(linha,23,get_size(disk_io.write_bytes))

      
        writer.writerow((datetime.datetime.now(),cpu_usage[0],cpu_usage[1],cpu_usage[2],cpu_usage[3], psutil.cpu_percent(),
                        svmem.total, svmem.available, svmem.used,svmem.percent,
                         svmem.buffers, svmem.cached,
                        swap.total, swap.free, swap.used,swap.percent,
                        partition_usage1.total, partition_usage1.used, partition_usage1.free, partition_usage1.percent,
                        partition_usage2.total, partition_usage2.used, partition_usage2.free, partition_usage2.percent,
                        disk_io.read_bytes, disk_io.write_bytes))
   
    finally:
        f.close()        
             
        
#-----------------------------------------------------------------------

parser = argparse.ArgumentParser(description = 'Entradas')

parser.add_argument('--dispositivo', action = 'store', dest = 'd',
                           required = True, help = 'Cloud ou Edge.')
parser.add_argument('--workload', action = 'store', dest = 'w', required = True,
                           help = '0.1, 0.5 or 1.0')

arguments = parser.parse_args()

criarCSV(arguments.d, arguments.w) #Chama a função para criar o cvs

while True:

    executeMonitoring(arguments.d, arguments.w) #Coleta os dados de monitoramento
    
    time.sleep(60) #Espera 60 segundos para coletar novamente



