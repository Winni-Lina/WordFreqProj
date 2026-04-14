import pandas as pd
from konlpy.tag import Komoran
from collections import Counter
from wordcloud import WordCloud

# 1. 파일에서 데이터 읽어오기
def load_corpus_from_csv(filename, column):
    data_df = pd.read_csv(filename)
    
    if column in data_df.columns:
        data_df = data_df.dropna(subset=[column])
        corpus = list(data_df[column])
        return corpus
    
    return None

# 2. 문장에서 단어만 골라내기
def tokenize_data(corpus):
    komo = Komoran()
    my_tags = ['NNP', 'NNG', 'VA']
    my_stopwords = ['없', '같', '많', '영화', "!!"]

    result_tokens = []
    for text in corpus:
        pos_list = komo.pos(text)
        
        for word, tag in pos_list:
            if tag in my_tags:
                if word not in my_stopwords:
                    result_tokens.append(word)
                    
    return result_tokens

# 3. 단어 개수 세기
def analyze_word_freq(corpus):
    tokens = tokenize_data(corpus)
    counter = Counter(tokens)
    return counter

# 4. 워드클라우드 그림 그리기
def generate_wordcloud(counter, num_words, font_file):
    wc = WordCloud(
        font_path=font_file,
        width=800,
        height=600,
        max_words=num_words,
        background_color='white'
    )
    wc.generate_from_frequencies(counter)
    return wc