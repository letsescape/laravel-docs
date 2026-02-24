import tiktoken


def get_token_count(text: str) -> int:
    """
    Return the number of tokens in a text string using the GPT-4 model encoding.
    
    Parameters:
        text (str): The input text to be tokenized.
    
    Returns:
        int: The number of tokens in the input text.
    """
    encoding = tiktoken.encoding_for_model("gpt-4")
    tokens = encoding.encode(text)

    return len(tokens)
