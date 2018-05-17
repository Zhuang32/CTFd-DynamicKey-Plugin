from flask import current_app as app, render_template, request, redirect, abort, jsonify, url_for, session, Blueprint, Response, send_file
from flask.helpers import safe_join
import os
import sys
import hashlib
import zipfile
Path = []
def generator_init():
        filedir_path = sys.argv[1]
        token = sys.argv[2]
	m = hashlib.md5()   
        m.update(token)   
        mtoken = m.hexdigest()
        teamdir_path = safe_join(filedir_path, mtoken)
	os.mkdir(teamdir_path)
        Path.append(teamdir_path)
        teamfile_path = safe_join(filedir_path, mtoken+".zip")
        Path.append(teamfile_path)

def generator_finalize():
        teamdir_path = Path[0]
        teamfile_path = Path[1]
	with zipfile.ZipFile(teamfile_path, 'w', zipfile.ZIP_DEFLATED) as mzip:
		for dirpath, dirnames, filenames in os.walk(teamdir_path):
			fpath = dirpath.replace(teamdir_path,'') 
			fpath = fpath and fpath + os.sep or ''
			for filename in filenames:
				mzip.write(os.path.join(dirpath, filename),fpath+filename)

def generate_file(content, filename):
        teamdir_path = Path[0]
	file_path = safe_join(teamdir_path, filename)
        with open(file_path, 'w') as f:
		f.write(content)
        
generator_init()
pwn_text = r'''#include <stdio.h>
int main(int argc, char** argv)
{
    int modified;
    char buffer[10];
    modified = 0;
    printf("Please fill the buffer:\n");
    fflush(stdout);
    gets(buffer);
    if (modified != 0)
    {
        printf("Congratulations, you got the shell.\n");
        printf("Remember you can only read your own team's flag!\n");
        fflush(stdout);
        system("/bin/sh");
        exit(0);
    }
    else
    {
        printf("Please try again.\n");
    }
    return 0;
}'''
generate_file(pwn_text, "pwn.c")
generator_finalize()
