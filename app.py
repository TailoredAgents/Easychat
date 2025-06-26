import streamlit as st
import openai
import os
import time
from dotenv import load_dotenv
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Universal Chat + Doc QA",
    page_icon="🤖",
    layout="wide"
)

# Simple authentication configuration with real bcrypt hashes
import bcrypt

# Generate password hashes (admin123 and user123)
def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

authentication_config = {
    'credentials': {
        'usernames': {
            'admin': {
                'email': 'admin@example.com',
                'name': 'Administrator',
                'password': '$2b$12$v0UQxza9FSOX0HKly.6.kug4e0ILwb03EKlHmhBbsxfpaK6ld8iZm'  # admin123
            },
            'user': {
                'email': 'user@example.com', 
                'name': 'Regular User',
                'password': '$2b$12$EteTxC1Uy/n7bixvxlp8Ee9Xvj8XqBXUEd1Fcvd3wHW9hVnPWJMAi'  # user123
            }
        }
    },
    'cookie': {
        'expiry_days': 30,
        'key': 'universal_chat_cookie',
        'name': 'universal_chat_cookie'
    }
}

def initialize_openai_client():
    """Initialize OpenAI client with API key from environment"""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        st.error("OPENAI_API_KEY not found in environment variables")
        st.stop()
    return openai.OpenAI(api_key=api_key)

def create_assistant(client, model_name):
    """Create or retrieve OpenAI assistant for the session"""
    if "assistant_id" not in st.session_state:
        try:
            assistant = client.beta.assistants.create(
                name="Universal Chat + Doc Bot",
                model=model_name,
                tools=[{"type": "file_search"}, {"type": "code_interpreter"}],
                instructions="You are a helpful assistant that can answer general questions and analyze uploaded documents. When documents are provided, reference them in your responses."
            )
            st.session_state.assistant_id = assistant.id
        except Exception as e:
            st.error(f"Failed to create assistant: {str(e)}")
            st.stop()
    return st.session_state.assistant_id

def create_thread(client):
    """Create or retrieve OpenAI thread for the session"""
    if "thread_id" not in st.session_state:
        try:
            thread = client.beta.threads.create()
            st.session_state.thread_id = thread.id
        except Exception as e:
            st.error(f"Failed to create thread: {str(e)}")
            st.stop()
    return st.session_state.thread_id

def upload_files_to_openai(client, uploaded_files):
    """Upload files to OpenAI and return file IDs"""
    file_ids = []
    
    if uploaded_files:
        for uploaded_file in uploaded_files:
            try:
                # Create a temporary file object that OpenAI can read
                file_obj = client.files.create(
                    file=uploaded_file,
                    purpose="assistants"
                )
                file_ids.append(file_obj.id)
                
                # Provide specific feedback based on file type
                filename = uploaded_file.name.lower()
                if filename.endswith(('.csv', '.xlsx', '.xls')):
                    st.success(f"✅ Uploaded: {uploaded_file.name} (Data Analysis)")
                elif filename.endswith(('.pdf', '.txt', '.docx')):
                    st.success(f"✅ Uploaded: {uploaded_file.name} (Text Search)")
                else:
                    st.success(f"✅ Uploaded: {uploaded_file.name}")
                    
            except Exception as e:
                st.error(f"❌ Failed to upload {uploaded_file.name}: {str(e)}")
    
    return file_ids

