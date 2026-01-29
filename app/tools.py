from google.cloud import bigquery
from google import genai
from .config import PROJECT_ID, DATASET

def get_customer_history(order_id: int):
    """Tool: Searches BigQuery for past customer complaints."""
    client = bigquery.Client(project=PROJECT_ID)
    query = f"SELECT * FROM `{PROJECT_ID}.{DATASET}.cymbaldirect_orders` WHERE order_id = {order_id}"
    results = client.query(query).to_dataframe()
    return results.to_json()


def analyze_damage_image(image_uri: str):
    """
    Tool: Uses Gemini 3 Flash to analyze complaint images via Vertex AI.
    """
    # Explicitly setting vertexai=True and project is best practice for Cloud Run
    client = genai.Client(vertexai=True, project=PROJECT_ID, location='us-central1')

    response = client.models.generate_content(
        model='gemini-2.0-flash-001', # Use the stable 2026 production version
        contents=[
            "Identify damage in this image for a customer complaint. "
            "Is the product broken, the box crushed, or the seal tampered with?",
            image_uri
        ]
    )
    
    return f"Vision Analysis: {response.text}"
