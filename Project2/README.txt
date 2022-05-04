1. Justin Davis, 10854905

2. Python 3.8.10 was used

3. Windows Version 10.0.19044 Build 19044

4. All code in contained inside of the maxconnect4.py file. The code is implemented in a functional style with no
classes used. There is no one entry function to the program either, it must be called as a file
The code for minimax is located within the minimax function in the code. This implements alpha-beta pruning and
depth limited search. The successor node prioritization was implmented by generating successor positions in
an in order manner. Thus, minimax traverse the game tree in an inorder manner which by definition gives us
successor node prioritization. A note in made on the getChildPositions function which is ultized in minimax directly
which also specifies this information.

5. Run the code using "python maxconnect4.py {game mode} {input file} {next player / output file} {depth}"
If on a system with both python 2 and 3 the python might have to be replaced with python3.
The code performs some checks on inputs, such as ensuring the game mode exists, input files exist, next player is
set correctly, and that the depth converted to an integer is greater than 0.
