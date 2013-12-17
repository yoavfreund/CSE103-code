#!/bin/env python

import argparse

# Implement this function
def factorial(n):
    return 0

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Compute N!')
    parser.add_argument('N', type=int, help='an input integer')
    args = parser.parse_args()
    print factorial(args.N)
