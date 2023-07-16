import math
import random

from . import factorization


# Use of prime numbers in data encryption
# Bachelor thesis
# Department of Computer Science, Faculty of Science, Palacký University Olomouc
# 2023
# Matěj Ošťádal


# Each of these algorithms is designed to decide, whether a given number n is a prime number.
# The answer True implies, that n is prime. (Mind that some of these algorithms are probabilistic,
# thus not provide correct answers all the time.)

# Each of these algorithms is designed to solve this problem for specific forms of number n.
# The theoretic part of each of these algorithms is described in the text, provided with this file.

# Sources that were used for implementation purposes (pseudocode, idea, trick):
# [1] Handbook of Applied Cryptography. (1997) ISBN 978-0-8176-8297-2.
# [2] PRIMES is in P. (2004) (https://doi.org/10.4007/annals.2004.160.781})
# [3] A Simple and Fast Algorithm for Computing the N-th Term of a Linearly Recurrent Sequence. (2020) (https://arxiv.org/pdf/2008.08822.pdf)
# [4] https://github.com/Ssophoclis/AKS-algorithm/blob/master/AKS.py


def trial_division(n, upper_bound=math.inf):
    """
    Deterministic test which decides if n is a prime number.

    Args:
        n (int): An integer being tested.

    Returns:
        boolean: The answer to the question: Is n a prime number?
    """

    # test basic properties
    if n <= 1:
        return False

    if is_even(n):
        return n == 2

    if is_divisible(n, 3):
        return n == 3

    upper_bound = min(math.isqrt(n), upper_bound)

    for number in range(5, upper_bound + 1, 6):
        if is_divisible(n, number) or is_divisible(n, number + 2):
            return False

    return True


# [1]
def fermat_test(n, test_bound=10):
    """
    Probability test which decides if n is prime.

    Args:
        n (int): An integer being tested.
        test_bound (int, optional): Gives us the upper limit for choices of a's. Defaults to 10.

    Returns:
        tuple: first: The final decision on the primality of n. second: Probability of the decision.
    """

    # test basic properties
    if n <= 1:
        return (False, 1)

    if is_even(n):
        return (n == 2, 1)

    # base picking
    for _ in range(test_bound):
        a = random.randint(2, n - 2)

        # fermat's theorem
        if pow(a, n - 1, n) != 1:
            return (False, 1)

    return (True, 1 - (0.5**test_bound))


