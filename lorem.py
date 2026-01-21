import argparse
import sys
import re
import random
from collections import defaultdict

def parse_ngram_input(input_text):
    """
    Parses the output of ngram.py.
    Returns:
        n (int): The order of N-grams.
        ngrams (dict): Dictionary mapping ngam strings to their counts.
    """
    n = None
    ngrams = {}
    
    # Regex to find N
    n_match = re.search(r"N=(\d+) N-grams:", input_text)
    if n_match:
        n = int(n_match.group(1))
    
    # Regex to find ngrams and counts: 'ngram': count
    # Matches lines like: 'th': 15
    # We need to be careful about newlines in regex, but ngram.py output seems line-based.
    # The ngram content is inside single quotes.
    # We use a non-greedy match for the content inside quotes.
    ngram_matches = re.findall(r"'(.+?)': (\d+)", input_text)
    
    for content, count in ngram_matches:
        ngrams[content] = int(count)
        
    return n, ngrams

def build_markov_model(n, ngrams):
    """
    Builds a Markov Chain model from N-grams.
    For order N, the state is the first N-1 characters (prefix).
    The transition is the Nth character (next_char).
    
    Returns:
        model (dict): Key = prefix (str), Value = list of (next_char, count)
        starts (list): List of (full_ngram, count) to choose initial state.
    """
    model = defaultdict(list)
    starts = []
    
    for ngram, count in ngrams.items():
        if len(ngram) != n:
            # Skip malformed ngrams if any, though regex should be safe
            continue
            
        starts.append((ngram, count))
        
        if n > 1:
            prefix = ngram[:-1]
            next_char = ngram[-1]
            model[prefix].append((next_char, count))
        else:
            # For N=1, prefix is empty string
            model[""].append((ngram, count))
            
    return model, starts

def generate_text(model, starts, n, length):
    """
    Generates random text of total length `length`.
    """
    if not starts:
        return ""
        
    output = []
    
    # Helper to weighted random choice
    def weighted_choice(choices):
        # choices is list of (item, weight)
        total = sum(w for c, w in choices)
        r = random.uniform(0, total)
        uptime = 0
        for c, w in choices:
            uptime += w
            if uptime >= r:
                return c
        return choices[-1][0] # Fallback

    # Initial state
    current_ngram = weighted_choice(starts)
    output.append(current_ngram)
    
    current_length = len(current_ngram)
    
    # Current state for lookup (last N-1 chars)
    if n > 1:
        state = current_ngram[-(n-1):]
    else:
        state = ""
        
    while current_length < length:
        # Get possibilities for current state
        transitions = model.get(state)
        
        if not transitions:
            # Dead end, pick a new random start
            next_chunk = weighted_choice(starts)
            output.append(next_chunk)
            current_ngram = next_chunk # Just for tracking if needed, primarily we need state
            if n > 1:
                state = next_chunk[-(n-1):]
            else:
                state = ""
            current_length += len(next_chunk)
            continue
            
        # Pick next character
        next_char = weighted_choice(transitions)
        output.append(next_char)
        current_length += 1
        
        # Update state
        if n > 1:
            state = state[1:] + next_char
        else:
            state = "" # Stay in empty state for N=1
            
    # Join and trim to exact length
    full_text = "".join(output)
    return full_text[:length]

def main():
    parser = argparse.ArgumentParser(description="Generate Lorem Ipsum text from N-gram statistics.")
    parser.add_argument("length", type=int, help="number of characters to generate")
    parser.add_argument("filename", nargs='?', help="Path to the input N-gram file (optional, defaults to stdin)")
    
    args = parser.parse_args()
    
    try:
        if args.filename:
            with open(args.filename, 'r', encoding='utf-8') as f:
                input_text = f.read()
        else:
            # Check if there is data on stdin
            if sys.stdin.isatty():
                # If no file and no stdin pipe, show help
                parser.print_help()
                return
            input_text = sys.stdin.read()
    except Exception as e:
        print(f"Error reading input: {e}", file=sys.stderr)
        sys.exit(1)
        
    n, ngrams = parse_ngram_input(input_text)
    
    if n is None:
        print("Error: Could not deduce N from input. Format expected: 'N=<int> N-grams:'", file=sys.stderr)
        sys.exit(1)
        
    if not ngrams:
        print("Error: No N-grams found in input.", file=sys.stderr)
        sys.exit(1)
        
    model, starts = build_markov_model(n, ngrams)
    
    # Generate text
    generated_text = generate_text(model, starts, n, args.length)
    
    print(generated_text)

if __name__ == "__main__":
    main()
