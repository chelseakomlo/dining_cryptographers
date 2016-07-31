from random import randint

# The dining cryptographers problem

# Problem: how to perform a secure multi-party computation of the
# boolean OR function

# source: https://en.wikipedia.org/wiki/Dining_cryptographers_problem

def gen_random():
    return randint(0, 1)

def gen_edge(left, right):
    return {"left": left, "right": right, "secret": gen_random()}

def create_cryptographers_graph(edges, n):
    edges.append(gen_edge(n, n-1))
    return _create_cryptographers_graph(edges, n-1, n)

def _create_cryptographers_graph(edges, counter, final):
    if counter == 1:
        edges.append(gen_edge(counter, final))
        return edges
    edges.append(gen_edge(counter, counter-1))
    return _create_cryptographers_graph(edges, counter-1, final)

def xor(a, b):
    return a ^ b

def opposite_xor(a, b):
    x = xor(a, b)
    return 0 if x == 1 else 1

# if the cryptographer didn't pay for the meal, they will announce the XOR of
# the two shared bits they hold with their two neighbors
# if they did pay, they announce the opposite of that XOR
def announce(cryptographers, paid):
    results = []
    for i in cryptographers:
        if i["left"] == paid: results.append(opposite_xor(i["left"], i["right"]))
        results.append(xor(i["left"], i["right"]))
    return results

def get_final_status(results):
    final = 0
    for i in results: final = xor(final, i)
    return final

cryptographers = create_cryptographers_graph([], 5)

results = announce(cryptographers, 2)
print "when a cryptographer pays, the final status is: ", get_final_status(results)
nsa_results = announce(cryptographers, 6)
print "when the nsa pays, the final status is: ", get_final_status(nsa_results)