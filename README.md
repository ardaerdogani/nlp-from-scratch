# NLP Project: Text Generation Models and Chatbots

Complete NLP system demonstrating probabilistic modeling, sequential neural networks, and attention-based architectures. All models are implemented from scratch using PyTorch with no pretrained weights.

## Project Structure

The project is split by task. Each task is self-contained (its own data, models, training, evaluation, and presentation notebooks). Shared utilities that both tasks need live in `shared/`.

```
nlp_project/
├── main.py                          # Runs the full pipeline (both tasks)
├── requirements.txt                 # Python dependencies
├── README.md                        # This file
├── evaluation_report.txt            # Combined report from last main.py run
├── 04_summary.ipynb                 # Cross-task wrap-up notebook
│
├── shared/                          # Helpers used by both tasks
│   ├── tokenizer.py                 # CharTokenizer and WordTokenizer
│   └── dataset.py                   # PyTorch Dataset classes
│
├── task1_text_generation/           # TASK 1 — Text generation (6 models)
│   ├── data/
│   │   ├── generate_dataset.py      # Text corpus generator (12,000+ words)
│   │   └── corpus.txt               # Generated corpus (after running)
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
    │   └── qa_pairs.json            # Generated pairs (after running)
    ├── models/
    │   ├── lstm_chatbot.py          # LSTM seq2seq with Bahdanau attention
    │   └── transformer_chatbot.py   # Transformer from scratch
    ├── train.py                     # Training for both chatbots
    ├── evaluate.py                  # 10-question comparison + loss plot
    ├── chatbot_loss_curves.png      # Saved loss curves from last run
    └── notebooks/
        ├── 01_data.ipynb            # QA dataset exploration
        └── 02_chatbots.ipynb        # Training + evaluation
```

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
- **Evaluation**: 10 prompts × 6 models, outputs ≥20 characters each, plus training-time / memory / loss table in `evaluation_report.txt`.

## Task 2: Chatbot Models

- **Dataset**: 2,000+ QA pairs (geography, science, math, technology, history, general knowledge) from `task2_chatbot/data/generate_qa_dataset.py`.
- **LSTM Chatbot** — bidirectional LSTM encoder, LSTM decoder with Bahdanau attention, teacher-forcing with decreasing ratio (embed_dim=128, hidden_dim=256).
- **Transformer Chatbot** — from-scratch encoder-decoder with multi-head attention (4 heads, 3+3 layers), sinusoidal positional encoding, warmup + inverse-sqrt LR schedule (d_model=128, d_ff=512).
- **Evaluation**: 10 questions × 2 models, loss curves PNG (`task2_chatbot/chatbot_loss_curves.png`), plus training-performance table.

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

## Dependencies

- PyTorch >= 2.0.0
- NumPy >= 1.24.0
- Matplotlib >= 3.7.0
- tabulate >= 0.9.0
- psutil >= 5.9.0
