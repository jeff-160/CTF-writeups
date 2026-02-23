#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

void persuade(persuation)
{
	if (persuation == 20)
	{
		puts("Fine you can get a flag for christmas");
		system("/bin/cat flag.txt");
		exit(0);
	}
}

int vuln()
{
	char buf[64];
	puts("Why should I get you a flag for christmas?");
	puts("Persuade: ");
	gets(buf);
	persuade(strlen(buf)%20);
}

int main()
{
	setvbuf(stdout, NULL, _IONBF, 0);
	vuln();
	
	puts("No, we already have flag at home");
	puts("NBY{flag_at_home}");
	puts("");
	puts("Better luck next christmas");
	return 0;
}

