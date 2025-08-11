# Azure Blob Storage Trigger Function

This Azure Function triggers automatically when a file is uploaded to Azure Blob Storage.

## Features

- **Automatic Trigger**: Responds to blob uploads in the specified container
- **File Type Processing**: Different handling for images, text, CSV, and JSON files
- **Logging**: Comprehensive logging for monitoring and debugging
- **Error Handling**: Robust error handling with detailed logging
- **Extensible**: Easy to add new file processing logic

## Setup Instructions

### Prerequisites

1. **Azure Storage Account**: You need an Azure Storage Account
2. **Azure Functions Core Tools**: Install from [here](https://docs.microsoft.com/en-us/azure/azure-functions/functions-run-local)
3. **Python 3.8+**: Ensure Python is installed

### Local Development Setup

1. **Clone/Download** this project
2. **Install dependencies**:
   ```powershell
   pip install -r requirements.txt
   ```

3. **Configure local.settings.json**:
   - Replace `your_storage_account` with your actual storage account name
   - Replace `your_storage_key` with your actual storage account key
   
   ```json
   {
     "IsEncrypted": false,
     "Values": {
       "AzureWebJobsStorage": "DefaultEndpointsProtocol=https;AccountName=your_storage_account;AccountKey=your_storage_key;EndpointSuffix=core.windows.net",
       "FUNCTIONS_WORKER_RUNTIME": "python"
     }
   }
   ```

4. **Create Storage Container**:
   - Create a container named `uploads` in your Azure Storage Account
   - This is where you'll upload files to trigger the function

### Running Locally

```powershell
func start
```

### Testing the Function

1. **Upload a file** to the `uploads` container in your Azure Storage Account
2. **Check the logs** in your terminal to see the function execution
3. **Try different file types**: .jpg, .png, .txt, .csv, .json

## Function Configuration

### Trigger Configuration (function.json)

```json
{
  "name": "myblob",
  "type": "blobTrigger",
  "direction": "in",
  "path": "uploads/{name}",
  "connection": "AzureWebJobsStorage"
}
```

- **path**: `uploads/{name}` - triggers on files uploaded to the 'uploads' container
- **connection**: Points to the storage account connection string

### Customizing the Trigger

To change the container or path pattern, modify the `path` in `BlobTrigger/function.json`:

- `uploads/{name}` - Any file in 'uploads' container
- `images/{name}.jpg` - Only .jpg files in 'images' container
- `data/{name}` - Any file in 'data' container
- `{container}/{name}` - Any file in any container

## File Processing Logic

The function includes handlers for different file types:

### Images (.jpg, .jpeg, .png)
- Processes image files
- Add your image processing logic in `process_image()`

### Text Files (.txt, .csv)
- Reads and processes text content
- Add your text processing logic in `process_text_file()`

### JSON Files (.json)
- Parses and processes JSON content
- Add your JSON processing logic in `process_json_file()`

## Deployment to Azure

1. **Create Azure Function App**:
   ```powershell
   az functionapp create --resource-group myResourceGroup --consumption-plan-location westus --runtime python --runtime-version 3.9 --functions-version 4 --name myFunctionApp --storage-account mystorageaccount
   ```

2. **Deploy the function**:
   ```powershell
   func azure functionapp publish myFunctionApp
   ```

3. **Configure App Settings**:
   - Set `AzureWebJobsStorage` in the Function App configuration

## Monitoring

- **Azure Portal**: Monitor function executions in the Azure portal
- **Application Insights**: Enable for detailed telemetry
- **Logs**: Check function logs for processing details

## Common Use Cases

1. **Image Processing**: Resize, compress, or analyze uploaded images
2. **Data Processing**: Process CSV/JSON files and store results
3. **File Validation**: Validate uploaded files and move invalid ones
4. **Notifications**: Send notifications when specific files are uploaded
5. **Data Migration**: Automatically process and migrate uploaded data

## Troubleshooting

1. **Function not triggering**:
   - Check storage account connection string
   - Verify container name exists
   - Check function app is running

2. **Import errors**:
   - Ensure all dependencies are in requirements.txt
   - Check Python version compatibility

3. **Permission errors**:
   - Verify storage account access keys
   - Check container permissions
