# ai-evaluation-lab
ChatBotEvaluator- Failure-aware CI/CD framework for testing AI systems using evaluation datasets, scoring, and risk-based quality gates.

## Setup
1. pip install openai pytest
2. Set API key- $env:OPENAI_API_KEY="your_api_key_here"
3. pytest test_chatbot_eval.py -s

## Output
After running:
1. eval_results.json — raw evaluation results
2. chatbot_eval_report.html — human-readable report
