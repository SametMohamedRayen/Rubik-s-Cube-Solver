#! /bin/python3
# vim: set fileencoding=utf-8
#
# (c) July 5, 2023, José Martinez, Polytech Nantes, University of Nantes
#
# Licence:  proprietary
# The use of this library is not authorised outside the Polytechnic School of the University of Nantes.
#


__all__ = ['meta_solver']


from typing import TypeVar, Callable, Tuple, List


State       = TypeVar('State')
Description = TypeVar('Description')
Cost        = TypeVar('Cost')
Transition  = Tuple[Description, State, Cost]
Solution    = List[Transition]


def meta_solver (solver:   Callable[[int, State], List[Solution]],
                 d_max:    int,
                 initial:  State) -> List[Solution]:
    """
    A meta solver with a maximal depth limit.

    :param solver:  The actual solver, one accepting a depth limit as its first argument and an initial state.
    :param d_max:  The maximal depth at which a solution is to be found.
    :param initial:  The initial state from which to explore the state graph of the problem.
    :return:  A list of alternative solutions at some minimal depth up to the maximal depth limit in non-decreasing depth.
    """
    return [ s
             for d in range(d_max + 1)
             for s in solver(d, initial)
             if len(s) >= d ]


if __name__ == "__main__":
    pass

