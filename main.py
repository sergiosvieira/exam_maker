import pyexcel_ods3 as pods
import json
import unidecode
import datetime
import random
import pdb

grades = ["A", "B", "C", "D", "E"]
show_answer = False
input_file = open("modelo.tex", "r")
model = input_file.read()
data = pods.get_data("fonte.ods")
counter = 0
course = ""
teacher_name = ""
lesson = ""
test = ""
questions = []
first_item = 2
for i in data['Sheet1']:
    if len(i) == 0:
        continue
    if counter < 5:
        if counter == 0:
            course = i[1]
        elif counter == 1:
            teacher_name = i[1]
        elif counter == 2:
            lesson = i[1]
        elif counter == 3:
            test = i[1]
        elif counter == 4:
            counter += 1
            continue
        counter += 1
    else:
        questions.append(i)
# print(model)
filename = "prova"
output_file = open("_" + filename + ".tex", "a")
str_output = model.replace("@curso", course).replace(
    "@disciplina", lesson).replace(
    "@professor", teacher_name).replace(
    "@prova", test)
str_questions = ""
# print(questions)
# pdb.set_trace()]
gabarito = r"""
\begin{table}
\centering
\begin{tabular}{|l|c|}
\hline
"""
for i, q in enumerate(questions):
    if str(q[1]).lower() == "sim":
        str_questions += r'\newpage'+"\n"
    str_questions += r'\question[1] \textbf{'+str(q[first_item])+"}\n"
    # print(q)
    # pdb.set_trace()
    if len(str(q[first_item+1])) > 0:
        str_questions += r'\begin{verbatim}'+"\n"
        str_questions += str(q[first_item+1])+"\n"
        str_questions += r'\end{verbatim}'+"\n"
    if len(str(q[first_item+2])) > 0:
        size = float(q[0])
        str_questions += r'\begin{figure}[hbt!]'+"\n"
        str_questions += r'\includegraphics[width='+str(size)+r'\textwidth]{'+str(q[first_item+2])+'}'+"\n"
        str_questions += r'\centering'+"\n"
        str_questions += r'\end{figure}'+"\n"
    if len(str(q[first_item+3])) > 0:
        str_questions += r'\par \textbf{' + str(q[first_item+3]) + "}\n"
    random_q = q[first_item+4:-1]
    answer_index = int(q[-1])-1
    answer = random_q[answer_index]
    r = random.SystemRandom()
    r.shuffle(random_q)
    if len(random_q) != 0:
        str_questions += r'\begin{choices}'+"\n"
    for w in random_q:
        if len(str(w)) == 0:
            continue
        str_questions += r'\choice '+str(w)+"\n"
    if len(random_q) != 0:
        str_questions += r'\end{choices}'+"\n"
    item = grades[random_q.index(answer)]
    gabarito += f"Q{i+1} & {item}"+r'\\'+'\n'
    gabarito += r'\hline'+"\n"
    if show_answer:
        str_questions += "Resp. " + str(answer) + f"- item {item}\n"

str_output = str_output.replace("@questoes", str_questions)
str_output = str_output.replace('#', '\\#')
str_output = str_output.replace('$', '\\$')
str_output = str_output.replace('@par', '\\par')
str_output = str_output.replace('@cifrao', '$')
gabarito += r"""
\end{tabular}
\end{table}
"""
str_output = str_output.replace('@gabarito', 
    "\n"+r'\newpage'+"\n"+gabarito)
output_file.write(str_output)
output_file.close()
