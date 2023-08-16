from summarizer import ensemble_summarization
import nltk
from nltk.translate.bleu_score import sentence_bleu
from rouge import Rouge

# Sample Article
article = "Machine learning (ML) is the scientific study of algorithms and statistical models that computer systems use to progressively improve their performance on a specific task. Machine learning algorithms build a mathematical model of sample data, known as 'training data', in order to make predictions or decisions without being explicitly programmed to perform the task. Machine learning algorithms are used in the applications of email filtering, detection of network intruders, and computer vision, where it is infeasible to develop an algorithm of specific instructions for performing the task. Machine learning is closely related to computational statistics, which focuses on making predictions using computers. The study of mathematical optimization delivers methods, theory and application domains to the field of machine learning. Data mining is a field of study within machine learning, and focuses on exploratory data analysis through unsupervised learning.In its application across business problems, machine learning is also referred to as predictive analytics."
reference_summaries = [
        "The article explains that machine learning is the study of algorithms and statistical models that help computer systems improve their performance on specific tasks without being explicitly programmed. It mentions that machine learning algorithms are useful in various fields such as email filtering, network intrusion detection, and computer vision, where it is difficult to create specific instructions for performing tasks. The article also notes that machine learning is related to computational statistics and data mining and is commonly referred to as predictive analytics in the business world"
        ,"The article discusses machine learning, which is the scientific study of algorithms and statistical models used by computer systems to improve their performance on specific tasks. These algorithms build mathematical models of sample data to make decisions without being explicitly programmed. Machine learning is used in areas like email filtering, network intrusion detection, and computer vision, where specific instructions are difficult to develop. It is closely related to computational statistics and data mining, and in business, it is often called predictive analytics.",
        "Machine learning also known by predictive analysis, has varied applications in terms of data science, statistical learning or mathematical optimization. Statistical learning involves data concerning a set of algorithms to take a specific decisions with the necessity to program. Data science and mathematical optimizations are more application-based. They imitate the functioning of a human brain.",
        "Machine learning is a subdomain of artificial intelligence in which algorithms build models based on training data in order to make predictions or decisions. They acquire knowledge by extracting patterns from raw data. These algorithms are used in a variety of applications, including medicine, email filtering, speech recognition, agriculture, and computer vision. ML algorithms use data and neural networks to mimic the operation of a biological brain."
    ]
generated_summary = ensemble_summarization(article, 3)[0]

# BLEU score
reference_tokens = [summary.split() for summary in reference_summaries]
generated_tokens = generated_summary.split()
bleu_score = sentence_bleu(reference_tokens, generated_tokens)
print(f"BLEU score: {bleu_score:.2f}")
# 0.30

# ROUGE score
rouge = Rouge()
generated_summary = ensemble_summarization(article, 3)[0]
scores = rouge.get_scores(generated_summary, reference_summaries[0], avg=True)
print(scores)
#{'rouge-1': {'r': 0.5396825396825397, 'p': 0.5396825396825397, 'f': 0.5396825346825398}, 'rouge-2': {'r': 0.325, 'p': 0.32098765432098764, 'f': 0.32298136145982026}, 'rouge-l': {'r': 0.5396825396825397, 'p': 0.5396825396825397, 'f': 0.5396825346825398}}