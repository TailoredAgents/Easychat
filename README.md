# 🤖 Universal Chat + Doc QA Web App

A powerful Streamlit web application that combines general chatbot capabilities with document analysis using OpenAI's Assistants API. Ask any question or upload documents for intelligent analysis - all in one seamless chat interface.

## ✨ Features

- **Dual Mode Operation**: General chatbot + document Q&A in the same chat thread
- **Multi-format Support**: PDF, CSV, XLSX, TXT, DOCX files
- **Model Selection**: Choose between GPT-4o (highest quality) or GPT-4o-mini (faster & cheaper)
- **Secure Authentication**: Built-in login system
- **Persistent Sessions**: Chat history and file attachments maintained throughout session
- **Modern UI**: Clean, responsive Streamlit interface

## 🚀 Quick Start

### 1. Clone and Setup

```bash
git clone <your-repo-url>
cd universal-chatbot
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Environment Configuration

```bash
cp .env.example .env
# Edit .env and add your OpenAI API key
```

Required environment variables:
- `OPENAI_API_KEY`: Your OpenAI API key from https://platform.openai.com/api-keys
- `MODEL_NAME`: Either `gpt-4o` or `gpt-4o-mini` (optional, defaults to gpt-4o)

### 3. Run Locally

```bash
streamlit run app.py
```

Navigate to `http://localhost:8501` and log in with:
- **Username**: `admin` **Password**: `admin123`
- **Username**: `user` **Password**: `user123`

## 📖 Usage Guide

### General Chat Mode
1. Simply type any question in the chat input
2. Get intelligent responses on any topic (news, math, coding, etc.)

### Document Analysis Mode
1. Upload documents using the sidebar file uploader
2. Click "🔄 Process Uploaded Files" 
3. Ask questions about your documents in the same chat interface
4. The AI will reference and analyze your uploaded files

### Supported File Types
- **PDF**: Text extraction and analysis
- **CSV/XLSX**: Data analysis with code interpreter
- **TXT**: Plain text analysis  
- **DOCX**: Microsoft Word document analysis

## 🔧 Configuration Options

### Model Selection
Choose your preferred model in the sidebar:
- **GPT-4o**: Highest quality responses, better reasoning
- **GPT-4o-mini**: Faster responses, lower cost

### Authentication
Demo credentials are provided for testing. For production use:
1. Update the `authentication_config` in `app.py`
2. Consider integrating with proper identity providers (Auth0, Google, etc.)

## 🌐 Deployment

### Streamlit Cloud
1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your repository
4. Add `OPENAI_API_KEY` in the secrets section
5. Deploy!

### Docker Deployment
```bash
# Create Dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]

# Build and run
docker build -t universal-chat .
docker run -p 8501:8501 --env-file .env universal-chat
```

### Production Considerations
- Set up proper SSL/TLS certificates
- Configure environment variables securely
- Implement proper user management
- Set up monitoring and logging
- Consider using a reverse proxy (nginx)

## 🛠 Technical Architecture

- **Frontend**: Streamlit web framework
- **AI Engine**: OpenAI Assistants API with file_search and code_interpreter tools
- **Authentication**: streamlit-authenticator with bcrypt
- **File Processing**: OpenAI Files API for document uploads
- **Session Management**: Streamlit session state

## 🔍 How It Works

1. **Assistant Creation**: One OpenAI assistant per session with retrieval and code interpreter tools
2. **Thread Management**: Persistent conversation thread maintains chat context
3. **File Handling**: Documents uploaded to OpenAI and attached to messages
4. **Dual Processing**: 
   - `file_search` tool for text-based documents (PDF, TXT, DOCX)
   - `code_interpreter` tool for structured data (CSV, XLSX)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and test thoroughly
4. Submit a pull request

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 🆘 Troubleshooting

### Common Issues

**"OPENAI_API_KEY not found"**
- Ensure your `.env` file exists and contains the correct API key
- Verify the API key is valid at https://platform.openai.com

**Authentication fails**
- Use the demo credentials: admin/admin123 or user/user123
- Check that streamlit-authenticator is properly installed

**File upload issues**
- Ensure files are in supported formats
- Check file size limits (OpenAI has upload limits)
- Verify network connectivity

**Assistant creation fails**
- Check your OpenAI API quota and billing
- Ensure you have access to the selected model (gpt-4o/gpt-4o-mini)

## 📞 Support

For issues or questions:
1. Check the troubleshooting section above
2. Review OpenAI's [API documentation](https://platform.openai.com/docs)
3. Open an issue in this repository

---

**Ready to chat with your documents? Get started in under 5 minutes!** 🚀 