import random
from math import floor

import modelisation as mod
import Solver_IDS

# print(mod.transpose([[1,2,3,4],[5,6,7,8]]))
# print(mod.get_face_contour(2,1,mod.just_bought_state))


just_bought_state = [[[j for _ in range(0, mod.n)] for _ in range(0, mod.n)] for j in mod.Color]
# print(just_bought_state)
# mod.rotation_n(3, 0, 0, just_bought_state)
# mod.rotation_n(3, 0, 1, just_bought_state)
# mod.rotation_n(2, 1, 0, just_bought_state)
# mod.rotation_n(2, 1, 1, just_bought_state)
# print(just_bought_state)
# print(mod.rotation_n(0, 1, 1, just_bought_state))
# mod.rotation_n(0, 1, 1, just_bought_state)

# Generating a random initial state
state = just_bought_state
iter = 2
for _ in range(0, iter):
    rand_face = random.randint(0, 5)
    rand_angle = random.randint(0, 1)
    state = mod.rotation(rand_face, rand_angle, state)
initial_state = state
print(initial_state)


# Now we can use one of the proposed solvers to try and solve for n = 2
# We start with IDS and with create
def transformations(state):
    transitions = []
    for angle in range(2):
        for face in range(6):
            new_s = mod.rotation(face, angle, state)
            transitions.append(("Desc", new_s, 1))
    return transitions


def is_final(state):
    for i in range(6):
        face = state[i]
        ref_color = face[0][0]
        r, c = 0, 0
        while r < mod.n:
            while c < mod.n:
                if face[r][c] != ref_color:
                    return False
                c += 1
            r += 1
    return True


d_max = 4

solver_result = Solver_IDS.solver(transformations, is_final, d_max, initial_state)
for solution in solver_result:
    print(solution)


# With the center slice rotation function added for the nxn generalization
# giving freedom to rotate only center slices parallel to faces in addition.
# We can now generate transformations according to that logic
# Note that here we are only allowed to rotate up to E(n/2) center slice (axis) at once
# in order to mitigate redundant equivalent transformations.
def transformations_n(state):
    transitions = []
    for angle in range(2):
        for face in range(6):
            for axis in range(0, floor(mod.n / 2)):
                new_s = mod.rotation_central_piece_n(face, axis, angle, state)
                transitions.append(("Desc", new_s, 1))
    return transitions


solver_result = Solver_IDS.solver(transformations, is_final, d_max, initial_state)
for solution in solver_result:
    print(solution)


# There is an optimization that we could implement also using the rotation_n
# function that always rotates a face along with a number of center slices
# parallel to it. This method has shown to introduce an optimization in the
# search algorithm for the solution compared to the first one.

def transformations_n_optimized(state):
    transitions = []
    for angle in range(2):
        for face in range(6):
            for axis in range(0, floor(mod.n / 2)):
                new_s = mod.rotation_n(face, axis, angle, state)
                transitions.append(("Desc", new_s, 1))
    return transitions


solver_result = Solver_IDS.solver(transformations, is_final, d_max, initial_state)
for solution in solver_result:
    print(solution)

# We can now also analyse the IDA solver.
