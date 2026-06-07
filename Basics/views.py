from django.shortcuts import render

# Create your views here.
def Sum(request):
    if request.method == 'POST':
        a=request.POST.get('txt_num1')
        b=request.POST.get('txt_num2')
        c=int(a)+int(b)
        return render(request,'Basics/Sum.html',{'Result':c})
    else:
        return render(request,'Basics/Sum.html')

def Largest(request):
    if request.method=='POST':
        a=int(request.POST.get('txt_num1'))
        b=int(request.POST.get('txt_num2'))
        if a>b:
            largest=a
        else:
            largest=b
        return render(request,'Basics/Largest.html',{'Result':largest})
    else:
         return render(request,'Basics/Largest.html')
    
def Calculator(request):
    if request.method=='POST':
        a=int(request.POST.get('num1'))
        b=int(request.POST.get('num2'))
        op=request.POST.get('btn')
        if op == "+":
            c=a+b
        elif op == "-":
            c=a-b
        elif op == "*":
            c=a*b
        else:
            c=a/b
        return render(request,'Basics/Calculator.html',{'Result':c})
    else:
        return render(request,'Basics/Calculator.html')
