import math

import factorization
import discrete_log
import primality_testing
import rsa


# Use of prime numbers in data encryption
# Bachelor thesis
# Department of Computer Science, Faculty of Science, Palacký University Olomouc
# 2023
# Matěj Ošťádal


# ===================================================
#                DISCRETE LOGARITHM
# ===================================================

# BRUTE FORCE
# -----------

# generator = 7
# result = 23
# modulus = 43241

# generator = 7
# result = 43240
# modulus = 43241

# generator = 2
# result = 7
# modulus = 19

# generator = 2
# result = 5
# modulus = 10

# generator = 3
# result = 29517
# modulus = 1234577

# not efficient for large modulus
# generator = 17
# result = 2
# modulus = 8503057

# TEST
# brute_force_e = discrete_log.brute_force_dlog(generator, result, modulus)
# print(brute_force_e)

# if brute_force_e is not None:
#     assert pow(generator, brute_force_e, modulus) == result % modulus


# RECURSIVE DISCRETE LOG
# ----------------------

# generator = 15
# result = 5
# q = 6
# y = 2
# modulus = 37

# generator = 15
# result = 5
# q = 10
# y = 2
# modulus = 101

# generator = 2
# result = 321
# q = 2
# y = 4
# modulus = 257

# NONE
# generator = 4
# result = 6
# q = 2
# y = 16
# modulus = 257

# NONE
# generator = 3
# result = 8
# q = 2
# y = 2
# modulus = 37

# generator = 3
# result = 29517
# q = 2
# y = 16
# modulus = 65537

# TEST
# recursive_e = discrete_log.recursive_dlog(generator, result, q, y, modulus)
# print(recursive_e)

# if recursive_e is not None:
#     assert result % modulus == pow(generator, recursive_e, modulus)


# SILVER-POHLIG-HELLMAN
# ---------------------

# generator = 18
# result = 2
# modulus = 29

# generator = 624
# result = 12
# modulus = 8101

# generator = 18222
# result = 8
# modulus = 50021

# generator = 8191
# result = 3689
# modulus = 432161

# generator = 17
# result = 1960308467209
# modulus = 2363916555000

# # TEST
# sph_e = discrete_log.silver_pohlig_hellman(generator, result, modulus)
# if sph_e is not None:
#     assert result % modulus == pow(generator, sph_e, modulus)


# ===================================================
#                   FACTORING
# ====================================================

# TRIAL DIVISION
# --------------

# n = 4567890123

# n = 29855491

# n = 2**11 + 1

# n = 4549 * 7883 * 2 * 7417 * 5281

# May not stop for large numbers
# n = 12345678910987654321

# TEST
# factors = factorization.trial_division(n)
# print(factors)
# prod = math.prod(factors)
# assert prod == n


# POLLARD RHO
# -----------

# TEST
# n = 4567890123

# n = 17 * 17 * 19

# n = 5 * 2 * 19

# d = factorization.pollard_rho_method(n)
# print(d)
# assert n % d == 0


# POLLARD P-1
# -----------

# n = 19048567
# bound = 19

# n = 471804060
# bound = 25

# n = 6238381150
# bound = 35

# n = 15739435638928
# bound = 35

# TEST
# d_1, d_2 = factorization.pollard_p_minus_1_method(n, bound)
# print(d_1, d_2)

# assert n % d_1 == n % d_1 == 0
# assert d_1 * d_2 == n


# SQUFOF
# ------

# n = 22117019

# n = 1000000000040000003

# n = 2547896352415748307

# n = 12345678987654321

# n = 15986516813548456466133

# n = 15986516813548456466133868517

# TEST
# divisor = factorization.squfof(n)
# print(divisor)
# assert n % divisor == 0


# ===================================================
#                 PRIMALITY TESTING
# ===================================================

# TRIAL DIVISION
# --------------

# n = 8191
# correct = True

# n = 923456790239
# correct = True

# May not stop for large numbers
# n = 618970019642690137449562111
# correct = True

# result = primality_testing.trial_division(n)
# assert correct == result


# FERMAT TEST
# -----------

# n = 522
# correct = False

# n = 29
# correct = True

# n = 1223
# correct = True

# n = 1293
# correct = False

# n = 986817733679
# correct = True

# n = 986817733667
# correct = False

# n = 62781381721
# correct = True

# This can fail, because n is a Carmichael number.
# n = 2455921
# correct = False

# TEST
# result, decision_probability = primality_testing.fermat_test(n, test_bound=15)
# print(decision_probability)
# assert correct == result


# SOLOVAY-STRASSEN TEST
# ---------------------

# n = 522
# correct = False

# n = 29
# correct = True

# n = 1223
# correct = True

# n = 1293
# correct = False

# n = 10631
# correct = True

# n = 62781381721
# correct = True

# n = 158681523057
# correct = False

# n = 986817733679
# correct = True

# This can fail, because n is an absolute Euler pseudoprime.
# n = 4903921
# correct = False

# TEST
# result, decision_probability = primality_testing.solovay_strassen_test(n)
# print(decision_probability)
# assert correct == result


