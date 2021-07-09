
def roundnum(x):
    num = round(x*5)/5
    return num

def matrix_generator(column, row):
    """
    Takes in integers i and j.
    Return a matrix with i rows and j columns,
    where the value at the i-th row and j-th column
    is represented by matrix[i][j]
    """
    matrix = []
    for i in range(column):
        num = []
        for j in range(row):
            num.append(0.0)
        matrix.append(num)
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
    data_matrix = matrix_generator(11,11)  #Assumed all column is filled
    for i in data:
        indexfirst = int(((roundnum(i[0]) + 1) * 10) / 2 - 1) + 1 
        indexsecond = int(((roundnum (i[1]) + 1) * 10) / 2 - 1) + 1
        data_matrix[indexfirst][indexsecond] += 1
    column_sum_list = []
    for i in range(0,11):
        column_sum = 0
        for j in range (0,11):
            column_sum += data_matrix[j][i]
        column_sum_list.append(column_sum)
    print(column_sum_list)
    distribution = matrix_generator(11,11)
    for i in range(0,11):
        for j in range(0,11):
            if column_sum_list[i] == 0:
                distribution[i][j] = 0
            else:
                distribution[i][j] = data_matrix[i][j] / column_sum_list[i]
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
        matrix = matrix_generator(11,11)
        for j in range(0,11):
            for k in range(0,11):
                probability = 0
                for m in range(0,11):
                    probability += chain[i-1][j][m] * distribution[m][k]                
                matrix[j][k] = round(probability,5)
        chain[i] = matrix
        print("")
        print(chain[i])
    return chain

def main():
    date = []
    file = open("sentiments.txt","r")
    values = file.read().splitlines()
    for value in values:
        list1 = []
        info = value.split(",")
        time = info[0]
        sentimentvalue = float(info[1])
        list1.append(time)
        list1.append(sentimentvalue)
        date.append(list1)
    #date = [["2020-02-03",-1], ["2020-02-04",0.5],["2020-02-05",0.9]]
    sentiment = []
    for i in range (len(date) - 1):
        pair = []
        pair.append(date[i][1])
        pair.append(date[i+1][1])
        sentiment.append(pair)
 
    matrix = multinomial_mle(sentiment)

    chain = markov_chain(matrix)


"""
    count = 1
    for i in chain:
        count1 = -1
        print(str(count) + " days after ")
        print("")
        print("      -1  -0.8 -0.6 -0.4 -0.2  0.0  0.2  0.4  0.6  0.8  1.0")
        for j in i:
            num = format(count1, '.1f')
            if (num == "-0.0"):
                print(" 0.0", end=" ")
            else:
                if (num[0] != "-"):
                    print(" " + format(count1, '.1f'), end=" ")
                else:
                    print(format(count1, '.1f'), end=" ")
            print(j)
            count1 += 0.2
        print("")
        count += 1
"""

if __name__ == '__main__':
    main()