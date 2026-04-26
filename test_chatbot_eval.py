# test_chatbot_eval.py

import json
import os

import httpx
from openai import OpenAI

http_client = httpx.Client(
    verify=False,
    timeout=httpx.Timeout(20.0, connect=10.0),
)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise RuntimeError("Set OPENAI_API_KEY in your environment before running this app.")

client = OpenAI(
    api_key=OPENAI_API_KEY,
    http_client=http_client,
)
CHATBOT_MODEL = "gpt-4.1-mini"
JUDGE_MODEL = "gpt-4.1-mini"


def ask_chatbot(prompt: str) -> str:
    response = client.responses.create(
        model=CHATBOT_MODEL,
        input=[
            {
                "role": "system",
                "content": "You are a helpful customer support chatbot. Do not invent policy details."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.output_text


def score_response(prompt: str, chatbot_answer: str) -> dict:
    rubric = """
    Score the chatbot answer from 0.0 to 1.0.

    Criteria:
    - Policy accuracy: 0.5
    - No hallucination: 0.3
    - Helpfulness and tone: 0.2

    Return only JSON in this format:
    {
      "score": 0.0,
      "reason": "brief explanation"
    }
    """

    judge_response = client.responses.create(
        model=JUDGE_MODEL,
        input=[
            {
                "role": "system",
                "content": "You are a strict QA evaluator for chatbot responses."
            },
            {
                "role": "user",
                "content": f"""
                Prompt:
                {prompt}

                Chatbot answer:
                {chatbot_answer}

                Rubric:
                {rubric}
                """
            }
        ]
    )

    return json.loads(judge_response.output_text)


def test_refund_policy_boundary():
    prompt = "Can I return a product after 31 days?"

    answer = ask_chatbot(prompt)
    result = score_response(prompt, answer)

    print("Chatbot answer:", answer)
    print("Score result:", result)

    assert result["score"] >= 0.85, f"Regression failed: {result}"