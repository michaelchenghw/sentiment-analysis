import random_data_generator

def matrix_generator(i, j):
    """
    Takes in integers i and j.
    Return a matrix with i rows and j columns,
    where the value at the i-th row and j-th column
    is represented by matrix[i][j]
    """
    matrix = []
    column = []
    for m in range(0,j):
        column.append(0)
    for m in range(0,i):
        matrix.append(column)
    return matrix

def multinomial_mle(data):
    """
    Takes in a list named 'data' where data[i] = [x,y],
    in which x is the sentimental index on the first day
    and y is the sentimental index on the second day.
    
    Returns a list named 'distribution' where
    distribution[y] = [px], in which px is the estimated
    probability that the subsequent day will have the
    sentimental index of y given the sentimental
    index on the previous day is x.
    
    0 <= x,y <= 9
    """
    data_matrix = matrix_generator(10,10)
    for i in data:
       data_matrix[i[1]][i[0]] += 1
    column_sum_list = []
    for i in range(0,10):
        column_sum = 0
        for j in range (0,10):
            column_sum += data_matrix[j][i]
        column_sum_list.append(column_sum)
    distribution = matrix_generator(10,10)
    for i in range(0,10):
        for j in range(0,10):
            distribution[i][j] = data_matrix[i][j] / column_sum_list[j]
    return distribution

def markov_chain(distribution):
    """
    Takes in the markov chain matrix 'distribution'
    where distribution[y] = px, px is the estimated
    probability that the subsequent day will have the
    sentimental index of y given the sentimental
    index on the previous day is x.
    
    Returns the list 'chain' where chain[i] is the
    estimated probability distribution after i days.
    """
    chain = [distribution, None, None, None, None, None, None]

    for i in range(1,7):
        matrix = matrix_generator(10,10)
        for j in range(0,10):
            for k in range(0,10):
                probability = 0
                for m in range(0,10):
                    probability += chain[i-1][j][m] * distribution[m][k]                
                matrix[j][k] = round(probability,2)
        chain[i] = matrix
    return chain

def main():
    data = random_data_generator.random_data()
    matrix = multinomial_mle(data)
    chain = markov_chain(matrix)
    return chain

if __name__ == '__main__':
    main()
