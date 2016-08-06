from random import randint

# The Dining Cryptographers Problem

# Problem: how to perform a secure multi-party computation of the
# boolean OR function
# Source: https://en.wikipedia.org/wiki/Dining_cryptographers_problem

def gen_random():
    return randint(0, 1)

def gen_edge(pos, n):
    return {"position": pos, "next": n, "secret": gen_random()}

def create_cryptographers_graph(n):
    graph = []
    graph.append(gen_edge(n-1, n-2)) # easier if everything is zero-indexed
    return _create_cryptographers_graph(graph, n-2, n-1)

def _create_cryptographers_graph(graph, counter, final):
    if counter == 0:
        graph.append(gen_edge(counter, final))
        return graph
    graph.append(gen_edge(counter, counter-1))
    return _create_cryptographers_graph(graph, counter-1, final)

def xor(a, b):
    return a ^ b

def opposite_xor(a, b):
    x = xor(a, b)
    return xor(x, 1) # xoring by 1 returns the opposite of the original number, if the set is limited to 0 or 1

def get_status(left, right, paid):
    if left["position"] == paid:
        return opposite_xor(left["secret"], right["secret"])
    return xor(left["secret"], right["secret"])

# if the cryptographer didn't pay for the meal, they will announce the XOR of
# the shared secrets they hold with their two neighbors
# if they did pay, they announce the opposite of that XOR
# final result is created by xoring all announcements together
def announce(cryptographers, paid):
    final = 0
    for c in cryptographers:
        _next = cryptographers[c["next"]]
        announcement = get_status(c, _next, paid)
        final = xor(final, announcement)
    return final

cryptographers = create_cryptographers_graph(5)

paying_cryptographer_position = 2
result = announce(cryptographers, paying_cryptographer_position)
print "when a cryptographer pays, the final status is: ", result

paying_nsa_position = 6 # out of range of the list of possible cryptographers who can pay
nsa_result = announce(cryptographers, paying_nsa_position)
print "when the nsa pays, the final status is: ", nsa_result
