import flask
from flask import Flask, jsonify, request
from flask_cors import CORS
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest
from collections import Counter
from sumy.parsers.plaintext import PlaintextParser
from sumy.summarizers.lsa import LsaSummarizer
from sumy.nlp.tokenizers import Tokenizer
from sumy.utils import get_stop_words
import math
from newspaper import Article
from textblob import TextBlob
import requests
from bs4 import BeautifulSoup
from deep_translator import MyMemoryTranslator

app = Flask(__name__)
CORS(app)

import nltk
nltk.download('punkt')

lang_dict = {
    'English': 'en',
    'French': 'fr',
    'Spanish': 'es',
    'German': 'de',
    'Italian': 'it',
    'Russian': 'ru',
    'Japanese': 'ja',
    'Hindi': 'hi'
}

# Post Processing techniques
def post_process_summary(summary):
    if not summary:
        return summary
    summary = summary\
        .replace('\xa0', ' ')\
            .strip('.,!?' )[0]\
                .upper() + summary[1:] + '.' if summary[-1] not in '.!?' \
                    else summary[0].upper() + summary[1:]   
    return summary

# Summarization algorithm using spacy
def summarize_using_spacy(text, number_of_sentences):
    nlp = spacy.load('en_core_web_md')
    doc= nlp(text)

    # Token Filtering
    keyword = []
    stopwords = list(STOP_WORDS)
    pos_tag = ['PROPN', 'ADJ', 'NOUN', 'VERB']
    for token in doc:
        if(token.text in stopwords or token.text in punctuation):
            continue
        if(token.pos_ in pos_tag):
            keyword.append(token.text)
    freq_word = Counter(keyword)

    # Normalization
    if len(Counter(keyword)):
        max_freq = Counter(keyword).most_common(1)[0][1]
        for word in freq_word.keys():  
                freq_word[word] = (freq_word[word]/max_freq)
    
    # Weighing Sentences
    sent_strength={}
    for sent in doc.sents:
        for word in sent:
            if word.text in freq_word.keys():
                if sent in sent_strength.keys():
                    sent_strength[sent]+=freq_word[word.text]
                else:
                    sent_strength[sent]=freq_word[word.text]

    summarized_sentences = nlargest(number_of_sentences, sent_strength, key=sent_strength.get)

    final_sentences = [ w.text for w in summarized_sentences ]
    summary = ' '.join(final_sentences)

    # Get top-5 tags
    tags = [tag for tag, _ in freq_word.most_common(5)]
    return post_process_summary(summary), tags

#Summarization using Sumy
def summarize_using_sumy(text, number_of_sentences):
    LANGUAGE = "english"
    parser = PlaintextParser.from_string(text, Tokenizer(LANGUAGE))
    summarizer = LsaSummarizer()
    summarizer.stop_words = get_stop_words(LANGUAGE)
    summarized_sentences = summarizer(parser.document, number_of_sentences)
    summary = ' '.join([str(sentence) for sentence in summarized_sentences])
    return post_process_summary(summary)

def ensemble_summarization(text, count, sumy_weight=0.8, spacy_weight=0.2):
    spacy_sentences =int(math.ceil(count * spacy_weight))
    sumy_sentences = count - spacy_sentences
    # Spacy summarizer
    spacy_summary, top_5_tags = summarize_using_spacy(text, spacy_sentences)
    # Sumy summarizer
    sumy_summary = summarize_using_sumy(text, sumy_sentences)

    combined_summary = sumy_summary + ' ' + spacy_summary
    return post_process_summary(combined_summary), top_5_tags


# Sentiment Analysis of the text
def get_sentiment(text):
    nlp = spacy.load('en_core_web_md')
    doc = nlp(text)
    sentences = [sent.text for sent in doc.sents]
    polarity = 0.0
    subjectivity = 0.0
    for sentence in sentences:
        blob = TextBlob(sentence)
        polarity += blob.sentiment.polarity
        subjectivity += blob.sentiment.subjectivity
    num_sentences = len(sentences)
    avg_polarity = polarity / num_sentences
    avg_subjectivity = subjectivity / num_sentences

    return get_sentiment_scale(avg_polarity), get_subjectivity_scale(avg_subjectivity)

