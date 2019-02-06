# Import libraries
import numpy as np
import math
import time
from decisiontree import build_decision_tree as getTree
from pruning import prune

# Define constants
NUM_CLASSES = 4

#########################################################
# Given a tree and a single measurement (7 values)
# return the predicted class
def predict(tree, value):
    # If tree is leaf, return its value
    if (tree["leaf"] != 0):
        return int(tree["leaf"])
    # Else traverse 1 level of the tree depending on the measurement and iterate recursively
    else:
        attr = tree["attribute"]
        split_val = tree["value"]
        if (value[attr] < split_val):
            return predict(tree["left"], value)
        else:
            return predict(tree["right"], value)


#########################################################
# Tests tree based on test set and return 5-tuple
# (Confusion Matrix | Recall | Precision | F score | Classification rate)
def evaluate(test_set, tree):
    # Initialize Confusion Matrix and other metrics variables
    CM = np.zeros((NUM_CLASSES, NUM_CLASSES))
    recall = 0
    precision = 0
    Fscore = 0
    classificationRate = 0
    # Test the tree and fill CM
    for test_val in test_set:
        # for each value in the test set, evaluate the prediction
        classPredicted = predict(tree, test_val)
        # check whether it matches the label and update confusion matrix accordingly
        trueLabel = int(test_val[7])
        CM[trueLabel-1][classPredicted-1] += 1
    # From CM calculate other metrics
        # 1 - Recall
    recallSum = 0
    for room in range(NUM_CLASSES):
        tp = CM[room][room]
        fn = 0
        for x in range(NUM_CLASSES):
            if (x != room):
                fn += CM[room][x]
            recallTemp = tp / (tp + fn)
        recallSum += recallTemp
    recall = recallSum / NUM_CLASSES
        # 2 - Precision
    precisionSum = 0
    for room in range(NUM_CLASSES):
        tp = CM[room][room]
        fp = 0
        for x in range(NUM_CLASSES):
            if (x != room):
                fp += CM[x][room]
        precisionTemp = tp / (tp + fp)
        precisionSum += precisionTemp
    precision = precisionSum / NUM_CLASSES
        # 3 - F score
    Fscore = 2 * precision * recall / (precision + recall)
    # 4 - Classification rate
    correctClass = 0
    totalData = 0
    for room in range(NUM_CLASSES):
        correctClass += CM[room][room]
        for x in range(NUM_CLASSES):
            totalData += CM[room][x]
    classificationRate = correctClass / totalData

    # Return the metrics
    return (CM, recall, precision, Fscore, classificationRate)


# Function that takes the metrics 5-tuple and prints it in a nice format
# (Confusion Matrix | Recall | Precision | F score | Classification rate)
def print_metrics(metrics):
    print("\tConfusion Matrix: ")
    print(metrics[0])
    print("\tRecall:              ", metrics[1])
    print("\tPrecision:           ", metrics[2])
    print("\tF Score:             ", metrics[3])
    print("\tClassification Rate: ", metrics[4])






set = np.loadtxt('co395-cbc-dt/wifi_db/clean_dataset.txt')
print(set)
np.random.shuffle(set)
crossValidate(set)
# print("Reading datafiles...")
# dataSet = np.loadtxt('co395-cbc-dt/wifi_db/clean_dataset.txt')
# print("Producing tree...")
# tree = getTree(dataSet, 0)[0]
# print("Testing tree...")
# # select TESTSET
# testSet = dataSet
# metrics = evaluate(testSet, tree)
# print("Confusion matrix")
# print(metrics[0])
# print("Recall\t", metrics[1])
# print("Precision\t", metrics[2])
# print("F Score\t", metrics[3])
# print("Accuracy\t", metrics[4])