# [1]
def solovay_strassen_test(n, test_bound=10):
    """
    Probability test which decides if n is prime.

    Args:
        n (int): An integer being tested.
        test_bound (int, optional): Gives us the upper limit for choices of a's. Defaults to 10.

    Returns:
        tuple: The final decision on the first position. Probability of the decision on the second position.
    """

    # test basic properties
    if n <= 1:
        return (False, 1)

    if is_even(n):
        return (n == 2, 1)

    # base picking
    for _ in range(test_bound):
        a = random.randint(2, n - 2)
        r = pow(a, (n - 1) // 2, n)

        if r != 1 and r != n - 1:
            return (False, 1)

        jacobi_symbol = jacobi(a, n)

        if not are_congruent(r, jacobi_symbol, n):
            return (False, 1)

    return (True, (1 - (0.5**test_bound)))


# [1]
def jacobi(a, n):
    """
    Counts the value of the Jacobi symbol for given values.

    Args:
        a (int): Numerator of the Jacobi symbol.
        n (int): Denominator of the Jacobi symbol.

    Raises:
        ValueError: If invalid value for n is given.

    Returns:
        int: The value of the Jacobi symbol for values a, n.
    """
    if n <= 0 or is_even(n):
        raise ValueError("Invalid input for n. It must be an odd positive integer.")

    a %= n

    jacobi_symbol = 1

    # recursion
    while a != 0:
        # a = 2^e * a_1, where a_1 is odd
        while is_even(a):
            a /= 2

            if are_congruent(n, 3, 8) or are_congruent(n, 5, 8):
                jacobi_symbol = -jacobi_symbol

        a, n = n, a

        if are_congruent(a, 3, 4) and are_congruent(n, 3, 4):
            jacobi_symbol = -jacobi_symbol
        a %= n

    if n == 1:
        return jacobi_symbol
    else:
        return 0


# [1]
def miller_rabin_test(n, test_bound=10):
    """
    Probability test which decides if n is prime.

    Args:
        n (int): An integer being tested.
        test_bound (int, optional): Gives us the upper limit for choices of a's. Defaults to 10.

    Returns:
        tuple: The final decision on the first position. Probability of the decision on the second position.
    """

    # test basic properties
    if n <= 1:
        return (False, 1)

    if is_even(n):
        return (n == 2, 1)

    if n == 3:
        return (True, 1)

    # n - 1 = 2^s * r, where r is odd
    s = 0
    r = n - 1
    while is_even(r):
        s += 1
        r //= 2

    # base picking
    for _ in range(test_bound):
        a = random.randint(2, n - 2)
        y = pow(a, r, n)

        if y != 1 and y != n - 1:
            j = 1

            while j <= s - 1 and y != n - 1:
                y = pow(y, 2, n)

                if y == 1:
                    return (False, 1)
                j += 1

            if y != n - 1:
                return (False, 1)

    return (True, 1 - (0.25**test_bound))


# [1]
def lucas_lehmer_test(n):
    """
    Deterministic test which decides if n is a Mersenne prime.

    Args:
        n (int): An integer being tested.

    Returns:
        boolean: The answer to the question: Is n a Mersenne prime?
    """
    # basic property
    if n <= 1:
        return False

    s = find_mersenne_exponent(n)

    if s is None:
        return False

    if s == 2:
        return True

    # testing whether exponent is prime
    if not trial_division(s):
        return False

    u = 4

    for _ in range(1, s - 1):
        u = (u**2 - 2) % n

    return u == 0


def find_mersenne_exponent(n):
    """
    Finds an exponent s (if it exsists), for which 2^s - 1 = n.

    Args:
        n (int): Number for which we attempt to find the exponent.

    Returns:
        int: Exponent s for which 2^s - 1 = n. (None if such exponent does not exist.)
    """
    total = n + 1
    exponent = 0

    # dividing by 2 if possible
    while total > 0 and is_even(total):
        exponent += 1
        total //= 2

    if total == 1:
        return exponent

    return None


# [1]
def pocklington_theorem_test(n, divisor=None, divisor_fact=None, test_bound=10):
    """
    Probabilistic version of a primality testing algorithm.

    Args:
        n (int): An integer being tested for primality.
        divisor (int, optional): A nontrivial divisor of n-1. Defaults to None.
        divisor_fact (list, optional): The prime factorization of the divisor. Defaults to None.
        test_bound (int, optional): Gives us the upper limit for choices of a's. Defaults to 10.

    Returns:
        boolean: A decision to the primality of n. None if the primality could not be decided.
    """

    # basic property
    if is_even(n):
        return n == 2

    # if not enough information was given, compute it
    if divisor is None or not is_divisible(n - 1, divisor):
        divisor = factorization.squfof(n - 1)
        divisor_fact = factorization.trial_division(divisor)

    if divisor_fact is None:
        divisor_fact = factorization.trial_division(divisor)

    # test the pocklington theorem
    if divisor > math.sqrt(n) - 1:
        for _ in range(test_bound):
            a = random.randint(2, n - 2)

            if pow(a, n - 1, n) == 1 and is_suitable(a, divisor_fact, n):
                return True

        return False

    return None


def is_suitable(a, factorization, n):
    """
    Tests whether a satisfies the second condition of Pocklington theorem.

    Args:
        a (int): The chosen base.
        factorization (int): Factorization of n-1.
        n (int): Number being tested for primality. Modulus.

    Returns:
        boolean: True if a satisfies the second condition of Pocklington theorem.
    """

    for prime in factorization:
        if math.gcd(pow(a, (n - 1) // prime, n)) != 1:
            return False

    return True


# [2]
def aks_test(n):
    """
    Deterministic test which decides if n is a prime number.

    Args:
        n (int): An integer being tested.

    Returns:
        boolean: The answer to the question: Is n prime number?
    """

    # basic property
    if n <= 1:
        return False

    if is_perfect_power(n):
        return False

    r = find_smallest_r(n)

    for a in range(1, r + 1):
        divisor = math.gcd(a, n)

        if 1 < divisor and divisor < n:
            return False

    if n <= r:
        return True

    limit = math.floor(math.sqrt(phi(r)) * math.log(n, 2))

    for a in range(1, limit + 1):
        if not polynomial_equivalency(a, n, r):
            return False

    return True


# [3], [4]
def polynomial_equivalency(a, n, r):
    """Checks whether two polynomials of form: (X + a)^n and X^n + a are equivalent mod X^r - 1 and mod n.

    Args:
        a (int): Constant in the polynomials.
        n (int): The exponent of both polynomials.
        r (int): The exponent of the modulus polynomial.

    Returns:
        boolean: True if polynomials are equivalent.
    """

    left_poly = [1, 0]
    base = [a, 1]
    const = a

    power = n
    while power > 0:
        if is_odd(power):
            left_poly = poly_mod_mul(left_poly, base, n, r)
        base = poly_mod_mul(base, base, n, r)
        power //= 2

    # ((X+ a)^n mod (X^r - 1, n)) - ((X^n + a) mod (X^r - 1, n))

    left_poly[0] -= const
    left_poly[n % r] -= 1

    # if the difference contains zeros only, the polynomials were equal
    return not any(left_poly)


# [3], [4]
def poly_mod_mul(poly_1, poly_2, modulus_1, modulus_2):
    """
    Performs a polynomial modular exponentiation of given polynomials and moduli.

    Args:
        poly_1 (list): Coefficients representing the first polynomial.
        poly_2 (list): Coefficients representing the second polynomial.
        modulus_1 (int): Represents the first modulus. (n)
        modulus_2 (int): Represents the first modulus. (X^r - 1)

    Returns:
        list: Coefficients of the result of modular exponentiation.
    """
    result_length = len(poly_1) + len(poly_2) - 1

    result_poly = [0] * result_length

    for i in range(len(poly_1)):
        for j in range(len(poly_2)):
            result_poly[(i + j) % modulus_2] += poly_1[i] * poly_2[j]
            result_poly[(i + j) % modulus_2] = (
                result_poly[(i + j) % modulus_2] % modulus_1
            )

    #
    # result_poly = result_poly[: -(len(result_poly) - modulus_2)]

    for _ in range(modulus_2, len(result_poly)):
        result_poly = result_poly[:-1]

    return result_poly


def is_perfect_power(n):
    """Checks if n is a perfect power. In other words, if there are numbers a,b for which a^b = n."""
    for b in range(2, math.floor(math.log(n, 2) + 1)):
        # b-th root of n
        a = n ** (1 / b)

        if a - int(a) == 0:
            return True
    return False


def find_smallest_r(n):
    """Finds the smallest r, such that the order of n mod r > log^2(n)."""
    log_bound = math.floor(math.log(n, 2) ** 2)
    searching = True
    r = 1

    while searching:
        r += 1
        searching = False

        # check if order is less than log^2(n)
        power = 1
        while power <= log_bound and not searching:
            if pow(n, power, r) == 0 or pow(n, power, r) == 1:
                searching = True
            power += 1
    return r


def phi(n):
    """Returns the count of coprime integers that are less than n."""
    count = 0

    for number in range(1, n + 1):
        if math.gcd(n, number) == 1:
            count += 1
    return count


def is_divisible(a, b):
    """Tests whether b divides a."""
    return a % b == 0


def is_even(a):
    """Tests whether a is even."""
    return is_divisible(a, 2)


def is_odd(a):
    """Tests whether a is odd."""
    return not is_even(a)


def are_congruent(a, b, n):
    """Tests whether a and b are congruent mod n."""
    return a % n == b % n
