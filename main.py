import PyPDF2
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from collections import Counter
from docx import Document

nltk.download("punkt")
nltk.download("stopwords")

def read_pdf_text(filename):
    with open(filename, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            text += page.extract_text()
        return text

def preprocess_text(text):
    # Remove caracteres especiais e números
    text = re.sub(r'\d+', '', text)
    text = re.sub(r'[^\w\s]', '', text)

    # Tokenize as palavras e as sentenças
    words = word_tokenize(text)
    sentences = sent_tokenize(text)

    # Remover stopwords (palavras irrelevantes)
    stop_words = set(stopwords.words('english'))
    words = [word.lower() for word in words if word.lower() not in stop_words]

    return words, sentences

def get_most_common_words(text, top_n=10):
    words = re.findall(r'\b\w+\b', text.lower())
    word_freq = Counter(words)
    return word_freq.most_common(top_n)

def summarize_text(sentences, ratio=0.3):
    num_sentences = max(1, int(ratio * len(sentences)))
    summarized_text = ' '.join(sentences[:num_sentences])
    return summarized_text

def create_summary_docx(summary_text, output_docx):
    doc = Document()
    doc.add_heading('Resumo', level=1)
    doc.add_paragraph(summary_text)
    doc.save(output_docx)

if __name__ == "__main__":
    pdf_filename = "SOWB2022_EN_compressed.pdf"  # Altere o nome do arquivo aqui, se necessário.
    output_filename = "resumo.docx"   # Nome do arquivo de saída do resumo em Word.

    try:
        pdf_text = read_pdf_text(pdf_filename)

        # Obter as palavras mais comuns no PDF
        most_common_words = get_most_common_words(pdf_text)
        print("Palavras mais repetidas no PDF:")
        for word, freq in most_common_words:
            print(f"{word}: {freq}")

        # Resumir o texto do PDF
        words, sentences = preprocess_text(pdf_text)
        summarized_text = summarize_text(sentences)

        # Criar o resumo em Word
        create_summary_docx(summarized_text, output_filename)

        print(f"Resumo criado com sucesso e salvo em '{output_filename}'.")
    except FileNotFoundError:
        print(f"O arquivo '{pdf_filename}' não foi encontrado.")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")
