#!/usr/bin/env python

import numpy as np
# import scipy.spatial
# import scipy.stats
import argparse

def knn_fit(train_data, train_label, test_data, k):
	# D = scipy.spatial.distance.cdist(test_data, train_data, 'euclidean')	
	AB = np.dot(test_data, train_data.T)
	A = np.sum(np.abs(test_data)**2,axis=1)
	AA = np.tile(A, (train_data.shape[0], 1))
	B = np.sum(np.abs(train_data)**2,axis=1)
	BB = np.tile(B, (test_data.shape[0], 1))
	D = AA.T + BB - 2*AB
	
	neighbor_labels = train_label[np.argsort(D, axis=1)[:,:k]]
	# label = np.squeeze(scipy.stats.mode(neighbor_labels, axis=1)[0])
	label = [np.argmax(np.bincount(l)) for l in neighbor_labels.astype(int)]
	return label

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='')
	parser.add_argument('--train_data', help='training data filename', type=str)
	parser.add_argument('--train_label', help='training label filename', type=str)
	parser.add_argument('--test_data', help='test data filename', type=str)
	parser.add_argument('--test_label', help='(output) test label filename', type=str)
	parser.add_argument('-k','--k', help='number of neighbors', type=int, default=3)
	args = vars(parser.parse_args())

	train_data = np.loadtxt(args['train_data'])
	train_label = np.loadtxt(args['train_label'])
	test_data = np.loadtxt(args['test_data'])
	test_label = knn_fit(train_data, train_label, test_data, args['k'])
	np.savetxt(args['test_label'], test_label, fmt='%d')
