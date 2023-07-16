from functools import reduce

from . import factorization


# Use of prime numbers in data encryption
# Bachelor thesis
# Department of Computer Science, Faculty of Science, Palacký University Olomouc
# 2023
# Matěj Ošťádal


# Each of these algorithms is designed to solve the discrete logarithm problem (DLP) for given values, that is:
#
# For given generator, result and modulus, find the least integer e, that:
#
#   generator^e = result (mod modulus)
#
# Each of these algorithms is designed to solve DLP in groups of certain shape.
# The theoretic part of each of these algorithms is described in the text, provided together with this file.

# REMARK: It is assumed, that there is a solution to the DLP for the given output.
# (If wrong generator is given, algorithms can fail.)

# Sources that were used for implementation purposes (pseudocode, idea, trick):
# [1] A Computational Introduction to Number Theory and Algebra. (2009) (https://www.shoup.net/ntb/)
# [2] A Graduate Course in Applied Cryptography. (2023) (http://toc.cryptobook.us/)
# [3] Handbook of Applied Cryptography. (1997) ISBN 978-0-8176-8297-2.


# [1]
def brute_force_dlog(generator, result, modulus):
    """
    Solves the DLP in groups of general order.
    (Mind that for large modulus, this algorithm is hardly inefficient.)

    Args:
        generator (int): Represents the base of the DLP.
        result (int): Represents the result of the DLP. (Must be greater than 0.)
        modulus (int): Represents the modulus of the DLP.

    Raises:
        ValueError: If result is less or equal to zero, DLP cannot be solved.

    Returns:
        int: Number e, which satisfies the equation generator^e = result (mod modulus).
        None: If DLP has no solution for given input.
    """

    if result <= 0:
        raise ValueError("Result must be greater than zero.")

    # make sure the result is in range
    result %= modulus

    # increase exponent until given result is found
    for exponent in range(modulus):
        current_result = pow(generator, exponent, modulus)

        if current_result == result:
            return exponent

    return None


# [1]
def recursive_dlog(generator, result, q, y, p):
    """
    Solves the DLP for group G of order q^y, that is a subgroup of the multiplicative Z*p.

    Args:
        generator (int): Represents the base of the DLP. (It must generate a group G of order q^y.)
        result (int): Represents the result of the DLP. (Must be greater than 0.)
        q (int): Information about the group order of G.
        y (int): Information about the group order of G.
        p (int): Prime number that defines the multiplicative group Z*p in which subgroup is DLP being solved.

    Returns:
        int: Number e, which satisfies the equation generator^e = result (mod p).
    """
    if result == 1:
        return 0

    # make sure the result is in range
    result %= p

    # base case, basic algorithm is used
    if y == 1:
        return brute_force_dlog(generator, result, p)

    # reduce the group order
    z = y // 2

    # find new generators and results in the smaller groups
    u_generator = pow(generator, q ** (y - z), p)
    u_result = pow(result, q ** (y - z), p)
    u = recursive_dlog(u_generator, u_result, q, z, p)

    if u is None:
        return None

    v_generator = pow(generator, q**z, p)
    v_result = result * pow(generator, -u, p)
    v = recursive_dlog(v_generator, v_result, q, y - z, p)

    if v is None:
        return None

    return (q**z) * v + u


# [2]
def silver_pohlig_hellman(generator, result, modulus, prime_factors=None):
    """
    Solves the DLP in groups of general order.
    (Mind that for modulus - 1 having only large prime factors, this algorithm is inefficient.)

    Args:
        generator (int): Represents the base of the DLP.
        result (int): Represents the result of the DLP. (Must be greater than 0.)
        modulus (int): Represents the modulus of the DLP. Prime values for modulus are recommended (modulus - 1 is the order of the group in which DLP is being solved)
        prime_factors (list, optional): Factorization of the group order (modulus - 1).

    Raises:
        ValueError: If result is less or equal to zero, DLP cannot be solved.

    Returns:
        int: Number e, which satisfies the equation generator^e = result (mod modulus).
    """

    # if factorization is not given, find it using factorization.py module
    if prime_factors is None:
        prime_factors = factorization.trial_division(modulus - 1)

    factors_with_count = [[x, prime_factors.count(x)] for x in set(prime_factors)]

    congruences = []

    for q_i, e_i in factors_with_count:
        new_order = int((modulus - 1) / pow(q_i, e_i))

        # calculate new generator and result of the new group
        generator_i = pow(generator, new_order, modulus)
        result_i = pow(result, new_order, modulus)

        # computing DLP in group of order q_i^e_i
        congruences.append(
            [recursive_dlog(generator_i, result_i, q_i, e_i, modulus), q_i**e_i]
        )

    solution = chinese_remainder_theorem(congruences)

    return solution


# [3]
def chinese_remainder_theorem(congruences):
    """
    Finds the unique solution to the system of congruences.

    Args:
        congruences (list): List of pairs (x_i, n_i) which represent the system of congruences in form: x \equiv a_i (mod n_i).

    Returns:
        int: The unique solution x to the system of congruences in form: x \equiv a_i (mod n_i).
    """
    # product of all moduli
    total_modulus = reduce(lambda x, y: x * y, [pair[1] for pair in congruences])

    # Finds the solution (mod total_modulus)
    x = 0

    for a_i, n_i in congruences:
        N_i = total_modulus // n_i

        # multiplicative inverse
        M_i = pow(N_i, -1, n_i)

        x += a_i * M_i * N_i

    return x % total_modulus
