import PyPDF4
from translate import Translator
from summa import summarizer, keywords
from docx import Document

def read_pdf_text(filename):
    pdf_text = ""
    with open(filename, 'rb') as file:
        reader = PyPDF4.PdfReader(file)
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            pdf_text += page.extract_text()
    return pdf_text

def translate_text(text, target_lang='pt'):
    translator = Translator(to_lang=target_lang)
    translation = translator.translate(text)
    return translation if translation else "Erro na tradução."

def create_summary_docx(text, output_docx):
    summarized_text = summarizer.summarize(text)

    doc = Document()
    doc.add_paragraph(summarized_text)

    doc.save(output_docx)

def create_summary_txt(text, output_txt):
    summarized_text = summarizer.summarize(text)
    keywords_text = keywords.keywords(text)

    with open(output_txt, 'w', encoding='utf-8') as file:
        file.write("Resumo:\n")
        file.write(summarized_text)
        file.write("\n\nPalavras-chave:\n")
        file.write(keywords_text)

if __name__ == "__main__":
    pdf_filename = "SOWB2022_EN_compressed.pdf"  # Altere o nome do arquivo aqui, se necessário.
    output_docx = "resumo.docx"  # Nome do arquivo de saída com o resumo em Word.
    output_txt = "resumo.txt"  # Nome do arquivo de saída com o resumo em formato de texto.

    try:
        pdf_text = read_pdf_text(pdf_filename)

        # Traduzir o texto para o português
        translated_text = translate_text(pdf_text, target_lang='pt')

        # Criar o resumo em um arquivo Word
        create_summary_docx(translated_text, output_docx)

        # Criar o resumo em um arquivo de texto
        create_summary_txt(translated_text, output_txt)

        print(f"Resumo traduzido criado com sucesso e salvo em '{output_docx}' e '{output_txt}'.")
    except FileNotFoundError:
        print(f"O arquivo '{pdf_filename}' não foi encontrado.")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")
