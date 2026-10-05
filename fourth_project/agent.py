import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from tavily import TavilyClient

# Load secret API keys from the .env file into environment variables
load_dotenv()

# Initialize the Tavily API client to search the web
tavily_client = TavilyClient(api_key=os.environ.get("TAVILY_API_KEY"))

# Initialize the Gemini AI client
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

def search_web(query: str) -> str:
    """Searches the web for current events, news, and real-time information."""
    print(f"Searching the web for: {query}")
    try:
        # Perform the actual web search using Tavily
        response = tavily_client.search(query)
        # Return the results as a string so the AI can read them
        return str(response.get("results", []))
    except Exception as e:
        # If the search API fails, we don't crash. We return the error to the AI!
        print(f"There is a failure in the web search {e} ")
        return f"Failed to get the information from the web {str(e)}"

def send_email(to_address: str, subject: str, body: str) -> str:
    """Send an email to the user"""
    # A dummy tool to demonstrate sensitive actions
    print(f"[ACTION]: pretending to send email to {to_address}...")
    return f"Success: Email sent to {to_address}."

def run_agent(user_prompt: str):
    print(f"User: {user_prompt}")

    # Create a chat session. This automatically handles State/History for us.
    chat = client.chats.create(
        model="gemini-3.5-flash",
        config=types.GenerateContentConfig(
            # Pass our Python functions to the AI so it knows what tools it can use
            tools=[search_web, send_email],
            # Temperature=0.2 keeps the AI factual and strictly logical (less creative)
            temperature=0.2, 
            # Disable automatic execution so WE control the loop (enabling human approval)
            automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True)
        )
    )

    # Max iterations prevent the agent from getting stuck in an infinite loop
    MAX_ITERATION = 5
    current_iteration = 0

    # Send the initial user prompt to the Brain (Gemini)
    response = chat.send_message(user_prompt)

    # The Agent Loop: Keep running until we hit the max iterations or the AI is finished
    while current_iteration < MAX_ITERATION:
        
        # Check if the AI decided it needs to call one of our tools
        if response.function_calls:
            
            # Loop through all the tools the AI wants to call
            for function_call in response.function_calls:
                tool_name = function_call.name 
                args = function_call.args
                
                # --- Human Approval Checkpoint ---
                SENSITIVE_TOOL = ["send_email"]
                if tool_name in SENSITIVE_TOOL:
                    print(f"\n⚠️ The agent wants to use a sensitive tool: {tool_name}")
                    print(f"Arguments: {args}")
                    
                    # Ask the human for permission before executing
                    approval = input("Do you approve this action? [y/n]: ")
                    if approval.lower() != 'y':
                        print("Access Denied")
                        # Tell the AI that the human said NO
                        response = chat.send_message("Error: permission denied")    
                        current_iteration += 1
                        continue # Skip execution and go to the next iteration

                # --- Direct Execution ---
                # Execute the specific tool requested by the AI
                if tool_name == "search_web":
                    result = search_web(args["query"])
                elif tool_name == "send_email":
                    result = send_email(args["to_address"], args["subject"], args["body"])
                
                print(f"[Agent Action]: sending {tool_name} results back to the brain...")
                
                # Send the tool's result back to the AI so it can read it
                response = chat.send_message(result)
                current_iteration += 1
                
        else:
            # Exit Condition: If response.function_calls is empty, the AI has a final answer!
            print("\nFinal Answer: ")
            print(response.text)
            break # Break out of the while loop completely

    # If the loop finished but we hit the max iterations, print a warning
    if current_iteration >= MAX_ITERATION:
        print("Maximum limit reached. Agent loop terminated.")

if __name__ == "__main__":
    # Start the agent with a complex prompt that requires multiple tools
    run_agent("Search for the latest news on Anthropic and then send an email to boss@company.com with a summary.")
