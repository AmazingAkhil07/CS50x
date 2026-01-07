#include <cs50.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

int main(int argc, char *argv[])
{
    // Check command-line arguments
    if (argc != 4)
    {
        printf("Usage: ./volume input.wav output.wav factor\n");
        return 1;
    }

    // Open input file
    FILE *input = fopen(argv[1], "rb");
    if (input == NULL)
    {
        printf("Could not open input file.\n");
        return 1;
    }

    // Open output file
    FILE *output = fopen(argv[2], "wb");
    if (output == NULL)
    {
        printf("Could not open output file.\n");
        fclose(input);
        return 1;
    }

    // Convert factor to float
    float factor = atof(argv[3]);

    // WAV header is 44 bytes
    uint8_t header[44];

    // Read header from input
    fread(header, sizeof(uint8_t), 44, input);

    // Write header to output
    fwrite(header, sizeof(uint8_t), 44, output);

    // Each sample is a 16-bit signed integer
    int16_t sample;

    // Process samples
    while (fread(&sample, sizeof(int16_t), 1, input))
    {
        sample *= factor;
        fwrite(&sample, sizeof(int16_t), 1, output);
    }

    // Close files
    fclose(input);
    fclose(output);

    return 0;
}
