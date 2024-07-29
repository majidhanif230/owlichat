# OwlieChat

OwlieChat is a Flask-based chatbot application that provides insights on sleep health and general queries. The application utilizes Google Vertex AI for chat functionalities and can be deployed using Google Cloud Run.
# Step1

gcloud config set project vertext-0001

# Step2
1. **Clone the Repository**

# bash
   git clone https://github.com/majidhanif230/owlichat.git
   cd owlichat
# Build the Docker Image
docker build -t gcr.io/vertext-0001/owliechat .
# Push the Docker Image
docker push gcr.io/vertext-0001/owliechat
# Deploy to Google Cloud Run
gcloud run deploy owliechat --image gcr.io/vertext-0001/owliechat --platform managed --region us-central1 --allow-unauthenticated

