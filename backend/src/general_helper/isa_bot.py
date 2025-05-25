"""
AI usage class
POTENTIALLY build encorporation of multiple AI sources to facilitate uses
USAGE:

"""

import os
from dotenv import load_dotenv
from openai import OpenAI


class AIBot:
    """
    Each object should be built and used for one convo/group of prompts
    """

    def __init__(self, ai_source: str = "gpt"):
        # Load environment variables from .env file
        load_dotenv()
        self.api_key = ""
        if ai_sourse == "gpt":
            # Read the OpenAI API secret key
            self.api_key = os.getenv("OPENAI_KEY")
            if not self.api_key:
                raise ValueError("OpenAI API key not found in .env file")

        else:
            raise ValueError("ai source bad")
        self.ai_client = OpenAI()
