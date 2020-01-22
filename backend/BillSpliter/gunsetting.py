import multiprocessing

bind = "0.0.0.0:80"
workers = multiprocessing.cpu_count() 
threads = workers*3