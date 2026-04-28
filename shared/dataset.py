import torch
from torch.utils.data import Dataset
from torch.nn.utils.rnn import pad_sequence

class TextGenDataset(Dataset):

    def __init__(self, encoded_text, seq_length):
        self.data = encoded_text
        self.seq_length = seq_length

    def __len__(self):
        return max(0, len(self.data) - self.seq_length)

    def __getitem__(self, idx):
        x = torch.tensor(self.data[idx:idx + self.seq_length], dtype=torch.long)
        y = torch.tensor(self.data[idx + 1:idx + self.seq_length + 1], dtype=torch.long)
        return x, y

class QADataset(Dataset):

    def __init__(self, qa_pairs, tokenizer):
        self.pairs = []
        for pair in qa_pairs:
            q_encoded = tokenizer.encode(pair["question"], add_special=True)
            a_encoded = tokenizer.encode(pair["answer"], add_special=True)
            self.pairs.append((
                torch.tensor(q_encoded, dtype=torch.long),
                torch.tensor(a_encoded, dtype=torch.long),
            ))

    def __len__(self):
        return len(self.pairs)

    def __getitem__(self, idx):
        return self.pairs[idx]

def qa_collate_fn(batch):
    questions, answers = zip(*batch)
    questions_padded = pad_sequence(questions, batch_first=True, padding_value=0)
    answers_padded = pad_sequence(answers, batch_first=True, padding_value=0)
    return questions_padded, answers_padded
