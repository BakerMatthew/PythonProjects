#!/usr/bin/python3

from BSTNode import BSTNode
from BSTree import BSTree
import random

# bugs to vladimir dot kulyukin at gmail dot com

# implement this method
def gen_rand_bst(num_nodes, a, b):
    bst = BSTree()
    for x in range(num_nodes):
        bst.insertKey(random.randint(a, b))
    return bst

# implement this method
def estimate_list_prob_in_rand_bsts_with_num_nodes(num_rbsts, num_nodes, a, b):
    # Set up bst list
    bst_list = [gen_rand_bst(num_nodes, a, b) for x in range(num_rbsts)]
    # Get total count of bst which are lists
    list_count = 0
    for tree in bst_list:
        if tree.isList():
            list_count += 1
    # Compute probability and return result in tuple
    return float(list_count) / float(num_rbsts), bst_list

def estimate_list_probs_in_rand_bsts(num_nodes_start, num_nodes_end, num_rbsts, a, b):
    d = {}
    for num_nodes in range(num_nodes_start, num_nodes_end+1):
        d[num_nodes] = estimate_list_prob_in_rand_bsts_with_num_nodes(num_rbsts, num_nodes, a, b)
    return d

# implement this method
def estimate_balance_prob_in_rand_bsts_with_num_nodes(num_rbsts, num_nodes, a, b):
    # Set up bst list
    bst_list = [gen_rand_bst(num_nodes, a, b) for x in range(num_rbsts)]
    # Get total count of bst which are balanced
    list_count = 0
    for tree in bst_list:
        if tree.isBalanced():
            list_count += 1
    # Compute probability and return result in tuple
    return float(list_count) / float(num_rbsts), bst_list

def estimate_balance_probs_in_rand_bsts(num_nodes_start, num_nodes_end, num_rbsts, a, b):
    d = {}
    for num_nodes in range(num_nodes_start, num_nodes_end+1):
        d[num_nodes] = estimate_balance_prob_in_rand_bsts_with_num_nodes(num_rbsts, num_nodes, a, b)
    return d
