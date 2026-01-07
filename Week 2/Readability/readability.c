#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <math.h>

int main(void)
{
    // Prompt user for text
    string text = get_string("Text: ");

    int letters = 0;
    int words = 1;     // Start at 1 since the last word may not have a space
    int sentences = 0;

    // Count letters, words, sentences
    for (int i = 0, n = strlen(text); i < n; i++)
    {
        char c = text[i];

        // Letters
        if (isalpha(c))
        {
            letters++;
        }
        // Words
        else if (c == ' ')
        {
            words++;
        }
        // Sentences
        else if (c == '.' || c == '!' || c == '?')
        {
            sentences++;
        }
    }

    // Calculate L and S
    float L = ((float)letters / words) * 100;
    float S = ((float)sentences / words) * 100;

    // Coleman-Liau index
    float index = 0.0588 * L - 0.296 * S - 15.8;
    int grade = round(index);

    // Print grade
    if (grade < 1)
    {
        printf("Before Grade 1\n");
    }
    else if (grade >= 16)
    {
        printf("Grade 16+\n");
    }
    else
    {
        printf("Grade %i\n", grade);
    }

    return 0;
}
