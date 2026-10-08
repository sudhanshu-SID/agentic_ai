def chunk_text (text: str, chunk_size: int, overlap:int)->list[str]:
    """" 
    Splits a large text into smaller chunks of `chunk_size` characters.
    `overlap` ensures we odn't cut a sentence in half and lose context! 

    """
    chunks= []
    start = 0

    while start<len(text):
        
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)

        start += (chunk_size - overlap)
    return chunks

if __name__=="__main__":
        company_policy =  """
        Welcome to NexusCorp! Here are the core policies for 2026.
        1. Remote Work: Employees can work remotely 3 days a week. Tuesdays and Thursdays are mandatory in-office days for team collaboration.
        2. Vacation: Every employee gets 20 days of paid time off (PTO) per year. Unused PTO does not roll over to the next year.
        3. IT Equipment: Upon joining, you will receive a laptop and a $500 stipend for your home office.
        """

        print(f"Total Document Length: {len(company_policy)} characters \n")

        print("---Experiment 1: Small chunks (size =50, overlap = 10) ---")

        small_chunks = chunk_text(company_policy, chunk_size = 50, overlap = 10)
        for i, chunk in enumerate (small_chunks):
            print(f"Chunk {i+1}: '{chunk.strip()}'")

        print("--- Experiment 2: medium chunks (size = 100), overlap = 20")

        medium_chunks = chunk_text(company_policy, chunk_size = 100, overlap = 20)
        for i, chunk in enumerate(medium_chunks):
            print(f"Chunk: {i+1}, '{chunk.strip()}'")
