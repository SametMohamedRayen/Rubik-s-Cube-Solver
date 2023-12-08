import modelisation as mod
import Solver_IDS

# print(mod.transpose([[1,2,3,4],[5,6,7,8]]))
# print(mod.get_face_contour(2,1,mod.just_bought_state))


just_bought_state = [[[j for _ in range(0, mod.n)] for _ in range(0, mod.n)] for j in mod.Color]
# print(just_bought_state)
# mod.rotation_n(0, 0, 0, just_bought_state)
# mod.rotation_n(0, 0, 1, just_bought_state)
# print(just_bought_state)
print(mod.rotation_n(0, 1, 1, just_bought_state))
# mod.rotation_n(0, 1, 1, just_bought_state)

# Generating a random initial state
"""
state = just_bought_state
rand_iter = random.randint(50, 120)
for _ in range(0, rand_iter):
    rand_face = random.randint(0, 5)
    rand_angle = random.randint(0, 1)
    state = mod.rotation(rand_face, rand_angle, state)
"""
initial_state = just_bought_state
# print(initial_state)


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


d_max = 5

# print(just_bought_state)
# print(is_final(just_bought_state))

# Solver_IDS.solver(transformations, is_final, d_max, initial_state)
