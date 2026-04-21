"""
Character-level and word-level tokenizers for text generation and chatbot models.
"""


class CharTokenizer:
    """Character-level tokenizer that maps each character to an integer index."""

    def __init__(self):
        self.char_to_idx = {}
        self.idx_to_char = {}
        self.vocab_size = 0

    def fit(self, text):
        """Build vocabulary from text."""
        chars = sorted(set(text))
        self.char_to_idx = {ch: i for i, ch in enumerate(chars)}
        self.idx_to_char = {i: ch for ch, i in self.char_to_idx.items()}
        self.vocab_size = len(chars)

    def encode(self, text):
        """Convert text to list of integer indices."""
        return [self.char_to_idx[ch] for ch in text if ch in self.char_to_idx]

    def decode(self, indices):
        """Convert list of integer indices back to text."""
        return "".join(self.idx_to_char.get(i, "") for i in indices)


class WordTokenizer:
    """Word-level tokenizer that maps each word to an integer index."""

    PAD_TOKEN = "<PAD>"
    UNK_TOKEN = "<UNK>"
    SOS_TOKEN = "<SOS>"
    EOS_TOKEN = "<EOS>"

    def __init__(self, min_freq=1):
        self.word_to_idx = {}
        self.idx_to_word = {}
        self.vocab_size = 0
        self.min_freq = min_freq
        self.pad_idx = 0
        self.unk_idx = 1
        self.sos_idx = 2
        self.eos_idx = 3

    def fit(self, text):
        """Build vocabulary from text. Input can be a string or list of strings."""
        if isinstance(text, str):
            texts = [text]
        else:
            texts = text

        word_freq = {}
        for t in texts:
            for word in t.lower().split():
                word_freq[word] = word_freq.get(word, 0) + 1

        special_tokens = [self.PAD_TOKEN, self.UNK_TOKEN, self.SOS_TOKEN, self.EOS_TOKEN]
        self.word_to_idx = {token: i for i, token in enumerate(special_tokens)}

        idx = len(special_tokens)
        for word in sorted(word_freq.keys()):
            if word_freq[word] >= self.min_freq:
                self.word_to_idx[word] = idx
                idx += 1

        self.idx_to_word = {i: w for w, i in self.word_to_idx.items()}
        self.vocab_size = len(self.word_to_idx)
        self.pad_idx = self.word_to_idx[self.PAD_TOKEN]
        self.unk_idx = self.word_to_idx[self.UNK_TOKEN]
        self.sos_idx = self.word_to_idx[self.SOS_TOKEN]
        self.eos_idx = self.word_to_idx[self.EOS_TOKEN]

    def encode(self, text, add_special=False):
        """Convert text to list of integer indices."""
        words = text.lower().split()
        indices = [self.word_to_idx.get(w, self.unk_idx) for w in words]
        if add_special:
            indices = [self.sos_idx] + indices + [self.eos_idx]
        return indices

    def decode(self, indices, remove_special=True):
        """Convert list of integer indices back to text."""
        special = {self.pad_idx, self.sos_idx, self.eos_idx}
        words = []
        for i in indices:
            if remove_special and i in special:
                continue
            words.append(self.idx_to_word.get(i, self.UNK_TOKEN))
        return " ".join(words)
