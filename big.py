from google.cloud import bigquery
import pandas as pd
import logging

# Set your Google Cloud project ID
project_id = "vertext-0001"

# Initialize BigQuery client
bq_client = bigquery.Client(project=project_id)

def query_bigquery():
    query = """
    SELECT `Section Title`, Prompt
    FROM `vertext-0001.dataset.data`
    LIMIT 200
    """
    try:
        # Execute the query and fetch the DataFrame
        df = bq_client.query(query).to_dataframe()
        
        
        # Convert DataFrame to dictionary
        if not df.empty:
            prompts = {row['Section Title']: row['Prompt'] for index, row in df.iterrows()}
        
            return prompts
        else:
            logger.warning("DataFrame is empty. No data retrieved.")
            return {}
    except Exception as e:
        logger.error(f"Failed to load prompts from BigQuery: {e}")
        return {}
