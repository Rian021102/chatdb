import pandas as pd
from google.cloud import bigquery
from google.oauth2 import service_account

# Set the path to your JSON key file
credentials_path = "/Users/rianrachmanto/pypro/bigquery/intricate-idiom-379506-21563d575ba3.json"

# Load the credentials from the JSON key file
credentials = service_account.Credentials.from_service_account_file(credentials_path)

# Create the BigQuery client with the loaded credentials
client = bigquery.Client(credentials=credentials)

# Define your BigQuery SQL query
QUERY = """
SELECT 
    DATEPRD,
    NPD_WELL_BORE_NAME,
    BORE_OIL_VOL,
    BORE_GAS_VOL,
    BORE_WAT_VOL
FROM 
    `intricate-idiom-379506.volveprod.volveprod`
ORDER BY 
    DATEPRD;
"""

# Run the query using the client
query_job = client.query(QUERY)

# Fetch the results into a DataFrame
df = query_job.to_dataframe()

# Now, df contains the query results in a DataFrame format
# You can work with df like any other DataFrame
print(df.head())  # Display the first few rows

print(df['NPD_WELL_BORE_NAME'].unique())  # Display the unique well names