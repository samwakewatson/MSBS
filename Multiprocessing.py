import multiprocessing
import os  
from Main import main                                                             
import base64
import pandas as pd
import time
import json

from matplotlib import pyplot as plt


                                                                                
if __name__ == '__main__': 

    f = open('experimentConfigs.json')
    configs = json.load(f)
    f.close()

    numThreads = 6

    process_pool = multiprocessing.Pool(processes = numThreads)                                                      
    results = process_pool.starmap(main, [(i, configs["configs"][i]) for i in range (0, len(configs["configs"]))])


    timestamp = time.time()

    #plt.plot([result["crossShardProp"] for result in results], [result["sameShardTxLatency"] for result in results]) 
    #plt.plot([result["crossShardProp"] for result in results], [result["crossShardTxLatency"] for result in results])

    #plt.plot([result["crossShardProp"] for result in results],[result["sameShardTxLatency"] for result in results])
    #plt.plot([result["crossShardProp"] for result in results],[result["crossShardTxLatency"] for result in results])

    x1 = []
    y1 = []
    for resultSet in results:
        for datapoint in resultSet:
            x1.append(datapoint["crossShardProp"])
            y1.append(datapoint["sameShardTxLatency"])

    x2 = []
    y2 = []
    for resultSet in results:
        for datapoint in resultSet:
            x2.append(datapoint["crossShardProp"])
            y2.append(datapoint["crossShardTxLatency"])

    x3 = []
    y3 = []
    for resultSet in results:
        for datapoint in resultSet:
            for i in datapoint["perShardFees"]:
                x3.append(datapoint["crossShardProp"])
                y3.append(i)

    print(x1)
    print(y1)
    print(y2)

    #plt.scatter(x1,y1)
    #plt.scatter(x2,y2)
    plt.scatter(x3,y3)

    plt.xlabel("crossShardProp")
    plt.ylabel("per shard fees")

    plt.show()