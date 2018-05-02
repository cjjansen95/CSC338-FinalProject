"""
    Group: PacMan
    Authors: Connor Jansen (cjjansen95), Eric McCullough (eam96), Jacob Wakefield (jwakefield97), John Bell (jab331)
    Assignment: CSC338 final project

    Description: A web crawler that takes an inital url from the command line and collects the links on that page. It then
                 links that are from the same origin. From those links it visits links that are from the same origin. It continues
                 this process until no more links from the starting origin are found. In other words it crawls through a website discovering
                 all of it's pages. The program does this by detecting how many cpu's the computer running it has, it then splits the initial
                 load (links) from the entry page amongst the processes which spawn threads to handle any further links that are discovered on
                 subsequent pages.
    Tech: Python 3, multiprocessing, threading, time (timing of threads/processes and overall program), sys (command line args),
          beautiful soup (parse html response), and requests (make network requests)

    Execution Flow: command line arg (entry domain) is passed to parsePage() which collects the all the links that are on the same domain.
                    The processManager() function is then called which sets up the processes based on the system cpu count and spreads
                    the links collected from  the initial page across the processes. Once the processes are initalized, they are all started.
                    Once the process is started it initializes a pool of threads to be used in the recursive link collection process.
                    Once a link is found on the same origin, a thread (one that is not busy working on another page) is used to process
                    the page and collect links (thread calls parsePage() which visits the page and processes links).
                    If all threads in the pool are busy then the process waits until a thread is freed up. Once each process is done collecting
                    /visiting the links it calls output() which waits for all processes to complete before gathering stats (execuetion time, number
                    of links etc.) and outputing all the links to a file.
"""

from bs4 import BeautifulSoup
from threading import Thread
import requests
import multiprocessing as mp
import sys
import time

DOMAIN = "" # Ex: https://www.google.com
MAX_PAGE_COUNT = 1000 #max number of threads the user wants to limit each process to.
THREADS_IN_USE = [] #threads that are currently working
URLS_TO_VISIT = [] #urls to be visited
URLS_VISITED = [] #urls that have been visited

"""
    Description: get number of cpus and setup/manage processes.
"""
def processManager():
    #get number of cpus
    #spawn the process with the threadManager as the function to execute
    #start the processes

    while len(URLS_VISITED) < MAX_PAGE_COUNT and len(URLS_TO_VISIT) > 0:
        cpu_count = mp.cpu_count()
        processes = []
        number_of_pages = len(URLS_TO_VISIT) // cpu_count
        beginIndex = 0
        endIndex = number_of_pages
        #balanced_number_of_pages = len(URLS_TO_VISIT)//cpu_count + len(URLS_TO_VISIT)%cpu_count
        for i in range(cpu_count):
            if i < cpu_count:
                p = mp.Process(target = parsePage, args = [URLS_TO_VISIT[0:number_of_pages]])
                del URLS_TO_VISIT[0:number_of_pages]
                p.start()
            else:
                p = mp.Process(target = parsePage, args = [URLS_TO_VISIT[0:]])
                del URLS_TO_VISIT[0:]
                p.start()
        for p in processes:
            p.join()

    output()
"""
    Description: function that spawns the threads for the process and manages the threads. Uses a set number
                 threads (thread pool).
"""
def threadManager():
    #if the max thread count hasn't been reached, acquire a lock to access URLS_TO_VISIT,
    #while if URLS_TO_VISIT isn't empty, grab URLS_TO_VISIT[0] remove it from the list, acquire the lock
    #to access URLS_VISITED and push URLS_TO_VISIT[0].
    #spawn a new thread to visit the url. Don't forget to release all locks after access the info needed.
    pass


"""
    Description: visit page distributed by inital page using a thread of the processes. This function gets
                 gets called by the threads.
"""
def parsePage(url):
    #visit url and parse the return html.
    #if the links contains the domain and aren't in URLS_VISITED (acquire lock for list), acquire the lock
    #for URLS_TO_VISIT and push the valid link to the list.
    #don't forget to release all locks after using them and try catch any network request or parsing.
    print("Firing parsePage")
    pass


"""
    Description: block for processes and threads to end then display stats/output links to a file.
"""
def output():
    #block for all processes to be finished.
    #then output stats about the runtime and links.
    pass


"""
    Description: entry point to the application. Grabs url from command line and passes it to initalPage(). After
                 the inital links are collected processManager() is called and the links are distributed amongst them.
"""
if __name__ == "__main__":

    DOMAIN = sys.argv[1]
    MAX_PAGE_COUNT = int(sys.argv[2]) #get thread pool size from command line
    parsePage(DOMAIN)
    processManager()
    output()
