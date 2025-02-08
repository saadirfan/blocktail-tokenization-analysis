#!/usr/bin/env python3

"""
A script that analyzes and compares token usage across different CSS naming conventions using various tokenizers.

Processes JSON result files from the results/ directory and generates a markdown summary
with statistics and practical impact analysis.

Usage:
    python analysis_compiler.py
"""

import json
import glob
import numpy as np
import pandas as pd
from typing import Dict, List, Any
from collections import defaultdict

class TokenizationAnalyzer:
    def __init__(self, results_dir: str, iteration_cycles: int = 1):
        """
        Initialize the TokenizationAnalyzer.
        
        :param results_dir: Directory containing *_results.json files
        :param iteration_cycles: Number of times code might be refined iteratively (chain-of-thought)
        """
        self.results_dir = results_dir
        self.tokenizer_results = {}
        self.iteration_cycles = iteration_cycles
        self.load_results()

    def load_results(self):
        """
        Load all JSON results files from self.results_dir.
        Each file is named like: <tokenizer_name>_results.json
        """
        for filepath in glob.glob(f"{self.results_dir}/*_results.json"):
            tokenizer_name = filepath.split('/')[-1].replace('_results.json', '')
            with open(filepath, "r") as f:
                self.tokenizer_results[tokenizer_name] = json.load(f)

    def analyze_methodology(self, results: Dict[str, List[Dict]], methodology: str) -> Dict[str, Any]:
        """
        Compute basic statistics for a given naming methodology (Blocktail, Traditional, BEM).

        :param results: The dictionary of results for a specific tokenizer
        :param methodology: 'Blocktail' | 'Traditional' | 'BEM'
        :return: A dict with 'avg_tokens', 'token_range', 'by_complexity'
        """
        if methodology not in results:
            return {
                'avg_tokens': 0.0,
                'token_range': (0, 0),
                'by_complexity': {}
            }

        tokens = [entry['num_tokens'] for entry in results[methodology]]
        avg_tokens = np.mean(tokens) if tokens else 0.0
        token_range = (min(tokens), max(tokens)) if tokens else (0, 0)

        # Complexity measure: count markers in the input
        component_sizes = defaultdict(list)
        for entry in results[methodology]:
            input_str = entry['input']
            # Markers: each '--' or ' -' indicates a tail or mutation
            markers = input_str.count('--') + input_str.count(' -')
            component_sizes[markers].append(entry['num_tokens'])

        complexity_stats = {
            markers: np.mean(sizes) for markers, sizes in component_sizes.items()
        }

        return {
            'avg_tokens': avg_tokens,
            'token_range': token_range,
            'by_complexity': complexity_stats
        }

    def generate_summary(self) -> str:
        """Generate a Markdown summary of the analysis."""
        summary = ["# Tokenization Analysis Summary\n"]

        # Build comparison table data
        comparison_rows = []
        for tokenizer_name, data in self.tokenizer_results.items():
            blocktail_data = data.get("Blocktail", [])
            trad_data = data.get("Traditional", [])
            bem_data = data.get("BEM", [])

            if not blocktail_data or not trad_data:
                # Skip incomplete data
                continue

            blocktail_avg = np.mean([e["num_tokens"] for e in blocktail_data])
            trad_avg = np.mean([e["num_tokens"] for e in trad_data])
            bem_avg = np.mean([e["num_tokens"] for e in bem_data]) if bem_data else None

            # Calculate percentage reductions
            vs_trad = (trad_avg - blocktail_avg) / trad_avg * 100 if trad_avg > 0 else 0.0
            vs_bem = (bem_avg - blocktail_avg) / bem_avg * 100 if bem_avg else None

            row = {
                "Tokenizer": tokenizer_name,
                "Blocktail Avg": f"{blocktail_avg:.1f}",
                "Traditional Avg": f"{trad_avg:.1f}",
                "BEM Avg": f"{bem_avg:.1f}" if bem_avg else "N/A",
                "vs Trad.": f"{vs_trad:.1f}%",
                "vs BEM": f"{vs_bem:.1f}%" if vs_bem else "N/A",
            }
            comparison_rows.append(row)

        # Format the comparison table
        df = pd.DataFrame(comparison_rows)
        summary.append("## Cross Comparison\n")
        if not df.empty:
            summary.append(df.to_markdown(index=False))
        else:
            summary.append("*No valid data found.*")
        summary.append("\n")

        # Practical impact
        summary.append("## Practical Impact\n")
        all_savings = []
        for data in self.tokenizer_results.values():
            blocktail_info = self.analyze_methodology(data, "Blocktail")
            trad_info = self.analyze_methodology(data, "Traditional")
            bem_info = self.analyze_methodology(data, "BEM") if "BEM" in data else None

            if trad_info["avg_tokens"] > 0:
                all_savings.append(trad_info["avg_tokens"] - blocktail_info["avg_tokens"])
            if bem_info and bem_info["avg_tokens"] > 0:
                all_savings.append(bem_info["avg_tokens"] - blocktail_info["avg_tokens"])

        if all_savings:
            avg_savings = np.mean(all_savings)
            summary.append(f"- Average token reduction per component: {avg_savings:.1f} tokens\n")
            summary.append(f"- In a typical page with 20 components: {avg_savings * 20:.0f} tokens\n")

            # Additional note on iterative chain-of-thought
            if self.iteration_cycles > 1:
                total_iter_savings = avg_savings * 20 * self.iteration_cycles
                summary.append(f"- Over {self.iteration_cycles} iterative refinements: "
                               f"{total_iter_savings:.0f} tokens saved per page\n")
                summary.append("(In long-chain AI-assisted development, these savings compound across multiple revisions.)\n")
        else:
            summary.append("- Not enough data to compute practical impact.\n")

        # Complexity breakdown (marker-based) for Blocktail
        summary.append("\n### Token Usage by Marker Complexity\n")
        marker_complex = defaultdict(list)
        for data in self.tokenizer_results.values():
            blocktail_info = self.analyze_methodology(data, "Blocktail")
            for k, v in blocktail_info["by_complexity"].items():
                marker_complex[k].append(v)

        if marker_complex:
            for k in sorted(marker_complex.keys()):
                values = marker_complex[k]
                mean_val = np.mean(values)
                std_val = np.std(values)
                summary.append(f"- {k} markers: {mean_val:.1f} tokens (±{std_val:.1f})")
        else:
            summary.append("- No marker complexity data.\n")

        summary.append("\n*Note:* Note: All naming conventions rely on some markers. As you add more states or contexts, token usage inevitably rises. However, methods like Blocktail aim to keep subword splitting minimal, leading to leaner tokens even when stacking multiple states or contexts.\n")

        return "\n".join(summary)

    def get_tokenizer_type(self, tokenizer_name: str) -> str:
        """Get the implementation type for a given tokenizer."""
        tokenizer_types = {
            "gpt4": "tiktoken",
            "gpt35": "tiktoken",
            "gpt2": "transformers",
            "llama3": "transformers",
            "mistral": "transformers",
            "bert": "transformers",
            "roberta": "transformers",
            "t5": "transformers",
            "spiece": "sentencepiece"
        }
        return tokenizer_types.get(tokenizer_name, "unknown")

def main():
    analyzer = TokenizationAnalyzer("results", iteration_cycles=5)
    summary = analyzer.generate_summary()
    
    # Save to tokenization_summary.md
    with open("tokenization_summary.md", "w") as f:
        f.write(summary)
    print("Summary saved to tokenization_summary.md")

    # Update README.md
    try:
        with open("README.md", "r") as f:
            readme_content = f.read()
        
        # Split at the results marker instead of horizontal rule
        if "<!-- RESULTS -->" in readme_content:
            readme_parts = readme_content.split("<!-- RESULTS -->", 1)
            new_content = f"{readme_parts[0]}<!-- RESULTS -->\n{summary}"
            if len(readme_parts) > 1 and "<!-- END_RESULTS -->" in readme_parts[1]:
                new_content += "\n<!-- END_RESULTS -->" + readme_parts[1].split("<!-- END_RESULTS -->", 1)[1]
        else:
            new_content = readme_content + "\n<!-- RESULTS -->\n" + summary + "\n<!-- END_RESULTS -->"
        
        with open("README.md", "w") as f:
            f.write(new_content)
        print("README.md updated with latest analysis")
            
    except FileNotFoundError:
        print("README.md not found - skipping update")


if __name__ == "__main__":
    main()
