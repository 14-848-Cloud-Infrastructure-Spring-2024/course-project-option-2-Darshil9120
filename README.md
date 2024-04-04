[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-24ddc0f5d75046c5622901739e7c5dd533143b0c8e959d652212380cedb1ea36.svg)](https://classroom.github.com/a/i8Qc23u7)

DARSHIL KIKANI
PEER NAME: DIVYANGAM DUTTA

**Frontend Application:**

The frontend is developed using HTML and CSS along with Bootstrap for styling. It consists of the following pages:

•	index.html: The landing page where users can upload tar files.

•	search.html: Redirected from the index page upon successful upload, allowing the option to choose to search or find Top-N words.

•	search_term.html: Provides a search interface, where we can search for a particular instance of a word. The output will be in the following format: Doc ID: 1, Folder: Hugo.tar.gz, Doc Name: NotreDame_De_Paris.txt, Frequencies: 300

•	Top_N.html: Allows users to find the top N terms within the uploaded documents. Suppose we put the value of N as 5. Output will be in following format: 

Term Total Frequencies

MAN 6200

UP 5260

OUT 4991

GOOD 4986

COME 4690

•	bootstrap.min.css is where the styling is done


**Backend Application:**

inverted_indices.py is our backend code with the entire bakcend logic. The backend logic is implemented in Flask, with several key functionalities:

1) **Building Inverted Indices**

The main assumption here is the input files that will be uploaded are tar archives. Extracts these files to build an inverted index, and then enable search operations   

2) **Search Term Functionality**

•	Provides a route to search for specific terms within the indexed data. The search considers only complete words. This is achieved using the regular expression pattern r'\b\w+\b', which matches whole words delimited by word boundaries. So for example if we search the word king- “king” and “king’s” will be counted but not “making” while computing the number of instances of the word “king”. We also print out the execution time of our search in milliseconds.

3) **Top_N Terms Functionality**

•	Identifies the most frequently occurring words across the documents, excluding a predefined list of stop words.  Here is the list of Stop words that we used. This can be increased to as many words we want to increase relevance. stop_words = set([ "the", "a", "an", "and", "or", "but", "is", "are", "of", "to", "in", "that", "it", "for", "on", "with", "as", "was", "were", "be", "been", "being", "i", "he", "his", "you", "not", "her", "had", "him", "her", "she", "my", "at", "this", "have", "which" , "all", "me", "what", "s", "how", "them", "then", "more", "did", "by", "so", "from", "one", "your", "no", "they", "said", "will", "there", "who", "do", "we", "do", "if", "when", "would", "their", "thou", "d", "now" # Add more stop words as needed ]). We also print out the execution time of our search in milliseconds.

**Interaction Between Frontend and Backend:**

We used AJAX to enable asynchronous communication between the frontend and backend. This allows the web page to send data to and receive data from the server without having to reload the page.

1) **File Uploads:**

For file uploads, we implemented a system where users select tar files via the index.html page. Through AJAX, these files are sent in the background to our Flask backend by making a POST request to the /upload endpoint. Our backend then processes these files by extracting their contents and building inverted indices.
•	Endpoint: /upload

•	Method: POST

•	Functionality: Handles tar files, extracts content, and builds inverted indices.

2) **Search Requests:**

Our search feature uses AJAX as well. Users input search terms on search.html or search_term.html, and AJAX sends these terms to our backend without page reloads. The backend searches through the inverted indices and returns the findings.
•	Endpoints:

•	/search_term for searching individual terms.

•	/top_n for finding the most frequent terms, with a stop words filter.

•	Method: POST

•	Functionality: Executes searches or computes top N terms.

After processing, the backend sends back a JSON response with search results or confirmation of index construction. The frontend then updates to display this information, showing either the search outcomes or a success message for file processing.

**Deployment:**

Create the Docker file. Build and run it to test it locally and it worked. Then, push the image (pro-backend) to Docker Hub. Then, pull the image, change its tag, and push it to the Container Registry.

**Google Kubernetes Engine (GKE) Deployment:**

After that we write the terraform code to deploy the GKE cluster alongside making pro-backend deployment and service yaml files. We deploy these yaml files using terraform. This is something we did in Homework-5. We then proceed to the services section (gateways, services and ingress) of the Kubernetes engine, where the frontend application was hosted at 34.127.109.17:80.

**Folder Structure**

/directory

    /templates
    
        - index.html
        
        - search.html
        
        - search_term.html
        
        - Top_N.html
        
    /static
    
        - bootstrap.min.css
        
    - inverted_indices.py
    
    - Dockerfile
    
 
Docker image link:

https://hub.docker.com/repository/docker/divyangam094/pro-backend
