import csv
import sys


def main():

    # Check for command-line usage
    if len(sys.argv) != 3:
        print("Usage: python dna.py database.csv sequence.txt")
        sys.exit(1)

    database = sys.argv[1]
    sequence_file = sys.argv[2]

    # Read database file into a variable
    with open(database, "r") as file:
        reader = csv.DictReader(file)
        people = list(reader)
        strs = reader.fieldnames[1:]  # exclude "name"

    # Read DNA sequence file into a variable
    with open(sequence_file, "r") as file:
        sequence = file.read()

    # Find longest match of each STR in DNA sequence
    str_counts = {}
    for s in strs:
        str_counts[s] = longest_match(sequence, s)

    # Check database for matching profiles
    for person in people:
        match = True
        for s in strs:
            if int(person[s]) != str_counts[s]:
                match = False
                break

        if match:
            print(person["name"])
            return

    print("No match")
    return


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):

        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring"
        while True:

            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1
            else:
                break

        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    return longest_run


main()
