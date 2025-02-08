# Blocktail Tokenization Analysis

This repository provides a proof-of-concept toolset for measuring how different naming approaches (including [Blocktail](https://blocktail.io)) affect token usage in modern language models (LLMs). The results here focus on token count and cost implications within pay-per-token systems or context-limited AI workflows. While this is only one benchmark among many possible tests, it demonstrates how methodology choices in class naming can reduce code verbosity and preserve context space.

## Overview

### Key Scripts

1. **`tokenize_tests.py`**
   - Reads class-naming examples from `data/test_cases.json`.
   - Applies multiple tokenizers (e.g., GPT-4, LLaMA) to these naming patterns.
   - Exports tokenized results as JSON in the `results/` directory (one file per tokenizer).

2. **`analysis-compiler.py`**
   - Processes the generated `*_results.json` files.
   - Aggregates token usage for each naming methodology (Blocktail, BEM, Traditional).
   - Calculates metrics such as:
     - Token reductions
     - Marker complexity
     - Projected iterative cost savings
   - Produces a detailed Markdown report (`tokenization_summary.md`) with cross-model comparisons.

### Workflow

1. **Prepare Test Cases**  
   - Add or edit naming examples in `data/test_cases.json`.  
   - Each entry corresponds to a potential "class naming scenario."

2. **Run Tokenization Tests**  
   - To test all configured tokenizers at once:
     ```bash
     python tokenize_tests.py all
     ```
   - Or run a single tokenizer:
     ```bash
     python tokenize_tests.py gpt2
     ```

3. **Compile Analysis**  
   - Generate the final summary report:
     ```bash
     python analysis-compiler.py
     ```
   - This reads all JSON output from `results/` and collates statistics.

4. **Review Results**  
   - Open `tokenization_summary.md` to see:
     - Average token counts per naming convention
     - Relative savings (e.g., "Blocktail reduces tokens by ~40% vs. X")
     - Marker-complexity breakdown
     - Potential cost/time gains for iterative AI prompts

## Dependencies

Make sure to install:

- `sentencepiece` (for SentencePiece-based models)
- `transformers` (Hugging Face)
- `tiktoken` (OpenAI GPT models)
- `numpy`, `pandas`, `scipy` (for basic statistical computations)

### Authentication

If you use private Hugging Face models (e.g., LLaMA 3), create a `.env` file with:
```bash
HF_AUTH_TOKEN=your_huggingface_token
```
---

<!-- RESULTS -->
# Tokenization Analysis Summary

## Cross Comparison

| Tokenizer   |   Blocktail Avg |   Traditional Avg |   BEM Avg | vs Trad.   | vs BEM   |
|:------------|----------------:|------------------:|----------:|:-----------|:---------|
| llama3      |             8.7 |               8.7 |      14.6 | 0.3%       | 40.5%    |
| t5          |            14.5 |              13.8 |      24.1 | -5.1%      | 39.7%    |
| spiece      |            14.5 |              13.8 |      24.1 | -5.1%      | 39.7%    |
| roberta     |            10.9 |              13.1 |      19.6 | 16.8%      | 44.3%    |
| gpt35       |             8.7 |               8.7 |      14.6 | 0.3%       | 40.5%    |
| gpt2        |            10.9 |              13.1 |      19.6 | 16.8%      | 44.3%    |
| bert        |            11.2 |              12.9 |      21.9 | 13.0%      | 48.9%    |
| gpt4        |             8.7 |               8.7 |      14.6 | 0.3%       | 40.5%    |
| mistral     |            10.6 |              13.4 |      19.3 | 20.5%      | 44.9%    |


## Practical Impact

- Average token reduction per component: 4.5 tokens

- In a typical page with 20 components: 90 tokens

- Over 5 iterative refinements: 450 tokens saved per page

(In long-chain AI-assisted development, these savings compound across multiple revisions.)


### Token Usage by Marker Complexity

- 0 markers: 2.7 tokens (±0.5)
- 1 markers: 5.2 tokens (±1.0)
- 2 markers: 6.2 tokens (±1.1)
- 3 markers: 8.4 tokens (±1.4)
- 4 markers: 11.6 tokens (±2.4)
- 5 markers: 13.7 tokens (±2.7)
- 6 markers: 15.6 tokens (±2.8)
- 7 markers: 14.4 tokens (±3.1)

*Note:* Note: All naming conventions rely on some markers. As you add more states or contexts, token usage inevitably rises. However, methods like Blocktail aim to keep subword splitting minimal, leading to leaner tokens even when stacking multiple states or contexts.

<!-- END_RESULTS -->

#### Sample Data
While the sample data aims to represent best-case code practices, particularly for traditional HTML, real-world naming patterns can vary significantly. When managing multiple states and dynamic behaviors, naming conventions may naturally become more verbose or semantic than those used here.

### Tokenizer Associations
| Implementation Library | Tokenizers Used |
|-----------------------|-----------------|
| `tiktoken`            | gpt-4, gpt-3.5-turbo |
| `transformers`        | meta-llama/Meta-Llama-3-70B, mistralai/Mistral-7B-v0.3, bert-base-uncased, roberta-base, t5-base, gpt2 |
| `sentencepiece`       | spiece.model |

This table reflects only the tokenizer implementations and specific tokenizers tested in our analysis. We access these tokenizers through their respective libraries but do not test or use the full models themselves.

For full methodology and extended documentation, see [blocktail.io](https://blocktail.io "blocktail.io")

