from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd

# Load the trained RidgeClassifier model
model = joblib.load("ridge_feature_engineering_model.joblib")

# Initialize FastAPI
app = FastAPI()

# Define the input schema for the POST request
class PredictRequest(BaseModel):
    Annual_Income: int
    Family_Size: int
    Age: int
    Work_Experience: int

@app.post("/predict")
def predict(data: PredictRequest):
    try:
        # Parse input into a dictionary
        input_dict = {
            "Annual_Income": [data.Annual_Income],
            "Family_Size": [data.Family_Size],
            "Age": [data.Age],
            "Work_Experience": [data.Work_Experience],
            "Income_Per_Family": [data.Annual_Income / (data.Family_Size + 1)],  # Float value
            "Age_Experience_Interaction": [data.Age * data.Work_Experience]
        }

        # Convert the dictionary into a Pandas DataFrame
        input_df = pd.DataFrame(input_dict)

        # Ensure the DataFrame column order matches the expected columns
        expected_columns = [
            "Annual_Income",
            "Family_Size",
            "Age",
            "Work_Experience",
            "Income_Per_Family",
            "Age_Experience_Interaction"
        ]
        input_df = input_df[expected_columns]  # Reorder columns to match expected order

        # Validate data types
        expected_dtypes = {
            "Annual_Income": "int64",
            "Family_Size": "int64",
            "Age": "int64",
            "Work_Experience": "int64",
            "Income_Per_Family": "float64",
            "Age_Experience_Interaction": "int64"
        }

        # Check if data types match the expected ones
        for column, dtype in expected_dtypes.items():
            if input_df[column].dtypes != dtype:
                raise ValueError(f"Data type mismatch for column '{column}'. Expected: {dtype}, Got: {input_df[column].dtypes}")

        # Pass the DataFrame to the model pipeline
        prediction = model.predict(input_df)

        return {"prediction": int(prediction[0])}
    except Exception as e:
        return {"error": str(e)}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)