from cs50 import get_string

def main():
    text = get_string("Text: ")

    letters = 0
    words = 0
    sentences = 0

    # Count letters, words, sentences
    for i, char in enumerate(text):
        if char.isalpha():
            letters += 1

        if char in [".", "!", "?"]:
            sentences += 1

        # Count words (space-based)
        if char == " ":
            words += 1

    # Last word
    words += 1

    # Coleman-Liau components
    L = (letters / words) * 100
    S = (sentences / words) * 100

    index = round(0.0588 * L - 0.296 * S - 15.8)

    # Output formatting
    if index < 1:
        print("Before Grade 1")
    elif index >= 16:
        print("Grade 16+")
    else:
        print(f"Grade {index}")


if __name__ == "__main__":
    main()
