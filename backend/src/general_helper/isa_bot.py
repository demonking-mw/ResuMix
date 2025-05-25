"""
AI usage class
POTENTIALLY build encorporation of multiple AI sources to facilitate uses
USAGE:

"""

import os
from dotenv import load_dotenv
from openai import OpenAI
from openai.types.chat import ChatCompletion


class AIBot:
    """
    Each object should be built and used for one convo/group of prompts
    """

    def __init__(
        self, ai_source: str = "gpt", default_model: str = "gpt-4o-mini"
    ) -> None:
        # Load environment variables from .env file
        load_dotenv()
        self.api_key = ""
        if ai_source == "gpt":
            # Read the OpenAI API secret key
            self.api_key = os.getenv("OPENAI_KEY")
            if not self.api_key:
                raise ValueError("OpenAI API key not found in .env file")

        else:
            raise ValueError("ai source bad")
        self.ai_client = OpenAI(api_key=self.api_key)
        self.default_model = default_model

    def response_simple(
        self, prompt: str, model: str = None, token_limit: int = 2000
    ) -> str:
        """
        Get a simple response from the AI
        :param prompt: The prompt to send to the AI
        :param model: The model to use (optional, defaults to self.default_model)
        :return: The AI's response as a string
        """
        if model is None:
            model = self.default_model

        response = self.ai_client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=token_limit,
            temperature=0.7,
        )
        return response.choices[0].message.content.strip()

    def response_instruction(
        self, prompt: str, instruction: str, model: str = None, token_limit: int = 2000
    ) -> str:
        """
        Get a response from the AI with an instruction
        :param prompt: The prompt to send to the AI
        :param instruction: The instruction to give to the AI
        :param model: The model to use (optional, defaults to self.default_model)
        :return: The AI's response as a string
        """
        if model is None:
            model = self.default_model

        response = self.ai_client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": instruction},
                {"role": "user", "content": prompt},
            ],
            max_tokens=token_limit,
            temperature=0.7,
        )
        return response.choices[0].message.content.strip()

    def response_dict(
        self,
        prompt_dict: dict,
        model: str = None,
        token_limit: int = 2000,
        response_temperature: float = 0.7,
    ) -> ChatCompletion:
        """
        Get a response from the AI using a dictionary of prompts
        :param prompt_dict: A dictionary where keys are roles and values are messages
        :param model: The model to use (optional, defaults to self.default_model)
        :param response_temperature: The temperature to use for the response (default is 0.7)
        :return: The AI's response as a string
        NOTE: the keys in prompt_dict should be 'system', 'user', or 'assistant' and its value is the content
        """
        if model is None:
            model = self.default_model

        messages = [
            {"role": role, "content": content} for role, content in prompt_dict.items()
        ]

        response = self.ai_client.chat.completions.create(
            model=model,
            messages=messages,
            max_tokens=token_limit,
            temperature=response_temperature,
        )
        return response
