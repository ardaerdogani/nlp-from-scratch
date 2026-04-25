# NLP From Scratch: Text Generation & Chatbots

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)
![PyTorch](https://img.shields.io/badge/PyTorch-2.0%2B-ee4c2c?logo=pytorch)
![License](https://img.shields.io/badge/License-MIT-green)

Complete NLP system demonstrating probabilistic modeling, sequential neural networks, and attention-based architectures. All models are implemented from scratch using PyTorch with no pretrained weights.

## Project Structure

The project is split by task. Each task is self-contained (its own data, models, training, evaluation, and presentation notebooks). Shared utilities that both tasks need live in `shared/`.

```
nlp_project/
├── main.py                          # Runs the full pipeline (both tasks)
├── requirements.txt                 # Python dependencies
├── README.md                        # This file
├── 04_summary.ipynb                 # Cross-task wrap-up notebook
│
├── shared/                          # Helpers used by both tasks
│   ├── tokenizer.py                 # CharTokenizer and WordTokenizer
│   └── dataset.py                   # PyTorch Dataset classes
│
├── task1_text_generation/           # TASK 1 — Text generation (6 models)
│   ├── data/
│   │   ├── generate_dataset.py      # Text corpus generator (12,000+ words)
│   │   └── corpus.txt               # Generated corpus (created on first run)
│   ├── models/
│   │   ├── markov_chain.py          # Markov Chain (char + word level)
│   │   ├── rnn_model.py             # Vanilla RNN (char + word level)
│   │   └── lstm_model.py            # LSTM (char + word level)
│   ├── train.py                     # Training for all 6 text-gen models
│   ├── evaluate.py                  # 10-prompt comparison table
│   └── notebooks/
│       ├── 01_data.ipynb            # Corpus generation + exploration
│       └── 02_text_generation.ipynb # Training + evaluation
│
└── task2_chatbot/                   # TASK 2 — Chatbots (2 models)
    ├── data/
    │   ├── generate_qa_dataset.py   # QA pairs generator (2,000+ pairs)
    │   └── qa_pairs.json            # Generated pairs (created on first run)
    ├── models/
    │   ├── lstm_chatbot.py          # LSTM seq2seq with Bahdanau attention
    │   └── transformer_chatbot.py   # Transformer from scratch
    ├── train.py                     # Training for both chatbots
    ├── evaluate.py                  # 10-question comparison + loss plot
    └── notebooks/
        ├── 01_data.ipynb            # QA dataset exploration
        └── 02_chatbots.ipynb        # Training + evaluation
```

> **Generated files** — `evaluation_report.txt`, `task2_chatbot/chatbot_loss_curves.png`, `corpus.txt`, and `qa_pairs.json` are all produced by running the pipeline. They are not tracked in git; re-run `main.py` to reproduce them.

## Setup

```bash
pip install -r requirements.txt

# Run the complete pipeline (both tasks end-to-end)
python main.py
```

## Task 1: Text Generation Models

Six models total (3 architectures × 2 tokenization levels):

| Model        | Character-Level               | Word-Level                    |
|--------------|-------------------------------|-------------------------------|
| Markov Chain | N-gram transitions (order=5)  | N-gram transitions (order=2)  |
| RNN          | Embedding + 2-layer RNN + Linear  | Embedding + 2-layer RNN + Linear  |
| LSTM         | Embedding + 2-layer LSTM + Linear | Embedding + 2-layer LSTM + Linear |

- **Dataset**: 12,000+ words of procedurally generated English text across 10 topics (see `task1_text_generation/data/generate_dataset.py`).
- **Evaluation**: 10 prompts × 6 models, plus training-time / memory / loss table saved to `evaluation_report.txt`.

## Task 2: Chatbot Models

- **Dataset**: 2,000+ QA pairs (geography, science, math, technology, history, general knowledge) from `task2_chatbot/data/generate_qa_dataset.py`.
- **LSTM Chatbot** — bidirectional LSTM encoder, LSTM decoder with Bahdanau attention, teacher-forcing with decreasing ratio (embed_dim=128, hidden_dim=256).
- **Transformer Chatbot** — from-scratch encoder-decoder with multi-head attention (4 heads, 3+3 layers), sinusoidal positional encoding, warmup + inverse-sqrt LR schedule (d_model=128, d_ff=512).
- **Evaluation**: 10 questions × 2 models, loss curves saved to `task2_chatbot/chatbot_loss_curves.png`, plus training-performance table.

## Running Individual Components

```bash
# Generate datasets only
python -m task1_text_generation.data.generate_dataset
python -m task2_chatbot.data.generate_qa_dataset

# Train text generation models only
python -m task1_text_generation.train

# Train chatbot models only
python -m task2_chatbot.train
```

## Notebooks (presentation)

Open these in order for a narrated walkthrough:

1. `task1_text_generation/notebooks/01_data.ipynb` — text corpus exploration.
2. `task1_text_generation/notebooks/02_text_generation.ipynb` — train + evaluate the 6 text-gen models.
3. `task2_chatbot/notebooks/01_data.ipynb` — QA dataset exploration.
4. `task2_chatbot/notebooks/02_chatbots.ipynb` — train + evaluate the 2 chatbots.
5. `04_summary.ipynb` (root) — cross-task parameter counts, comparison tables, and conclusions.

Notebooks 01 and 04 render quickly (no training). Notebooks 02 have an `EPOCHS` knob near the top — drop it for fast demo runs.

## Technical Notes

- All models implemented from scratch in PyTorch; no pretrained weights or external APIs.
- Training uses gradient clipping (max norm = 1.0) and learning-rate scheduling.
- Transformer uses warmup + inverse square root decay; LSTM chatbot uses decreasing teacher-forcing ratio.
- Dataset generation is deterministic (seeded).

## Results

After a full pipeline run (`python main.py`), results are saved to `evaluation_report.txt`. Loss curves from the chatbot training are written to `task2_chatbot/chatbot_loss_curves.png`.

### Task 1 — Text Generation Training Performance

| Model            | Level | Training Time | Final Loss | Notes                                        |
|------------------|-------|---------------|------------|----------------------------------------------|
| Markov Chain     | Char  | 0.15s         | —          | No gradient descent; pure frequency table    |
| Markov Chain     | Word  | 0.01s         | —          | Fastest; copies real phrases from corpus     |
| RNN              | Char  | 101.6s        | 0.6689     | Learns spelling patterns; vanishing gradient |
| RNN              | Word  | 18.4s         | 0.7746     | Faster than char; limited long-range context |
| LSTM             | Char  | 107.6s        | **0.2943** | Best loss; gates retain long character context |
| LSTM             | Word  | 20.2s         | 0.7861     | Real words; word-level needs more data       |

### Task 2 — Chatbot Training Performance

| Model               | Training Time | Parameters | Final Loss | Notes                                          |
|---------------------|---------------|------------|------------|------------------------------------------------|
| LSTM Chatbot        | 105.2s        | 6,019,947  | **0.1014** | Low loss; teacher forcing aids convergence     |
| Transformer Chatbot | 33.4s         | 1,971,819  | 4.3724     | 3× faster; needs more epochs/data to converge |

The Transformer trains faster per epoch due to parallel self-attention, but its warmup LR schedule and lack of teacher forcing mean it requires significantly more data and training steps to reach the LSTM's loss on this small dataset.

## Dependencies

- PyTorch >= 2.0.0
- NumPy >= 1.24.0
- Matplotlib >= 3.7.0
- tabulate >= 0.9.0
- psutil >= 5.9.0

## License

MIT — see [LICENSE](LICENSE).
