import math
import random
from collections import deque


# Use of prime numbers in data encryption
# Bachelor thesis
# Department of Computer Science, Faculty of Science, Palacký University Olomouc
# 2023
# Matěj Ošťádal


# Each of these algorithms is designed to solve the factorization problem (FP) (or its part) for a given value of n, that is:
#
# For given integer n > 1, find a prime numbers pi and positive integers ei, that:
#
#   n = p1^e1 * p2^e2 * ... * pk^ek
#
# For purpose of these algorithms, we won't provide the exponents in the equation above, but only a list of prime factors.
# Thus, if p1^2 divides n, p1 will appear twice in the returned list of prime factors.

# Some of these algorithms can also find composite factors or not all of the prime factors.
# Each of these algorithms is designed to solve this problem for specific forms of number n.
# The theoretic part of each of these algorithms is described in the text, provided together with this file.


# Sources that were used for implementation purposes (pseudocode, idea, trick):
# [1] Prime Numbers and Computer Methods for Factorization. (2011) ISBN 0-8493-8523-7.
# [2] Handbook of Applied Cryptography. (1997) ISBN 978-0-8176-8297-2.
# [3] Development of sieve of Eratosthenes and sieve of Sundaram's proof. (https://doi.org/10.48550/arXiv.2102.06653)
# [4] Square Form Factorization. (https://homes.cerias.purdue.edu/~ssw/squfof.pdf)


def naive_trial_division(n):
    """
    Returns the factorization of the given value n.

    Args:
        n (int): Number to factor.

    Returns:
        list: List of prime factors that divide the number n.
    """
    prime_factors = []
    upper_bound = math.isqrt(n)

    while is_even(n):
        prime_factors.append(2)
        n //= 2

    while is_divisible(n, 3):
        prime_factors.append(3)
        n //= 3

    for number in range(5, upper_bound + 1, 6):
        while is_divisible(n, number):
            prime_factors.append(number)
            n //= number

        while is_divisible(n, number + 2):
            prime_factors.append(number + 2)
            n //= number + 2

    if n != 1:
        prime_factors.append(n)

    return prime_factors


# [1]
def trial_division(n, given_upper_bound=math.inf):
    """
    Returns the factorization of the given value n with respect to the given upper bound.

    Args:
        n (int): Number to factor.
        given_upper_bound (int, optional): If this bound is given, factors only smaller than this bound are found. Defaults to math.inf.

    Returns:
        list: List of prime factors that divide the number n that are smaller than given_upper_bound.
    """

    prime_factors = []
    current = n
    upper_bound = min(given_upper_bound, math.isqrt(n))

    def reduce(number):
        nonlocal current
        nonlocal upper_bound

        if number > 1:
            while is_divisible(current, number):
                prime_factors.append(number)
                current //= number

        upper_bound = min(upper_bound, math.isqrt(current))

    reduce(2)
    reduce(3)
    number = 5

    while number <= upper_bound:
        if is_divisible(current, number):
            reduce(number)

        if is_divisible(current, number + 2):
            reduce(number + 2)

        number += 6

    if number > math.isqrt(current):
        reduce(current)

    if current != 1:
        print(
            f"Factorization was NOT COMPLETED because of the given upper bound.\nFound prime factors are {prime_factors,}. The remaining cofactor is {current}.\n"
        )

    return prime_factors


# [2]
def pollard_rho_method(n, f=lambda x, p: (x**2 + 1) % p):
    """
    Searches for a nontrivial factor of n.

    Args:
        n (int): Number for which we try to find the nontrivial factor.
        f (function, optional): Random function to use in Floyd's algorithm. Defaults to lambda x,p: (x**2 + 1) % p.

    Returns:
        int: A factor of n. (May be trivial.)
    """
    tortoise, hare = 2, 2
    d = 1

    while d == 1:
        tortoise = f(tortoise, n)
        hare = f(f(hare, n), n)
        d = math.gcd(tortoise - hare, n)

    if d == n:
        print("Nontrivial factor was NOT FOUND. Try a different f function.")

    return d


