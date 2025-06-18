"""
AI usage class
POTENTIALLY build encorporation of multiple AI sources to facilitate uses
USAGE:

"""

import ast
import os
from dotenv import load_dotenv
from openai import OpenAI
from openai.types.chat import ChatCompletion
from typing import Type, TypeVar, Any


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
        self.total_tokens = 0

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
        self.total_tokens += response.usage.total_tokens
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
        self.total_tokens += response.usage.total_tokens
        return response.choices[0].message.content.strip()

    def pythoned_response_instruction(
        self,
        prompt: str,
        instruction: str,
        datatype: type,
        model: str = None,
        token_limit: int = 2000,
        retries: int = 3,
        temperature: float = 0.1,
    ) -> "datatype":
        """
        Get a response from the AI with an instruction and parse it into a specific type
        Have up to retries attempts to get valid response
        """
        if model is None:
            model = self.default_model
        messages = [
            {"role": "system", "content": instruction},
            {"role": "user", "content": prompt},
        ]
        for attempt in range(retries):
            resp = self.ai_client.chat.completions.create(
                model=model,
                messages=messages,
                max_tokens=token_limit,
                temperature=temperature,
            )
            self.total_tokens += resp.usage.total_tokens
            reply = resp.choices[0].message.content.strip()
            try:
                parsed = ast.literal_eval(reply)
                if isinstance(parsed, datatype):
                    return parsed
                else:
                    print(
                        f"Attempt {attempt + 1}: Parsed type mismatch. Expected {datatype}, got {type(parsed)}"
                    )
            except (SyntaxError, ValueError) as e:
                print(f"Attempt {attempt + 1}: Error parsing response: {e}")
                messages.append({"role": "assistant", "content": reply})
                correction = (
                    f"Your last response was not a valid {datatype.__name__}. \n"
                    f"Please ensure your response is a valid Python {datatype.__name__}.\n"
                )
                message.append({"role": "user", "content": correction})
                time.sleep(0.1)  # Optional: wait before retrying
        print(f"Failed to get a valid response after {retries} attempts.")
        return None

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
        self.total_tokens += response.usage.total_tokens
        return response
