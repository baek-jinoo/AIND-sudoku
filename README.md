# Artificial Intelligence Nanodegree

## Jin Notes

### Run

Within a python3 environment, run `python solution.py`

### Project Conclusion

This introductory project by Udacity provided a step by step guide to solving Sudoku via constraint satisfaction and search.

This project uses domain specific methods to apply the constraint satisfaction strategy. It was a good introduction into how problems with rules can be solved using constraint satisfaction and search.

Lastly, it was great to see how we could try different values to solve problems that doesn't have a single option available. However, also good to learn about the algorithmic complexity implications of search.



## Introductory Project: Diagonal Sudoku Solver

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?  
A: We apply the constraint that when a unit has two boxes that shares two of the same possible digits, it can not have those two digits in any of the other boxes in the same unit. Thus, we iterate through all the other boxes to delete those digits. We can apply this method iteratively between other constraint propagation methods such as elimination and only_choice.

# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?  
A: We can solve the diagonal sudoku problem by adding two more units (the diagonal units) into unit_list. These two units will be incorporated into our elimination, only_choice, and naked_twins techniques.

### Install

This project requires **Python 3**.

We recommend students install [Anaconda](https://www.continuum.io/downloads), a pre-packaged Python distribution that contains all of the necessary libraries and software for this project. 
Please try using the environment we provided in the Anaconda lesson of the Nanodegree.

##### Optional: Pygame

Optionally, you can also install pygame if you want to see your visualization. If you've followed our instructions for setting up our conda environment, you should be all set.

If not, please see how to download pygame [here](http://www.pygame.org/download.shtml).

### Code

* `solution.py` - You'll fill this in as part of your solution.
* `solution_test.py` - Do not modify this. You can test your solution by running `python solution_test.py`.
* `PySudoku.py` - Do not modify this. This is code for visualizing your solution.
* `visualize.py` - Do not modify this. This is code for visualizing your solution.

### Visualizing

To visualize your solution, please only assign values to the values_dict using the ```assign_values``` function provided in solution.py

### Submission
Before submitting your solution to a reviewer, you are required to submit your project to Udacity's Project Assistant, which will provide some initial feedback.  

The setup is simple.  If you have not installed the client tool already, then you may do so with the command `pip install udacity-pa`.  

To submit your code to the project assistant, run `udacity submit` from within the top-level directory of this project.  You will be prompted for a username and password.  If you login using google or facebook, visit [this link](https://project-assistant.udacity.com/auth_tokens/jwt_login for alternate login instructions.

This process will create a zipfile in your top-level directory named sudoku-<id>.zip.  This is the file that you should submit to the Udacity reviews system.

