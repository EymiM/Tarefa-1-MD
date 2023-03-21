import time
import os

start_time = time.time()

A = (1, 2, 3, 4, 5)

def generate_relations(A):
    n = len(A)
    with open('relations.txt', 'w') as file:
        for i in range(2 ** (n * n)):
            relation = set()
            for j in range(n):
                for k in range(n):
                    if (i >> (j*n) + k) & 1:
                        relation.add((A[j], A[k]))
            if len(relation) == 0:
                file.write('{} ' + classify_relation(relation, A) + '\n')
            else:
                file.write(str(relation) + ' ' + classify_relation(relation, A) + '\n')


def classify_relation(relation, A):

    symmetric = True
    transitive = True
    reflexive = True
    equivalence = False

    # verifica simetria e transitividade
    for x, y in relation:
        if (y, x) not in relation:
            symmetric = False
            break
        for z, w in relation:
            if y == z and (x, w) not in relation:
                transitive = False
                break
 
    # verifica reflexividade
    for a in A:
        if (a, a) not in relation:
            reflexive = False
            break
    
    # verifica equivalência
    if reflexive and symmetric and transitive:
        equivalence = True
    
    # verifica irreflexividade
    irreflexive = True
    for a in A:
        if (a, a) in relation:
            irreflexive = False
            break
    
    classification = ''

    if equivalence:
        classification += "STRE"
    else:
        if symmetric:
            classification = "S"
        if transitive:
            classification += "T"

        if reflexive:
            classification += "R"

    if irreflexive:
        classification += "I"
    
    # verifica se é função
    if len(relation) < 2:
        return classification
    else:
        for x, y in relation:
            for z, w in relation:
                if x == z and y != w:
                    return classification
    
    function_bij = True
    function_surj = True
    function_inj = True

    # segue para verficição do tipo de função, apenas se for função

    range_values = set([y for x, y in relation])
    if len(range_values) != len(A):
        function_bij = False
    else:
        for a in A:
            count = 0
            for x, y in relation:
                if y == a:
                    count += 1
            if count != 1:
                function_bij = False
                break
    if range_values != set(A):
        function_surj = False

    domain_values = set([x for x, y in relation])
    if len(domain_values) != len(A):
        function_inj = False
    else:
        for y in set([y for x, y in relation]):
            count = 0
            for x, z in relation:
                if y == z:
                    count += 1
            if count != 1:
                function_inj = False
                break

    # classifica a relação
    
    classification += "Fu"

    if function_bij:
        classification += "Fb"

    if function_surj:
        classification += "Fs"

    if function_inj:
        classification += "Fi"
    
    return classification

generate_relations(A)

end_time = time.time()
total_time = end_time - start_time
print(f"Tempo total de execução: {total_time} segundos")

size = os.path.getsize("relations.txt")
print(f"Tamanho do arquivo: {size} bytes")