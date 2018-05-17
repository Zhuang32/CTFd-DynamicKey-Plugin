from flask import current_app as app, render_template, request, redirect, abort, jsonify, url_for, session, Blueprint, Response, send_file
from flask.helpers import safe_join
import os
import sys
import hashlib
import zipfile
Path = []
from aes import prpcrypt
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
        pc = prpcrypt(token[-32:])
        return pc

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

def generate_executable_file(content, filename):
        teamdir_path = Path[0]
	tmpfile_path = safe_join(teamdir_path, "tmp.c")
        file_path = safe_join(teamdir_path, filename)
        with open(tmpfile_path, 'w') as f:
		f.write(content)
        os.system("gcc %s -o %s"%(tmpfile_path,file_path))
        os.system("rm %s"%tmpfile_path)
