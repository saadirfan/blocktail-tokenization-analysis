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
