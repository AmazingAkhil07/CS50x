#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int cents;

    // Prompt user until they give a non-negative integer
    do
    {
        cents = get_int("Change owed: ");
    }
    while (cents < 0);

    int coins = 0;

    // Quarters
    coins += cents / 25;
    cents = cents % 25;

    // Dimes
    coins += cents / 10;
    cents = cents % 10;

    // Nickels
    coins += cents / 5;
    cents = cents % 5;

    // Pennies
    coins += cents; // remaining cents are all pennies

    printf("%d\n", coins);
}
