# Marker OCR RunPod Serverless Handler

This is a RunPod serverless endpoint for processing PDFs with Marker OCR on A100 GPU.

## Features

- High-accuracy PDF to text extraction using Marker
- GPU-accelerated processing (A100 recommended)
- Auto-scaling from 0 to N workers
- Pay-per-use pricing model

## Deployment

### Option 1: Deploy via RunPod Console

1. Go to https://www.runpod.io/console/serverless
2. Click "Add your repo"
3. Connect this GitHub repository: `t4tarzan/marker-ocr-runpod`
4. Select GPU: **A100 SXM 80GB** or **A100 PCIe 80GB**
5. Configure scaling:
   - Min Workers: 0
   - Max Workers: 3
   - Idle Timeout: 5 seconds
6. Deploy

### Option 2: Deploy via CLI

```bash
runpod deploy \
  --name marker-ocr-a100 \
  --gpu A100 \
  --repo https://github.com/t4tarzan/marker-ocr-runpod \
  --min-workers 0 \
  --max-workers 3 \
  --idle-timeout 5
```

## Usage

### Input Format

```json
{
  "input": {
    "pdf_base64": "base64_encoded_pdf_content",
    "filename": "document.pdf",
    "output_format": "json"
  }
}
```

### Output Format

```json
{
  "text": "Extracted text content from PDF...",
  "metadata": {
    "filename": "document.pdf",
    "pages": 10,
    "language": "en",
    "toc": []
  },
  "success": true
}
```

### Python Client Example

```python
import runpod
import base64

runpod.api_key = "your_api_key"

# Read PDF
with open("document.pdf", "rb") as f:
    pdf_base64 = base64.b64encode(f.read()).decode()

# Send to endpoint
endpoint = runpod.Endpoint("YOUR_ENDPOINT_ID")
result = endpoint.run({
    "input": {
        "pdf_base64": pdf_base64,
        "filename": "document.pdf"
    }
})

# Get result
output = result.output()
print(output["text"])
```

## Performance

- **Processing Time**: 3-5 seconds per PDF on A100
- **Accuracy**: 95-98% for printed text
- **Supported**: Tables, multi-column layouts, forms

## Cost

With A100 SXM 80GB at $1.39/hr:
- 10 PDFs: ~$0.02
- 100 PDFs: ~$0.20
- 1000 PDFs: ~$2.00

## Requirements

- RunPod account with API key
- A100 GPU (80GB recommended)
- PDFs under 50MB each

## License

MIT
