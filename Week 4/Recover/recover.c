#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

#define BLOCK_SIZE 512

int main(int argc, char *argv[])
{
    // Ensure correct usage
    if (argc != 2)
    {
        printf("Usage: ./recover image\n");
        return 1;
    }

    // Open forensic image
    FILE *card = fopen(argv[1], "r");
    if (card == NULL)
    {
        printf("Could not open %s.\n", argv[1]);
        return 1;
    }

    uint8_t buffer[BLOCK_SIZE];
    FILE *img = NULL;

    int img_count = 0;
    char filename[8];

    // Read memory card 512 bytes at a time
    while (fread(buffer, BLOCK_SIZE, 1, card) == 1)
    {
        // Check for JPEG signature
        if (buffer[0] == 0xff &&
            buffer[1] == 0xd8 &&
            buffer[2] == 0xff &&
            (buffer[3] & 0xf0) == 0xe0)
        {
            // Close previous image if open
            if (img != NULL)
            {
                fclose(img);
            }

            // Create new JPEG file
            sprintf(filename, "%03i.jpg", img_count);
            img = fopen(filename, "w");

            img_count++;
        }

        // Write block to current JPEG if one is open
        if (img != NULL)
        {
            fwrite(buffer, BLOCK_SIZE, 1, img);
        }
    }

    // Close remaining files
    if (img != NULL)
    {
        fclose(img);
    }

    fclose(card);
    return 0;
}
