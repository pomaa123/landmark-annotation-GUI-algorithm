import pandas as pd

# Load your CSV file with landmarks
landmarks_df = pd.read_csv("./landmarks.csv")

# Inspect the range of each landmark coordinate
for col in landmarks_df.columns[1:]:  # Skip the filename column
    min_value = landmarks_df[col].min()
    max_value = landmarks_df[col].max()
    print(f"{col}: Min = {min_value}, Max = {max_value}")


# target_range = landmarks_df.iloc[:, 1:].max().max()  # Example: if range is 0 to 500
avg_error = 5  # Assume you want an average error of 5 pixels
expected_loss = avg_error**2
print(f"Expected Loss: {expected_loss}")
