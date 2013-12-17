#!/usr/bin/env python

## This is a skeleton code for students who use Python.

import numpy
import argparse

def knn_fit(train_data, train_label, test_data, k):
	# train_data, train_label, test_data are numpy arrays; 
	# each row represents an instance;
	# train_data and test_data both have 784 columns;
	# train_label has one column;
	# k is the number of neighbors to use, an integer

	AB = numpy.dot(test_data, train_data.T)
	A = numpy.sum(numpy.abs(test_data)**2,axis=1)
	AA = numpy.tile(A, (train_data.shape[0], 1))
	B = numpy.sum(numpy.abs(train_data)**2,axis=1)
	BB = numpy.tile(B, (test_data.shape[0], 1))
	D = AA.T + BB - 2*AB
	
	neighbor_labels = train_label[numpy.argsort(D, axis=1)[:,:k]]
	label = [numpy.argmax(numpy.bincount(l)) for l in neighbor_labels.astype(int)]
	return numpy.array(label)

def compute_test_error_rate(label_predicted, label_true):
	# TODO: Return the percentage of prediction errors
	return 0


if __name__ == "__main__":
	# load data
	dataset = numpy.loadtxt('digits.txt')
	# dataset is loaded as a matrix with shape 1600 by 785 
	# (1600 rows; each row represents an image; each row has 784 integers for feature vector + 1 integer for label)
	num_examples = dataset.shape[0]

	K = [3,5,7,9,11]	# choices of k
	M = 6 				# number of folds

	# initialize the error matrix
	errors = numpy.zeros((M, len(K)))
	
	for fold_index in range(M):

		# TODO: Partition the dataset into a training set and a testing set for this fold.
		# To get a submatrix within the dataset matrix, use dataset[row_start:row_end, col_start:col_end]
		# The first index is the row range (row_end not included), the second index is the column range;
		# index can also be a single number, in which case you get a 1-d array. 
		# index starts from 0 and -1 represents the last element.
		# You can use numpy.vstack([A,B]) to vertically stack two matrices to form a new matrix.
		train_data = dataset[0:1000, 0:-1]	# for example, this gets you the data part of the first 1000 examples; 
							# it is a 1000 by 784 matrix.
		train_label = dataset[0:1000, -1]	# this gives you the label part of the first 1000 examples;
							# it is a 1000 by 1 matrix.
		test_data = dataset[1001:num_examples, 0:-1]
		test_label_true = dataset[1001:num_examples, -1]

		for k_index, k in enumerate(K):

			# run knn classifier; get the predicted test labels
			test_label_predicted = knn_fit(train_data, train_label, test_data, k)

			# compute test error rate by comparing the predicted test labels with ground truth
			test_error_rate = compute_test_error_rate(test_label_predicted, test_label_true)
			
			# fill in the error matrix
			errors[fold_index, k_index] = test_error_rate

	# compute the average test error over all folds for each k
	average = numpy.mean(error, axis=0)

	# TODO: choose the best k based on the average test error rate
	best_k = 11

	# output result
	output_file = open('output.txt', 'w')
	output_file.write("%d\n" % M)
	for err_row in errors:
		output_file.write(" ".join(["%.4f" % j for j in err_row]) + '\n')
	output_file.write(" ".join(["%.4f" % i for i in average]) + "\n")
	output_file.write("%d\n" % best_k)
	output_file.close()
