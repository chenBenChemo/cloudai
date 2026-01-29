from google.cloud import bigquery
from .config import PROJECT_ID, DATASET

def get_customer_history(order_id: int):
    """Tool: Searches BigQuery for past customer complaints."""
    client = bigquery.Client(project=PROJECT_ID)
    query = f"SELECT * FROM `{PROJECT_ID}.{DATASET}.cymbaldirect_orders` WHERE order_id = {order_id}"
    results = client.query(query).to_dataframe()
    return results.to_json()

def analyze_damage_image(image_uri: str):
    """Tool: Placeholder for Gemini Multimodal image analysis."""
    # This would typically call Vertex AI Gemini
    return f"Vision Analysis for {image_uri}: Package seal is broken, box is crushed."
