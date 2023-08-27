RESOURCE_GROUP=""
LOCATION="westeurope"
CONTAINERAPPS_ENVIRONMENT=""
APP_NAME=""
STORAGE_RG=""
STORAGE_NAME=""
REGISTRY_SERVER=""
BING_SUBSCRIPTION_KEY=""
BING_ENDPOINT="https://api.bing.microsoft.com/v7.0/search"
RESOURCE_NAME=""
DEPLOYMENT_NAME=""
DALLE_RESOURCE_NAME=""
OPENAIAPIKEY=""
DALLEOPENAIAPIKEY=''
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
  --secrets openai-apikey=$OPENAIAPIKEY
  az containerapp secret set \
  --name $APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --secrets dalle-openai-apikey=$DALLEOPENAIAPIKEY
az containerapp secret set \
  --name $APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --secrets bing-skey=$BING_SUBSCRIPTION_KEY
az containerapp update \
  --name $APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --set-env-vars "AZURE_STORAGE_ACCOUNT_NAME=$STORAGE_NAME" "AZURE_STORAGE_CONNECTION_STRING=secretref:qconnection-string" \
  "OPENAIAPIKEY=secretref:openai-apikey" "DALLEOPENAIAPIKEY=secretref:dalle-openai-apikey" "BING_SUBSCRIPTION_KEY=secretref:bing-skey" "BING_ENDPOINT=$BING_ENDPOINT" \
  "RESOURCE_NAME=$RESOURCE_NAME" "DEPLOYMENT_NAME=$DEPLOYMENT_NAME" "DALLE_RESOURCE_NAME=$DALLE_RESOURCE_NAME"
  