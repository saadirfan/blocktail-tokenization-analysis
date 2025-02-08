#!/usr/bin/env python3

import json
import sys
import os
from typing import Dict, Any, List
import sentencepiece as spm
from transformers import AutoTokenizer
import tiktoken
from dotenv import load_dotenv

# Load the .env file
load_dotenv()

class TokenizerTest:
    def __init__(self):
        # Define available tokenizers and their configurations
        self.tokenizers = {
            "gpt4": {
                "name": "gpt-4",
                "type": "tiktoken"
            },
            "gpt35": {
                "name": "gpt-3.5-turbo",
                "type": "tiktoken"
            },
            "llama3": {
                "name": "meta-llama/Meta-Llama-3-70B",
                "type": "transformers"
            },
            "mistral": {
                "name": "mistralai/Mistral-7B-v0.3",
                "type": "transformers"
            },
            "bert": {
                "name": "bert-base-uncased",
                "type": "transformers"
            },
            "roberta": {
                "name": "roberta-base",
                "type": "transformers"
            },
            "t5": {
                "name": "t5-base",
                "type": "transformers"
            },
            "gpt2": {
                "name": "gpt2",
                "type": "transformers"
            },
            "spiece": {
                "name": "spiece.model",
                "type": "sentencepiece"
            }
        }

    def get_tokenizer(self, tokenizer_id: str) -> Any:
        """Load the specified tokenizer."""
        if tokenizer_id not in self.tokenizers:
            raise ValueError(f"Unknown tokenizer: {tokenizer_id}")
        
        config = self.tokenizers[tokenizer_id]
        
        if config["type"] == "sentencepiece":
            sp = spm.SentencePieceProcessor()
            sp.load(config["name"])
            return sp
        elif config["type"] == "tiktoken":
            return tiktoken.encoding_for_model(config["name"])
        else:  # transformers
            token = os.getenv("HF_AUTH_TOKEN")  # Use token from environment
            return AutoTokenizer.from_pretrained(config["name"], token=token)

    def tokenize(self, text: str, tokenizer_id: str, tokenizer: Any) -> Dict:
        """Tokenize text using the specified tokenizer."""
        config = self.tokenizers[tokenizer_id]
        
        if config["type"] == "sentencepiece":
            tokens = tokenizer.encode_as_pieces(text)
        elif config["type"] == "tiktoken":
            tokens = tokenizer.encode(text)
        else:  # transformers
            tokens = tokenizer.tokenize(text)

        return {
            "input": text,
            "tokens": tokens,
            "num_tokens": len(tokens)
        }

def process_tokenizer(tester: TokenizerTest, tokenizer_name: str, test_cases: Dict[str, List[str]], results_dir: str):
    """Process a single tokenizer."""
    results_path = os.path.join(results_dir, f"{tokenizer_name}_results.json")

    try:
        tokenizer = tester.get_tokenizer(tokenizer_name)
        results = {}
        for naming_convention, examples in test_cases.items():
            results[naming_convention] = []
            for example in examples:
                try:
                    result = tester.tokenize(example, tokenizer_name, tokenizer)
                    results[naming_convention].append(result)
                except Exception as e:
                    print(f"Error processing example '{example}' with {tokenizer_name}: {str(e)}")
                    continue

        with open(results_path, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        print(f"Results saved to {results_path}")
        return True

    except Exception as e:
        print(f"Error initializing or processing tokenizer '{tokenizer_name}': {str(e)}")
        return False

def main():
    """
    Usage: python tokenize_tests.py <tokenizer_name>
    Example: python tokenize_tests.py gpt2
             python tokenize_tests.py all
    """
    if len(sys.argv) != 2:
        print("Usage: python tokenize_tests.py <tokenizer_name>")
        print("\nAvailable tokenizers:")
        tester = TokenizerTest()
        for name in tester.tokenizers.keys():
            print(f"  - {name}")
        sys.exit(1)

    tokenizer_name = sys.argv[1]

    # Setup paths
    test_cases_path = "data/test_cases.json"
    results_dir = "results"
    os.makedirs(results_dir, exist_ok=True)

    # Create data directory if test_cases.json doesn't exist
    if not os.path.exists(test_cases_path):
        os.makedirs(os.path.dirname(test_cases_path), exist_ok=True)
        sample_cases = {
            "traditional": [
                "product-card featured",
                "sidebar-navigation active",
                "header-logo dark-theme"
            ],
            "blocktail": [
                "product_card --featured",
                "sidebar_navigation --active",
                "header_logo --dark_theme"
            ]
        }
        with open(test_cases_path, "w", encoding="utf-8") as f:
            json.dump(sample_cases, f, indent=2)
        print(f"Created sample test cases in {test_cases_path}")

    # Load test cases
    try:
        with open(test_cases_path, "r", encoding="utf-8") as f:
            test_cases = json.load(f)
    except Exception as e:
        print(f"Error loading test cases: {str(e)}")
        sys.exit(1)

    tester = TokenizerTest()

    if tokenizer_name == "all":
        success = []
        failed = []
        for name in tester.tokenizers.keys():
            print(f"Processing tokenizer: {name}")
            if process_tokenizer(tester, name, test_cases, results_dir):
                success.append(name)
            else:
                failed.append(name)
        print("\nSummary:")
        print(f"  Successfully processed: {', '.join(success) if success else 'None'}")
        print(f"  Failed: {', '.join(failed) if failed else 'None'}")
    else:
        process_tokenizer(tester, tokenizer_name, test_cases, results_dir)

if __name__ == "__main__":
    main()
