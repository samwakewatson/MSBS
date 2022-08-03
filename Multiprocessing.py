import multiprocessing
import os  
from Main import main                                                             
import base64
from github import Github
import pandas as pd
import time

ids = [0,1,2,3]                            
                                                                                
if __name__ == '__main__':                                                                                
    process_pool = multiprocessing.Pool(processes = len(ids))                                                        
    process_pool.map(main, ids)

    g = Github("")

    repo = g.get_user().get_repo('testresults')

    timestamp = time.time()

    for id in ids:
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
        print(git_file + ' CREATED')

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