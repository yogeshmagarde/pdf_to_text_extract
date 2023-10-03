
import os
import fitz
from flask import Flask, jsonify, request
from models import ExtractDataSchema
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def is_article_block(block):
    return len(block[4].split()) > 10

@app.route('/api/extract', methods=['POST'])

def extract_articles():
    schema = ExtractDataSchema()
    errors = schema.validate(request.files)

    if errors:
        return jsonify({'error': errors}), 400

    pdf_file = request.files['pdf']  # Access the uploaded PDF file

    save_path = os.path.join('E:\\FLASK2', pdf_file.filename)
    pdf_file.save(save_path)

    output_content1 = []
    output_content2 = []
    doc = fitz.open(save_path)
    page_number = 1
    #for page_number in range(len(doc)):
    page = doc[page_number]
    blocks = page.get_text("blocks")

    if blocks:
        article_blocks = [block for block in blocks if is_article_block(block)]

        if article_blocks:
            for i, article_block in enumerate(article_blocks):
                article_text = article_block[4]

                if article_text.strip():
                    article_text = article_text.replace("�", "P")
                    paragraph = article_text
                        
                    output_content1.append(paragraph)
                else:
                    print(f"Page {page_number+1} - No text found in Article {i+1}")
        else:
            print(f"Page {page_number+1} - No articles found")
    else:
        print(f"Page {page_number+1} - No words found")
    
    doc.close()
    for index,arpara in enumerate(output_content1):
        paragrap=index,arpara.replace("\n"," ")
        # result = {"extract_data":paragrap}
        # output_content2.append(result)
        output_content2.append(paragrap)
        print(output_content2)
    return jsonify(output_content2)
                        



if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
    


    