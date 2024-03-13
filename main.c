#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int args, char** argv) {
	if (args != 2) {
		fprintf(stderr, "Program and file only.\n");
		exit(1);
	}

	char* filename = argv[1];
	char* extension_position = strrchr(filename, '.');
	if (extension_position == NULL) {
		fprintf(stderr, "the file does not have any extension");
		exit(EXIT_FAILURE);
	}
	size_t filename_length = extension_position - filename;
	char output_extension[] = ".hack";
	int output_extension_length = strlen(output_extension);

	char* input = malloc(filename_length + output_extension_length + 1);
	if (input == NULL) {
		fprintf(stderr, "Could not allocate memory for input,\n");
		exit(EXIT_FAILURE);
	}

	strncpy(input, filename, filename_length);
	strcat(input, output_extension);
	
	printf("%s\n", input);
	free(input);

	return 0;
}