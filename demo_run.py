# -*- coding: utf-8 -*-
"""
# © 07/20/2020 by ZihaoDONG, ALL RIGHTS RESERVED
# File name: demo_run.py
# This project is an upgrade version of @zhanzecheng's Project
# Replaced list with dict, significantly boosting searching and insertion time
"""

import os
import jieba
from model import TrieNode
from utils import get_stopwords, load_dictionary, generate_ngram, save_model, load_model
from config import basedir
import jieba.posseg as peg
import threading
from multiprocessing import Process

def load_data(filename, stopwords):
    """

    :param filename:
    :param stopwords:
    :return: 二维数组,[[句子1分词list], [句子2分词list],...,[句子n分词list]]
    """
    data = []
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f.readlines():
            word_list = [x for x in jieba.cut(line.strip(), cut_all=False) if x not in stopwords]
            if word_list:
                data.append(word_list)
    return data


def load_data_2_root(data):
    print('------> 插入节点')
    for word_list in data:
        # tmp 表示每一行自由组合后的结果（n gram）
        # tmp: [['它'], ['是'], ['小'], ['狗'], ['它', '是'], ['是', '小'], ['小', '狗'], ['它', '是', '小'], ['是', '小', '狗']]
        ngrams = generate_ngram(word_list, 3)
        print(ngrams)
        for d in ngrams:
            root.add(d)
    print('------> 插入成功')


def load(filename, stopwords):
    load_data_2_root(load_data(filename, stopwords))


def func(demopath, add_word_path, wordFreq_path, wordFreq_sorted_path):

    # 加载新的文章
    filename1 = demopath
    # filename2 = 'data/demo2.txt'
    data = load_data(filename1, stopwords)
    # 将新的文章插入到Root中
    # mid = len(data)//2
    # first_half = data[0:mid]
    # second_half = data[mid:len(data)]
    # processes = []
    # p1 = Process(target=load_data_2_root, args=(first_half))
    # processes.append(p1)
    # p2 = Process(target=load_data_2_root, args=(second_half))
    # processes.append(p2)
    # t1.start()
    # print("t1 has started...")
    # t2.start()
    # print("t2 has started...")
    # index = 1
    # for p in processes:
    #     # p.setDaemon(True)
    #     print(f"Process {index} starts...\n")
    #     index += 1
    #     p.start()
    # p.join()

    load_data_2_root(data)

    # 定义取TOP5000个
    topN = 5000
    result, add_word = root.find_word(topN)
    add_word = dict(sorted(add_word.items(), key=lambda x: x[1], reverse=True))
    filepath = add_word_path
    with open(filepath, 'w', encoding='utf-8') as fw:
        for word in add_word.keys():
            print(word + ': ' + str(add_word[word]))
            fw.write(word + ': ' + str(add_word[word]) + '\n')
            jieba.add_word(word)
        with open(demopath, 'r', encoding='utf-8') as f:
            txt = ''
            for line in f.readlines():
                txt = txt + line.strip()
            res = peg.cut(txt)
            words = []
            for word, Type in res:
                if Type in ['n','nz','v','vn','x','nr']:
                    words.append(word)
            word_freq = {}
            for word in words:
                word_freq[word] = word_freq.get(word, 0) + 1

            fw1 = open(wordFreq_path, 'w', encoding='utf-8')
            for item_name, item_freq in word_freq.items():
                fw1.write(item_name + ': ' + str(item_freq) + '\n')

            word_freq_sorted = dict(sorted(word_freq.items(), key=lambda x: x[1], reverse=True))
            fw2 = open(wordFreq_sorted_path, 'w', encoding='utf-8')
            for name, freq in word_freq_sorted.items():
                fw2.write(name + ": " + str(freq) + '\n')

            fw1.close()
            fw2.close()

if __name__ == "__main__":
    root_name = basedir + "/data/root.pkl"
    stopwords = get_stopwords()
    if os.path.exists(root_name):
        root = load_model(root_name)
    else:
        dict_name = basedir + '/data/dict.txt'
        word_freq = load_dictionary(dict_name)
        root = TrieNode('*', word_freq)
        save_model(root, root_name)


    #choose and modify paths below
    func('data/demo_bid_data.txt', 'data/add_word_bid_data.txt', 'data/wordFreq_bid_data.txt', 'data/wordFreq_sorted_bid_data.txt')
    print("finished 1st run...")

    func('data/demo_bid_data.txt', 'data/add_word_bid_data_3To5.txt', 'data/wordFreq_bid_data_3To5.txt', 'data/wordFreq_sorted_bid_data_3To5.txt')
    # 2nd run will help find out new words composed of 3-5 words.

    # import cProfile
    # cProfile.run("func()", filename="cpresult.out", sort="cumulative")
    #
    # import pstats
    # p = pstats.Stats("cpresult.out")
    # p.strip_dirs().sort_stats("cumulative", "name").print_stats(0.5)
            # fw.write("".join([(x + '/ ') for x in jieba.cut(txt, cut_all=False) if x not in stopwords]))
    # 如果想要调试和选择其他的阈值，可以print result来调整
    # print("\n----\n", result)
    # print("\n----\n", '增加了 %d 个新词, 词语和得分分别为: \n' % len(add_word))
    # print('#############################')
    # for word, score in add_word.items():
    #     print(word + ' ---->  ', score)
    # print('#############################')

    # 前后效果对比
    # test_sentence = '蔡英文在昨天应民进党当局的邀请，准备和陈时中一道前往世界卫生大会，和谈有关九二共识问题'
    # print('添加前：')
    # print("".join([(x + '/ ') for x in jieba.cut(test_sentence, cut_all=False) if x not in stopwords]))
    #
    # for word in add_word.keys():
    #     jieba.add_word(word)
    # print("添加后：")
    # print("".join([(x + '/ ') for x in jieba.cut(test_sentence, cut_all=False) if x not in stopwords]))
