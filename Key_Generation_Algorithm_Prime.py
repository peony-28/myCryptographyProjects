import random 

# Function to check if a number is prime 
def is_prime(num): 
    if num <= 1: 
        return False 
    for i in range(2, int(num**0.5) + 1): 
        if num % i == 0: 
            return False 
    return True 

# Function to generate a list of prime numbers in a given range 
def generate_primes(lower, upper): 
    primes = [] 
    for num in range(lower, upper + 1): 
        if is_prime(num): 
            primes.append(num) 
    return primes 

# Function to select two distinct primes 
def select_two_primes(primes): 
    p = random.choice(primes) 
    q = random.choice(primes) 
    while p == q: 
        q = random.choice(primes) 
    return p, q 

# Execution 
lower_bound = 10 
upper_bound = 100 
primes = generate_primes(lower_bound, upper_bound) 
p, q = select_two_primes(primes) 
print(f"Selected primes: p = {p}, q = {q}")
