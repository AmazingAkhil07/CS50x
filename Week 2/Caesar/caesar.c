#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// Function prototypes
bool only_digits(string s);
char rotate(char c, int k);

int main(int argc, string argv[])
{
    // 1️⃣ Check command-line arguments
    if (argc != 2)
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }

    // 2️⃣ Check if key contains only digits
    if (!only_digits(argv[1]))
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }

    // 3️⃣ Convert key to integer
    int k = atoi(argv[1]);

    // 4️⃣ Get plaintext
    string plaintext = get_string("plaintext: ");

    // 5️⃣ Print ciphertext
    printf("ciphertext: ");

    for (int i = 0; i < strlen(plaintext); i++)
    {
        printf("%c", rotate(plaintext[i], k));
    }

    printf("\n");
    return 0;
}

// ✅ Returns true if string contains only digits
bool only_digits(string s)
{
    for (int i = 0; i < strlen(s); i++)
    {
        if (!isdigit(s[i]))
        {
            return false;
        }
    }
    return true;
}

// ✅ Rotates a character by k positions
char rotate(char c, int k)
{
    if (isupper(c))
    {
        return (c - 'A' + k) % 26 + 'A';
    }
    else if (islower(c))
    {
        return (c - 'a' + k) % 26 + 'a';
    }
    else
    {
        return c;
    }
}
