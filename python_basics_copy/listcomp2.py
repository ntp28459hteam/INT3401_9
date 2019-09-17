strings = ['Some string','Art','Music','Artificial Intelligence']
# Print all elements satisfying if-condition
print [x.lower() for x in strings if len(x) > 5]
# Equivalently, we print all the elements by iterating our list with an if-condition inside forloop
for str in strings:
    if(len(str) > 5):
        print str.lower()