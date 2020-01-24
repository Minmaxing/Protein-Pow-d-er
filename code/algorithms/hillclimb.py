from .generalfunctions import stability_calculator, make_move
import copy
import random

def pullmove(chain, stability, iterations):
    """Hill climb algorithm based on diagonal pull moves"""

    # save current best chains and stabilities
    best_chain = chain
    best_stability = stability

    i = 0

    max_reached = False
    while i < iterations:
        if max_reached == True:
            break

        # new_chain = copy.deepcopy(best_chain)
        # new_chain_stability = copy.deepcopy(best_stability)
        moves_tried = 0
        for element in range(1, len(best_chain) - 1):
            new_chain = copy.deepcopy(best_chain)
            new_chain_stability = copy.deepcopy(best_stability)

            moves_list = makepull(new_chain, new_chain[element], new_chain[element+1])
            if len(moves_list) == 0:
                moves_tried += 1
                if moves_tried == len(chain):
                    max_reached = True
                continue

            # Counts iteration only if a move has actually been made
            i += 1
            moves_tried = 0

            for other_element in range(element - 1):

                other_amino = new_chain[other_element]
                amino_ahead = new_chain[other_element + 2]

                x, y, z = amino_ahead.get_location()

                other_amino.set_coordinates(x, y, z)

            best_move = 0
            best_stability_move = 0
            for move in moves_list:
                new_move = copy.deepcopy(new_chain)
                new_move_stability = copy.deepcopy(new_chain_stability)
                amino = new_move[element]
                previous_amino = new_move[element - 1]

                diagonal = move[0]
                adjacent = move[1]

                # set current element and the previous one to the move made
                amino.set_coordinates(diagonal[0], diagonal[1], diagonal[2])
                previous_amino.set_coordinates(adjacent[0], adjacent[1], adjacent[2])

                new_move_stability = stability_calculator(new_move)

                if new_move_stability <= best_stability_move:
                    best_stability_move = new_move_stability
                    best_move = new_move

            if best_stability_move <= best_stability:
                best_stability = best_stability_move
                best_chain = best_move

    #print(best_chain)
    return best_chain, best_stability

def makepull(chain, element, next_element):

    x, y, z = element.get_location()
    x_next, y_next, z_next = next_element.get_location()

    possible_diagonals = []
    taken_coords = []
    selected_diagonals = []

    # All possible coordinates for a diagonal move from the current element
    diagonal_coords = [(x + 1, y, z + 1), (x + 1, y, z - 1), (x + 1, y - 1, z), (x + 1, y + 1, z), (x, y - 1, z - 1), (x, y - 1, z + 1), (x - 1, y - 1, z), (x - 1, y, z + 1), (x - 1, y, z - 1), (x - 1, y + 1, z), (x, y + 1, z + 1), (x, y + 1, z - 1)]

    # All possible coordinates that are adjacent to the next protein element
    next_element_adj_coords = [(x_next + 1, y_next, z_next), (x_next - 1, y_next, z_next), (x_next, y_next + 1, z_next), (x_next, y_next - 1, z_next), (x_next, y_next, z_next + 1), (x_next, y_next, z_next - 1)]

    for element in chain:
        taken_coords.append(element.get_location())

    for coords in ((x + 1, y, z + 1), (x + 1, y, z - 1), (x + 1, y - 1, z), (x + 1, y + 1, z), (x, y - 1, z - 1), (x, y - 1, z + 1), (x - 1, y - 1, z), (x - 1, y, z + 1), (x - 1, y, z - 1), (x - 1, y + 1, z), (x, y + 1, z + 1), (x, y + 1, z - 1)):

        if coords not in taken_coords:

            if coords == (x + 1, y, z + 1):
                if (x, y, z + 1) not in taken_coords:
                    possible_diagonals.append((coords, (x, y, z + 1)))
                if (x + 1, y, z) not in taken_coords:
                    possible_diagonals.append((coords, (x + 1, y, z)))


            elif coords == (x + 1, y, z - 1):
                if (x, y, z - 1) not in taken_coords:
                    possible_diagonals.append((coords, (x, y, z - 1)))
                if (x + 1, y, z) not in taken_coords:
                    possible_diagonals.append((coords, (x + 1, y, z)))

            elif coords == (x + 1, y - 1, z):
                if (x + 1, y, z) not in taken_coords:
                    possible_diagonals.append((coords, (x + 1, y, z)))
                if (x, y - 1, z) not in taken_coords:
                    possible_diagonals.append((coords, (x, y - 1, z)))

            elif coords == (x + 1, y + 1, z):
                if (x + 1, y, z) not in taken_coords:
                    possible_diagonals.append((coords, (x + 1, y, z)))
                if (x, y + 1, z) not in taken_coords:
                    possible_diagonals.append((coords, (x, y + 1, z)))

            elif coords == (x, y - 1, z - 1):
                if (x, y - 1, z) not in taken_coords:
                    possible_diagonals.append((coords, (x, y - 1, z)))
                if (x, y, z - 1) not in taken_coords:
                    possible_diagonals.append((coords, (x, y, z - 1)))

            elif coords == (x, y - 1, z + 1):
                if (x, y - 1, z) not in taken_coords:
                    possible_diagonals.append((coords, (x, y - 1, z)))
                if (x, y, z + 1) not in taken_coords:
                    possible_diagonals.append((coords, (x, y, z + 1)))

            elif coords == (x - 1, y - 1, z):
                if (x - 1, y, z) not in taken_coords:
                    possible_diagonals.append((coords, (x - 1, y, z)))
                if (x, y - 1, z) not in taken_coords:
                    possible_diagonals.append((coords, (x, y - 1, z)))

            elif coords == (x - 1, y, z + 1):
                if (x - 1, y, z) not in taken_coords:
                    possible_diagonals.append((coords, (x - 1, y, z)))
                if (x, y, z + 1) not in taken_coords:
                    possible_diagonals.append((coords, (x, y, z + 1)))

            elif coords == (x - 1, y, z - 1):
                if (x - 1, y, z) not in taken_coords:
                    possible_diagonals.append((coords, (x - 1, y, z)))
                if (x, y, z - 1) not in taken_coords:
                    possible_diagonals.append((coords, (x, y, z - 1)))

            elif coords == (x - 1, y + 1, z):
                if (x - 1, y, z) not in taken_coords:
                    possible_diagonals.append((coords, (x - 1, y, z)))
                if (x, y + 1, z) not in taken_coords:
                    possible_diagonals.append((coords, (x, y + 1, z)))

            elif coords == (x, y + 1, z + 1):
                if (x, y + 1, z) not in taken_coords:
                    possible_diagonals.append((coords, (x, y + 1, z)))
                if (x, y, z + 1) not in taken_coords:
                    possible_diagonals.append((coords, (x, y, z + 1)))

            elif coords == (x, y + 1, z - 1):
                if (x, y + 1, z) not in taken_coords:
                    possible_diagonals.append((coords, (x, y + 1, z)))
                if (x, y, z - 1) not in taken_coords:
                    possible_diagonals.append((coords, (x, y, z - 1)))

    for coords in possible_diagonals:
        if coords[0] in next_element_adj_coords:
            selected_diagonals.append(coords)

    return selected_diagonals
