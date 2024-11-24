from pyswip import Prolog

def infer_pits_from_breezes(prolog):
    # Query all squares with breezes
    breeze_locations = list(prolog.query("breeze(X, Y)"))
    
    # Iterate over all breeze locations
    for breeze in breeze_locations:
        x = breeze['X']
        y = breeze['Y']
        
        # Check adjacent squares
        for dx, dy in directions:
            adj_x, adj_y = x + dx, y + dy
            
            # Ensure it's within bounds
            if 0 <= adj_x < 5 and 0 <= adj_y < 5:
                # If the adjacent square is not safe, assume it's a pit
                if not list(prolog.query(f"safe({adj_x}, {adj_y})")):
                    # Assert the pit in the knowledge base
                    prolog.assertz(f"pit({adj_x}, {adj_y})")

# Example grid size and directions
directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right

# Initialize Prolog
prolog = Prolog()

# Example of adding breezes and safe locations
prolog.assertz("breeze(2, 1)")
prolog.assertz("breeze(1, 2)")
prolog.assertz("safe(3, 3)")
prolog.assertz("safe(0, 0)")

# Infer pits from the knowledge base
infer_pits_from_breezes(prolog)

# Query and print inferred pits
inferred_pits = list(prolog.query("pit(X, Y)"))
print("Inferred Pits:", inferred_pits)
