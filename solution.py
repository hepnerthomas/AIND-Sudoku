assignments = []   

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
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
    # Find all instances of naked twins
    visited_twins = set()
    naked_twins = []
    for box in boxes:
        if len(values[box]) == 2:
            for peer in peers[box]:
                if(values[peer] == values[box] and (peer not in visited_twins or box not in visited_twins)):
                    naked_twins.append((box, peer))
                    visited_twins.add(peer)
                    visited_twins.add(box)
        else:
            pass
        
    # Eliminate the naked twins as possibilities for their peers
    visited = set()
    for twin in naked_twins:
        box1 = twin[0]
        box2 = twin[1]
        visited.add(box1)
        visited.add(box2)
        for unit in unitlist:
            if(box1 in unit and box2 in unit):
                for box in unit:
                    if(box not in visited):
                        visited.add(box)
                        for digit in values[box1]:
                            value = values[box].replace(digit, "")
                            values = assign_value(values, box, value) 
    return values

def cross(a, b):
    "Cross product of elements in A and elements in B."
    return [s+t for s in a for t in b]

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
    values = []
    all_digits = '123456789'
    for c in grid:
        if c == '.':
            values.append(all_digits)
        elif c in all_digits:
            values.append(c)
    assert len(values) == 81
    return dict(zip(boxes, values))

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
    """Eliminate values from peers of each box with a single value.

    Go through all the boxes, and whenever there is a box with a single value,
    eliminate this value from the set of values of all its peers.

    Args:
        values: Sudoku in dictionary form.
    Returns:
        Resulting Sudoku in dictionary form after eliminating values.
    """
    solved_values = values.keys()
    for box in solved_values: 
        if len(values[box]) == 1:
            digit = values[box]
            for peer in peers[box]:
                value = values[peer].replace(digit, "")
                values = assign_value(values, peer, value)
        else:
            pass
    return values   

def only_choice(values):
    """Finalize all values that are the only choice for a unit.

    Go through all the units, and whenever there is a unit with a value
    that only fits in one box, assign the value to this box.

    Input: Sudoku in dictionary form.
    Output: Resulting Sudoku in dictionary form after filling in only choices.
    """
    new_values = values.copy()
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                new_values = assign_value(new_values, dplaces[0], digit)
    return new_values

def reduce_puzzle(values):
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

        # Your code here: Use the Eliminate Strategy
        values = eliminate(values)
        
        # Your code here: Use the Only Choice Strategy
        values = only_choice(values)
        
        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
        
    return values

def search(values):
    "Using depth-first search and propagation, create a search tree and solve the sudoku."
    
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)
    if values is False:
        return False ## Failed earlier
    if all(len(values[s]) == 1 for s in boxes): 
        return values ## Solved!
    
    # Choose one of the unfilled squares with the fewest possibilities
    n,s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    
    # Now use recurrence to solve each one of the resulting sudokus, and 
    for value in values[s]:
        new_sudoku = values.copy()
        #new_sudoku[s] = value
        new_sudoku = assign_value(new_sudoku, s, value)
        attempt = search(new_sudoku)
        if attempt:
            return attempt 

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """

    print("\n1. Set up the Board")
    
    print("\n2. Encode the Board")
    values = grid_values(grid)
    display(values)

    print("\n3. Find and return the Solution.")
    new_values = search(values)
    display(new_values)
    print("\n")

    return new_values

""" Set up the variables for the Sudoku board. 
"""
rows = 'ABCDEFGHI'
cols = '123456789' 
boxes = cross(rows, cols)
row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
reverse_cols = cols[::-1]
diag_units1 = [rows[i] + cols[i] for i in range(len(rows))]
diag_units2 = [rows[i] + reverse_cols[i] for i in range(len(rows))]
diag_units = [diag_units1, diag_units2]
unitlist = row_units + column_units + square_units + diag_units 
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)


if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
