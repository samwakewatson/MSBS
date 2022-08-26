import multiprocessing
import os  
from Main import main                                                             
import base64
from github import Github
import pandas as pd
import time
import json

from matplotlib import pyplot as plt


#ids = [i for i in range (0,len(configs["configs"]))]                            
                                                                                
if __name__ == '__main__': 

    f = open('experimentConfigs.json')
    configs = json.load(f)
    f.close()

    numThreads = 10

    process_pool = multiprocessing.Pool(processes = numThreads)                                                      
    results = process_pool.starmap(main, [(i, configs["configs"][i]) for i in range (0, len(configs["configs"]))])

    #g = Github("")

    #repo = g.get_user().get_repo('testresults')

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

    print(x1)
    print(y1)
    print(y2)

    plt.scatter(x1,y1)
    plt.scatter(x2,y2)

    plt.show()

    '''for id in range (0,len(configs["configs"])):
        read_file = pd.read_excel (r'ID{0}.xlsx'.format(id), sheet_name="Shard 0")
        read_file.to_csv (r'ID{0}.txt'.format(id), index = None, header=True)

        with open('ID{0}.txt'.format(id), 'r') as file:
            content = file.read()

        # Upload to github
        git_file = "ID{0}_Timestamp{1}".format(id, timestamp) + "/BlockData"
        repo.create_file(git_file, "committing files", content, branch="main")
        print(git_file + ' CREATED')

        read_file = pd.read_excel (r'ID{0}.xlsx'.format(id), sheet_name="SimOutput")
        read_file.to_csv (r'ID{0}_{1}.txt'.format(id, "SimOutput"), index = None, header=True)

        with open('ID{0}_{1}.txt'.format(id, "SimOutput"), 'r') as file:
            content = file.read()

        # Upload to github
        git_file = "ID{0}_Timestamp{1}".format(id, timestamp) + "/SimOutput"
        repo.create_file(git_file, "committing files", content, branch="main")
        print(git_file + ' CREATED')'''

    #read_file = pd.read_excel (r'ID0.xlsx', sheet_name="Shard 0")
    #read_file.to_csv (r'ID0.txt', index = None, header=True)

    #with open('ID0.xlsx', 'r') as file:
        #content = file.read()
    #content = pd.read_excel('ID0.xlsx')
    #with open('C:\\path\\filename.txt', 'w') as outfile:
    #    content.to_string(outfile)

    '''with open('ID0.txt', 'r') as file:
        content = file.read()

    # Upload to github
    git_file = 'ID{0}Timestamp{1}.txt'.format()
    repo.create_file(git_file, "committing files", content, branch="main")
    print(git_file + ' CREATED')'''