def get_sentiment_scale(avg_polarity):
    if avg_polarity >= 0.2:
        return 1                    # Positive
    elif avg_polarity >= 0:
        return 0                    # Neutral
    else: 
        return -1                   # Negative

def get_subjectivity_scale(avg_subjectivity):
    if avg_subjectivity < 0.4:
        return 1                    # objective
    elif avg_subjectivity < 0.6:
        return 0                    # Neutral
    else: 
        return -1                   # subjective


def generate_citations(website_url):
    metadata = get_metadata_information(website_url)
    citation_parts = []

    if metadata.get("author"):
        citation_parts.append(metadata["author"])

    if metadata.get("date_published"):
        citation_parts.append(f"({metadata['date_published']})")

    if metadata.get("title"):
        citation_parts.append(metadata["title"])

    citation_parts.append(website_url)

    citation = ". ".join(citation_parts)
    return citation

def get_metadata_information(website_url):
    response = requests.get(website_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    title_tag = soup.find('title')
    if title_tag:
        title = title_tag.text.strip()
    else:
        title_tag = soup.find('h1', {'class': 'title'})
        title = title_tag.text.strip() if title_tag else ""

    author_tag = soup.find('meta', {'name': 'author'})
    if author_tag:
        author = author_tag.get('content')
    else:
        author_tag = soup.find('span', {'class': 'author'}) or soup.find('div', {'class': 'author'})
        author = author_tag.text if author_tag else ""
    
    date_published_tag = soup.find('meta', {'property': 'article:published_time'})
    if date_published_tag:
        date_published = date_published_tag.get('content').strip()
    else:
        date_published_tag = soup.find('time', {'class': 'published'})
        date_published = date_published_tag.get('datetime').strip() if date_published_tag else ""

    metadata = {
        "title": title,
        "author": author,
        "website_url": website_url,
        "date_published": date_published
    }
    return metadata

def perform_text_translation(text, source_lang, destination_lang, batch_size=400):
    source_lang_key = lang_dict[source_lang]
    target_lang_key= lang_dict[destination_lang]
    translator = MyMemoryTranslator(source=source_lang_key, target=target_lang_key)

    # Split the text into batches of size batch_size
    num_batches = math.ceil(len(text) / batch_size)
    batches = [text[i*batch_size:(i+1)*batch_size] for i in range(num_batches)]

    # Translate each batch and concatenate the results
    translated_batches = []
    for batch in batches:
        translated_batch = translator.translate(batch)
        translated_batches.append(translated_batch)
    translated_text = ''.join(translated_batches)

    return translated_text

@app.route('/summarize', methods=['POST'])
def example_api():
    data = request.json
    website_url = data['message']
    numSentences = data.get('numSentences', 2)  # Get the number of sentences from the request data
    numSentences = max(1, int(numSentences))  # Ensure numSentences is at least 1
    target_lang = data['targetLang']
    try:
        article = Article(website_url)
        article.download()
        article.parse()
        text = article.text
    except requests.exceptions.RequestException as e:
        print("FAILURE EXCEPTION HIT: ", e)
        text = ""
    if text == "":
        response = requests.get(website_url)
        soup = BeautifulSoup(response.content, 'html.parser')
        main_content = soup.find('div', {'class': 'main-content'})
        if main_content:
            text = main_content.get_text()
            text = ' '.join(text.split())
    
        if text == "":
            text = soup.body.get_text(separator=' ')

        if text == "":
            return None
    citation = generate_citations(website_url)
    summary, tags = ensemble_summarization(text, numSentences)  # Use the numSentences value when calling the summarize function
    polarity, subjectivity = get_sentiment(text)
    if target_lang:
        translated_summary = perform_text_translation(summary, 'English', target_lang)
    response_data = {
        'summary': translated_summary if target_lang else summary, 
        'tags': tags, 
        'sentiment': polarity, 
        'subjectivity': subjectivity,
        'citation': citation
    }
    return jsonify(response_data)

if __name__ == '__main__':
    app.run(host='localhost', port=8000)
