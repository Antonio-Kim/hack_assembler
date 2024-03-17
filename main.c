#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <stdbool.h>

int main(int args, char** argv) {
	if (args != 2) {
		fprintf(stderr, "Program and file only.\n");
		exit(1);
	}
	char* filename = argv[1];

	/**
	 * Converting File extension name from .asm to .hack. The output of
	 * the following lines dynamically creates new string that takes
	 * the name of the file, extract the filename without the .asm
	 * and then add .hack string onto the output file name
	*/
	char* extension_position = strrchr(filename, '.');
	if (extension_position == NULL) {
		fprintf(stderr, "the file does not have any extension.\n");
		exit(EXIT_FAILURE);
	}
	size_t filename_length = extension_position - filename;
	char output_extension[] = ".hack";
	int output_extension_length = strlen(output_extension);

	char* output_filename = malloc(filename_length + output_extension_length + 1);
	if (output_filename == NULL) {
		fprintf(stderr, "Could not allocate memory for input,\n");
		exit(EXIT_FAILURE);
	}

	strncpy(output_filename, filename, filename_length);
	strcat(output_filename, output_extension);

	/**
	 * Here the file for input is being read based on the second
	 * command-line argument, and then the new file is being created.
	 * Error could occur here if the file does not exist.
	*/
	FILE *input_file = fopen(filename, "r");
	FILE *output_file = fopen(output_filename, "w");
	if (!input_file) {
		fprintf(stderr, "Could not open the file, or the file does not exists.\n");
		exit(EXIT_FAILURE);
	}

	if (!output_file) {
		fprintf(stderr, "Could not create the hack file.\n");
	}

	/**
	 * File must remove all the whitespace before it can process and save it to a file
	 * This is where the first reading happens. Perhaps translation could also occur here
	*/
	char line[256];
	while(fgets(line, 256, input_file) != NULL) {
		bool empty_line = true;
		int len = strlen(line);
		int start = 0;
		int end = len - 1;

		// check for empty line
		for(size_t i = 0; i < len; i++) {
			if (!isspace(line[i])) empty_line = false;
			break;
		}
		
		// remove whitespaces both ends
		for (size_t i = 0; i < len; i++) {
			if (isspace(line[i])) start++;
			else break;
		}

		int i;
		for (i = start; i <= end; i++) {
			line[i - start] = line[i];
		}
		line[i - start] = '\0'; // Null-terminate the shifted string

		for (size_t j = len; j >= 0; j--) {
			if(isspace(line[j])) end--;
			else break;
		}

		// process leading and trailing whitespaces;
		char output_line[256];
		unsigned int copy_length = end - start + 1;
		strncpy(output_line, line+start, copy_length);
		output_line[copy_length] = '\0';

		if (empty_line || (output_line[0] && output_line[1] == '/')) continue;
		else fputs(output_line, output_file); 
	}
	
	free(output_filename);
	fclose(input_file);
	fclose(output_file);
	return 0;
}