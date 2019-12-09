import random
import copy
import requests,json,time
from statistics import stdev

gene_length = 50 
individual_length = 15 
generation = 999 
elite_rate = 0.2 
token = "4MXDSzVToPJTwnRTZdvbYJBP4sx7uwXC"
def get_population():
    population = []
    for i in range(individual_length):
        population.append([random.choice(["A","B","C","D"]) for j in range(gene_length)])
    return population

def fitness(pop):

    url = "https://runner.team-lab.com/q?token={0}&str={1}".format(token,''.join(pop))
    result = requests.get(url)
    sc=int(json.loads(result.text))
    print(sc)
    time.sleep(1)
    return sc

def two_point_crossover(parent1, parent2):
    r1 = random.randint(0, gene_length-1)
    r2 = random.randint(r1, gene_length-1)
    child = copy.deepcopy(parent1)
    child[r1:r2] = parent2[r1:r2]
    return child


def mutate(parent):
    child = copy.deepcopy(parent)
    for i in range(random.randint(0,49)):
        r = random.randint(0, gene_length-1)

        child[r] =random.choice(['A',"B","C","D"])
    return child

def evaluate(pop):
    pop.sort(reverse=True)
    return pop


def main():
    # 初期個体生成
    mutate_rate = 0.4 # 突然変異の確率
    pop = evaluate([(fitness(p), p) for p in get_population()])
    print('Generation: 0')
    print('Min : {}'.format(pop[-1][0]))
    print('Max : {}'.format(pop[0][0]))
    print('--------------------------')

    for g in range(generation):
        print('Generation: ' + str(g+1))

        # エリートを選択
        eva = evaluate(pop)
        elites = eva[:int(len(pop)*elite_rate)]

        # 突然変異、交叉
        pop = elites
        while len(pop) < individual_length:
            if random.random() < mutate_rate:
                m = random.randint(0, len(elites)-1)
                child = mutate(elites[m][1])
            else:
                m1 = random.randint(0, len(elites)-1)
                m2 = random.randint(0, len(elites)-1)
                child = two_point_crossover(elites[m1][1], elites[m2][1])
            pop.append((fitness(child), child))

        # 評価
        eva = evaluate(pop)
        pop = eva

        print('Min : {}'.format(pop[-1][0]))
        print('Max : {}'.format(pop[0][0]))
        print('--------------------------')
    print('Result : {}'.format(pop[0]))


if __name__ == '__main__':
    main()