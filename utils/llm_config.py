# utils/llm_config.py
import os
import time # Import time for potential retry delays

# Global LLM variable, initialized to None
llm = None

def setup_llm():
    """
    Sets up the Large Language Model (LLM) provider.
    Tries to configure Gemini first, then falls back to OpenAI if Gemini fails.
    The configured LLM instance is stored in the global 'llm' variable.
    """
    global llm # Declare 'llm' as global to modify the module-level variable
    print("Setting up LLM provider...")

    # Try Gemini with better error handling and retry logic
    try:
        from langchain_google_genai import ChatGoogleGenerativeAI
        google_api_key = os.getenv('GOOGLE_API_KEY') # Retrieve API key from environment variables

        if google_api_key and google_api_key.strip():
            print("✓ Attempting to use Google Gemini (gemini-1.5-flash-latest)...")
            
            # Initialize Gemini LLM with specified model, temperature, and token limits
            # Also includes request timeout and max retries for robustness
            gemini_llm_instance = ChatGoogleGenerativeAI(
                model="gemini-1.5-flash-latest",
                temperature=0.3, # Controls creativity of the response
                max_tokens=2000, # Maximum number of tokens in the generated response
                convert_system_message_to_human=True, # Converts system messages to human messages
                request_timeout=60, # Timeout for each API request in seconds
                max_retries=2 # Number of retries for failed requests
            )
            
            # Test the Gemini connection
            try:
                print("Testing Gemini connection...")
                test_response = gemini_llm_instance.invoke("Hello, please respond with 'Gemini ready'.")
                if test_response and "Gemini ready" in (test_response.content if hasattr(test_response, 'content') else str(test_response)):
                    print("✓ Gemini connection successful")
                    llm = gemini_llm_instance # Assign the successful instance to the global llm
                    return
                else:
                    print(f"❌ Gemini test failed: Unexpected response. {test_response.content if hasattr(test_response, 'content') else str(test_response)}")
            except Exception as test_error:
                print(f"❌ Gemini test failed during invoke: {test_error}")
        else:
            print("❌ Google API key (GOOGLE_API_KEY) not found or empty.")
    except ImportError:
        print("❌ 'langchain_google_genai' not installed. Skipping Gemini setup.")
    except Exception as e:
        print(f"❌ Gemini setup experienced an unexpected error: {e}")

    # Fallback to OpenAI if Gemini setup or test failed
    if llm is None: # Only try OpenAI if Gemini wasn't successfully set up
        try:
            from langchain_openai import ChatOpenAI
            openai_api_key = os.getenv('OPENAI_API_KEY') # Retrieve OpenAI API key

            if openai_api_key and openai_api_key.strip():
                print("✓ Attempting to use OpenAI GPT-3.5-turbo (Fallback)...")
                # Initialize OpenAI LLM
                openai_llm_instance = ChatOpenAI(
                    model="gpt-3.5-turbo", # Using a common and cost-effective model
                    temperature=0.3,
                    max_tokens=2000,
                    request_timeout=120, # Increased timeout for OpenAI
                    openai_api_key=openai_api_key
                )
                
                # Test the OpenAI connection
                try:
                    print("Testing OpenAI connection...")
                    test_response = openai_llm_instance.invoke("Hello, please respond with 'OpenAI ready'.")
                    if test_response and "OpenAI ready" in (test_response.content if hasattr(test_response, 'content') else str(test_response)):
                        print("✓ OpenAI connection successful")
                        llm = openai_llm_instance # Assign the successful instance to the global llm
                        return
                    else:
                        print(f"❌ OpenAI test failed: Unexpected response. {test_response.content if hasattr(test_response, 'content') else str(test_response)}")
                except Exception as test_error:
                    print(f"❌ OpenAI test failed during invoke: {test_error}")
            else:
                print("❌ OpenAI API key (OPENAI_API_KEY) not found or empty.")
        except ImportError:
            print("❌ 'langchain_openai' not installed. Skipping OpenAI setup.")
        except Exception as e:
            print(f"❌ OpenAI setup experienced an unexpected error: {e}")

    # If no LLM could be set up
    if llm is None:
        print("⚠️ No LLM available. The system will operate in fallback (non-AI) mode.")

def test_llm_simple():
    """
    Tests the functionality of the globally configured LLM.
    Returns True if the LLM responds as expected, False otherwise.
    """
    global llm
    if not llm:
        print("LLM is not initialized for testing.")
        return False

    try:
        print("Initiating simple LLM functionality test...")
        # A specific prompt to ensure the LLM is responding and is callable
        response = llm.invoke("Hello! Please respond with 'LLM is working correctly.'")
        if response:
            content = response.content if hasattr(response, 'content') else str(response)
            if "LLM is working correctly." in content:
                print(f"✓ LLM test successful. Response snippet: '{content.strip()[:50]}...'")
                return True
            else:
                print(f"❌ LLM test failed: Unexpected response. Full response: '{content.strip()}'")
                return False
        else:
            print("❌ LLM test failed: No response object received.")
            return False
    except Exception as e:
        print(f"❌ LLM test encountered an error: {e}")
        return False