# [2]
def pollard_p_minus_1_method(n, smoothness_bound=10**5):
    """
    Searches for a nontrivial factor of n.

    Args:
        n (int): Number for which we try to find the nontrivial factor.
        smoothness_bound: All the prime factors of n are less or equal to smoothness_bound. Defaults to 10**5.

    Returns:
        tuple: Two factors of n. (May be trivial.)
    """
    a = random.randrange(2, 10)
    d = math.gcd(a, n)

    if d > 1:
        return d, n // d

    # for each prime <= B
    small_primes = find_small_primes(smoothness_bound + 1)

    for prime in small_primes:
        l = math.floor(math.log(n) / math.log(prime))
        a = pow(a, (prime**l), n)

    d = math.gcd(a - 1, n)

    if d == n or d == 1:
        print("Nontrivial factor was NOT FOUND. Try a bigger smoothness bound.")

    return d, n // d


# [3]
def find_small_primes(smoothness_bound):
    """
    Finds all small primes less than given bound using the Sieve of Sundaram.

    Args:
        n (int): Number for which we try to find the nontrivial factor.
        smoothness_bound (int): Represents the bound up to which we find the primes.

    Returns:
        int: List of primes less than given smoothness_bound.
    """

    k = (smoothness_bound - 2) // 2
    integers = list(range(k + 1))

    # sieving
    for i in range(1, k + 1):
        j = i
        while i + j + 2 * i * j <= k:
            integers[i + j + 2 * i * j] = 0
            j += 1

    # for all numbers i that are not 0, 2i+1 is prime
    small_primes = [2 * number + 1 for number in [x for x in integers if x != 0]]

    if smoothness_bound > 2:
        small_primes.insert(0, 2)

    return small_primes


# [4]
def squfof(n):
    """
    Attempts to find a nontrivial divisor of given number n.

    Args:
        n (int): Number for which we try to find the nontrivial factor.

    Returns:
        int: A nontrivial factor of n.
        None: If the search for nontrivial factor fails.
    """

    result = trivial_divisibility_check(n)
    if result is not None:
        return result

    # 1.
    if n % 4 == 1:
        d = 2 * n
    else:
        d = n

    first_partial_quotient = math.isqrt(d)
    q_with_caret = 1
    p_1 = first_partial_quotient
    large_Q = d - p_1 * p_1
    small_bound = 2 * math.isqrt(2 * math.isqrt(d))
    large_bound = 2 * small_bound

    # 2.
    iteration = 0
    queue = deque()
    while True:
        partial_quotient = (first_partial_quotient + p_1) // large_Q
        p_2 = partial_quotient * large_Q - p_1

        if large_Q <= small_bound and is_even(large_Q):
            queue.append((large_Q / 2, p_1 % (large_Q / 2)))
        elif large_Q <= small_bound / 2:
            queue.append((large_Q, p_1 % large_Q))

        t = q_with_caret + partial_quotient * (p_1 - p_2)
        q_with_caret = large_Q
        large_Q = t
        p_1 = p_2

        if is_even(iteration) and is_square(large_Q):
            r = math.isqrt(large_Q)

            for x, y in queue:
                if r == x and is_divisible(p_1 - y, r):
                    if r == 1:
                        return None

                    index = queue.index((x, y)) + 1
                    while index != 0:
                        queue.popleft()
                        index -= 1
                    break
            else:
                break

        iteration += 1
        if broken_upper_bound(large_bound, iteration):
            return None

    # 3.
    q_with_caret = r
    p_1 = p_1 + r * ((first_partial_quotient - p_1) // r)
    large_Q = (d - p_1 * p_1) / q_with_caret

    # 4.
    iteration = 0
    while True:
        partial_quotient = (first_partial_quotient + p_1) // large_Q
        p_2 = partial_quotient * large_Q - p_1

        if p_1 == p_2:
            break

        t = q_with_caret + partial_quotient * (p_1 - p_2)
        q_with_caret = large_Q
        large_Q = t
        p_1 = p_2

        iteration += 1
        if broken_upper_bound(large_bound, iteration):
            return None

    if is_even(large_Q):
        return int(large_Q // 2)

    return int(large_Q)


def broken_upper_bound(bound, i):
    """Tests if given bound was broken."""
    return bound < i


def is_square(number):
    """Tests if number is a square."""
    sqrt = math.isqrt(number)
    return sqrt * sqrt == number


def trivial_divisibility_check(n):
    """Tests basic situations of divisibility."""
    if n % 2 == 0:
        return 2

    if is_square(n):
        return int(math.isqrt(n))

    return None


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
