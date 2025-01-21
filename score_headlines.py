import os
from datetime import datetime
import joblib
from sentence_transformers import SentenceTransformer
import argparse

def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Process and score headlines.")
    parser.add_argument("file_path", help="Path to the text file containing headlines.")
    parser.add_argument("source", help="Source of the headlines (e.g., chicagotribune, nyt).")
    args = parser.parse_args()

    file_path = args.file_path
    source_parameter = args.source

    # Check if the file exists
    if not os.path.isfile(file_path):
        print(f"Error: The file '{file_path}' does not exist. Please check the file path and try again.")
        exit()

    # Process the headlines
    try:
        # Get today's date and format it as "year_month_date"
        today_date = datetime.now().strftime("%Y_%m_%d")

        # Read the headlines from the file
        with open(file_path, 'r') as file:
            headlines = file.readlines()

        if not headlines:
            print("Error: The input file is empty. Please provide a file with at least one headline.")
            exit()

        # Load the classifier and SentenceTransformer model
        clf = joblib.load('svm.joblib')
        model = SentenceTransformer("all-MiniLM-L6-v2")

        # Generate embeddings and predict labels
        embeddings = model.encode(headlines)
        predicted_labels = clf.predict(embeddings)

        # Write the output to a file
        filename = f"headline_scores_{source_parameter}_{today_date}.txt"
        with open(filename, "w") as f:
            for label, headline in zip(predicted_labels, headlines):
                f.write(f"{label}, {headline.strip()}\n")

        print(f"Processing complete! Results have been saved to '{filename}'.")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()