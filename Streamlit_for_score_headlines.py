import streamlit as st
import requests
import os

# Web Service API URL
URL = "http://104.248.15.218:8088/score_headlines"

# Streamlit UI
def main():
    st.title("Headline Sentiment Scoring")
    st.write("To get their sentiment analysis:")

    # User Input
    headlines_input = st.text_area("Enter headlines separated by commas:")

    if st.button("Analyze Sentiment"):
        if headlines_input.strip():
            # Convert input into dictionary format
            headlines_dict = {"headlines": [h.strip() for h in headlines_input.split(",")]}

            try:
                # Send POST request to the API
                response = requests.post(URL, json=headlines_dict)

                if response.status_code == 200:
                    st.subheader("Sentiment Results:")
                    st.json(response.json())  # Display formatted JSON response
                else:
                    st.error(f"API Error: {response.status_code} - {response.text}")

            except requests.exceptions.RequestException as e:
                st.error(f"Failed to connect to the API: {e}")
        else:
            st.warning("Please enter at least one headline.")

if __name__ == '__main__':
  #main()
  os.system("streamlit run test.py --server.address 104.248.15.218 --server.port 9088")
