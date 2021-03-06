#!/usr/local/bin/python3

import sys, os, string, threading
import paramiko
import json

lock = threading.Lock()

def main():
    threads = []
    with open('loadtest.json', 'r') as f:
        loadtest_config = json.load(f)
    host = loadtest_config['host']
    port = loadtest_config['port']
    load = loadtest_config['load']
    username = loadtest_config['username']
    password = loadtest_config['password']
    sleeptime = loadtest_config['sleeptime']

    run = "echo hi; sleep " + str(sleeptime)
    for _ in range(load):
        thread = threading.Thread(target=sshRun, args=(host, port, run, username, password))
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()
    

def sshRun(host,port,run,username,password):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, port=port, username=username, password=password)
    stdin, stdout, stderr = ssh.exec_command(run)
    stdin.write('xy\n')
    stdin.flush()
    with lock:
        _ = stdout.readlines()

if __name__ == "__main__":
    main()