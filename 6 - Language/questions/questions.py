import nltk
import sys
import os 
import string
import math

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens
    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    files = dict()
    for filename in os.listdir(directory):
        if not filename.endswith(".txt"):
            continue
        with open(os.path.join(directory, filename)) as f:
            files[filename] = f.read()
    return files
    
def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    return [ word.lower() for word in nltk.word_tokenize(document) 
             if word not in string.punctuation and word.lower() not in nltk.corpus.stopwords.words("english")]

def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    idfs = dict()
    for file in documents:
        for word in documents[file]:
            if word in idfs:
                continue
            f = sum(word in documents[file] for file in documents)
            idfs[word] = math.log(len(documents) / f)
            
    return idfs            

def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """        
    # dictionary to store a score for each file 
    tfidf = dict()
    
    for word in query:
        if word not in idfs:
            continue
        # for each file calculate a score based on tfidf of words in the query
        for filename in files:     
            if  filename not in tfidf:     
                tfidf[filename] = files[filename].count(word) * idfs[word]
            else:
                tfidf[filename] += files[filename].count(word) * idfs[word]
    # Sort and get n top files that match the query ranked according to tf-idf.
    sorted_scores = sorted([filename for filename in files], key=lambda x:tfidf[x], reverse=True) 
    
    return sorted_scores[:n]

def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    # Dict to score sentences score
    top = {sentence:{'idf_score': 0, 'qtd_score':0} for sentence in sentences}
    # Iterate through sentences:
    for sentence in sentences:
        for word in query:
            # Sentences ranked according to “matching word measure”
            if word in sentences[sentence]:
                    top[sentence]["idf_score"] += idfs[word]
        # ranking according “query term density”
        top[sentence]["qtd_score"] = sum(w in query for w in sentences[sentence]) / len(sentences[sentence])
    # Sentences ordered with the best match first acording to “matching word measure” & “query term density”
    sorted_sentences = sorted([sentence for sentence in sentences], key=lambda x:(top[x]['idf_score'], top[x]['qtd_score']), reverse=True) 
    # return a list of the n top sentences
    return sorted_sentences[:n]
    
if __name__ == "__main__":
    main()