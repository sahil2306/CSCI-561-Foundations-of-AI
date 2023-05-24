# CSCI-561-Foundations-of-AI

## Assignment 1
You will write a program that will take an input file that describes the land, the starting point, potential lodges we can relax in, and some other characteristics for our skier. For each lodge location, you should find the optimal (shortest) safe path from the starting point to that target
lodge. A path is composed of a sequence of elementary moves. Each elementary move consists of moving the skier from their current position to one of its 8 neighbors. To find the solution you will use the following algorithms:

- Breadth-first search (BFS)
- Uniform-cost search (UCS)
- A* search (A*)

Your algorithm should return an optimal path, that is, with shortest possible journey cost. Journey cost is further described below and is not equal to geometric path length.  If an optimal path cannot be found, your algorithm should return “FAIL” as further described below.

Input: The file input.txt in the current directory of your program will be formatted as follows:
First line: Instruction of which algorithm to use, as a string: BFS, UCS or A*
Second line: Two strictly positive 32-bit integers separated by one space character, for
“W H” the number of columns (width) and rows (height), in cells, of the map.
Third line: Two positive 32-bit integers separated by one space character, for
“X Y” the coordinates (in cells) of the starting position for our skier. 0 £ X £ W-1
and 0 £ Y £ H-1 (that is, we use 0-based indexing into the map; X increases when
moving East and Y increases when moving South; (0,0) is the North West corner
of the map). Starting point remains the same for each of the N lodge sites below
and will never contain a tree.
Fourth line: Positive 32-bit integer number for the stamina S of the skier which determines
how advanced our skier is. S will be used to compute allowed moves if we’re
moving into a non-tree cell.
Fifth line: Strictly positive 32-bit integer N, the number of lodges on the mountain.
Next N lines: Two positive 32-bit integers separated by one space character, for
“X Y” the coordinates (in cells) of each lodge site. 0 £ X £ W-1 and 0 £ Y £ H-1 (that
is, we again use 0-based indexing into the map). These N target lodge sites are
not related to each other, so you will run your search algorithm on each lodge
site and write the result to the output as specified below. We will never give you
a lodge site that is the same as the starting point. They will never contain a tree.
Next H lines: W 32-bit integer numbers separated by any numbers of spaces for the M values
of each of the W cells in each row of the map. Each number can represent the
following cases:
⚫ E >= 0, snowy mountain slope with elevation E
⚫ E < 0, tree of height |E| that might be covered with snow depending on the elevation we approach it from

For example:
A*
8 6
4 4
5
2
2 1
6 3
-10 40 34 21 42 37 18 7
-20 10 5 27 -6 5 2 0
-30 8 17 -3 -4 -1 0 4
-25 -4 12 14 -1 9 6 9
-15 -9 46 6 25 11 31 -21
-5 -6 -3 -7 0 25 53 -42


## Assignment 2
In this project, we will implement agent that plays the game of Pente, the two-player version of the abstract strategy board game.
It is played on a 19x19 board, where pieces are placed on the intersection of the lines (like the game Go). White always opens the game (like in Chess). The players take turns putting pieces on the board until: 
1) A player connects 5 of their pieces in a horizontal, vertical or a diagonal line, OR
2) A player makes 5 total captures (equals to 10 pieces of their opponent’s since pieces can only be captured in pairs)

Capture: 
The custodial capture mechanic, where a player flanks the opponent’s pieces with their own to capture them, only applies to pairs of the opponent’s pieces. Therefore, if the current board formation is XOO_ and player X plays their piece as XOOX, the O pieces are captured and the board becomes X_ _X. Note again that this only works for pairs of pieces, therefore X cannot capture their opponent’s pieces from a board like XOOO_ or XO_.

** Input and output file formats: **
Input: The file input.txt in the current directory of your program will be formatted as follows:

First line: A string BLACK or WHITE indicating which color you play. White will always start the game.
Second line: A strictly positive floating point number indicating the amount of play time remaining for your agent (in seconds).
Third line: Two non-negative 32-bit integers separated by a comma indicating the number of pieces captured by White and Black players consecutively. Caution, it will always be ordered as first captured by White, then by Black, irrespective of what color is given in the first line.

Next 19 lines: Description of the game board, with 19 lines of 19 symbols each:
⚫ w for a cell occupied by a white piece
⚫ b for a cell occupied by a black piece
⚫ . (a dot) for an empty intersection

### Input and Output

Input: The file input.txt in the current directory of your program will be formatted as follows:
First line: A string BLACK or WHITE indicating which color you play. White will always start
the game.
Second line: A strictly positive floating point number indicating the amount of play time
remaining for your agent (in seconds).
Third line: Two non-negative 32-bit integers separated by a comma indicating the number of
pieces captured by White and Black players consecutively. Caution, it will always
be ordered as first captured by White, then by Black, irrespective of what color is
given in the first line.
Next 19 lines: Description of the game board, with 19 lines of 19 symbols each:
⚫ w for a cell occupied by a white piece
⚫ b for a cell occupied by a black piece
⚫ . (a dot) for an empty intersection
For example:
BLACK
100.0
0,0
...................
...................
...................
...................
...................
...................
...................
.........w.........
..........b........
.........w.bw......
...................
...................
...................
...................
...................
...................
...................
...................
...................
In this input.txt example, your agent should play a move as the Black agent and has 100.0 seconds. The board configuration is 5 turns into the game. There’s a capture condition for White, so your agent could likely choose to block that by putting their piece in the red highlighted position on the board.

