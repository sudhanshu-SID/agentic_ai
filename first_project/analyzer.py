import argparse

def main():

    parser = argparse.ArgumentParser(description= "Job Description Analyzer CLI")


    parser.add_argument("job_input", help = "The job description text or URL analyze")

    args = parser.parse_args()

    print(f"Analyzing: {args.job_input}")


if __name__ == "__main__":
    main()
