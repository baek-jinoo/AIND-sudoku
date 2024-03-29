assignments = []

rows = 'ABCDEFGHI'
cols = '123456789'

def cross(A, B):
    """Cross product of elements in A and elements in B.
    Args:
        A(string): Elements to cross with B
        B(string): Elements to cross with A

    Returns:
        Array of the cross between the two input elements
    """
    return [s+t for s in A for t in B]

boxes = cross(rows, cols)

row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
diag_units = [[rows[i]+cols[i] for i in range(9)], [rows[i]+cols[8 - i] for i in range(9)]]
unitlist = row_units + column_units + square_units + diag_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}
        box(string): a key for the new value in the form {RowColumn}
        value(string): a new value with digits

    Returns:
        the values dictionary with the updated value with the box key
    """

    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
    for key, value in values.items():
        if len(value) != 2:
            continue

        for unit in units[key]:
            foundTwin = False
            for box in unit:
                if box == key:
                    continue
                if value != values[box]:
                    continue
                #twin is found
                foundTwin = box
                break
            if foundTwin is False:
                continue

            #eliminate values of twins in other boxes in the unit
            for box in unit:
                if box == key or box == foundTwin:
                    continue
                current_box_value = values[box]
                if value[0] in current_box_value:
                    assign_value(values, box, current_box_value.replace(value[0], ""))
                if value[1] in current_box_value:
                    assign_value(values, box, current_box_value.replace(value[1], ""))

    return values

def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    values = {}
    for index, box in enumerate(boxes):
        value = grid[index]
        if value == ".":
            value = "123456789"
        values[box] = value
    return values

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return

def eliminate(values):
    """Eliminate values using the eliminate strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the eliminate strategy eliminated from peers.
    """
    keys = set(values.keys())
    while len(keys) > 0:
        key = keys.pop()
        value = values[key]
        
        if len(value) > 1:
            continue
        
        for peer_unit in peers[key]:
            update_value = values[peer_unit].replace(value, "")
            assign_value(values, peer_unit, update_value)
            
    return values

def only_choice(values):
    """Eliminate values using the only_choice strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the only_choice eliminated from peers.
    """
    for unit in unitlist:
        # Create the dictionary of digits as key to values as boxes
        digitToLocations = {}
        for key in unit:
            for digit in values[key]:
                if digit in digitToLocations:
                    digitToLocations[digit].append(key)
                else:
                    digitToLocations[digit] = [key]
        # If the there is only one box for a digit,
        # we set that digit as the sole value for that box
        for digit in digitToLocations:
            locations = digitToLocations[digit]
            if len(locations) == 1:
                assign_value(values, locations[0], digit)
    return values

def reduce_puzzle(values):
    """ Constraint propagation algorithm that utilizes the three strategies to
    solve the Sudoku problem. The three strategies include elimination, only
    choice, and naked twins.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary or False
        False if there are validation error
        Otherwise, the dictionary with the three strategies iterated until no
        further progress is made through the three strategies.
    """
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

        values = eliminate(values)
        values = only_choice(values)
        values = naked_twins(values)

        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def search(values):
    """ Recursive function that alternates search and constraint propagtion
    through elimination strategies
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary or False
        False if there are is no solution
        Otherwise, the dictionary with the solution through search and
        constraint propagation applied iteratively
    """
    values = reduce_puzzle(values)
    if values == False:
        return False
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    if len(solved_values) == 81:
        return values
    # Choose one of the unfilled squares with the fewest possibilities
    least_num_possibilities = 10
    least_key = ""
    for key in values:
        if len(values[key]) == 1:
            continue
        if least_num_possibilities > len(values[key]):
            least_num_possibilities = len(values[key])
            least_key = key
    for digit in values[least_key]:
        new_potential = values.copy()
        assign_value(new_potential, least_key, digit)
        new_values = search(new_potential)
        if new_values != False:
            return new_values
    return False

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    values = grid_values(grid)
    return search(values)

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        pass
