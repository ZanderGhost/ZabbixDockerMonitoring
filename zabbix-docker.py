#!/usr/bin/env python

import docker
import sys
from datetime import datetime

def numberOfContainers(containerList):

    return len(containerList)

def numberOfRunningContainer(containerList):

    number = 0
    for container in containerList:
        state = container['State']
        if state == 'running':
            number += 1

    return number

def nameOfContainer(containerList):

    names = []
    for container in containerList:
        name = container['Names'][0]
        if name[0].startswith('/'):
            name = name.split('/')[1]
        names.append({'{#NAME}': name})

    con_dict = {}
    con_dict['data'] = names

    return json.dumps(con_dict)


#function converts string to object "datetime".
def strToDate(str_date):
    date = datetime.strptime(str_date, '%Y-%m-%dT%X')
    return date

#The function returns the difference between the current time and the passed one.
def timeDelta(start_time):
    result = datetime.today() - start_time
    return result.total_seconds()

#The function checks the status of the container and returns the status of the container.

def inspectContainer(client, container):
    container_data = client.inspect_container(container)
    state = container_data[u'State']
    container_status = str(state[u'Status'])
    container_started = str(state[u'StartedAt']).split('.')[0]
    if container_status == 'running':
        if timeDelta(strToDate(container_started)) > 30:                  #Check if the container was started within 30 seconds.
            return container_status
        else:
            return 'Warning! Possibly the container is in a cyclic reboot.'
    else:
        return container_status


if __name__ == "__main__":

    if len(sys.argv) > 1:
        client = docker.APIClient(base_url='unix://var/run/docker.sock')
        if sys.argv[1] == 'list':
            import json
            containerList = client.containers()
            sys.exit(nameOfContainer(containerList))
        else:
            client = docker.APIClient(base_url='unix://var/run/docker.sock')
            sys.exit(inspectContainer(client, sys.argv[1]))
    else:
        print ('Please run script with list or container name')
        sys.exit(0)
