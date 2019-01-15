# NLP-自然语言处理
![](https://github.com/richieBao/python-urbanPlanning/blob/master/images/959.png)
* 标记解析：例如将一段文字分割成单词或句子，即有意义的片段。
* 词干提取/词形还原：将不同词形的单词转为其原形。例如plays player playing到play，wolves到wolf。
* 文本分块：如果需要处理较大文本文档时，需要对文本分块，以便进一步分析。分块不需要有实际意义。

**BOW词袋模型**
```python
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
```
## 结果
![](https://github.com/richieBao/python-urbanPlanning/blob/master/images/960.png)

创建文本分类器。配合词频-逆向文件频率（tf-idf）/from sklearn.feature_extraction.text import TfidfTransformer的语料向量化，此工具有助于理解一个单词在一组文档中对某一文档的重要性。配合使用朴素贝叶斯分类器/from sklearn.naive_bayes import MultinomialNB 训练tf-idf向量数据。