def send_message_and_get_response(client, thread_id, assistant_id, message, file_ids=None):
    """Send message to assistant and get response"""
    try:
        # Prepare attachments with appropriate tools based on file types
        attachments = []
        if file_ids:
            for file_id in file_ids:
                # Get file info to determine appropriate tools
                try:
                    file_info = client.files.retrieve(file_id)
                    filename = file_info.filename.lower() if hasattr(file_info, 'filename') else ""
                    
                    # Use code_interpreter for data files, file_search for text files
                    if filename.endswith(('.csv', '.xlsx', '.xls')):
                        tools = [{"type": "code_interpreter"}]
                    else:
                        tools = [{"type": "file_search"}]
                    
                    attachments.append({"file_id": file_id, "tools": tools})
                except:
                    # Default to both tools if we can't determine file type
                    attachments.append({"file_id": file_id, "tools": [{"type": "code_interpreter"}]})
        
        # Add message to thread
        client.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=message,
            attachments=attachments if attachments else None
        )
        
        # Create and run the assistant
        run = client.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=assistant_id
        )
        
        # Poll for completion
        with st.spinner("🤖 Thinking..."):
            while run.status in ["queued", "in_progress", "cancelling"]:
                time.sleep(1)
                run = client.beta.threads.runs.retrieve(
                    thread_id=thread_id,
                    run_id=run.id
                )
        
        if run.status == "completed":
            # Get the latest message
            messages = client.beta.threads.messages.list(thread_id=thread_id)
            latest_message = messages.data[0]
            return latest_message.content[0].text.value
        else:
            return f"❌ Run failed with status: {run.status}"
            
    except Exception as e:
        return f"❌ Error: {str(e)}"

def main():
    """Main application function"""
    
    # Initialize authenticator
    authenticator = stauth.Authenticate(
        authentication_config['credentials'],
        authentication_config['cookie']['name'],
        authentication_config['cookie']['key'],
        authentication_config['cookie']['expiry_days']
    )
    
    # Authentication
    try:
        authenticator.login()
    except Exception as e:
        st.error(f"Authentication error: {e}")
        return
    
    # Check authentication status from session state
    if st.session_state.get('authentication_status') == False:
        st.error('Username/password is incorrect')
        return
    elif st.session_state.get('authentication_status') == None:
        st.warning('Please enter your username and password')
        st.info("Demo credentials: admin/admin123 or user/user123")
        return
    
    # Main app content (only shown when authenticated)
    authenticator.logout('Logout', 'sidebar', key='unique_key')
    st.sidebar.write(f'Welcome *{st.session_state.get("name")}*')
    
    st.title("🤖 Universal Chat + Doc QA")
    st.markdown("Ask any question or upload documents for analysis!")
    
    # Initialize OpenAI client
    client = initialize_openai_client()
    
    # Sidebar configuration
    st.sidebar.header("⚙️ Configuration")
    
    # Model selection
    model_options = ["gpt-4.1-mini", "gpt-4o", "gpt-4o-mini"]
    selected_model = st.sidebar.selectbox(
        "Select Model",
        model_options,
        index=0,  # Default to gpt-4.1-mini (best for documents)
        help="💡 GPT-4.1 Mini: Best for documents (1M context, cheaper)\n🔥 GPT-4o: Highest quality\n⚡ GPT-4o Mini: Fastest/cheapest"
    )
    
    # File upload
    st.sidebar.header("📁 Document Upload")
    uploaded_files = st.sidebar.file_uploader(
        "Upload documents for analysis",
        accept_multiple_files=True,
        type=["pdf", "csv", "xlsx", "txt", "docx"],
        help="Upload documents to ask questions about them"
    )
    
    # Initialize session state
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "file_ids" not in st.session_state:
        st.session_state.file_ids = []
    
    # Create assistant and thread
    assistant_id = create_assistant(client, selected_model)
    thread_id = create_thread(client)
    
    # Handle file uploads
    if uploaded_files:
        if st.sidebar.button("🔄 Process Uploaded Files"):
            with st.sidebar:
                st.session_state.file_ids = upload_files_to_openai(client, uploaded_files)
    
    # Display current files
    if st.session_state.file_ids:
        st.sidebar.success(f"📎 {len(st.session_state.file_ids)} files attached")
    
    # Chat interface
    st.header("💬 Chat")
    
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask me anything or ask about your uploaded documents..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Get assistant response
        with st.chat_message("assistant"):
            response = send_message_and_get_response(
                client, 
                thread_id, 
                assistant_id, 
                prompt, 
                st.session_state.file_ids if st.session_state.file_ids else None
            )
            st.markdown(response)
        
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main() 