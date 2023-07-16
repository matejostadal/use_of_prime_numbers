import random
import math

from . import primality_testing as primes


# Use of prime numbers in data encryption
# Bachelor thesis
# Department of Computer Science, Faculty of Science, Palacký University Olomouc
# 2023
# Matěj Ošťádal


# These algorithms form the RSA cryptosystem that was described in the text, provided with this file
# (where the theoretic parts are described).

# Note that this implementation of the RSA cryptosystem is not the best possible. The main idea was to
# make it easy to understand.

# REMARK: As in the theoretical part of our work, we assume that the message being sent is a integer smaller than n.
# (n is a part of the sender's public key)

# Sources that were used for implementation purposes (pseudocode, idea, trick):
# [1] A Graduate Course in Applied Cryptography. (2023) (http://toc.cryptobook.us/)
# [2] RSA and Public-Key Cryptography. (2002) ISBN 1-58488-338-3
# [3] Cryptography: Theory and Practice. (2018) ISBN 978-1138197015.
# [4] Handbook of Applied Cryptography. (1997) ISBN 978-0-8176-8297-2.


# [1], [2]
def encrypt(message, others_kp, mine_kp, mine_ks):
    """
    Encrypts a message in RSA. (Including digital signatures.)

    Args:
        message (int):A number representing a message we want to send.
        others_kp (tuple): Public key of the recipient.
        mine_kp (tuple): Public key of the user encrypting.
        mine_ks (int): Secret key of the user encrypting.

    Raises:
        ValueError: If message is not of wanted length (must be < n, where n is a part of mine_kp).

    Returns:
        tuple: The encrypted message and a message signature.
    """
    n, e = others_kp

    # checking the proper form of message
    if not isinstance(message, int) or message >= n:
        raise ValueError(
            "Messages must be an integer smaller than the modulus of the recipient."
        )

    # encryption
    cipher = pow(message, e, n)

    # signing
    digital_signature = sign_message(message, mine_kp, mine_ks)

    return cipher, digital_signature


# [3]
def sign_message(message, mine_kp, mine_ks):
    """Signs the given message. (Based on the RSA signature scheme.)"""
    n, _ = mine_kp

    hash = make_hash_of(message)
    signature = pow(hash, mine_ks, n)

    return signature


def make_hash_of(message):
    """This function returns the hash of given message."""

    # this hash function returns the same message without damage
    # this function can be changed anytime with a proper choice of hash function anytime
    return hash(message)


# [1], [2]
def decrypt(cipher_pair, others_kp, mine_kp, mine_ks):
    """
    Decrypts the received cipher_pair in RSA. (Including digital signatures.)

    Args:
        cipher_pair (tuple): The pair representing the cipher (ciphered message and a signature) sent to us.
        others_kp (tuple): Public key of the user that sent the message.
        mine_kp (tuple): Public key of the user decrypting.
        mine_ks (int): Secret key of the user decrypting.

    Raises:
        ValueError: If the message was changed, or signed falsely.
        ValueError: If message is not of wanted length (must be < n, where n is a part of mine_kp).

    Returns:
        int: The decrypted message.
    """
    cipher, signature = cipher_pair
    n, _ = mine_kp

    # checking the proper form of message
    if not isinstance(cipher, int) or cipher >= n:
        raise ValueError(
            "Messages must be an integer smaller than the modulus of the recipient."
        )

    # decryption
    message = pow(cipher, mine_ks, n)

    # signing
    if not valid_signature(message, signature, others_kp):
        raise ValueError(
            "Invalid signature. The received message is a fake one. (Or numbers used in key generation were not primes. - try again)"
        )
    return message


# [3]
def valid_signature(message, signature, others_kp):
    """Makes sure that the signature is valid. (Based on the RSA signature scheme.)"""
    n, e = others_kp

    signature = pow(signature, e, n)
    hash = make_hash_of(message)

    return hash == signature


# [1], [2]
def generate_key_pair(min, max):
    """
    Follows the key generation protocol of RSA.

    Args:
        min (int): Minimal size of the probable prime used in the key generation.
        max (int): Maximal size of the probable prime used in the key generation.

    Returns:
        tuple: First position of tuple is a tuple which is the generated public key. The second position is the generated secret key.
    """
    p = generate_prime_number(min, max)
    q = generate_prime_number(min, max)

    n = p * q
    phi_n = (p - 1) * (q - 1)

    # calculate encryption exponent
    # (notice we do not care about the effectivity
    # as we do not necessarily pick small values)
    e = random.randint(2, phi_n)
    while math.gcd(e, phi_n) != 1:
        e = random.randint(2, phi_n)

    # find decryption exponent
    d = pow(e, -1, phi_n)

    return ((n, e), d)


# [4]
def generate_prime_number(bottom_limit, top_limit, test_bound=1000000):
    """
    Generates a probable prime in the given range.

    Args:
        bottom_limit (int): Minimal size of the probable prime.
        top_limit (int): Maximal size of the probable prime.
        test_bound (int, optional): The upper limit used in primality tests. Defaults to 1000000.

    Returns:
        int: A probable prime.
    """
    n = random.randint(bottom_limit, top_limit)
    test_bound = min(test_bound, math.isqrt(top_limit))

    # to save extra generating
    if primes.is_even(n):
        n += 1

    # test if it has small prime factors
    if not primes.trial_division(n, upper_bound=test_bound):
        return generate_prime_number(bottom_limit, top_limit)

    # test with miller-rabin
    if not primes.miller_rabin_test(n, test_bound=test_bound):
        return generate_prime_number(bottom_limit, top_limit)

    return n
