import os
import tarfile
import collections
import re
from typing import Dict, List, Tuple
from io import TextIOWrapper
from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename
import tempfile
import os
from flask_cors import CORS
from time import time

app = Flask(__name__)
CORS(app)



@app.route('/')
def index():
    # This route serves the index.html file
    return render_template('index.html')

@app.route('/search')
def search():
    return render_template('search.html')

@app.route('/search_term')
def search_term_page():
    return render_template('search_term.html')

@app.route('/top_n')
def Top_N():
    return render_template('Top_N.html')

inverted_index = {}
InvertedIndex = Dict[str, List[Tuple[int, str, str, int]]]

def map_function(tar_path: str, doc_id_start: int) -> List[Tuple[str, Tuple[int, str, str, int]]]:
    
    intermediate = []
    doc_id = doc_id_start
    word_pattern = re.compile(r'\b\w+\b')

    with tarfile.open(tar_path, 'r:gz') as tar:
        for member in tar.getmembers():
            if member.isfile():
                doc_id += 1
                file: TextIOWrapper = tar.extractfile(member)
                text = file.read().decode('latin-1')
                words = word_pattern.findall(text.lower())
                word_count = collections.Counter(words)
                for word, count in word_count.items():
                    intermediate.append((word, (doc_id, tar_path, member.name, count)))
    
    return intermediate, doc_id

def reduce_function(intermediate: List[Tuple[str, Tuple[int, str, str, int]]]) -> InvertedIndex:

    index = collections.defaultdict(list)
    for key, value in intermediate:
        index[key].append(value)
    return index

def build_inverted_index_from_tar(tar_files: List[str]) -> InvertedIndex:

    intermediate = []
    doc_id_start = 0

    # Map phase
    for tar_path in tar_files:
        mapped, last_doc_id = map_function(tar_path, doc_id_start)
        intermediate.extend(mapped)
        doc_id_start = last_doc_id

    # Reduce phase
    inverted_index = reduce_function(intermediate)
    
    return inverted_index

def search_term(index: InvertedIndex, term: str) -> List[Tuple[int, str, str, int]]:
    return index.get(term.lower(), [])

# Define a set of stop words
stop_words = set([
    "the", "a", "an", "and", "or", "but", "is", "are", "of", "to", "in", "that", "it", 
    "for", "on", "with", "as", "was", "were", "be", "been", "being", "i", "he", "his",
    "you", "not", "her", "had", "him", "her", "she", "my", "at", "this", "have", "which"
    , "all", "me", "what", "s", "how", "them", "then", "more", "did", "by", "so", "from", 
    "one", "your", "no", "they", "said", "will", "there", "who", "do", "we", "do", "if", 
    "when", "would", "their", "thou", "d", "now", "has", "himself", "herself", "its", "into"
])

def get_top_n_terms(inverted_index: InvertedIndex, n: int) -> List[Tuple[str, int]]:
    # Initialize a dictionary to store term frequencies excluding stop words
    term_frequencies = {}
    
    for term, occurrences in inverted_index.items():
        if term not in stop_words:
            total_frequency = sum([freq for _, _, _, freq in occurrences])
            term_frequencies[term] = total_frequency
    
    # Sort terms by their frequencies in descending order
    sorted_terms = sorted(term_frequencies.items(), key=lambda item: item[1], reverse=True)
    
    # Return the top-N terms
    return sorted_terms[:n]

@app.route('/upload', methods=['POST'])
def upload_files():
    global inverted_index
    uploaded_files = request.files.to_dict()  # Converts ImmutableMultiDict to dict
    tar_files = []
    for filename, file in uploaded_files.items():
        temp_path = os.path.join(tempfile.gettempdir(), secure_filename(file.filename))
        file.save(temp_path)
        tar_files.append(temp_path)
    
    try:
        inverted_index  = build_inverted_index_from_tar(tar_files)
        
        return jsonify(success=True)
    except Exception as e:
        print(e)  
        return jsonify(success=False), 
    
@app.route('/search_term', methods=['POST'])
def handle_search():
    
    start_time = time()
    search_word = request.form['searchTerm']  
    results = search_term(inverted_index, search_word) 
    
    end_time = time()  # End the timer
    search_time = (end_time - start_time)*1000
    
    
    results_list = [{"doc_id": doc_id, "folder": os.path.basename(folder), "name": os.path.basename(name), "freq": freq} for doc_id, folder, name, freq in results]
    return jsonify({"results": results_list, "search_time": search_time})    

@app.route('/top_n', methods=['POST'])
def handle_top_n():
    
    start_time = time()
    n = int(request.form['topN']) 
    top_n_terms = get_top_n_terms(inverted_index, n)
    
    end_time = time()
    search_time = (end_time - start_time)*1000
    
    results_list = [{"term": term, "frequency": freq} for term, freq in top_n_terms]
    
    return jsonify({"results": results_list, "search_time": search_time})


if __name__ == '__main__':
    app.run(debug=True)



