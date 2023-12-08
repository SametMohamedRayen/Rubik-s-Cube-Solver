# States space
from enum import Enum
import copy

Color = Enum('Color', ['vert', 'blanc', 'rouge', 'jaune', 'orange', 'blue'])
indices = [1, 2, 3, 4]
n = 2


# Now we can define util functions to work on retriving indices of certain columns and rows in a certain order
# from our model in order to extract the face and contour facelettes that are concerned with rotations afterwards

# Transpose a matrix
def transpose(a):
    a_t = [[0] * len(a) for _ in range(len(a[0]))]
    for i in range(0, len(a[0])):
        for j in range(0, len(a)):
            a_t[i][j] = a[j][i]
    return a_t


# order = order of retrival of elements of an array
def read_array(order, a):
    if (order == 1):
        return a[::-1]
    return a


# direction = column or row write
# index = the index in which to write
def write_array(direction, index, a, face):
    if (direction == 1):
        for i in range(0, len(face)):
            face[index][i] = a[i]
    else:
        for i in range(0, len(face[0])):
            face[i][index] = a[i]


# axis = index of row/column to retrive from the face
# direction = 0 for row, 1 for column
# order = order of retrival following the clockwise form, 0 for positive (normal), 1 for negative (inverse)
# face = index of the concerned face from [[0,5]] for the 6 faces of the cube
def retrive(axis, direction, order, face):
    if direction == 1:
        face_t = transpose(face)
        return read_array(order, face_t[axis])
    return read_array(order, face[axis])


# Now we can define a list that associates every face with its contour.
# Indexes are directly associated to faces => element[0] -> contains face 0 data.
# First list in each element contains indexes of contour faces following the clockwise form.
# Second list contains tuples that contain (axis, direction, order) to be considered for each contour face.
contour_data_init = [[[1, 2, 3, 4], [(n - 1, 0, 0), (0, 1, 0), (0, 0, 1), (n - 1, 1, 1)]],
                     [[5, 2, 0, 4], [(0, 0, 1), (0, 0, 1), (0, 0, 1), (0, 0, 1)]],
                     [[1, 5, 3, 0], [(n - 1, 1, 1), (0, 1, 0), (n - 1, 1, 1), (n - 1, 1, 1)]],
                     [[0, 2, 5, 4], [(n - 1, 0, 0), (n - 1, 0, 0), (n - 1, 0, 0), (n - 1, 0, 0)]],
                     [[1, 0, 3, 5], [(0, 1, 0), (0, 1, 0), (0, 1, 0), (n - 1, 1, 1)]],
                     [[1, 4, 3, 2], [(0, 0, 1), (0, 1, 0), (n - 1, 0, 0), (n - 1, 1, 1)]]]


# Now we can define the rotation function that takes in the face index, the angle and the state and returns the new
# state, but first we will define a function that take in the face and the angle and returns the center and contour
# indexes.
def get_face_contour(face, angle, state):
    contour_data = copy.deepcopy(contour_data_init)
    face_indices = state[face]
    contour_indices = [[0] * n for _ in range(4)]
    for i in range(0, 4):
        contour_face = contour_data[face][0][i]
        (axis, direction, order) = contour_data[face][1][i]
        contour_indices[i] = retrive(axis, direction, order, state[contour_face])
    if angle == 1:
        # Inverse order of contour indices
        contour_indices_rev = [[0] * n for _ in range(4)]
        contour_indices_rev[0] = read_array(1, contour_indices[0])
        for i in range(1, 4):
            for j in range(0, n):
                contour_indices_rev[i][j] = contour_indices[-i][-j - 1]
        return face_indices, contour_indices_rev
    return face_indices, contour_indices


