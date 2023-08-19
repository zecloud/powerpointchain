RESOURCE_GROUP=""
LOCATION="westeurope"
CONTAINERAPPS_ENVIRONMENT=""
OPENAI_API_KEY=""
APP_NAME=""
STORAGE_RG=""
STORAGE_NAME=""
REGISTRY_SERVER=""
az containerapp up \
  --name $APP_NAME \
  --source . \
  --location $LOCATION \
  --resource-group $RESOURCE_GROUP \
  --registry-server $REGISTRY_SERVER \
  --environment $CONTAINERAPPS_ENVIRONMENT
CONNECTIONSTRING=$(az storage account show-connection-string \
  --resource-group $STORAGE_RG \
  --name $STORAGE_NAME \
  --query connectionString \
  --output tsv)
az containerapp secret set \
  --name $APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --secrets qconnection-string=$CONNECTIONSTRING
az containerapp secret set \
  --name $APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --secrets openai-apikey=$OPENAI_API_KEY
az containerapp update \
  --name $APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --set-env-vars "AZURE_STORAGE_ACCOUNT_NAME=$STORAGE_NAME" "AZURE_STORAGE_CONNECTION_STRING=secretref:qconnection-string" "OPENAIAPIKEY=secretref:openai-apikey"
  