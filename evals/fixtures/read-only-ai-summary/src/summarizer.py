from openai import OpenAI


def summarize(text: str) -> str:
    client = OpenAI()
    response = client.responses.create(model="gpt-5-mini", input=text)
    return response.output_text
