import argparse
from pydantic import BaseModel, Field
import requests
import json
import os
from dotenv import load_dotenv
from google import genai 
from google.genai import types 


class JobRequirements(BaseModel):
    role_title: str
    required_skills : list[str]
    experience_level : str
    matched_skills: list[str]
    missing_skills: list[str]
    interview_topics : list[str]

my_resume = """
I am a software engineer with 3 years of experience.
I know python, react and SQL
I have build web applications and APIs
I am looking for a software engineer role
"""

def main():

    parser = argparse.ArgumentParser(description= "Job Description Analyzer CLI")
    # This line creates our main "parser" object. It's like setting up a tool that knows how to read command-line arguments. 
    # The 'description' is what shows up at the top when someone runs the program with '-h' for help.

    parser.add_argument("job_input", help = "The job description text or URL analyze")
    # Here, we tell our parser to expect one specific piece of information from the user. 
    # We name it "job_input". Because it doesn't have a '--' in front of it, it's a required "positional" argument.
    # The 'help' text is what explains this argument in the help menu.

    args = parser.parse_args()
    # This line is where the action happens! It tells the parser to actually look at what the user typed in the terminal, 
    # process it according to the rules we set up above, and store the result in a variable called "args".
    # 1. We define the URL of the API we want to call
    # api_url = "https://jsonplaceholder.typicode.com/posts/1"
    
    # # 2. We use requests.get() to send an HTTP GET request to that URL
    # response = requests.get(api_url)
    
    # # 3. The API sends back data in JSON format, which we convert into a Python dictionary
    # api_data = response.json()

    
    print(f"Analyzing: {args.job_input}")
    # Finally, we access the information the user provided using 'args.job_input' and print it out to the screen.
    # print(api_data)

    prompt = f"""
    
    You are an expert techincal recruiter.
    Compare the following Resume to the Job description.

    Resume: {my_resume}

    job Description: {args.job_input}

    Analyze the match and return a JSON response matching the required schema.
    
    """
    load_dotenv()
    client = genai.Client(api_key = os.getenv("GEMINI_API_KEY"))

    print("Wait for some moment we're getting you job description match with your resume...")
    
    try:
        response = client.models.generate_content (
            model = "gemini-3.5-flash",
            contents = prompt,
            config = types.GenerateContentConfig(
                response_mime_type = "application/json",
                response_schema = JobRequirements
            ),
        )

        print("--AI RESPONSE ---")
        job = JobRequirements.model_validate_json(response.text)
        print("\n ---EXTRACTED DATA ---")
        print(" Required Skills:  ",job.required_skills)

    except Exception as e:
        print(f"Oops! the API call failed: {e}")
        return
    # try:

    #     with open("dummy_response.json",'r') as file:

    #         api_data = json.load(file)
    #         print("successfully loaded data!")

    #         job = JobRequirements(**api_data)
    #         print(job)
    #     with open("output.json",'w') as out_file:
    #         json_string = job.model_dump_json(indent = 2)
    #         out_file.write(json_string)

    #         print("Successfully saved results to output.json!")

    # except FileNotFoundError:
    #     print("could not find the dummy response.json file")
    #     return

if __name__ == "__main__":
    main()
