# coding: utf-8
""" N-Gram 模型

- 原理:
  假设一个语言序列中某个元素(gram)出现的概率只与前 n-1 个元素的概率相关，语言序列是由多个 n元 的词组成。

- 实现:
  1. 构建语料库
  2. 分词: 把句子分成 N 个 'Gram'
  3. 计算每个 n-gram 在语料库中的词频
  4. 计算每个 n-gram 出现的概率
  5. 根据输入，通过不断预计最大出现概率的下一个元素形成连续文本

- 优缺点:
  - 优点: 模型简单
  - 缺点: 无法考虑长距离元素间的关系
"""
from collections import defaultdict, Counter

# 构建 demo 数据集
Corpus = [
    "我喜欢吃苹果",
    "我喜欢吃香蕉",
    "她喜欢吃葡萄",
    "他不喜欢吃香蕉",
    "他喜欢吃苹果",
    "她喜欢吃草莓"
]

N = 2  # 二元组


# 定义分词函数
def tokenize(text):
    return [char for char in text]


# 计算 N-Gram 词频
def count_n_grams(corpus, n):
    n_grams_counter = defaultdict(Counter)
    for text in corpus:
        tokens = tokenize(text)  # 分词
        for idx in range(len(tokens)-n+1):
            n_gram = tuple(text[idx: idx + n])  # 创建 n元组
            prefix = n_gram[:-1]
            token = n_gram[-1]
            n_grams_counter[prefix][token] += 1  # 统计前 n-1 为 prefix 时 token 出现的频率
    return n_grams_counter


bigrams_counts = count_n_grams(Corpus, N)
print("Bigrams 词频: ")
for prefix, counter in bigrams_counts.items():
    print("{}: {}".format(prefix, counter))


f4_grams_counts = count_n_grams(Corpus, 4)
print("F4grams 词频: ")
for prefix, counter in f4_grams_counts.items():
    print("{}: {}".format(prefix, counter))


# 统计 N-Gram 概率
def n_gram_probabilities(n_gram_counts):
    n_gram_probs = defaultdict(Counter)
    for prefix, counts in n_gram_counts.items():
        # 统计每个 token 在当前 prefix 下的总数
        total_count = sum(counts.values())
        for token, count in counts.items():
            n_gram_probs[prefix][token] = count/total_count
    return n_gram_probs


bigrams_probs = n_gram_probabilities(bigrams_counts)
print("\n Bigrams 概率: ")
for prefix, probs in bigrams_probs.items():
    print("{}: {}".format(prefix, probs))

f4grams_probs = n_gram_probabilities(f4_grams_counts)
print("\n F4grams_probs 概率: ")
for prefix, probs in f4grams_probs.items():
    print("{}: {}".format(prefix, probs))


# 根据前 N-1 获取下一个 token
def generate_next_token(prefix, n_gram_probs):
    # 前缀不在 N-Gram 中直接返回
    if not prefix in n_gram_probs:
        return None
    next_token_probs = n_gram_probs[prefix]
    next_token = max(next_token_probs, key=next_token_probs.get)  # 获取最大概率对应的 token
    return next_token


# 生成连续文本
def generate_text(prefix, n_gram_probs, n, length=8):
    tokens = list(prefix)
    for _ in range(length-len(prefix)):  # 需要生成的长度
        next_token = generate_next_token(tuple(tokens[-n+1:]), n_gram_probs)  # 生成下一个token
        if next_token is None:
            break
        tokens.append(next_token)
    return "".join(tokens)


# 输入前缀，生成文本
generated_text = generate_text("我", bigrams_probs, 2)
print("\n 生成文本: ", generated_text)
generated_text = generate_text("我喜欢", f4grams_probs, 4)
print("\n 生成文本: ", generated_text)
