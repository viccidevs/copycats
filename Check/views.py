from django.shortcuts import render

from django.http import HttpResponse

from Check.models import Tuple;

from PlagiarismChecker import settings

delete_files = 1

def index(request):
	if request.method=="POST":
		print "="*100
		print request
		print "="*1000
		afile = request.FILES['file1']
		print afile.name,afile.read()
		instance = Tuple(file1 = request.FILES['file1'], file2 = request.FILES['file2'])
		instance.save();
		print str(instance.file1)[1:], str(instance.file2)
		file1 = str(instance.file1)[2:]
		file2 = str(instance.file2)[2:]
		dire = str(settings.MEDIA_ROOT)
		ccod1 = open(dire+file1).read().split('\n')
		ccod2 = open(dire+file2).read().split('\n')
		datastuff = process_it(file1, file2, dire)
		ccod1.insert(0,'')
		ccod2.insert(0,'')
		print datastuff[0][2]
		return render(request, 'ComparedResult\\ComparedResult.html', {'code1' : ccod1, 'code2' :ccod2, 'ccode1': ["",datastuff[1][1]], 'ccode2':["",datastuff[1][2]],\
		 'assembly1': ["",datastuff[0][1]], 'assembly2': ["",datastuff[0][2]]})
	return render(request, 'ComparedResult\\ComparedResult.html', {'ccode1':["",'''<div><mark>.def __main; .scl 2; .type 32; .endef</mark><br>.LC0:<br>.ascii "Hello world\\0"<br>.text<br>.globl main<br>.def main; .scl 2; .type 32; .endef<br>.seh_proc main<br>main:<br>pushq %rbp<br>.seh_pushreg %rbp<br>movq %rsp, %rbp<br>.seh_setframe %rbp, 0<br>subq $32, %rsp<br>.seh_stackalloc 32<br>.seh_endprologue<br>call __main<br>leaq .LC0(%rip), %rcx<br>call puts<br>movl $0, %eax<br>addq $32, %rsp<br><mark>popq %rbp</mark><br><mark>ret</mark><br><mark>.seh_endproc</mark><br><mark>.def puts; .scl 2; .type 32; .endef</mark><br></div> ''']})




'''
Code from Plagiarism Detectior
Changes must be reflected here
'''


from re import match;
import difflib;
from popen2 import popen3;


delete_files = 0;

# def compile(file_name, dire):
#     s_filename = dire + file_name.replace('.c','.s','.txt')
#     args = ['gcc', '-S','-o', s_filename, '-w', dire+file_name ]
#     print args
#     r,w,e = popen3(' '.join(args))
#     s=e.read()
#     if not s.lower().find('error') == -1:
#     	print 'ininini'
#     	print s
#         return "ERROR"
#     return s_filename;

def open_and_process(file_name, dire):
    # filename = compile(file_name, dire)
    filename = dire + file_name
    if filename=="ERROR":
    	print 'inopenndproc'
        return "ERROR"

    data = open(filename, "r")
    code = []
    side_data = []
    for line in data:
        while line[0]==' ' or line[0]=='\t':
            line=line[1:]
        line = line[:-1]
        #Removing stack push
        reg = "([a-zA-Z]+(\t)(-))[0-9]+(.*)"
        r = match(reg, line)
        if r:
            line = r.group(1)+"%d"+r.group(2)
        reg = "(.file)|(.section)|(.ident)|(.size).*"
        r = match(reg,line)
        if r:
            continue
        code.append(line)
    return [code,side_data]


