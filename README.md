# SimonTathamFlip
Implementation of the Flip game from Simon Tatham's Puzzles with an optimal linear algebra-based solution in Python. A standalone executable can be downloaded and run to try out the game [(link)](https://github.com/JamilHaidar/SimonTathamCube/raw/main/cube.exe).

The way I solved this game is based on doing linear algebra on matrices where singular elements are from the Galois field GF(2). This means that we can only have the elements 0 and 1, with all operations defined on these elements. For example, addition is a XOR operation and multiplication is an AND operation.

The linear algebra approach uses a very neat trick to solve the game, but this approach requires a functioning Gaussian Elimination algorithm that works with GF(2) matrices.

I decided to be very strict on memory and computational optimality in the representation of the game grid. Instead of having a 2D array with 1s or 0s (or booleans), I decided to represent each row as an unsigned int n, where n is the dimension of the grid.
This gives rise to multiple challenges including: bit selection, slicing bits across columns, performing linear algebra, etc. Therefore, I implemented my own functions to perform all operations I'd need such as matrix slicing (row and column), transpose, inner product, outer product, argmax, etc.

However, this is not necessary. I did implement a completely viable and working script that utilizes ``numpy`` as seen in the ``solve_numpy.py`` script, where I use built in numpy functions to handle all heavy handling, but doing everything from scratch and forcing myself to work with bit manipulations was a good challenge.

Controls:
- Press with mouse cursor to flip a grid cell and its orthogonal neighbors.
- N to start new game
- S to solve puzzle
- Press on any number (1-9) to change the grid size. Default grid size is ``n=5`` (5x5).

The game being explored can be found [here](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/flip.html).
I have been able to find strategies and algorithms for all puzzles in this game (even NP hard ones, I just iterate through possible states in a greedy/pruning way). 
I decided to start implementing solutions for these games. This is the second game I have implemented.

## Objective and Approach
The objective of Cube is simple:
Try to light up all the squares in the grid by flipping combinations of them. Click in a square to flip it and its orthogonal neighbours.

### Game Implementation
I recreate the game in Python using PyGame. I created a simple grid, coloring ON lights as white and OFF lights as dark gray. When solve mode is on, the cells needed to be pressed get a red outline around their border.
Once a new game is started, I iterate over each cell and perform a move on it with a certain probability p (default = 0.6), randomizing the grid and ensuring that it's solvable.

### Game solution

The first observation to be made is that if a set of moves is performed on the grid, doing this set of moves again, where order is not necessary, will undo all changes made. The game's design allows for the application of the principle of superposition, where assuming a move set A and another move set B, the order of applying these subsets does not affect the final position.

We first create transition matrices for each possible move. For an $n \cdot n$ grid, there are $n^2$ possible moves. For each move, we can create a column of 1s and 0s where 1 means the cell's position (unraveled to an $n^2\times1$ vector) is affected, and 0 means it is not.

Then, we stack the columns horizontally, creating a full transition matrix. Therefore, multiplying a move vector, which would be an $n^2\times1$ vector where a 1 represents a move being performed on the cell's position and 0 means no move, with the transition matrix, leads to the board's state.

Finally, assume we have a set of moves. Using the transition matrix, we can find the board's state. It is easy to see that given a random board, all we need to do is find a set of moves that when transformed through the transition matrix, would allow us to reach the current board's state, effectively canceling it out and clearing the board.
[This](https://people.sc.fsu.edu/~jburkardt/classes/imps_2017/11_28/2690705.pdf) is a very nice resource I have found that describes my approach almost exactly. The way I solved it is a little different, but my approach and the paper are similar in essense. 

## Algorithm

Let A be the transition matrix that transforms possible moves to the board's states, m be the vector of moves, and b be the board's current state.
We know that $Am = b$. Therefore, the solution is given by $m = A^{-1}b$. The way I approached this is by creating a matrix $M = [A|b]$ and performing Gaussian Elimination on this matrix. The final column once Gaussian Elimination is finished represents the solution $m$.

### Implementation
An example solution may look like this one:

<img src="https://raw.githubusercontent.com/michal-stachurski/rolling-cube/main/example/solution.gif" width="250" height="250">

My approach for the optimal solution looks like:

<img src="https://user-images.githubusercontent.com/60647115/210168448-c440d7ea-a00f-4313-b7dd-317cb10fdd0f.gif" width="300" height="300">
