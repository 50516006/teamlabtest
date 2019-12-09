# -*- coding: utf-8 -*-

import random
import copy
import requests,json,time

gene_length = 50 #遺伝子の長さ=最大文字数50
individual_length = 15 #1世代の人口
generation = 999 #世代数。これは3時間のアクセス可能数の論理値を超えるためコンテスト中に処理が終わることはない
elite_rate = 0.2 #エリート率
token = "4MXDSzVToPJTwnRTZdvbYJBP4sx7uwXC" #トークン


#第一世代の遺伝子(文字列)をランダムに作成
def get_population():
    return [[random.choice(["A","B","C","D"]) for j in range(gene_length)] for i in range(individual_length)]




#各遺伝子の適応度=スコアの算出。また1秒のウェイトはここで行う。
def fitness(pop):
    url = "https://runner.team-lab.com/q?token={0}&str={1}".format(token,''.join(pop))
    result = requests.get(url)
    sc=int(json.loads(result.text))
    print(sc)
    time.sleep(1)
    return sc
#評価、スコア順に並び替える。
def evaluate(pop):
    pop.sort(reverse=True)
    return pop



#二点交叉による次世代の作成
def two_point_crossover(parent1, parent2):
    
    r1 = random.randint(0, gene_length-1)#親2の始点
    r2 = random.randint(r1, gene_length-1)#親2の終点
    child = copy.deepcopy(parent1)#親1の遺伝子を深いコピー
    child[r1:r2] = parent2[r1:r2]#親2の遺伝子の対応範囲を深いコピー
    return child

#突然変異
def mutate(parent):
    child = copy.deepcopy(parent)
    for i in range(random.randint(0,49)):
        r = random.randint(0, gene_length-1)

        child[r] =random.choice(['A',"B","C","D"])
    return child




def main():

    mutate_rate = 0.4 # 突然変異の確率、袋小路に入りやすいので大きめに

    pop = evaluate([(fitness(p), p) for p in get_population()])#第一世代
    print('0-Max : {}'.format(pop[0][0]))

    for g in range(generation):

        # エリートの抽出
        eva = evaluate(pop)
        elites = eva[:int(len(pop)*elite_rate)]

        # 突然変異、交叉
        pop = elites #エリートのみ浅いコピー
        while len(pop) < individual_length:#個体数が規定に届くまで次世代の作成
            if random.random() < mutate_rate:#突然変異：1個体追加
                m = random.randint(0, len(elites)-1)#突然変異遺伝子の選択
                child = mutate(elites[m][1])#突然変異遺伝子を子孫に指定
            else:#交叉：1個体作成
                m1 = random.randint(0, len(elites)-1)#親となる遺伝子の選択
                m2 = random.randint(0, len(elites)-1)#親となる遺伝子の選択
                child = two_point_crossover(elites[m1][1], elites[m2][1])#交叉の実行
            pop.append((fitness(child), child))#次世代に追加

        # 評価
        eva = evaluate(pop)
        pop = eva


        print('{0}-Max : {1}'.format(g+1,pop[0][0]))#ベスト遺伝子のスコアを表示




if __name__ == '__main__':
    main()