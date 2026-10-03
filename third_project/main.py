import os
from dotenv import load_dotenv 
from google import genai 
from google.genai import types 


def get_weather(city:str) ->str:
    """Returns the current weather of the given city"""
    if city.lower() == "tokyo":
        return f"The weather in {city} is 20 degrees and sunny."
    elif city.lower() =="paris":
        return f"The weather in {city} is 10 degrees and cloudy."
    else:
        return f"The weather in {city} is unknown."


load_dotenv()
 
client = genai.Client()

try:
    # 1. Create a Chat Session. Unlike generate_content, chats remember history.
    chat = client.chats.create(
        model = "gemini-3.5-flash",
        # contents = "What is the weather in Tokyo?",
        config = types.GenerateContentConfig(
            tools = [get_weather], # Give Gemini the schema of our tool
            automatic_function_calling = types.AutomaticFunctionCallingConfig(disable = True) # Force it to give us the request manually
        )
    )
    
    print("Asking gemini...")
    # 2. Send the initial message. 
    response = chat.send_message("what is the weather in tokyo?")

    # 3. Check if Gemini decided to call a function instead of giving text
    if response.function_calls:
        
        # 4. Extract the specific function call it made
        tool_request = response.function_calls[0]
        function_name = tool_request.name 
        arguments = tool_request.args

        print(f"Gemini wants to run: {function_name} with args: {arguments}")

        # 5. Route the request to the correct python function
        if function_name == "get_weather":
            city_to_check = arguments["city"]

            # 6. Actually run our local code!
            function_result = get_weather(city_to_check)
            print(f"The result from our python code is: {function_result}")
            
            print("Sending the result back to gemini....")
            
            # 7. Package our result into a format Gemini can understand
            tool_response_part = types.Part.from_function_response(
                name = function_name,
                response = {"Result": function_result}
            )
            
            # 8. Send the packaged result back into the chat to get the final text answer
            final_response = chat.send_message(tool_response_part) 
            print("Final Answer:", final_response.text)

    # print("Response",response.text)
    # print("Function Calls", response.function_calls)
except genai.types.GenerateContentError as e:
    print("Error",e)
except Exception as e:
    print("Error",e)