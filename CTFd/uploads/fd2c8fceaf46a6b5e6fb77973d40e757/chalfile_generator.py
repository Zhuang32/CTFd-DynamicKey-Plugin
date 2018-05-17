import os,sys
plugins_path = os.path.join(sys.argv[3], "plugins")
sys.path.append(plugins_path)
from chalfile_generator_lib import generator_init, generate_executable_file, generator_finalize
##dont remove the codes above

pc = generator_init()
flag = pc.encrypt("PKUCTF{Dynamic_Flag_Is_Powerful}")
text = r'''#include <stdio.h>
int main(int argc, char** argv)
{
    unsigned char flag[] = "%s";
    printf("Flag is %%s\n", flag);
    return 0;
}
''' % flag
generate_executable_file(text, "reverse")

generator_finalize()
