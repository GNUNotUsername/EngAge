/*
 * imagegen suburb in|de percentage emoji outfile
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#define ARGS1	"magick", "magick", "base.png"
#define ARGS2	"-layers", "flatten", "-font", "Sansita-One-Regular", "-pointsize", "64", "-fill", "black", "-annotate", "+400+250"
#define ARGS3	"-annotate", "+200+1000"
#define TOP_EXT	31
#define BOT_EXT	46
#define SUBURB	1
#define IN		2
#define PERCENT	3
#define EMOJI	4
#define OUTFILE	5

int main(int argc, char **argv) {
	char *bottom, *top;

	top = calloc(strlen(argv[SUBURB]) + TOP_EXT, sizeof(char));
	bottom = calloc(strlen(argv[PERCENT]) + BOT_EXT, sizeof(char));
	sprintf(top, "%s's senior citizens are feeling", argv[SUBURB]);
	sprintf(bottom, "Community wellbeing %screased by %s%c this month", argv[IN], '%', argv[PERCENT]);
	printf(bottom);
	fflush(stdout);
	printf("%s", top);
	fflush(stdout);
	execlp(ARGS1, argv[EMOJI], ARGS2, top, ARGS3, bottom, argv[OUTFILE], NULL);
}
