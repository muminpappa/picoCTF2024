#include <unistd.h>
#include <stdio.h>
#include <sys/wait.h>

pid_t pid;
char *cmd = "/bin/sh";

int main(void)
{

  pid = fork();
  
  if (pid < 0) { /* error occurred */ 
    fprintf(stderr, "Fork Failed"); 
    return 1;
  }
  else if (pid == 0) { /* child process */
    if(execl(cmd, NULL) < 0)
      perror(cmd);
  }
  else { /* parent process */
    /* Wait on all child processes */
    while(wait(NULL) > 0);
  }
  return 0;
}
