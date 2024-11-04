# PowerpointChain

PowerpointChain is an automated PowerPoint generation tool that leverages Azure OpenAI and other APIs to create slides with text and images. The application fetches web content, processes it, and generates a PowerPoint presentation.

## Features

- Fetches content from web pages using the Bing Search API.
- Uses Azure OpenAI to generate text content for slides.
- Generates images for slides using the DALL-E API.
- Saves the generated slides to Azure storage.
- Provides a Streamlit interface for user interaction.

## Installation

### Prerequisites

- Python 3.9
- Docker (optional, for containerized deployment)

### Steps

1. Clone the repository:
   ```
   git clone https://github.com/zecloud/powerpointchain.git
   cd powerpointchain
   ```

2. Install the required Python packages:
   ```
   pip install -r requirements.txt
   ```

3. Set the environment variables:
   ```
   export OPENAIAPIKEY=<your_openai_api_key>
   export DALLEOPENAIAPIKEY=<your_dalle_api_key>
   export RESOURCE_NAME=<your_azure_resource_name>
   export DEPLOYMENT_NAME=<your_azure_deployment_name>
   export DALLE_RESOURCE_NAME=<your_dalle_resource_name>
   export BING_ENDPOINT=<your_bing_search_endpoint>
   ```

4. Run the Streamlit app:
   ```
   streamlit run app.py
   ```

## Usage

1. Open the Streamlit app in your browser at `http://localhost:8501`.
2. Enter the prefix for the file name in the sidebar.
3. Enter your query in the chat input to generate slides.
4. The generated slides will be saved to Azure storage.

## Deployment

To deploy the application using Azure Container Apps, use the provided `deploy.sh` script in the `infra` directory:

```
cd infra
./deploy.sh
```

Make sure to set the necessary environment variables in the `deploy.sh` script before running it.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [LangChain](https://github.com/langchain/langchain)
- [Streamlit](https://github.com/streamlit/streamlit)
- [Azure OpenAI](https://azure.microsoft.com/en-us/services/cognitive-services/openai-service/)
- [DALL-E](https://openai.com/dall-e/)
