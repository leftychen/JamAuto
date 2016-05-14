import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mlxtend.evaluate import plot_decision_regions
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
class BP_Netural:
    '''
    Netural Networking model using
    Back Propagation
    '''
    def __init__(self, repeat = 2000, eta = 0.01, reg_lambda = 0.01, reg_switch = True):
        self.repeat = repeat # how many times of iteration for learning
        self.eta = eta # learning speed
        self.reg_lambda =reg_lambda #regularization strength
        self.N_example = 0 # training set size
        self.input_dim = 0 # input dimension
        self.output_dim = 0 # output dimension
        self.reg_lambda_switch = reg_switch # add regularization term or not
        self.model = {}

    def modelloss(self,model, X, y):
        '''
        model is the input for {weight and constant term for activation function}
        z1 and z2 is the input layer; a1 and exp_scores is the output layers
        '''
        W1, b1, W2, b2 = model['W1'], model['b1'], model['W2'], model['b2']

        self.N_example = len(X)
        z1 = X.dot(W1) + b1
        a1 = np.tanh(z1)
        z2 = a1.dot(W2) + b2
        exp_scores = np.exp(z2)
        probs = exp_scores / np.sum(exp_scores, axis = 1, keepdims = True) # get the probability for each output
        correct_logprobs = -np.log(probs[range(self.N_example), y]) # compare the result to real output
        data_loss = np.sum(correct_logprobs) # get the sum of error
        if self.reg_lambda_switch:
            data_loss += self.reg_lambda/2 * (np.sum(np.square(W1)) + np.sum(np.square(W2)))

        return 1./ self.N_example * data_loss

    def predict(self, X, model = None):
        W1, b1, W2, b2 = self.model['W1'], self.model['b1'], self.model['W2'], self.model['b2']
        if model is not None:
            W1, b1, W2, b2 = model['W1'], model['b1'], model['W2'], model['b2']
        z1 = X.dot(W1) + b1
        a1 = np.tanh(z1)
        z2 = a1.dot(W2) + b2
        exp_scores = np.exp(z2)
        probs = exp_scores / np.sum(exp_scores, axis = 1, keepdims = True)
        return np.argmax(probs, axis = 1) # choose the value with the highest probability

    def train(self, node_dim , X , y ,result_type = 2, loss_print = False): # training data
        # node_dim is how many hidden layer you gonna use for training
        self.N_example = len(X)
        self.input_dim = X.shape[1]
        self.output_dim = result_type
        np.random.seed(123)
        W1 = np.random.randn(self.input_dim, node_dim) / np.sqrt(self.input_dim)
        # get the random weight of function z1 =  W1 * x + b
        b1 = np.zeros((1, node_dim))
        W2 = np.random.randn(node_dim, self.output_dim) / np.sqrt((node_dim))
        b2 = np.zeros((1, self.output_dim))
        model = {}
        for i in range(self.repeat):
            #Forward Propagation
            z1 = X.dot(W1) + b1
            a1 = np.tanh(z1)
            z2 = a1.dot(W2) + b2
            exp_scores = np.exp(z2)
            probs = exp_scores / np.sum(exp_scores, axis = 1, keepdims = True)
            #Back Propagation
            # Compare to the real result and make some adjustment using learning speed
            delta3 = probs
            delta3[range(self.N_example), y] -= 1
            dW2 = (a1.T).dot(delta3)
            db2 = np.sum(delta3, axis = 0, keepdims = True)
            delta2 = delta3.dot(W2.T) * (1 - np.power(a1, 2))
            dW1 = np.dot(X.T, delta2)
            db1 = np.sum(delta2, axis = 0)

            if  self.reg_lambda_switch:
                dW1 += self.reg_lambda * W1
                dW2 += self.reg_lambda * W2

            W1 += -self.eta * dW1
            W2 += -self.eta * dW2
            b1 += -self.eta * db1
            b2 += -self.eta * db2

            model = {'W1':W1, 'b1':b1, 'W2':W2, 'b2':b2}
            #record the model into a dict
            if loss_print and i % 1000 == 0:
                print("Loss after iteration %s: %s" %(i, self.modelloss(model, X, y)))

            self.model = model

        return model

    def plot_decision_boundary(self, X, y):
        #plot the boundary
        plot_decision_regions(X, y, clf = self)
        plt.show()








