#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int height;

    // Prompt user until they enter a positive integer
    do
    {
        height = get_int("Height: ");
    }
    while (height < 1);

    // Build the pyramid
    for (int i = 1; i <= height; i++)
    {
        // Print spaces first
        for (int j = 0; j < height - i; j++)
        {
            printf(" ");
        }

        // Print hashes
        for (int k = 0; k < i; k++)
        {
            printf("#");
        }

        // Move to next line
        printf("\n");
    }
}

