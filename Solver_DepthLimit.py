#! /bin/python3
# vim: set fileencoding=utf-8
#
# (c) February 28, 2019, José Martinez, Polytech Nantes, University of Nantes
#
# Licence:  proprietary
# The use of this library is not authorised outside the Polytechnic School of the University of Nantes.
#


__all__ = ['solver']


from typing import TypeVar, Callable, Tuple, List


State       = TypeVar('State')
Description = TypeVar('Description')
Cost        = TypeVar('Cost')
Transition  = Tuple[Description, State, Cost]
Solution    = List[Transition]


def solver (transformations:  Callable[[State], List[Transition]],
            isFinal:          Callable[[State], bool],
            state:            State,
            d_max:            int) -> List[Solution]:
    """
    A basic backtracking solver with a depth limit in order to avoid infinite searches in infinite graphs.

    :param transformations:  The function that return the successors of a given state.
    :param isFinal:  The predicate that determines whether a state is a solution.
    :param state:  Some state from which to explore the state graph of the problem.
    :param d_max:  The maximal authorised search depth.
    :return:  A list of alternative solutions.
    """
    return ([]   if d_max < 0      else
            [[]] if isFinal(state) else
            [ [(d, s, c)] + solution
              for (d, s, c) in transformations(state)
              for solution in solver(transformations, isFinal, s, d_max - 1) ])
    

if __name__ == "__main__":
    pass

