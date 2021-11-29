import sys

from PyQt5.QtCore import QTimer

from PyQt5.QtWidgets import QApplication
w = 5
c = w
c = c + 4
print(w)

st1 = 'a'
st2 = st1
st2  = st2 + 'fa'
print(st1)

l1 = [1,2,3]
l2 = l1
l2.append('fa')
print(l1)