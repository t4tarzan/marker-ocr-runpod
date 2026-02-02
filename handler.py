"""
RunPod Serverless Handler for Marker OCR
Processes PDF files using Marker and returns extracted text
"""

import runpod
import base64
import json
import tempfile
import os
import sys
from pathlib import Path

print("Handler starting...")
print(f"Python version: {sys.version}")

# Import marker after it's installed in the container
PdfConverter = None
create_model_dict = None
text_from_rendered = None

try:
    print("Importing marker modules...")
    from marker.converters.pdf import PdfConverter
    from marker.models import create_model_dict
    from marker.output import text_from_rendered
    print("Marker modules imported successfully")
except ImportError as e:
    print(f"CRITICAL: Marker import failed: {e}")
    print("This container does not have marker-pdf installed correctly")
    import sys
    sys.exit(1)

# Initialize converter once at startup
converter = None

def initialize_converter():
    """Initialize Marker converter once at container startup"""
    global converter
    if converter is None:
        print("Initializing Marker converter...")
        try:
            artifact_dict = create_model_dict()
            converter = PdfConverter(artifact_dict=artifact_dict)
            print("Converter initialized successfully")
        except Exception as e:
            print(f"Error initializing converter: {e}")
            raise
    return converter

def process_pdf(job):
    """
    Process a single PDF file with Marker OCR
    
    Input format:
    {
        "input": {
            "pdf_base64": "base64_encoded_pdf_data",
            "filename": "document.pdf",
            "output_format": "json"  # or "markdown"
        }
    }
    
    Returns:
    {
        "text": "extracted text content",
        "metadata": {...},
        "success": true
    }
    """
    print(f"Received job: {job.get('id', 'unknown')}")
    try:
        job_input = job["input"]
        print(f"Job input keys: {list(job_input.keys())}")
        
        # Get PDF data
        pdf_base64 = job_input.get("pdf_base64")
        filename = job_input.get("filename", "document.pdf")
        output_format = job_input.get("output_format", "json")
        
        if not pdf_base64:
            return {"error": "No pdf_base64 provided", "success": False}
        
        # Decode PDF
        pdf_bytes = base64.b64decode(pdf_base64)
        
        # Save to temp file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(pdf_bytes)
            tmp_path = tmp_file.name
        
        try:
            # Initialize models if not already loaded
            models = initialize_models()
            
            # Process with Marker
            print(f"Processing {filename}...")
            full_text, images, metadata = convert_single_pdf(
                tmp_path,
                models,
                max_pages=None,
                langs=None,
                batch_multiplier=1
            )
            
            # Clean up temp file
            os.unlink(tmp_path)
            
            # Return results
            result = {
                "text": full_text,
                "metadata": {
                    "filename": filename,
                    "pages": metadata.get("pages", 0),
                    "language": metadata.get("language", "en"),
                    "toc": metadata.get("toc", []),
                },
                "success": True
            }
            
            print(f"Successfully processed {filename}")
            return result
            
        except Exception as e:
            # Clean up temp file on error
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)
            raise e
            
    except Exception as e:
        import traceback
        error_msg = str(e)
        error_trace = traceback.format_exc()
        print(f"Error processing PDF: {error_msg}")
        print(f"Traceback: {error_trace}")
        return {
            "error": error_msg,
            "traceback": error_trace,
            "success": False
        }

# Start the RunPod serverless handler
runpod.serverless.start({"handler": process_pdf})
