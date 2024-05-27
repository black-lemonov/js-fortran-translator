import json
import re

CLASSES_OF_TOKENS = ['W', 'I', 'O', 'R', 'N', 'C']

def is_identifier(token):
    return ((token in inverse_tokens) and re.match(r'^I\d+$', inverse_tokens[token])) or re.match(r'^М\d+$', token)

def is_constant(token):
    return ((token in inverse_tokens) and re.match(r'^C\d+$', inverse_tokens[token])) or ((token in inverse_tokens) and re.match(r'^N\d+$', inverse_tokens[token])) or token.isdigit()

def is_operation(token):
    return (token in inverse_tokens) and re.match(r'^O\d+$', inverse_tokens[token])

# лексемы (код-значение)
tokens = {}

# файлы, содержащие все таблицы лексем
for token_class in CLASSES_OF_TOKENS:
    with open('lexemes/%s.json' % token_class, 'r') as read_file:
        data = json.load(read_file)
        if token_class == 'I':
            for k, v in data.items():
                if v[0] == '$':
                    data[k] = v[1:]
        tokens.update(data)

# лексемы (значение-код)
inverse_tokens = {val: key for key, val in tokens.items()}

replace = {'abs': 'Math.abs', 'cos': 'Math.cos', 'exp': 'Math.exp', 'log': 'Math.log', 'sin': 'Math.sin', 'sqrt': 'Math.sqrt', 'print': 'alert'}

# файл, содержащий обратную польскую запись
f = open('inter-results/2_reverse_polish_entry.txt', 'r')
inp_seq = f.read()
f.close()

t = re.findall(r'(?:\'[^\']*\')|(?:"[^"]*")|(?:[^ ]+)', inp_seq)
t = [i[1:] if i[0] == '$' else i for i in t]

i = 0
stack = []
out_seq = ''
is_func = False
program_name = ''
while i < len(t):
    if is_func == True and not(is_identifier(t[i])):
        out_seq += ' {\n'
        is_func = False
    if is_identifier(t[i]) or is_constant(t[i]):
        stack.append(replace[t[i]] if t[i] in replace else t[i])

    elif t[i] == 'НП':
        stack.pop()
        stack.pop()
        arg1 = stack.pop()
        out_seq += f'program {arg1}'
        program_name = arg1
        is_func = True
    elif t[i] == 'КП':
        out_seq += f'end program {program_name}'
    elif t[i] == 'КО':
        stack.pop()
        stack.pop()
    elif t[i] == 'УПЛ':
        arg1 = stack.pop()
        arg2 = stack.pop()
        out_seq += f'if (.not.({arg2})) then go to {arg1}\nend if\n{arg1}: '
    elif t[i] == 'БП':
        arg1 = stack.pop()
        #out_seq += f'go to {arg1}\n'
    elif t[i] == ':':
        arg1 = stack.pop()
        #out_seq += f'{arg1}: '
    elif is_operation(t[i]):           
        if t[i] == '=':
            arg1 = stack.pop()
            arg2 = stack.pop()
            out_seq += f'{arg2} = {arg1}\n'
        else:
            operation = replace[t[i]] if t[i] in replace else t[i]
            arg1 = stack.pop()
            if t[i] != 'not':
                arg2 = stack.pop()
                stack.append(f'({arg2} {operation} {arg1})')
            else:
                stack.append(f'({operation}{arg1})')

    elif t[i] == 'АЭМ':
        k = int(stack.pop())
        a = []
        while k != 0:
            a.append(stack.pop())
            k -= 1
        a.reverse()
        out_seq += a[0] + '[' + ']['.join(a[1:]) + ']'
    elif t[i] == 'Ф':
        k = int(stack.pop()) + 1
        a = []
        while k != 0:
            a.append(stack.pop())
            k -= 1
        a.reverse()
        stack.append('call ' + a[0] + '(' + ', '.join(a[1:]) + ')')
    elif t[i] == 'alert':
        out_seq += 'print ' + stack.pop() + '\n'
    i += 1

# Находим все строки с объявлениями переменных
variable_declarations = re.findall(r'(\w+)\s*=\s*(.*)', out_seq)

declarations = ''

# Определяем тип каждой переменной и сохраняем в новой строке
for declaration in variable_declarations:
    var_name, var_value = declaration
    var_name = var_name.strip()
    var_value = var_value.strip()

    if var_value.isdigit():
        declarations += f"integer :: {var_name}\n"
    elif re.match(r'^-?\d+(?:\.\d+)?$', var_value) is not None:
        declarations += f"real :: {var_name}\n"


FORTRAN_TEMPLATE = '''
program main
{0}
{1}
end program main
'''

# файл, содержащий текст на выходном языке программирования
f = open('inter-results/3_fortran.txt', 'w')
f.write(FORTRAN_TEMPLATE.format(declarations, out_seq.replace('М', 'M')))
f.close()