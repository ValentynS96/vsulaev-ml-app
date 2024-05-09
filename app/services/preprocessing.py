import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.tokenize import word_tokenize

# Завантаження даних для nltk
import ssl
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')


def preprocess_text(text, options):
    # Токенізація
    if 'use_tokenize' in options:
        tokens = word_tokenize(text)
    else:
        tokens = text.split()

    # Видалення стоп-слів
    if 'use_stopwords' in options:
        stop_words = set(stopwords.words('english'))
        tokens = [word for word in tokens if word not in stop_words]

    # Стемінг
    if 'use_stemming' in options:
        stemmer = PorterStemmer()
        tokens = [stemmer.stem(word) for word in tokens]

    # Лематизація
    if 'use_lemmatize' in options:
        lemmatizer = WordNetLemmatizer()
        tokens = [lemmatizer.lemmatize(word) for word in tokens]

    if 'use_lowers' in options:
        tokens = [word.lower() for word in tokens]

    return tokens
