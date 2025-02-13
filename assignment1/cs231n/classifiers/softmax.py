from builtins import range
import numpy as np
from random import shuffle
from past.builtins import xrange

def softmax_loss_naive(W, X, y, reg):
    """
    Softmax loss function, naive implementation (with loops)

    Inputs have dimension D, there are C classes, and we operate on minibatches
    of N examples.

    Inputs:
    - W: A numpy array of shape (D, C) containing weights.
    - X: A numpy array of shape (N, D) containing a minibatch of data.
    - y: A numpy array of shape (N,) containing training labels; y[i] = c means
      that X[i] has label c, where 0 <= c < C.
    - reg: (float) regularization strength

    Returns a tuple of:
    - loss as single float
    - gradient with respect to weights W; an array of same shape as W
    """
    # Initialize the loss and gradient to zero.
    loss = 0.0
    dW = np.zeros_like(W)

    #############################################################################
    # TODO: Compute the softmax loss and its gradient using explicit loops.     #
    # Store the loss in loss and the gradient in dW. If you are not careful     #
    # here, it is easy to run into numeric instability. Don't forget the        #
    # regularization!                                                           #
    #############################################################################
    # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****

    num_classes = W.shape[1]
    num_train = X.shape[0]
    #compute scores
    for i in xrange(num_train):
        scores = X[i].dot(W)
        scores -= np.amax(scores) #avoid instability
        correct_class_score = scores[y[i]]
        #loss calculation
        sum_scores = np.sum(np.exp(scores))
        softmax_loss = np.exp(correct_class_score)/sum_scores 
        loss += -np.log(softmax_loss)

        #grad calculation
        for j in xrange(num_classes):
            if j == y[i]:
                continue
            dW[:,j]+= (np.exp(scores[j])/sum_scores)*X[i]

        #gradient update for the correct class    
        dW[:,y[i]]-= (1-softmax_loss)*X[i]
        

    # Right now the loss is a sum over all training examples, but we want it
    # to be an average instead so we divide by num_train.
    loss /= num_train
    dW /= num_train
    # Add regularization to the loss and dW
    loss += reg * np.sum(W * W)
    dW+=2*reg*W
  

    # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****

    return loss, dW


def softmax_loss_vectorized(W, X, y, reg):
    """
    Softmax loss function, vectorized version.

    Inputs and outputs are the same as softmax_loss_naive.
    """
    # Initialize the loss and gradient to zero.
    loss = 0.0
    dW = np.zeros_like(W)

    #############################################################################
    # TODO: Compute the softmax loss and its gradient using no explicit loops.  #
    # Store the loss in loss and the gradient in dW. If you are not careful     #
    # here, it is easy to run into numeric instability. Don't forget the        #
    # regularization!                                                           #
    #############################################################################
    # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
    num_classes = W.shape[1]
    num_train = X.shape[0]
    scores = X.dot(W)
    scores -= np.amax(scores, axis=1).reshape(num_train,-1) #avoid instability
    #correct class scores into a column array
    correct_class_score=scores[np.arange(num_train),y]
    sum_scores = np.sum(np.exp(scores),axis=1)
    softmax_loss = np.exp(correct_class_score)/sum_scores 
    loss = np.sum(-np.log(softmax_loss))

    loss /= num_train

    # Add regularization to the loss.
    loss += reg * np.sum(W * W)

    #grad calculation
    margin_grad = np.zeros_like(scores)
    margin_grad = np.exp(scores)/sum_scores.reshape(num_train,1)
    margin_grad [np.arange(num_train),y] = -(1-softmax_loss)
    dW = X.T.dot(margin_grad)
    dW /= num_train

    dW+=2*reg*W
    

    # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****

    return loss, dW
