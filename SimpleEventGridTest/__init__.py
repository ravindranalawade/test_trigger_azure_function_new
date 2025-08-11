import logging
import json
import azure.functions as func
from datetime import datetime

def main(event: func.EventGridEvent) -> None:
    """
    Simple Event Grid test function that prints hello message when blob is uploaded
    """
    
    # Get the event data
    event_data = event.get_json()
    
    # Extract blob information
    blob_url = event_data.get('url', 'Unknown')
    blob_name = blob_url.split('/')[-1] if blob_url != 'Unknown' else 'Unknown'
    event_time = event_data.get('eventTime', datetime.utcnow().isoformat())
    
    # Create hello message
    hello_message = f"""
    🎉 HELLO! New file uploaded to blob storage!
    
    📁 File: {blob_name}
    🔗 URL: {blob_url}
    ⏰ Time: {event_time}
    📧 Event Type: {event.event_type}
    📋 Subject: {event.subject}
    
    ✅ Event Grid trigger is working perfectly!
    """
    
    # Print to console (visible in Azure Function logs)
    print(hello_message)
    
    # Also log it properly
    logging.info(f"🎉 HELLO! File uploaded: {blob_name}")
    logging.info(f"📁 Blob URL: {blob_url}")
    logging.info(f"⏰ Event Time: {event_time}")
    
    # Return success message
    return f"Hello message printed for blob: {blob_name}"
