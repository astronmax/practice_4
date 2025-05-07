import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
import pandas as pd

# Загрузка необходимых ресурсов NLTK
nltk.download('punkt')
nltk.download('stopwords')

# Функция для предобработки текста
def preprocess_text(text):
    # Приведение к нижнему регистру
    text = text.lower()
    # Удаление специальных символов
    text = re.sub(r'[^\w\s]', '', text)
    # Токенизация
    tokens = word_tokenize(text, language='russian')
    # Удаление стоп-слов
    stop_words = set(stopwords.words('russian'))
    tokens = [token for token in tokens if token not in stop_words]
    # Стемминг
    stemmer = SnowballStemmer("russian")
    tokens = [stemmer.stem(token) for token in tokens]
    
    return tokens

# Загрузка словаря эмоциональной окраски слов
def load_sentiment_dictionary():
    # Это пример словаря, в реальном приложении вы можете использовать готовый словарь
    # или создать свой на основе размеченных данных
    positive_words = ['хорош', 'отличн', 'прекрасн', 'замечательн', 'великолепн', 
                      'радост', 'счаст', 'любов', 'добр', 'приятн', 'позитивн']
    negative_words = ['плох', 'ужасн', 'отвратительн', 'неприятн', 'грустн', 
                      'печальн', 'страшн', 'злой', 'ненавист', 'негативн', 'раздраж']
    
    sentiment_dict = {}
    for word in positive_words:
        sentiment_dict[word] = 1
    for word in negative_words:
        sentiment_dict[word] = -1
        
    return sentiment_dict

# Функция для анализа настроения текста
def analyze_sentiment(text, sentiment_dict):
    tokens = preprocess_text(text)
    
    sentiment_score = 0
    matched_words = 0
    
    for token in tokens:
        if token in sentiment_dict:
            sentiment_score += sentiment_dict[token]
            matched_words += 1
    
    # Нормализация оценки настроения
    if matched_words > 0:
        normalized_score = sentiment_score / matched_words
    else:
        normalized_score = 0
    
    return {
        'raw_score': sentiment_score,
        'matched_words': matched_words,
        'normalized_score': normalized_score
    }

# Основная функция для анализа файла
def analyze_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()
        
        sentiment_dict = load_sentiment_dictionary()
        result = analyze_sentiment(text, sentiment_dict)
        
        print(f"Анализ настроения текста из файла: {file_path}")
        print(f"Сырая оценка настроения: {result['raw_score']}")
        print(f"Количество найденных эмоционально окрашенных слов: {result['matched_words']}")
        print(f"Нормализованная оценка настроения: {result['normalized_score']:.4f}")
        
        # Интерпретация результата
        if result['normalized_score'] > 0:
            print("Текст имеет положительное настроение")
        elif result['normalized_score'] < 0:
            print("Текст имеет отрицательное настроение")
        else:
            print("Текст имеет нейтральное настроение")
            
        return result
    
    except Exception as e:
        print(f"Произошла ошибка при анализе файла: {e}")
        return None

# Функция для сравнения нескольких текстов
def compare_texts(file_paths):
    results = []
    
    for file_path in file_paths:
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()
            
            sentiment_dict = load_sentiment_dictionary()
            result = analyze_sentiment(text, sentiment_dict)
            result['file_path'] = file_path
            results.append(result)
            
        except Exception as e:
            print(f"Произошла ошибка при анализе файла {file_path}: {e}")
    
    # Сортировка результатов по нормализованной оценке
    results.sort(key=lambda x: x['normalized_score'], reverse=True)
    
    # Вывод сравнительной таблицы
    if results:
        df = pd.DataFrame(results)
        print("\nСравнительная таблица настроения текстов:")
        print(df[['file_path', 'normalized_score', 'raw_score', 'matched_words']])
    else:
        print("Нет результатов для сравнения")
    
    return results

# Пример использования
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Использование: python sentiment_analyzer.py <путь_к_файлу> [<путь_к_файлу2> ...]")
    elif len(sys.argv) == 2:
        analyze_file(sys.argv[1])
    else:
        compare_texts(sys.argv[1:])