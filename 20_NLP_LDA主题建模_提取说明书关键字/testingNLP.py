# -*- coding: utf-8 -*-
"""
Created on Sun Mar 18 16:23:21 2018

"""
#PunktWordTokenizer/ImportError: cannot import name PunktWordTokenize
from nltk.tokenize import sent_tokenize,word_tokenize,WordPunctTokenizer,RegexpTokenizer

from nltk.stem.porter import PorterStemmer
from nltk.stem.lancaster import LancasterStemmer 
from nltk.stem.snowball import SnowballStemmer

from nltk.stem import WordNetLemmatizer

from sklearn.datasets import fetch_20newsgroups

from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfTransformer

import random
from nltk.corpus import names
from nltk import NaiveBayesClassifier
from nltk.classify import accuracy as nltk_accuracy

import nltk.classify.util
from nltk.corpus import movie_reviews

from gensim import models,corpora
from nltk.corpus import stopwords
'''
#import nltk
#nltk.download('punkt')
text="Are you curious about tokenization?Let's see how it works! we need to ananlyses a couple of sentences with punchtuations to see it in action."
sen_tokenize_list=sent_tokenize(text)
print(sen_tokenize_list)
print(word_tokenize(text))
#Punkt_Word_Tokenizer=PunktWordTokenizer()
#print(Punkt_Word_Tokenizer.tokenize(text))
word_punct_tokenizer=WordPunctTokenizer()
print(word_punct_tokenizer.tokenize(text))
'''
'''
words=['table','probably','wolves','playing','is','dog','the','beaches','grounded','dreamt','envision']
stemmers=['porter','lancaster','snowball']
stemmer_porter=PorterStemmer()
stemmer_lancaster=LancasterStemmer()
stemmer_snowball=SnowballStemmer('english')
formatted_row='{:>16}'*(len(stemmers)+1)
print(formatted_row.format('word', *stemmers))
#stemmer_word=[stemmer_porter.stem(word) for word in words]
for word in words:
    stemmed_words=[stemmer_porter.stem(word),stemmer_lancaster.stem(word),stemmer_snowball.stem(word)]
    print(formatted_row.format(word, *stemmed_words))
'''
'''
#import nltk
#nltk.download('wordnet')
words=['table','probably','wolves','playing','is','dog','the','beaches','grounded','dreamt','envision']
lemmatizers=['noun lemmatizer','verb lemmatizer']
lemmatizer_wordnet=WordNetLemmatizer()
formatted_row='{:>24}'*(len(lemmatizers)+1)
print(formatted_row.format('word', *lemmatizers))
for word in words:
    lemmatized_words=[lemmatizer_wordnet.lemmatize(word,pos='n'),lemmatizer_wordnet.lemmatize(word,pos='v')]
    print(formatted_row.format(word,*lemmatized_words))
'''

#import nltk
#nltk.download('brown')
def splitter(data,num_words):
    words=data.split(' ')
    output=[]
    cur_count=0
    cur_words=[]
    for word in words:
        cur_words.append(word)
        cur_count+=1
        if cur_count==num_words:
            output.append(' '.join(cur_words))
            cur_words=[]
            cur_count=0
    output.append(' '.join(cur_words))
    return output
'''

if __name__=='__main__':
    data=' '.join(brown.words()[:10000])
    num_words=1700
    chunks=[]
    counter=0
    text_chunks=splitter(data,num_words)
    print("number of text chunks=",len(text_chunks))
'''
import numpy as np
from nltk.corpus import brown
from sklearn.feature_extraction.text import CountVectorizer
def splitter(data,num_words):
    words=data.split(' ')
    output=[]
    cur_count=0
    cur_words=[]
    for word in words:
        cur_words.append(word)
        cur_count+=1
        if cur_count==num_words:
            output.append(' '.join(cur_words))
            cur_words=[]
            cur_count=0
    output.append(' '.join(cur_words))
    return output
if __name__=='__main__':
    data=' '.join(brown.words()[:10000]) #从布朗语料库中加载输入数据。
    num_words=2000
    chunks=[]
    counter=0
    text_chunks=splitter(data,num_words) #分块，每块数量为 num_words
    for text in text_chunks:  
        chunk={'index':counter,'text':text} #建立基于文本块的字典
        chunks.append(chunk)
        counter+=1
        
#    print(chunks)
    vectorizer=CountVectorizer(min_df=5,max_df=.95)  #使用scikit_learn库建立BOW单词频次(文档-词矩阵)
    doc_term_matrix=vectorizer.fit_transform([chunk['text'] for chunk in chunks])
    vocab=np.array(vectorizer.get_feature_names()) #从vectorizer模型对象中提取词汇
    print('vocabulary:',vocab)
    print("nDocument term matrix:")
    chunk_names=['Chunk-0','Chunk-1','Chunk-2','Chunk-3','Chunk-4']
    formatted_row='{:>12}'*(len(chunk_names)+1) #打印结果格式配置
    print(formatted_row.format('Word',*chunk_names))
    for word,item in zip(vocab,doc_term_matrix.T):
        output=[str(x) for x in item.data]
        print(formatted_row.format(word,*output)) #打印每个单词出现在不同块中的次数

