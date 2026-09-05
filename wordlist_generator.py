from itertools import permutations, product


def generate_combinations(words, separators, max_length):
    results = set()

    for r in range(1, len(words) + 1):

        for perm in permutations(words, r):

            if r == 1:
                candidate = perm[0]

                if len(candidate) <= max_length:
                    results.add(candidate)

                continue

            for sep_combo in product(separators, repeat=r-1):

                candidate = perm[0]

                for i in range(r-1):
                    candidate += sep_combo[i] + perm[i+1]

                if len(candidate) <= max_length:
                    results.add(candidate)

    return sorted(results)


def save_to_file(wordlist, filename):
    with open(filename, "w", encoding="utf-8") as f:
        for word in wordlist:
            f.write(word + "\n")


def main():

    print("\n=== Wordlist Generator ===\n")

    raw_words = input("Enter comma separated words: ")
    words = [w.strip() for w in raw_words.split(",") if w.strip()]

    max_length = int(input("Maximum length (e.g. 20): "))

    separators = ["", ".", "_", "-"]

    print("\nGenerating combinations...")

    wordlist = generate_combinations(words, separators, max_length)

    print(f"Generated {len(wordlist)} combinations")

    filename = "wordlist.txt"

    save_to_file(wordlist, filename)

    print(f"\nSaved to: {filename}")


if __name__ == "__main__":
    main()