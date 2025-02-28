import streamlit as st
#from flask import Flask, request, jsonify
import requests
#import json
#import logging
import os




url = "http://104.248.15.218:8088/score_headlines"


# Streamlit UI
def main():
	st.title("Headline Sentiment Scoring")

	st.write("Enter headlines separated by commas, and get their sentiment analysis.")

	headlines_input= st.text_area("Enter headlines separated by commas:")

	headlines_dict = {"headlines": headlines_input.split(", ")}

	response = requests.post(url, json=headlines_dict)

	st.write(f"{response.json()}")


if __name__ == '__main__':
    # Start the Streamlit app on port 9088 and allow external access
	

    main()
    #os.system("streamlit run test.py --server.address 104.248.15.218 --server.port 9088")