'''
category_map={'misc.forsale':'Scales','rec.motorcycles':'Motorcycles','rec.sport.baseball':'Baseball','sci.crypt':'Cryptography','sci.space':'Space'}
training_data=fetch_20newsgroups(subset='train',categories=category_map.keys(),shuffle=True,random_state=7,download_if_missing=True)
vectorizer=CountVectorizer()
X_train_termcounts=vectorizer.fit_transform(training_data.data)
print("nDimentions of training data:",X_train_termcounts.shape)
input_data=["The curvaballs of ight handed pitchers tend to curve to the left","Caesar cipher is an ancient form of encryption","This two-wheeler is really good on slippery roads"]
tfidf_transformer=TfidfTransformer()
X_train_tfidf=tfidf_transformer.fit_transform(X_train_termcounts)
classifier=MultinomialNB().fit(X_train_tfidf,training_data.target)
X_input_termcounts=vectorizer.transform(input_data)
X_input_tfidf=tfidf_transformer.transform(X_input_termcounts)
predicted_categories=classifier.predict(X_input_tfidf)
for sentence,category in zip(input_data,predicted_categories):
    print("nInput:",sentence,"nPreddicted category:",category_map[training_data.target_names[category]])
'''

#import nltk
#nltk.download('names')
'''
def gender_features(word,num_letters=2):
    return{'feature':word[-num_letters:].lower()}
if __name__=='__main__':
    labeled_names=([(name,'male') for name in names.words('male.txt')]+[(name,'female') for name in names.words('female.txt')])
    random.seed(7)
    random.shuffle(labeled_names)
    input_names=['Leonardo','Amy','Sam']
    for i in range(1,5):
        print('nNumber of letters:',i)
        featuresets=[(gender_features(n,i),gender) for (n,gender) in labeled_names]
    train_set,test_set=featuresets[500:],featuresets[:500]
    classifier=NaiveBayesClassifier.train(train_set)
    print('Accuracy==>',str(100*nltk_accuracy(classifier,test_set))+str('%'))
    for name in input_names:
        print(name,'==>',classifier.classify(gender_features(name,i)))
'''
'''
#import nltk
#nltk.download('movie_reviews')   
def extract_features(word_list):
    return dict([(word,True) for word in word_list])
if __name__=='__main__':
    positive_fileids=movie_reviews.fileids('pos')
    negative_fileids=movie_reviews.fileids('neg')
    features_positive=[(extract_features(movie_reviews.words(fileids=[f])),'Positive') for f in positive_fileids]
    features_negative=[(extract_features(movie_reviews.words(fileids=[f])),'Negative') for f in negative_fileids]
    threshold_factor=0.8
    threshold_positive=int(threshold_factor*len(features_positive))
    threshold_negative=int(threshold_factor*len(features_negative))
    features_train=features_positive[:threshold_positive]+features_negative[:threshold_negative]
    features_test=features_positive[threshold_positive:]+features_negative[threshold_negative:]
    print("nNumber of training datapoints:",len(features_train))
    print("Number of test datapointss:",len(features_test))
    classifier=NaiveBayesClassifier.train(features_train)
    print("nAccuracy of the classifier:",nltk.classify.util.accuracy(classifier,features_test))
    print("nTop 10 most informative words:")
    for item in classifier.most_informative_features()[:10]:
        print(item[0])
        
    input_reviews=["It is an amzing movies","This is a dull movie.I would never recommand it to anyone.","The cinamatography is pretty great in this movie.","The direction was terrrible and the stroay was alll over the place."]
    print("nPredictions:")
    for review in input_reviews:
        print("nReview:",review)
        probdist=classifier.prob_classify(extract_features(review.split()))
        pred_sentiment=probdist.max()
        print("Predicted sentiment:",pred_sentiment)
        print("Probability:",round(probdist.prob(pred_sentiment),2))
'''
#import nltk
#nltk.download('stopwords')  
#def load_data(input_file):
#    data=[]
#    with open(input_file,'r') as f:
#        for line in f.readlines():
#            data.append(line[:-1])
#    return data
#class Preprocessor(object):
#    def __init__(self):
#        self.tokenizer=RegexpTokenizer(r'\w+')
#        self.stop_word_english=stopwords.words('english')
#        self.stemmer=SnowballStemmer('english')
#    def process(self,input_text):
#        tokens=self.tokenizer.tokenize(input_text.lower())
#        tokens_stopwords=[x for x in tokens if not x in self.stop_word_english]
#        tokens_stemmed=[self.stemmer.stem(x) for x in tokens_stopwords]
#        return tokens_stemmed
#if __name__=='__main__':
#    input_file=r'E:\MUBENAcademy\pythonSystem\Machine+Deep_learning\pythonmachinelearningcookbook\Chapter06\data_topic_modeling.txt'
#    data=load_data(input_file)
#    preprocessor=Preprocessor()
#    processed_tokens=[preprocessor.process(x) for x in data]
#    dict_tokens=corpora.Dictionary(processed_tokens)
#    corpus=[dict_tokens.doc2bow(text) for text in processed_tokens]
#    num_topics=2
#    num_words=4
#    ldamodel=models.ldamodel.LdaModel(corpus,num_topics=num_topics,id2word=dict_tokens,passes=25)
#    print("nMost contributing words to the topics:")
#    for item in ldamodel.print_topics(num_topics=num_topics,num_words=num_words):
#        print("nTopic",item[0],"==>",item[1])
#        
    

