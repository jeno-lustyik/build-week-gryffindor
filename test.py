a = "Published October 2 2006 by Alfred A. Knopf"
b = a.split()
years = []
for i in b:
    if i.isdigit() and len(i) == 4:
        years.append(int(i))
print(years)