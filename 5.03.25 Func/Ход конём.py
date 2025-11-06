def list_of_turns(cell):
    
    knight_moves = [
        (2, 1), (2, -1), (-2, 1), (-2, -1),
        (1, 2), (1, -2), (-1, 2), (-1, -2)
    ]

    def chess_to_coords(chess_pos):
        col = ord(chess_pos[0]) - ord('A') + 1
        row = int(chess_pos[1])
        return (col, row)
    
    def coords_to_chess(coords):
        col = chr(coords[0] - 1 + ord('A'))
        row = str(coords[1])
        return col + row
    
    def is_valid(pos):
        return 1 <= pos[0] <= 8 and 1 <= pos[1] <= 8
    
    
    current_pos = chess_to_coords(cell)
    
    possible_moves = []
    for move in knight_moves:
        new_col = current_pos[0] + move[0]
        new_row = current_pos[1] + move[1]
        new_pos = (new_col, new_row)
        
        if is_valid(new_pos):
            possible_moves.append(coords_to_chess(new_pos))
    
    possible_moves.sort()
    
    return possible_moves

print(list_of_turns("B1"))