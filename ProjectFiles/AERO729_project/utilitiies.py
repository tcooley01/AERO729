import numpy as np
from numpy.polynomial import Polynomial

def calculate_box_width(tol: float,
                        sigma: float,
                        epsilon: float
                        )-> float:
    
    """
    Calculates what the size of the boxes should be based on the roots of the polynomial:

                    alpha*z^2 + (sigma^6)*z - simga^12 = 0
    
    Where:

                    alpha = tol/(4*epsilon), z = r^6, r = distance
    
    Parameters
    ----------

    tol: float

        The tolerance for how small a potential should be to be considered effectively zero

    sigma: float

        where the zero of the LJ potential function occurs

    epsilon: float

        controls depth of the well in LJ potential

    Returns
    -------
        float

        how wide the boxes dividing the domain should be
    """

    alph = -tol/(4*epsilon)

    quadratic = Polynomial([-sigma**12, sigma**6, alph])

    quad_roots = quadratic.roots()

    # if sigma and epsilon are both greater than zero as they should be we will 
    # have 2 non-complex roots so raise an error if any of them are complex
    if np.iscomplex(quad_roots).any():
        raise ValueError('Invalid values of input parameters leading to complex roots')
    
    # the two roots then each have corresponding 6th degree polynomials that must solved
    # resulting in 4 real roots, throwing away the 2 negative ones leaves the desired and
    # the one near sigma which should also be thrown out

    sixth_one = np.zeros(7)
    sixth_two = np.zeros(7)

    sixth_one[0] = -quad_roots[0]
    sixth_one[6] = 1

    sixth_two[0] = -quad_roots[1]
    sixth_two[6] = 1

    sixth_one = Polynomial(sixth_one)
    sixth_two = Polynomial(sixth_two)

    first_roots = sixth_one.roots()
    second_roots = sixth_two.roots()

    canidate_1 = max(
        first_roots[np.where(~np.iscomplex(first_roots))]
    )
    canidate_2 = max(
        second_roots[np.where(~np.iscomplex(second_roots))]
    )
    return np.real(max(canidate_1, canidate_2))