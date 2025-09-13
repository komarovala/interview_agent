def load_data(file_path):
    """Load data from a specified file path."""
    import pandas as pd
    return pd.read_csv(file_path)

def preprocess_data(df):
    """Preprocess the DataFrame by handling missing values and encoding categorical variables."""
    df = df.dropna()  # Example: drop missing values
    df = pd.get_dummies(df)  # Example: one-hot encoding for categorical variables
    return df

def evaluate_model(model, X_test, y_test):
    """Evaluate the model using accuracy score."""
    from sklearn.metrics import accuracy_score
    predictions = model.predict(X_test)
    return accuracy_score(y_test, predictions)