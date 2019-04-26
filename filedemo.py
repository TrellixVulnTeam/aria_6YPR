# -*- coding: utf8 -*-
__author__ = 'yqzhang'
import os, zipfile
#打包目录为zip文件（未压缩）
def make_zip(source_dir, output_filename):
    zipf = zipfile.ZipFile(output_filename, 'w')
    pre_len = len(os.path.dirname(source_dir))
    for parent, dirnames, filenames in os.walk(source_dir):
        for filename in filenames:
            pathfile = os.path.join(parent, filename)
            arcname = pathfile[pre_len:].strip(os.path.sep)   #相对路径
            zipf.write(pathfile, arcname)
    zipf.close()

zipf = zipfile.ZipFile('1.zip', 'w')
pre_len = len(os.path.dirname('D:\lg-apiscript-python\ApkChannelBuildTool2\srcApks'))
for parent, dirnames, filenames in os.walk('D:\lg-apiscript-python\ApkChannelBuildTool2\srcApks'):
    for filename in filenames:
        pathfile = os.path.join(parent, filename)
        arcname = pathfile[pre_len:].strip(os.path.sep)   #相对路径
        zipf.write(pathfile, arcname)
zipf.close()

# make_zip('D:\lg-apiscript-python\ApkChannelBuildTool2\srcApks','1.zip')