# The main rotation function taking the face and angle and state and returning a new state
def rotation(face, angle, state):
    contour_data = copy.deepcopy(contour_data_init)
    (face_indices, contour_indices) = get_face_contour(face, angle, state)
    # Now we modify the state and we return the new state
    new_state = copy.deepcopy(state)
    # Rotate the center face
    face_t = transpose(new_state[face])
    if angle == 0:
        for i in range(0, len(face_t)):
            new_state[face][i] = read_array(1, face_t[i])
    else:
        new_state[face] = read_array(1, face_t)
    # Apply contour rotation
    last_el = contour_indices[3]
    if angle == 0:
        for i in range(3, 0, -1):
            contour_indices[i] = contour_indices[i - 1]
        contour_indices[0] = last_el
    else:
        contour_indices = contour_indices[::-1]
    # print(contour_indices)
    for i in range(0, 4):
        contour_face = contour_data[face][0][i]
        (axis, direction, order) = contour_data[face][1][i]
        write_array(abs(direction - 1), axis, contour_indices[i], new_state[contour_face])
    # print(new_state)
    return new_state


def rotation_central_piece_n(face, axis, angle, state):
    contour_data = copy.deepcopy(contour_data_init)
    # Same logic as the normal rotation but without rotating the face and with a small
    # tweak in the contour data indices
    for j in range(0, 4):
        (old_axis, direction, order) = contour_data[face][1][j]
        # If we are rotating the last column or row we will not rotate the last-axis column or row
        if old_axis == n - 1:
            contour_data[face][1][j] = (n - axis - 1, direction, order)
        # Else if we are rotating the first column or row we will now rotate the first+axis column or row
        else:
            contour_data[face][1][j] = (axis, direction, order)
    (face_indices, contour_indices) = get_face_contour(face, angle, state)
    # Now we modify the state and we return the new state
    new_state = copy.deepcopy(state)
    # Apply contour rotation directly without central face rotation
    last_el = contour_indices[3]
    if angle == 0:
        for j in range(3, 0, -1):
            contour_indices[j] = contour_indices[j - 1]
        contour_indices[0] = last_el
    else:
        contour_indices = contour_indices[::-1]
    # print(contour_indices)
    for j in range(0, 4):
        contour_face = contour_data[face][0][j]
        (axis, direction, order) = contour_data[face][1][j]
        write_array(abs(direction - 1), axis, contour_indices[j], new_state[contour_face])
    # print(new_state)
    return new_state


# Now we can start defining a rotation that works for a NxN cube
# The only difference here is that we can rotate not a face but a center slice
# of the Rubik's cube and so for that we will add a parameter called axis that will
# represent the index of the portion to rotate parallel to the give face
def rotation_n(face, axis, angle, state):
    new_state = copy.deepcopy(state)
    for i in range(0, axis + 1):
        if i == 0:
            new_state = rotation(face, angle, new_state)
        else:
            # We will just rotate the rest of the central pieces until the desired axis
            contour_data = copy.deepcopy(contour_data_init)
            # Same logic as the normal rotation but without rotating the face and with a small
            # tweak in the contour data indices
            for j in range(0, 4):
                (old_axis, direction, order) = contour_data[face][1][j]
                # If we are rotating the last column or row we will not rotate the last-axis column or row
                if old_axis == n - 1:
                    contour_data[face][1][j] = (n - i - 1, direction, order)
                # Else if we are rotating the first column or row we will now rotate the first+axis column or row
                else:
                    contour_data[face][1][j] = (i, direction, order)
            (face_indices, contour_indices) = get_face_contour(face, angle, state)
            # Now we modify the state and we return the new state
            # new_state = copy.deepcopy(state)
            # Apply contour rotation directly without central face rotation
            last_el = contour_indices[3]
            if angle == 0:
                for j in range(3, 0, -1):
                    contour_indices[j] = contour_indices[j - 1]
                contour_indices[0] = last_el
            else:
                contour_indices = contour_indices[::-1]
            # print(contour_indices)
            for j in range(0, 4):
                contour_face = contour_data[face][0][j]
                (axis, direction, order) = contour_data[face][1][j]
                write_array(abs(direction - 1), axis, contour_indices[j], new_state[contour_face])
            # print(new_state)
    # print(new_state)
    return new_state
