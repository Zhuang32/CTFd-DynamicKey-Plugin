from flask import current_app as app, render_template, request, redirect, abort, jsonify, url_for, session, Blueprint, Response, send_file
from flask.helpers import safe_join
import os
import sys
import hashlib
import zipfile
def generator(filedir_path, token):
        m = hashlib.md5()   
        m.update(token)   
        mtoken = m.hexdigest()
        teamdir_path = safe_join(filedir_path, mtoken)
	os.mkdir(teamdir_path)

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
        pwn_path = safe_join(teamdir_path, "pwn.c")
        with open(pwn_path, 'w') as f:
		f.write(pwn_text)

        teamfile_path = safe_join(filedir_path, mtoken+".zip")
	with zipfile.ZipFile(teamfile_path, 'w', zipfile.ZIP_DEFLATED) as mzip:
		for dirpath, dirnames, filenames in os.walk(teamdir_path):
			fpath = dirpath.replace(teamdir_path,'') 
			fpath = fpath and fpath + os.sep or ''
			for filename in filenames:
				mzip.write(os.path.join(dirpath, filename),fpath+filename)

generator(sys.argv[1], sys.argv[2])
