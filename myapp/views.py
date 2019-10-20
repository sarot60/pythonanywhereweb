from IPython.display import display
from django.shortcuts import render
from django.http import HttpResponse
from math import e, sin, cos, tan


def index(request):
    return render(request, 'myapp/index.html')


def f(x, fx):
    return eval(fx)


def d2(x, dx):
    return eval(dx)


def sign(x):
    return 1 if x > 0 else -1


def differentiation(req):
    if req.method == 'POST':
        function = req.POST.get('function')
        fx = req.POST.get('fx')
        x = eval(req.POST.get('x'))
        h = eval(req.POST.get('h'))

        re1 = (f(x+h, fx) - f(x-h, fx))/(2*h)
        re2 = (f(x+h, fx) - 2*f(x, fx)+f(x-h, fx))/(h**2)
        re3 = (f(x+2*h, fx) - 2*f(x+h, fx) + 2 *
               f(x-h, fx) - f(x-2*h, fx))/2*h**3
        re4 = (f(x+2*h, fx) - 4*f(x+h, fx) + 6*f(x, fx) -
               4*f(x-h, fx) + f(x-2*h, fx)) / h**4

        print(f'fu={function} fx={fx} x={x} h={h} re1={re1}')
        return render(req, 'myapp/differentiation.html', {'re1': re1, 're2': re2, 're3': re3, 're4': re4})
    return render(req, 'myapp/differentiation.html')


def integration(req):
    if req.method == 'POST':
        function = req.POST.get('function')
        fx = req.POST.get('fx')
        print(f, function)
        if function == 'trapezoidal':
            a = 1
            b = 2
            n = 12

            h = (b - a)/n
            I = [f(a, fx), f(b, fx)]
            I.extend([2*f(a+i*h, fx) for i in range(1, n)])

            x = sum(I)*h/2

            return render(req, 'myapp/integration.html', {'x': x})
        elif function == 'simson':
            a = 1
            b = 2
            n = 12

            h = (b - a)/n
            I = [f(a, fx), f(b, fx)]
            I.extend([2*f(a+i*h, fx) for i in range(2, n, 2)])
            I.extend([4*f(a+i*h, fx) for i in range(1, n, 2)])
            x = sum(I)*h/3
            return render(req, 'myapp/integration.html', {'x': x})
    return render(req, 'myapp/integration.html')


def rootfinding(req):
    if req.method == 'POST':
        function = req.POST.get('function')
        fx = req.POST.get('fx')
        print(function, fx)
        if function == 'incremental':
            epsilon = 10**-2
            step = 10**-4
            x = -3
            n = 0
            while abs(f(x, fx)-0) > epsilon:
                x += step
                n += 1
            return render(req, 'myapp/rootfinding.html', {'x': x})
        elif function == 'bisection':
            x = 0
            a = -2
            b = 1
            eps = 10**-3
            count = 0
            while True:
                count += 1
                m = (a+b)/2
                if abs(f(m, fx)-0) < eps:
                    print(f'หาค่าต่ำสุดเจอแล้วx = {m}')
                    print(f'จำนวนครั้ง{count}')
                    x = m
                    break
                else:
                    if sign(f(a, fx)) == sign(f(m, fx)):
                        a = m
                        print(f'ขยับ a ช่วงค่าใหม่ที่ต้องค้นหาคือ ({a}, {b})')
                    else:
                        b = m
                        print(f'ขยับ b ช่วงค่าใหม่ที่ต้องค้นหาคือ ({a}, {b})')
            return render(req, 'myapp/rootfinding.html', {'x': x})
        elif function == 'newton':
            dxx = req.POST.get('dx')
            x = 0
            a = -1.5
            b = 1
            epsilon = 10**-4
            x = (a+b)/2
            n = 0
            dx = 1000000000000000
            while abs(dx) > epsilon:
                dx = -f(x, fx)/d2(x, dxx)
                x = dx
                n += 1
            return render(req, 'myapp/rootfinding.html', {'x': x})
        elif function == 'secant':
            x = -1
            n = 20
            h = 0.0000001
            for i in range(n):
                Qx = (f(x+h, fx) - f(x, fx)) / h
                dx = - f(x, fx)/Qx
                x = x+dx
            return render(req, 'myapp/rootfinding.html', {'x': x})
    return render(req, 'myapp/rootfinding.html')
