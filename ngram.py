import argparse
import re
import sys
from collections import Counter

def preprocess_text(text):
    """
    Converts text to lowercase, replaces punctuation with spaces,
    and collapses multiple spaces into a single space.
    """
    # Convert to lowercase
    text = text.lower()
    
    # Replace punctuation with spaces
    # Using regex to keep only alphanumeric characters (including international ones), spaces, dashes and quotes.
    # We replace:
    # 1. [^\w\s\-\']: Anything not a word char, space, dash, or quote.
    # 2. \d: Digits (which are included in \w).
    # 3. _: Underscore (which is included in \w).
    text = re.sub(r"[^\w\s\-\']|\d|_", ' ', text)
    
    # Collapse multiple spaces into a single space
    text = re.sub(r'\s+', ' ', text)
    
    return text.strip()

def generate_ngrams(text, n):
    """
    Generates a list of N-grams from the text.
    Handles the case where N=1 specially to match expected requirement 
    (though sliding window logic works mostly the same, handling spaces might be subtle).
    
    Reflecting on requirements:
    "Input: "banana"
    N=1: b:1, a:3, n:2" -> Standard character count.
    
    "N=2: ba:1, an:2, na:2" -> Sliding window.
    
    The preprocessed text might have spaces inside.
    If text is "hello world", N=2 produces "he", "el", "ll", "lo", "o ", " w", ...
    Steps confirm "Textfiles" and "construct a table of N-grams".
    Usually N-grams cross word boundaries if punctuation is removed and replaced by space.
    """
    if n < 1:
        return []
    
    # If the text is shorter than N, return empty
    if len(text) < n:
        return []
        
    ngrams = [text[i:i+n] for i in range(len(text) - n + 1)]
    return ngrams

def main():
    parser = argparse.ArgumentParser(description="N-gram Generator")
    parser.add_argument("n", type=int, help="Length of the N-gram")
    parser.add_argument("filename", nargs='?', help="Path to the input text file")
    
    args = parser.parse_args()
    
    try:
        if args.filename:
            with open(args.filename, 'r', encoding='utf-8') as f:
                text = f.read()
        else:
            text = sys.stdin.read()
    except FileNotFoundError:
        print(f"Error: File '{args.filename}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading input: {e}")
        sys.exit(1)
        
    processed_text = preprocess_text(text)
    
    # Debug print could go here, but requirements say print table at end.
    
    ngrams = generate_ngrams(processed_text, args.n)
    
    counts = Counter(ngrams)
    
    # Print table
    # Requirement: "The program must store the nmuber of occurences for each n-gram."
    # Requirement: "prints out tha table of N-grams at the end."
    # The example format: "b:1, a:3, n:2"
    
    # Implementing a cleaner table output or matching the example style?
    # Req: "constructs a table of N-grams"
    # Example output format in preplan.txt is linear: "N=1: b:1, a:3, n:2"
    # I will try to match the output format roughly or make it a list.
    # Given "table", a list of "ngram : count" is best.
    
    print(f"N={args.n} N-grams:")
    for ngram, count in sorted(counts.items()):
        # Handle displaying space clearly if part of ngram?
        # Example just shows chars.
        print(f"'{ngram}': {count}")

if __name__ == "__main__":
    main()
