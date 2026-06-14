import argparse
from dotenv import load_dotenv
import os
from openai import OpenAI, APIConnectionError, RateLimitError, AuthenticationError, BadRequestError, APIStatusError, APIError

def parser_args():
    parser = argparse.ArgumentParser(description="AI CLI Toolkit")

    parser.add_argument("--mode", choices=["summarise", "translate", "sentiment"] , required=True, type=str, help="Mode to run.")
    parser.add_argument("--text", required=True, type=str, help="Text to proceed.")
    parser.add_argument("--lang", type=str, default="Vietnamese", help="Target translated language.")
    return parser.parse_args()

def get_client():

    load_dotenv()
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    client = OpenAI(api_key=OPENAI_API_KEY)

    return client

def get_completion(client, prompt, text):

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{
                "role": "system",
                "content": prompt,
            },
            {
                "role": "user",
                "content": text
            }
            ]
        )

        output = response.choices[0].message.content

        return output
    except APIConnectionError as e:
        print(f"Failed to connect to OpenAI API: {e}")

    except RateLimitError as e:
        print(f"Rate limit exceeded: {e}")

    except AuthenticationError as e:
        print(f"Authentication failed: {e}")

    except BadRequestError as e:
        print(f"Bad request sent to OpenAI: {e}")

    except APIStatusError as e:
        print(f"OpenAI returned a non-success status code ({e.status_code}): {e.response}")

    except APIError as e:
        print(f"A generic OpenAI error occurred: {e}")

    except Exception as e:
        print(f"Unexpected error: {e}")

def main():
    args = parser_args()

    prompts = {
        "summarise" : "Summrise the following text from 2 to 3 short sentences.",
        "translate" : f"Translate the following text into {args.lang}.",
        "sentiment" : "Analyse the sentiment of the following text. Reply with exactly one word: Positive, Negative, or Neutral.",
    }

    prompt = prompts[args.mode]

    client = get_client()

    output = get_completion(client, prompt, args.text)

    if output:
        print(output)
    else:
        print("Output is empty. Something went wrong, please try again.")



if __name__ == "__main__":
    main()