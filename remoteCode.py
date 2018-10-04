#!/usr/bin/env python
# -*- coding=utf-8 -*-


import os, sys, json, textwrap

'''
Script to use remoteVSCode plugin more easily.
'''

def error_gen(err_str):
    exa_str = textwrap.dedent('''
        Please refer to this example to edit the config file:
        {
            "port": 58888,
            "Node": {
                "Node1": {
                    "address": "192.168.0.101",
                    "user": "username",
                    "key": "/path/to/your/key/file"
                },
                "Node2": {
                    "address": "192.168.0.102",
                    "user": "username",
                    "key": "/path/to/your/key/file"
                }
            }
        }
        ''').strip()
    exit(err_str + "\n" + exa_str)


def run(port, node_dict):
    cmd_str = textwrap.dedent('''
        nohup ssh -N -i {KEY} -R {PORT}:127.0.0.1:{PORT} {USER}@{ADDRESS} > ~/remoteCode.log &
    '''.format(PORT = port, **node_dict)).strip()
    # print(cmd_str)
    os.system(cmd_str)


def node_check(node, node_dict):
    try:
        node_dict = node_dict[node]
        node_dict = {i.upper(): node_dict[i] for i in node_dict}
        return node_dict
    except KeyError:
        error_gen("Node '{}' not found in config file, please check!".format(node))


def port_check():
    pass


def dict_get(in_dict, key):
    try:
        val = in_dict[key]
        return val
    except KeyError:
        error_gen("Item '{}' not found in config".format(key))



def config_parse(config_file):
    '''
    load config file and return port & node info
    '''
    try:
        with open(config_file, 'r') as conf:
            config_dict = json.load(conf)
    except FileNotFoundError:
        exit("Config file '{}' was not found, please check".format(config_file))
    port = dict_get(config_dict, 'port')
    if type(port) != int and not port.isdigit():
        try:
            port = int(port)
        except ValueError:
            error_gen("Invalid port input, it can only be a number.")
    node_dict = dict_get(config_dict, 'Node')
    return port, node_dict


def main():
    port, node_dict = config_parse(CONFIG_FILE)
    node_dict = node_check(NODE, node_dict)
    run(port, node_dict)



if __name__ == '__main__':
    BASE_PATH = os.path.dirname(os.path.realpath(__file__))  # Script path
    CONFIG_FILE = os.path.join(BASE_PATH, 'config.json')
    NODE = 'Chuwi'
    main()