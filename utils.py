# -*- coding: utf-8 -*-
"""
# © 07/20/2020 by ZihaoDONG, ALL RIGHTS RESERVED
# File name: utils.py
# This project is an upgrade version of @zhanzecheng's Project
# Replaced list with dict, significantly boosting searching and insertion time
"""
import pickle
import re

def get_stopwords():
    with open('data/stopword.txt', 'r', encoding='utf-8') as f:
        stopword = [line.strip() for line in f]
    return set(stopword)


def generate_ngram(input_list, n):
    result = []
    new_list = []
    for item in input_list:
        new_item = re.sub('\d+',' ',str(item).strip())    # "strip" meaningless words
        new_item = re.sub("[^\u4e00-\u9fa5]+", '',new_item)
        new_list.append(new_item)
    filtered_list = [x for x in new_list if x and x not in ['', ' ', '\t', '\n']]
    for i in range(1, n+1):
        result.extend(zip(*[filtered_list[j:] for j in range(i)]))
    return result


def load_dictionary(filename):
    """
    Load external dictionary
    :param filename:
    :return:
    """
    word_freq = {}
    print('------> Loading External Dictionary')
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                line_list = line.strip().split(' ')
                # Word_freq min threshold
                if int(line_list[1]) > 2:
                    word_freq[line_list[0]] = line_list[1]
            except IndexError as e:
                print(line)
                continue
    return word_freq


def save_model(model, filename):
    with open(filename, 'wb') as fw:
        pickle.dump(model, fw)


def load_model(filename):
    with open(filename, 'rb') as fr:
        model = pickle.load(fr)
    return model
