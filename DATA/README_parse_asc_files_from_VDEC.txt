

1) run

python3 extracor3.py

this will read a file named e.g. dag123.asc and parse the data into named file:

-rw-rw-r-- 1 pth pth 33430569 Jun  1 13:03 I18L4_BDF_1727999.txt
-rw-rw-r-- 1 pth pth 10465370 Jun  1 13:03 I18L3_BDF_523199.txt
-rw-rw-r-- 1 pth pth  1720253 Jun  1 13:03 I18L3_BDF_85600.txt
-rw-rw-r-- 1 pth pth 21677665 Jun  1 13:03 I18L3_BDF_1091200.txt
-rw-rw-r-- 1 pth pth 33060407 Jun  1 13:03 I18L2_BDF_1727999.txt
-rw-rw-r-- 1 pth pth 33481602 Jun  1 13:03 I18L1_BDF_1727999.txt
-rw-rw-r-- 1 pth pth 33577060 Jun  1 13:03 I18H4_BDF_1727999.txt
-rw-rw-r-- 1 pth pth 33044993 Jun  1 13:03 I18H3_BDF_1727999.txt
-rw-rw-r-- 1 pth pth 33665005 Jun  1 13:03 I18H2_BDF_1727999.txt
-rw-rw-r-- 1 pth pth 33968017 Jun  1 13:03 I18H1_BDF_1727999.txt

Sometimes there are multiple files from the same instrument - here there are three L3 BDF files and theyneed to be concattenated manually:

(base) pth@Monster:~/WORKSHOP/QAANAAQ/DATA$ ls -alt I18L3*BDF*
-rw-rw-r-- 1 pth pth 10465370 Jun  1 13:03 I18L3_BDF_523199.txt
-rw-rw-r-- 1 pth pth  1720253 Jun  1 13:03 I18L3_BDF_85600.txt
-rw-rw-r-- 1 pth pth 21677665 Jun  1 13:03 I18L3_BDF_1091200.txt
(base) pth@Monster:~/WORKSHOP/QAANAAQ/DATA$ cat I18L3_BDF_85600.txt >> I18L3_BDF_1091200.txt
(base) pth@Monster:~/WORKSHOP/QAANAAQ/DATA$ cat I18L3_BDF_523199.txt >> I18L3_BDF_1091200.txt
rm I18L3_BDF_85600.txt I18L3_BDF_523199.txt

for instance.

The files can then be plotted in R using the script 'plot_I18_files_2.Rmd'