Output: The format we will use for describing the square positions is borrowed from the notations from Pente.org, where every column is described by a letter and every row is described by a number. The position for a given square is given as the concatenation of these. Here’s a useful visualization on how we identify each intersection for the 19x19 

Pente board:
Using the above image as reference, in the input.txt sample given above, White has pieces on 10K, 10N and 12K, while Black has pieces on 11L and 10M. Using this type of notation for the cells on our gameboard, the file output.txt which your program creates in the current directory should be formatted as follows:
1 line: PIECE_POS which describes your move with an integer (1-19) and an uppercase letter (A-T) concatenated.
For example, for the red highlighted move in the input sample, output.txt may contain:
9N The resulting board would look like this, given the above input.txt (the master game playing engine will compute this and it is not part of output.txt):
...................
...................
...................
...................
...................
...................
...................
.........w.........
..........b........
.........w.bw......
............b......
...................
...................
...................
...................
...................
...................
...................
...................


## Assignment 3
Implement it using first-order logic resolution. Current restaurant status, policies, ingredient stock and customer status will all be encoded as first order logic sentences in the knowledge base. The knowledge given to you contains sentences with the following defined operators:
NOT X ~X
X OR Y X | Y
X AND Y X & Y
X IMPLIES Y X => Y

The program takes a query and provides a logical conclusion to whether it is true or not.
Format for input.txt:
<QUERY>
<K = NUMBER OF GIVEN SENTENCES IN THE KNOWLEDGE BASE>
<SENTENCE 1>
...
<SENTENCE K>

The first line contains a query as one logic sentence (further detailed below). The line after contains an integer K specifying the number of sentences given for the knowledge base. The remaining K lines contain the sentences for the knowledge base, one sentence per line.

Query format: The query will be a single literal of the form Predicate(Constant_Arguments) or ~Predicate(Constant_Arguments) and will not contain any variables. Each predicate will have between 1 and 25 constant arguments. Two or more arguments will be separated by commas. KB input format: Each sentence to be inserted into the knowledge base is written in FOL using operators &, |, =>, and ~, with the following conventions:
1. & denotes the conjunction operator.
2. | denotes the disjunction operator.
3. => denotes the implication operator.
4. ~ denotes the negation operator.
5. No other operators besides &, |, =>, and ~ are used in the input to the knowledge base.
6. There will be NO parentheses in the input to the KB except to mark predicate arguments. For example: Pred(x,y) is allowed, but A & (B | C) is not.
7. Variables are denoted by a single lowercase letter.
8. All predicates (such as Order(x,y) which means person x orders food item y) and constants (such as Broccoli) are case sensitive alphanumeric strings that begin with an uppercase letter.
9. Thus, when parsing words in the input to the KB, use the following conventions:
9.1. Single lowercase letter: variable. E.g.: x, y, z
9.2. First letter is uppercase and opening parenthesis follows the
current word: predicate. E.g.: Order(x,y), Pred52(z)
9.3. Otherwise: constant. E.g.: Harry, Pizza123
10. Each predicate takes at least one argument (so, all predicate names are always followed by an opening parenthesis). Predicates will take at most 25 arguments. A given predicate name will not appear with different number of arguments.
11. Predicate arguments will only be variables or constants (no nested predicates).
12. There will be at most 100 sentences in the knowledge base.
13. See the sample input below for spacing patterns.
14. You can assume that the input format is exactly as it is described.
15. There will be no syntax errors in the given input.
16. The KB will be true (i.e., will not contain contradictions).
17. Note that the format we just specified is broader than both Horn form and CNF. Thus, you should first convert the given input sentences into CNF and then insert the converted sentences into your CNF KB for resolution. Format for output.txt:
Your program should determine whether the query can be inferred from the knowledge base or not, and write a single line to output.txt:
<ANSWER>
Each answer should be either TRUE if you can prove that the corresponding query sentence is true given the knowledge base, or FALSE if you cannot. This is a so-called “closed-world assumption” (things that cannot be proven from the KB are considered false).

Notes and hints:
- Please name your program “homework.xxx” where ‘xxx’ is the extension for the programming language you choose. (“py” for python3, “cpp” for C++11, and “java” for Java).
- If you decide that the given statement can be inferred from the knowledge base, every variable in each sentence used in the proving process should be unified with a Constan (i.e., unify variables to constants before you trigger a step of resolution).
- All variables are assumed to be universally quantified. There is no existential quantifier in this homework. There is no need for Skolem functions or Skolem constants.
- Operator priorities apply (e.g., negation has higher priority than conjunction).
- The knowledge base is consistent.
- If you run into a loop and there is no alternative path you can try, report FALSE. For example, if you have two rules (1) ~A(x) | B(x) and (2) ~B(x) | A(x) and wanting to prove A(Teddy). In this case your program should report FALSE.
- Note that the input to the KB is not in Horn form. So you indeed must use resolution and cannot use generalized Modus Ponens.

Example 1:
For this input.txt:
Order(Jenny,Pizza)
7
Order(x,y) => Seated(x) & Stocked(y)
Ate(x) => GetCheck(x)
GetCheck(x) & Paid(x) => Leave(x)
Seated(x) => Open(Restaurant) & Open(Kitchen)
Stocked(Hamburger)
Open(Restaurant)
Open(Kitchen)

output.txt:
FALSE