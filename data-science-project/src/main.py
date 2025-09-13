# main.py

import pandas as pd
from utils import load_data, process_data, train_model

def main():
    # Load raw data
    raw_data = load_data('data/raw/data.csv')
    
    # Process the data
    processed_data = process_data(raw_data)
    
    # Train the model
    model = train_model(processed_data)
    
    # Save the model or results if necessary
    # model.save('model/model.pkl')

if __name__ == "__main__":
    main()