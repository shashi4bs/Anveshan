import math

class BM25(object):
    def __init__(self, corpus, k1=1.5, b=0.75, epsilon=0.25):
        self.k1 = k1
        self.b = b
        self.epsilon = epsilon
        self.corpus_size = len(corpus)
        self.avgdl = 0
        self.doc_freq = []
        self.idf = {}
        self.doc_len = []

        nd = self._initialize(corpus)
        self._calc_idf(nd)


    def _initialize(self, corpus):
        nd = {}
        num_doc = 0
        for document in corpus:
            self.doc_len.append(len(document))
            num_doc += len(document)
            frequencies = {}

            for word in document:
                if word not in frequencies:
                    frequencies[word] = 0
                frequencies[word] += 1

            self.doc_freq.append(frequencies)
            
            for word, freq in frequencies.items():
                if word not in nd:
                    nd[word] = 0
                else:
                    nd[word] += 1

        self.avgdl = num_doc / self.corpus_size
        return nd

    def _calc_idf(self, nd):
        idf_sum = 0
        negative_idfs = []

        for word, freq in nd.items():
            idf = math.log(self.corpus_size - freq + 0.5) - math.log(freq + 0.5)
            self.idf[word] = idf
            idf_sum += idf
            
            if idf < 0:
                negative_idfs.append(word)
        self.average_idf = idf_sum / len(self.idf)

        eps = self.epsilon * self.average_idf
        for word in negative_idfs:
            self.idf[word] = eps

    def get_scores(self, query):
        score = np.zeros(self.corpus_size)
        doc_len = np.array(self.doc_len)
        for q in query:
            q_freq = np.array([(doc.get(q) or 0 ) for doc in self.doc_freq])
            score += (self.idf.get(q) or 0) * \
                    (q_freq * (self.k1 + 1)/ \
                    (q_freq + self.k1 * (1 - self.b + self.b * doc_len / self.avgdl)))

        return score

    def get_top_n(self, query, urls, n=5):
        scores = self.get_scores(query)
        top_n = np.argsort(scores)[::-1][:n]
        return [urls[i] for i in top_n]
