"""
Markov Chain Model for text generation.
Supports both character-level and word-level operation.
"""

import random
from collections import defaultdict


class MarkovChain:
    """N-gram Markov Chain model for text generation."""

    def __init__(self, order=2):
        """
        Args:
            order: The number of previous tokens to condition on (n-gram order).
        """
        self.order = order
        self.transitions = defaultdict(lambda: defaultdict(int))
        self.starts = []

    def fit(self, tokens):
        """
        Train the model on a sequence of tokens.

        Args:
            tokens: List of tokens (characters or words).
        """
        if len(tokens) <= self.order:
            return

        self.starts.append(tuple(tokens[:self.order]))

        for i in range(len(tokens) - self.order):
            state = tuple(tokens[i:i + self.order])
            next_token = tokens[i + self.order]
            self.transitions[state][next_token] += 1

    def _sample_next(self, state):
        """Sample the next token given current state using weighted random selection."""
        if state not in self.transitions:
            return None
        candidates = self.transitions[state]
        tokens = list(candidates.keys())
        weights = list(candidates.values())
        total = sum(weights)
        probs = [w / total for w in weights]
        return random.choices(tokens, weights=probs, k=1)[0]

    def generate(self, length=200, seed_tokens=None, seed_value=None):
        """
        Generate a sequence of tokens.

        Args:
            length: Number of tokens to generate.
            seed_tokens: Optional starting tokens (list). Must be >= order length.
            seed_value: Random seed for reproducibility.

        Returns:
            List of generated tokens.
        """
        if seed_value is not None:
            random.seed(seed_value)

        if seed_tokens and len(seed_tokens) >= self.order:
            current = list(seed_tokens[:self.order])
        elif self.starts:
            current = list(random.choice(self.starts))
        else:
            return []

        output = list(current)

        for _ in range(length - len(current)):
            state = tuple(current[-self.order:])
            next_token = self._sample_next(state)
            if next_token is None:
                if self.starts:
                    new_start = list(random.choice(self.starts))
                    current = new_start
                    output.extend(new_start)
                else:
                    break
            else:
                output.append(next_token)
                current.append(next_token)

        return output[:length]

    def generate_text(self, length=200, seed_text=None, mode="char", seed_value=None):
        """
        Generate text as a string.

        Args:
            length: Number of tokens to generate.
            seed_text: Optional seed text string.
            mode: 'char' for character-level, 'word' for word-level.
            seed_value: Random seed for reproducibility.

        Returns:
            Generated text string.
        """
        seed_tokens = None
        if seed_text:
            if mode == "char":
                seed_tokens = list(seed_text)
            else:
                seed_tokens = seed_text.lower().split()

        tokens = self.generate(length=length, seed_tokens=seed_tokens, seed_value=seed_value)

        if mode == "char":
            return "".join(tokens)
        else:
            return " ".join(tokens)