# MILLER-RABIN TEST
# -----------------

# n = 522
# correct = False

# n = 29
# correct = True

# n = 1223
# correct = True

# n = 1293
# correct = False

# n = 10631
# correct = True

# n = 62781381721
# correct = True

# n = 158681523057
# correct = False

# n = 986817733679
# correct = True

# n = 4903921
# correct = False

# n = 67779370450709991273608419493793130527925903913537
# correct = True

# n = 67779370450709991273608419493793130527925903913529
# correct = False

# n = 5990103512870556906180584080180268237931650875781672937166634642761543
# correct = True

# TEST
# result, decision_probability = primality_testing.miller_rabin_test(n)
# print(decision_probability)
# assert correct == result


# MERSENNE PRIMES
# ---------------

# n = 2
# correct = False

# n = 170141183460469231731687303715884105727
# correct = True

# n = 618970019642690137449562111
# correct = True

# This is not a Mersenne prime
# n = 5990103512870556906180584080180268237931650875781672937166634642761543
# correct = False

# result = primality_testing.lucas_lehmer_test(n)
# assert correct == result


# POCKLINGTON
# -----------

# n = 29
# divisor = None
# test_bound = 10
# correct = True

# may fail
# n = 27457
# divisor = 192
# test_bound = 10
# correct = True

# should not fail
# n = 27457
# divisor = 192
# test_bound = 200
# correct = True

# TEST
# result = primality_testing.pocklington_theorem_test(
#     n, divisor=divisor, test_bound=test_bound
# )
# if result is not None:
#     assert result == correct
# else:
#     print("None")


# AKS
# ---

# n = 29
# correct = True

# n = 569
# correct = True

# may take long time even for small values
# n = 3593
# correct = True

# TEST
# result = primality_testing.aks_test(n)
# assert result == correct


# ===================================================
#                       RSA
# ===================================================

# the protocol may fail sometimes because probabilistic primes
# generation is used in the key generation

# min_size_of_primes = 100
# max_size_of_primes = 1000

# Mind that for these values the key generation may take some time
# min_size_of_primes = 10**12
# max_size_of_primes = 10**13


# # ALICE
# public_key_ALICE, secret_key_ALICE = rsa.generate_key_pair(
#     min_size_of_primes, max_size_of_primes
# )

# # BOB
# public_key_BOB, secret_key_BOB = rsa.generate_key_pair(
#     min_size_of_primes, max_size_of_primes
# )

# print("\nKEYS GENERATION")
# print("===============")
# print(f"ALICE: public key = {public_key_ALICE}, secret_key = {secret_key_ALICE}")
# print(f"BOB: public key = {public_key_BOB}, secret_key = {secret_key_BOB}\n\n")

# print("SENDING OF m_1 (from Alice to Bob)")
# print("==================================\n")

# # Alice sends m_1 to Bob
# m_1 = 123
# m_1_encrypted = rsa.encrypt(m_1, public_key_BOB, public_key_ALICE, secret_key_ALICE)

# print(f"Alice writes m_1 = {m_1}. Encrypts it into (c_1, s_1) = {m_1_encrypted}.\n")

# # Bob receives m_1
# m_1_decrypted = rsa.decrypt(
#     m_1_encrypted, public_key_ALICE, public_key_BOB, secret_key_BOB
# )

# print(
#     f"Bob receives: (c_1, s_1) = {m_1_encrypted}. Decrypts it into m_1 = {m_1_decrypted}.\n\n"
# )

# print("SENDING OF m_2 (from Bob to Alice)")
# print("==================================\n")

# # Bob sends m_2 to Alice
# m_2 = 987
# m_2_encrypted = rsa.encrypt(m_2, public_key_ALICE, public_key_BOB, secret_key_BOB)

# print(f"Bob writes m_2 = {m_2}. Encrypts it into (c_2, s_2) = {m_2_encrypted}.\n")

# # Alice receives m_2
# m_2_decrypted = rsa.decrypt(
#     m_2_encrypted, public_key_BOB, public_key_ALICE, secret_key_ALICE
# )

# print(
#     f"Alice receives: (c_2, s_2) = {m_2_encrypted}. Decrypts it into m_2 = {m_2_decrypted}.\n"
# )


# EVE AND MALLORY

# this is the problem that the adversaries have to solve
# if they manage to find the primes used in the key generation of both users, they break the entire communication

# Mind that when testing, this may take a lot of time for large bounds for primes.
# We can use several factoring algorithms we have implemented

# n_A, _ = public_key_ALICE

# alice_primes = factorization.trial_division(n_A)
# alice_primes = factorization.pollard_rho_method(n_A)
# alice_primes = factorization.pollard_p_minus_1_method(n_A)
# alice_primes = factorization.squfof(n_A)
# print(alice_primes)

# n_B, _ = public_key_BOB

# bob_primes = factorization.trial_division(n_B)
# bob_primes = factorization.pollard_rho_method(n_B)
# bob_primes = factorization.pollard_p_minus_1_method(n_B)
# bob_primes = factorization.squfof(n_B)
# print(bob_primes)
