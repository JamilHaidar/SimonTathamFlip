import numpy as np

def gaussian_elimination_GF2(M):
    rows,cols = M.shape

    i=0
    j=0

    while i < rows and j < cols:
        k = np.argmax(M[i:, j]) +i
        
        temp = np.copy(M[k])
        M[k] = M[i]
        M[i] = temp
        
        rem = M[i, j:]
        col = np.copy(M[:, j])
        col[i] = 0
        
        flip = np.outer(col, rem)
        
        M[:, j:] = M[:, j:] ^ flip
        
        i += 1
        j +=1
    return M

n = 3
transition_matrix = np.identity(n*n)
for i in range(n):
    for j in range(n):
        m = n*i+j
        if i>0: transition_matrix[m,m-n] = True
        if i<n-1: transition_matrix[m,m+n] = True
        if j>0: transition_matrix[m,m-1] = True
        if j<n-1 : transition_matrix[m,m+1] = True
transition_matrix = transition_matrix.astype('uint8')

moves = np.zeros((n*n,1))
moves[0] = 1

final_board = (np.matmul(transition_matrix,moves)%2).astype('uint8')

M = np.hstack((transition_matrix,final_board))

print(gaussian_elimination_GF2(M))