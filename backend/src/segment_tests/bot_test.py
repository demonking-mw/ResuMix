"""
testing bot
"""

from ..general_helper.isa_bot import AIBot

ai_test = AIBot()
chat_input = {
    "developer": "You must not use more than 7 words per sentence",
    "user": "explain why pineapple juice is better than pineapple on pizza",
}
response = ai_test.response_dict(chat_input)
print(response)  # Should print a response from the AI
