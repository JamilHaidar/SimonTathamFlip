def print_matrix(M,n=-1):
    if n==-1:
        n=len(M)+1
    for row in M:
        print(f'{row:0{n}b}')
    print()

def extract_matrix(M,m=-1,start_row=-1,start_column=-1,end_row=-1,end_column=-1):
    n = len(M)
    if m==-1:m=n+1
    if start_row == -1: start_row = 0
    if end_row == -1: end_row = n
    if start_column == -1: start_column = 0
    if end_column == -1: end_column = m

    select_all = (1<<m)-1
    select_start = select_all>>start_column
    select_end = select_all<<(m-end_column)
    selection = select_start & select_end
    res = []
    for row in M[start_row:end_row]:
        res.append((row&selection)>>(m-end_column))
    return res

def transpose(M,m):
    res = []
    for col_idx in range(m):
        val = 0
        for elem in extract_matrix(M,m=m,start_column=col_idx,end_column=col_idx+1):
            val  = (val<<1)|elem
        res.append(val)
    if len(M)==1:
        res = [ravel(res)]
    return res

def ravel(arr):
    val = 0
    for elem in arr:
        val = (val<<1)|elem
    return val

def inner_mul(A,B,m):
    temp = transpose(B,m)
    res = []
    for column in temp:
        val = 0
        for row in A:
            val= (val<<1) | bin(column&row).count('1')%2
        res.append(val)
    return res

def outer_mul(A,B):
    res = []
    for row in A:
        res.append(row*B)
    return res

def xor_mat(A,B):
    res = []
    for i in range(A):
        res.append(A[i]^B[i])
    return res

def find_max(arr):
    idx = 0
    while idx<len(arr):
        if arr[idx]==1:return idx
        idx+=1
    return 0

def print_board(M,n):
    selection = ((1<<(n))-1)<<(n*(n-1))
    for i in range(n):
        print(f'{((M&selection)>>(n*(n-i-1))):0{n}b}')
        selection = selection>>n
    print()

def solve_game(M,n):
    rows=n*n
    cols = n*n+1
    i=0
    j=0

    while i < rows and j < cols:
        k = find_max(extract_matrix(M,start_row=i,start_column=j,end_column=j+1))+i
        
        temp = M[k]
        M[k] = M[i]
        M[i] = temp

        rem = extract_matrix(M,start_row=i,end_row=i+1,start_column=j)[0]
        col = extract_matrix(M,start_column=j,end_column=j+1) # get pivot column
        col[i] = 0 # avoid xoring pivot row with itself

        flip = outer_mul(col,rem)

        select_start = ((1<<cols)-1)>>j
        select_end = ((1<<cols)-1)-select_start
        for idx in range(len(flip)):
            temp = M[idx]
            temp = temp&select_start
            temp = temp^flip[idx]
            M[idx] = (M[idx]&select_end) | (temp&select_start)
        i+=1
        j+=1
    return M

def generate_transition(n):
    transition_matrix = [1<<(n*n-i-1) for i in range(n*n)]

    for i in range(n):
        for j in range(n):
            m = n*i+j
            if i>0: transition_matrix[m] |= 1<< n*n-(m-n)-1
            if i<n-1: transition_matrix[m] |= 1<<n*n-(m+n)-1
            if j>0: transition_matrix[m] |= 1<<n*n-(m-1)-1
            if j<n-1 : transition_matrix[m] |= 1<<n*n-(m+1)-1

    return transition_matrix

def perform_move(moves,n,cell_index):
    moves ^= 1<<n*n-cell_index
    return moves

# n = 4

# transition_matrix = generate_transition(n)
# moves = 1<<n*n-1

# moves = perform_move(moves,n,16)
# # moves |= 1<<n*n-2

# final_board = inner_mul(transition_matrix,[moves],n*n)[0]

# M = []
# for i in range(n*n):
#     M.append(transition_matrix[i]<<1 | (final_board>>(n*n-i-1))&1)

# print_board(final_board,n)
# print_board(moves,n)