def get_html_markup_diflib(a,b,dif):
    htmla = '<div>'
    htmlb = '<div>'
    marka, markb=[0 for i in range(len(a))],[0 for i in range(len(b))]
    for block in dif.get_matching_blocks():
        l1=block[0]
        l2=block[2]
        l3=block[1]
        l4=block[2]
        for lim in range(l1,l1+l2):
            marka[lim]=1;
        for lim in range(l3,l3+l4):
            markb[lim]=1
    i=0
    while i<len(a):
        if(a[i]=="\n"):
            htmla+='<br>'
        if marka[i]==1:
            htmla+= '<mark>'+a[i]+'</mark>'
        else:
            htmla+= a[i]
        i=i+1
    htmla+='</div>'
    i=0
    while i<len(b):
        if(b[i]=="\n"):
            htmlb+='<br>'
        if markb[i]==1:
            htmlb+= '<mark>'+b[i]+'</mark>'
        else:
            htmlb+= b[i]
        i=i+1
    htmlb+='</div>'
    #print ("here")
    return [htmla,htmlb]

            #print (a[lim],end="")

def compile_and_give(file1, file2, dire):
    #would retutn the thing to display
    data1 = open_and_process(file1, dire)
    data2 = open_and_process(file2, dire)
    if data1 == "ERROR" or data2=="ERROR":
    	return "ERROR"
    data1=data1[0]
    data2=data2[0]
    print data1,data2,'-'*100
    for i in range(len(data1)):
        data1[i]=data1[i].replace('\t',' ')
    for i in range(len(data2)):
        data2[i]=data2[i].replace('\t',' ')
    return get_html_markup(data1,data2)
        
def process_it(file1, file2, dire):

    #for gcc, you got to create the .s file  at dire
    assembly = compile_and_give(file1, file2, dire)
    if assembly=="ERROR":
    	assembly=[1,1,1]
    	assembly[0]="-1"
    	assembly[1]="<mark>ERROR!</mark>"
    	assembly[2]="<mark>ERROR!</mark>"
    data1 = open(dire+file1).read()
    data2 = open(dire+file2).read()
    dif=difflib.SequenceMatcher(None,data1,data2);
    mainc = get_html_markup_diflib(data1,data2,dif)
    ccode = [dif.ratio(), mainc[0], mainc[1]]
    if delete_files == 1:
        popen3('rm '+dire+file1)
        popen3('rm '+dire+file2)
        s_file1 = file1.replace('.c','.s','txt')
        s_file2 = file2.replace('.c','.s','.txt')
        popen3('rm '+dire+s_file1)
        popen3('rm '+dire+s_file2)
    return [assembly, ccode]

def get_html_markup(a,b):
    dp=[]    
    for i in xrange(len(a)):
        p=[]
        for j in xrange(len(b)):
            p.append(0)
        dp.append(p)
    i=0
    j=0
    while i<len(a):
        j=0
        while(j<len(b)):
            maxi=0
            if not i==0:
                maxi=max(maxi,dp[i-1][j])
            if not j==0:
                maxi=max(maxi,dp[i][j-1])
            if a[i]==b[j]:
                if i>0 and j>0:
                    maxi=max(maxi, dp[i-1][j-1]+1)
                else:
                    maxi=1
            dp[i][j]=maxi
            j+=1
        i+=1
    htmla = '<div>'
    stk=[]
    stk.append((i-1,j-1))
    marka, markb=[0 for i in range(len(a))],[0 for i in range(len(b))]
    while True:
        x,y = stk.pop()
        if x<0 or y<0:
            break
        elif(a[x]==b[y]):
            marka[x]=1
            markb[y]=1
            stk.append((x-1, y-1))
        elif x==0:
            stk.append((x,y-1))
        elif y==0:
            stk.append((x-1,y))
        else:
            stk.append((x-1,y) if dp[x][y]==dp[x-1][y] else (x,y-1))

    i=0
    while i<len(a):
        if marka[i]==1:
            htmla+= '<mark>'+a[i]+'</mark><br>'
        else:
            htmla+= a[i]+'<br>'
        i+=1
    i=0
    htmla+='</div>'
    htmlb = '<div>'
    while i<len(b):
        if markb[i]==1:
            htmlb+= '<mark>'+b[i]+'</mark><br>'
        else:
            htmlb+= b[i]+'<br>'
        i+=1
    htmlb+='</div>'
    return [dp[-1][-1],htmla,htmlb]

