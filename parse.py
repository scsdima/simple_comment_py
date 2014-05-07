import os
import sys
import string
import time
import shutil
from glob import glob

g_parameters = {'header':False} #make header comment for file

#------------------------------------------------------------------------------
# MAKES COMMENT FOR FILE
def make_file_comment(filename):
  global localtime 
  localtime   = time.localtime()
  time_string  = time.strftime("%Y\%m\%d %H-%M-%S", localtime)
  comment_file = open("comment_file.txt","rb")  
  comment_txt = comment_file.read(1000);  
  comment_txt =  comment_txt.replace("$file",filename)
  comment_txt =  comment_txt.replace("$date",time_string)
  comment_txt =  comment_txt.replace("$prj",os.getcwd())
  return comment_txt

#------------------------------------------------------------------------------
# MAKES COMMENT FOR FUNCTION
def make_func_comment(func_decl_txt,line_n,  func_description ):
  global ifile_str_n
  func_decl_txt.strip()
  c_ind=0
  comment_txt = ""
  func_parameters_txt=""
  func_name_txt = ""
  func_return_txt = ""
  if func_decl_txt == "" or func_decl_txt ==None or '#define' in func_decl_txt: 
    return
  #parsing :)
  c_ind = func_decl_txt.rfind(')')
  func_decl_txt = func_decl_txt[:c_ind] 
  c_ind = func_decl_txt.find('(')+1            
  func_parameters_txt  =  func_decl_txt[c_ind:]  
  c_ind = func_decl_txt.find('(')
  func_name_txt  = func_decl_txt[:c_ind]
  c_ind = func_name_txt.find(' ')
  func_return_txt =   func_name_txt[:c_ind+1]
  c_ind = func_name_txt.rfind(' ')
  func_name_txt  = func_name_txt[c_ind:]
  #FUNC prameters
  func_parameters_txt = func_parameters_txt.strip();
  if func_parameters_txt == "" :
    func_parameters_txt = "void"
  else:  
    func_parameters_txt = "\n\t" + func_parameters_txt.replace(",","\n\t")   
  #FUNC return
  func_return_txt = func_return_txt.strip()
  #FUNC name
  func_name_txt = func_name_txt.strip()  
  
  if "#define" in func_return_txt : 
    func_return_txt="MACRO"
  #check on Warnings  
  if func_return_txt == "" or func_name_txt == "" :
    print chr(7),"[%d]Warning!"%(line_n)
  #out
  comment_file = open("comment_func.txt","rb")  
  comment_txt =comment_file.read(1000);  
  comment_txt=  comment_txt.replace("$par",func_parameters_txt)
  comment_txt=  comment_txt.replace("$func",func_name_txt)
  comment_txt=  comment_txt.replace("$ret",func_return_txt)
  comment_txt = comment_txt.replace("$descr",  func_description)  
  #D: print   comment_txt,"\nfunction=",func_name_txt ,"\nparameters=", func_parameters_txt
  return comment_txt

#------------------------------------------------------------------------------
def process_file(ifilename):
  global g_parameters
  g_parameters['header'] = False
  ofile=None
  ifile = None
  ifile_function_count=0
  br_level=0  
  istr=""
  ostr=""
  func_head_str=""
  ifile_line_n=0
  possible_func_descr = ""
  ofilename = ifilename
  ifilename = ifilename+"_"
  if shutil.copyfile(ofilename,ifilename):
    print "file copied:",ofilename," to ",ifilename+"_"
    
  ifile= open(ifilename,"rb");
  ofile= open(ofilename,"wb");
  ofile.write(make_file_comment(ofilename))

  if ".h" in ifilename:
    g_parameters['header'] = True

  #countfunctions
  while True:  
    ifile_line_n +=1
    s= ifile.readline();
	    
    if len(s) == 0 :
      break;
    #function detection
    if ('(' in s) and (')' in s) and (br_level == 0):
      ifile_function_count += 1
      if g_parameters['header'] == False:
	func_comment_text = make_func_comment(s,ifile_line_n,  possible_func_descr )
	if func_comment_text != None and func_comment_text != "":
          ofile.write(func_comment_text)
    for symbol in s :
      if symbol == '{' : br_level+=1
      if symbol == '}' : br_level-=1
    #ofile.write(str(br_level))
    ofile.write(s);

    if ('//' in s) : 
      possible_func_descr =s.replace('//','')
    else: 
      possible_func_descr = "---"
  return ifile_function_count  




#------------------------------------------------------------------------------
def main():
  global g_parameters
  files_count=0
  print "\n\n\n*****Autocomment script*****\n\n\n"
  del sys.argv[0]
  filelist=[]
  for txt in sys.argv:
    if '*' in txt :
      filelist += glob(txt)
    elif txt == 'h':
      g_parameters['header']=True
    else :
      filelist.append(txt)

  for i in range(0,len(filelist)):
    function_count = process_file(filelist[i])    
    print ">File:",filelist[i],"functions:",function_count
    files_count+=1

  print "TOTAL files processed:",files_count


#------------------------------------------------------------------------------
if __name__ == '__main__': 
  main()