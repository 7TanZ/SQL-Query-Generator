import streamlit as st
import requests

# API configuration
API_KEY = "CS2iq3kE5NTmtA97BjhkmprNEya6EuQH"
API_ENDPOINT = "https://api.mistral.ai/v1/chat/completions"

# Static context to guide the AI in generating SQL queries
static_context = """
You are an expert SQL Query Generator and Debugger.
Given a natural language query description, generate a well-optimized SQL query.
Provide an explanation of the query and suggest possible optimizations.
Ensure the query is syntactically correct and follows best practices.
"""

def call_mistral_api(prompt):
    """Calls the Mistral API's chat completions endpoint with the given prompt."""
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "open-mixtral-8x22b",  # Replace with the desired model ID
        "messages": [{"role": "user", "content": prompt}]
    }
    try:
        response = requests.post(API_ENDPOINT, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        return result.get("choices", [])[0].get("message", {}).get("content", "")
    except requests.exceptions.RequestException as e:
        return f"An error occurred: {e}"
    except (IndexError, KeyError) as e:
        return f"Unexpected response format: {e}"

def main():
    """Main function to run the Streamlit app."""
    # Centered Title and Subheader
    st.markdown(
        """
        <h1 style='text-align: center;'>SQL Query Generator & Debugger</h1>
        <h3 style='text-align: center; font-weight: normal;'>Generate optimized SQL queries from natural language descriptions</h3>
        """,
        unsafe_allow_html=True
    )

    # Input Section
    st.markdown("---")
    st.header("Enter Query Description")
    query_description = st.text_area("Describe your SQL query:", placeholder="e.g., Find the top 5 highest-paid employees in a company")
    
    # Button to Generate SQL Query
    if st.button("Generate SQL Query"):
        if not API_KEY or not API_ENDPOINT:
            st.error("API key or endpoint is missing. Please check your configuration.")
            return
        
        # Construct prompt
        prompt = f"{static_context}\n\nUser Input:\n{query_description}\n"
        output = call_mistral_api(prompt)
        
        # Display results
        st.markdown("### Generated SQL Query:")
        st.code(output, language='sql')

# Run the main function
if __name__ == "__main__":
    main()
