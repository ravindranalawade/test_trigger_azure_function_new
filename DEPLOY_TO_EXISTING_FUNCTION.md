# 🚀 Deploy Your Code to Existing Azure Function App

Since you've already created the Azure Function App through the UI, here are the best methods to deploy your hello message code:

## 🎯 **Method 1: Azure Functions Core Tools (Recommended)**

### Step 1: Login and Get Function App Name

```bash
# Login to Azure
az login --use-device-code

# List your function apps to get the exact name
az functionapp list --query "[].{Name:name, ResourceGroup:resourceGroup, State:state}" -o table

# Or if you know the resource group:
az functionapp list --resource-group YOUR-RESOURCE-GROUP --query "[].name" -o table
```

### Step 2: Deploy Your Code

```bash
# Navigate to your project directory
cd /home/azureuser/blob_trigger

# Deploy to your existing function app
func azure functionapp publish YOUR-FUNCTION-APP-NAME

# Example:
# func azure functionapp publish func-hello-message-12345
```

## 🎯 **Method 2: VS Code Extension (Easy)**

### Step 1: Install VS Code Azure Functions Extension

1. Open VS Code
2. Go to Extensions (Ctrl+Shift+X)
3. Search for "Azure Functions"
4. Install the Azure Functions extension by Microsoft

### Step 2: Deploy Through VS Code

1. Open your `blob_trigger` folder in VS Code
2. Press `Ctrl+Shift+P` and type "Azure Functions: Deploy to Function App"
3. Select your subscription
4. Select your existing Function App
5. Confirm deployment

## 🎯 **Method 3: ZIP Deployment**

### Step 1: Create Deployment Package

```bash
# Create a zip file of your project
cd /home/azureuser
zip -r blob_trigger_deploy.zip blob_trigger/ -x "*.git*" "*__pycache__*" "*.pyc"
```

### Step 2: Deploy via Azure CLI

```bash
# Deploy the zip file
az functionapp deployment source config-zip \
  --resource-group YOUR-RESOURCE-GROUP \
  --name YOUR-FUNCTION-APP-NAME \
  --src blob_trigger_deploy.zip
```

## 🎯 **Method 4: Portal Upload (Manual)**

### Step 1: Create ZIP File

```bash
# Create a clean zip with just the necessary files
cd /home/azureuser/blob_trigger
zip -r ../hello_function.zip . -x "*.git*" "*__pycache__*" "*.pyc" "test-*" "deploy-*"
```

### Step 2: Upload via Azure Portal

1. Go to [Azure Portal](https://portal.azure.com)
2. Navigate to your Function App
3. Go to **Development Tools** → **Advanced Tools** → **Go**
4. In Kudu, go to **Tools** → **Zip Push Deploy**
5. Drag and drop your zip file

## 🎯 **Method 5: GitHub Integration**

If your code is in GitHub:

1. Go to your Function App in Azure Portal
2. Go to **Deployment** → **Deployment Center**
3. Choose **GitHub** as source
4. Authorize and select your repository
5. Azure will auto-deploy from your repository

## 📋 **What Files Will Be Deployed**

Your deployment will include:

```
SimpleEventGridTest/
├── __init__.py          # Your hello message function
└── function.json        # Function configuration

requirements.txt         # Python dependencies
host.json               # Azure Functions configuration
local.settings.json     # Local settings (won't be deployed)
```

## 🧪 **After Deployment: Test Your Function**

### Step 1: Verify Function is Deployed

```bash
# List functions in your app
az functionapp function list --name YOUR-FUNCTION-APP-NAME --resource-group YOUR-RESOURCE-GROUP
```

### Step 2: Get Function URL

```bash
# Get the Event Grid trigger URL
az functionapp function show \
  --resource-group YOUR-RESOURCE-GROUP \
  --name YOUR-FUNCTION-APP-NAME \
  --function-name SimpleEventGridTest \
  --query "invokeUrlTemplate" -o tsv
```

### Step 3: Set Up Event Grid Subscription

```bash
# Create Event Grid subscription (replace with your details)
az eventgrid event-subscription create \
  --name hello-message-subscription \
  --source-resource-id /subscriptions/YOUR-SUBSCRIPTION-ID/resourceGroups/YOUR-RESOURCE-GROUP/providers/Microsoft.Storage/storageAccounts/aimldocs \
  --endpoint-type webhook \
  --endpoint "YOUR-FUNCTION-URL" \
  --event-types Microsoft.Storage.BlobCreated
```

### Step 4: Test with File Upload

```bash
# Upload a test file to trigger the function
echo "Hello from Azure Function!" > test-hello-azure.txt
az storage blob upload \
  --account-name aimldocs \
  --container-name docs \
  --name "test-hello-$(date +%s).txt" \
  --file test-hello-azure.txt
```

### Step 5: Check Function Logs

```bash
# View live logs
az functionapp logs tail --name YOUR-FUNCTION-APP-NAME --resource-group YOUR-RESOURCE-GROUP

# Or check logs in Azure Portal:
# Function App → Functions → SimpleEventGridTest → Monitor
```

## 🎉 **Expected Result**

After successful deployment and Event Grid setup, when you upload a file to blob storage, you should see this in your Azure Function logs:

```
🎉 HELLO! New file uploaded to blob storage!

📁 File: test-hello-1723456789.txt
🔗 URL: https://aimldocs.blob.core.windows.net/docs/test-hello-1723456789.txt
⏰ Time: 2025-08-07T10:00:00Z
📧 Event Type: Microsoft.Storage.BlobCreated
📋 Subject: /blobServices/default/containers/docs/blobs/test-hello-1723456789.txt

✅ Event Grid trigger is working perfectly!
```

## 🚨 **Troubleshooting**

### Function Not Found After Deployment
- Check that `SimpleEventGridTest` folder has both `__init__.py` and `function.json`
- Verify the function.json has correct Event Grid trigger configuration

### Deployment Fails
- Make sure you're in the correct directory (`/home/azureuser/blob_trigger`)
- Check that `requirements.txt` and `host.json` exist
- Verify Azure CLI is logged in: `az account show`

### Event Grid Not Triggering
- Ensure Event Grid subscription is created correctly
- Check the function URL is accessible
- Verify blob storage account has the correct resource ID in the subscription

## 💡 **Quick Start Command**

If you just want to deploy quickly using Azure Functions Core Tools:

```bash
# One-liner deployment (replace with your function app name)
cd /home/azureuser/blob_trigger && func azure functionapp publish YOUR-FUNCTION-APP-NAME
```

Your hello message function is ready to go live! 🚀
