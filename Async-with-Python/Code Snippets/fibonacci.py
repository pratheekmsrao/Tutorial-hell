from typing import List


# Simple function to calculate the fibonnaci number series of 'n' numbers
def fib(n: int) -> List[int]:
    numbers = []
    current, nxt = 0, 1
    while len(numbers) < n:
        current, nxt = nxt, current + nxt
        numbers.append(current)
    return numbers


print(fib(10))


# fibonacci function as a generator
def fib_as_generator():
    current, nxt = 0, 1
    while True:
        current, nxt = nxt, current + nxt
        yield current


# create a generator object
result = fib_as_generator()

# use the generator to get the fibinacci number which is less than 10000
for n in result:
    print(n, end=", ")
    if n > 10000:
        break
print()
print("Done")
