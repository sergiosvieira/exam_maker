#!\bin\bash
for i in $(ls _*.tex); do
	pdflatex -interaction nonstopmode $i
	pdflatex -interaction nonstopmode $i
done
