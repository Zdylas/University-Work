import numpy as np
import numpy.linalg as la
import matplotlib.pyplot as plt


def markov_chains(transition_matrix, vector, n):
    # Computes markov chain to n power returning the last matrix in chain
    # Using A^k = P D^k P_-1

    eigenvalues, EV_matrix = la.eig(transition_matrix)
    EV_matrix_inverse = la.inv(EV_matrix)
    diagonalized = np.diag(eigenvalues)

    nth_term = EV_matrix @ la.matrix_power(diagonalized, n) @ EV_matrix_inverse @ vector 
    
    return nth_term
    
def power_method(matrix, vector, iterations):
    # Finds an estimation for the dominant eigenvalue and eigenvector pair
    # Return last iteration 

    for _ in range(iterations):
        vector = vector/la.norm(vector, 2)
        vector = matrix @ vector

    dominant_eigenvector = vector/la.norm(vector, 2)
    dominant_eigenvalue = la.norm(vector, 2) 

    return dominant_eigenvalue, dominant_eigenvector

def leslie(matrix, starting_vector, iterations):
    # Prints the leslie matrix each iteration 

    new_vector = matrix @ starting_vector
    for i in range(iterations-1):
        new_vector = matrix @ new_vector
    return new_vector

    
def test_markov():
    # Setup matrices to find markov chain results for nth term
    transition_matrix = np.array([[1/7,  3/10,     0,     0,  3/10,     0,     0],
                                  [3/7,  1/10,     0,  3/13,     0,     0,  3/10],
                                  [  0,     0,  1/10,  3/13,  3/10,  3/13,     0],
                                  [  0,  3/10,  3/10,  1/13,     0,  3/13,  3/10],
                                  [3/7,     0,  3/10,     0,  1/10,  3/13,     0],
                                  [  0,     0,  3/10,  3/13,  3/10,  1/13,  3/10],
                                  [  0,  3/10,     0,  3/13,     0,  3/13,  1/10]])

    initial_s_vector = np.array([[1/7],
                                 [1/7],
                                 [1/7],
                                 [1/7],
                                 [1/7],
                                 [1/7],
                                 [1/7]])


    long_term = markov_chains(transition_matrix, initial_s_vector, 1000000)
    probabilities = (np.diagonal(transition_matrix)**2).T * long_term.T
    print(probabilities.T)



def test_leslie():

    leslie_matrix = np.array([[   0,    0,   0, 100,  100,  100, 100],
                              [0.15,    0,   0,   0,    0,    0,   0],
                              [   0,  0.3,   0,   0,    0,    0,   0],
                              [   0,    0, 0.5,   0,    0,    0,   0],
                              [   0,    0,   0, 0.4,    0,    0,   0],
                              [   0,    0,   0,   0, 0.25,    0,   0],
                              [   0,    0,   0,   0,    0, 0.25,   0]])

    initial_s_vector = np.array([[ 0],
                                 [ 0],
                                 [ 0],
                                 [10],
                                 [ 0],
                                 [ 0],
                                 [ 0]])
    final_data = np.array([[0],
                           [0],
                           [0],
                           [10],
                           [0],
                           [0],
                           [0]])
    
    harvesting = np.array([[0.29114, 0, 0, 0, 0, 0, 0],
                           [      0, 1, 0, 0, 0, 0, 0],
                           [      0, 0, 1, 0, 0, 0, 0],
                           [      0, 0, 0, 1, 0, 0, 0],
                           [      0, 0, 0, 0, 1, 0, 0],
                           [      0, 0, 0, 0, 0, 1, 0],
                           [      0, 0, 0, 0, 0, 0, 1]])

    new_leslie = harvesting @ leslie_matrix 
    print(new_leslie)
    eigenvalues, eigenvectors = la.eig(new_leslie)
    print(eigenvalues)
    """
    for _ in range(50):
        final_data = np.c_[final_data, leslie(leslie_matrix, initial_s_vector, iterations)]
        initial_s_vector = leslie(leslie_matrix, initial_s_vector, iterations)

    fig, ax = plt.subplots()
    labels = np.array(range(50 + 1)) * 5

    total = np.zeros(51)
    width = 5
    for i in range(7):
        age_data = final_data[i, :]
        ax.bar(labels, age_data, width,  label=f"{i*5}-{i*5+5}", bottom=total)
        total += age_data
        
    ax.set_ylabel("Population")
    ax.set_xlabel("Time (Days)")
    ax.legend()
    plt.show()
    """

def test_power_method():
    matrix = np.array([[7, 2],
                         [2, 3]])

    start_vector = np.array([[1],
                             [0]])

    iterations = 6

    eigenvalue, eigenvector = power_method(matrix, start_vector, iterations)

    print(f"Eigenvalue: {eigenvalue}\nEingenvector:\n{eigenvector}")


def main():

    #test_markov()
    
    test_leslie()

    #test_power_method()


if __name__ == "__main__":
    main()


