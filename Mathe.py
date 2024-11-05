import math as m

tolerance = 1e-9

def equal(a, b, tolerance=1e-9):
    return abs(a - b) < tolerance

def VekEqual(a, b):
    for i in range(a.n):
        if not equal(a.tupel[i], b.tupel[i]):
            return False
    return True

class Vektor:

  def __init__(self, x, n):
    self.tupel = x
    self.n = n
    self.length = self.length()

  def length(self):
    return sum([x**2 for x in self.tupel])**0.5

  def __add__(self, other):
    return Vektor(tuple([self.tupel[i] + other.tupel[i] for i in range(self.n)]), self.n)
  
  def __sub__(self, other): 
    return Vektor(tuple([self.tupel[i] - other.tupel[i] for i in range(self.n)]), self.n)
  
  def skalar(self, other):
    return sum([self.tupel[i] * other.tupel[i] for i in range(self.n)])
  
  def kreuz(self, other):
    return Vektor(tuple([self.tupel[(i+1)%self.n] * other.tupel[(i+2)%self.n] - self.tupel[(i+2)%self.n] * other.tupel[(i+1)%self.n] for i in range(self.n)]), self.n)
  
  def __mul__(self, other):
    return Vektor(tuple([self.tupel[i] * other for i in range(self.n)]), self.n)
  
  def kolinear(self, other):
    return equal( self.skalar(other), (self.length * other.length) )
  
  def orthogonal(self, other):
    return equal( self.skalar(other), 0 )
  
  def winkel(self, other):
    return m.acos(self.skalar(other) / (self.length * other.length))
  
  def sum(self):
    return sum(self.tupel)
  
  def __str__(self):
    return str(self.tupel)
  
class Gerade:

  def __init__(self, stutz, richtung):
    self.stutz = stutz
    self.richtung = richtung

  def __call__(self, t):
    return Vektor(tuple([self.stutz.tupel[i] + t * self.richtung.tupel[i] for i in range(self.stutz.n)]), self.stutz.n)

  def schnittpunkt(self, other):
    if self.richtung.kolinear(other.richtung) & (self.stutz - other.stutz).kolinear(other.richtung):
      return 0
    elif self.richtung.kolinear(other.richtung):
      return None
    elif self.stutz == other.stutz:
      return self.stutz
    else:
      winkel = self.richtung.winkel(other.richtung)
      v = (self.stutz - other.stutz).length / m.sin(winkel)
      winkel2 = (self.stutz - other.stutz).winkel(other.richtung)
      l = v * m.sin(winkel2)
      s = l / self.richtung.length
      print(winkel, winkel2, v, l, s)
      return self(s)

  def __str__(self):
    return f"{self.stutz} + t * {self.richtung}"


class Ebene:

  def __init__(self, normal, abstand):
    self.normal = normal
    self.abstand = abstand

  def __call__(self, x):
    return equal(self.normal.skalar(x), self.abstand)
  
  def schnittgerade(self, other):
    richtung = self.normal.kreuz(other.normal)
    a = self.normal.tupel[0]
    b = self.normal.tupel[1]
    c = self.abstand
    d = other.normal.tupel[0]
    e = other.normal.tupel[1]
    f = other.abstand
    y = (a * f - d * c) / (e * a - b * d)
    x = (c - b * y) / a
    stutz = Vektor((x, y, 0), 3)
    return Gerade(stutz, richtung)

  def schnittpunkt(self, other):
    if self.normal.orthogonal(other.richtung) & self(other.stutz):
      return other.stutz
    elif self.normal.orothogonal(other.richtung):
      return None
    else:
      s = (self.abstand - sum(other.stutz)) / self.normal.skalar(other.richtung)
      return other(s)



  
  
  def __str__(self):
    return f"{self.normal} * x = {self.abstand}"
  


def UnitTest():
  v1 = Vektor((1, 2, 3), 3)
  v2 = Vektor((4, 5, 6), 3)

  v3 = v1 + v2

  assert v3.tupel == (5, 7, 9)

  v3 = (v3 - v2) * 3

  assert v3.tupel == (3, 6, 9)

  assert v3.kolinear(v1) == True

  v4 = v1 - v2

  assert v4.tupel == (-3, -3, -3)

  v5 = v1 * 2

  assert v5.tupel == (2, 4, 6)

  assert v1.skalar(v2) == 32

  assert v1.length == 14**0.5

  g = Gerade(v1, v2)

  assert g(2).tupel == (9, 12, 15)

  assert v1.kolinear(v2) == False

  assert (v1 - v1).kolinear(v2) == True

  print("g.richtung.kolinear(g.richtung) == True, s = ", g.richtung.skalar(g.richtung), "l == ", g.richtung.length * g.richtung.length, "True == ", g.richtung.skalar(g.richtung) == 77.00000000000001)

  assert g.richtung.kolinear(g.richtung) == True

  print("g.schnittpunkt(Gerade(v1, v2)) == 0, s = ", g.schnittpunkt(Gerade(v1, v2)))

  assert g.schnittpunkt(g) == 0

  assert g.schnittpunkt(Gerade(v1, v1)) == v1
  print("g.schnittpunkt(Gerade(v1, v1)) == 0, s = ", g.schnittpunkt(Gerade(v1, v1)))

  assert g.schnittpunkt(Gerade(v3, v2)) == None

  assert v1.kolinear(v2) == False

  assert v2.kolinear(v1) == False

  assert v1.winkel(v2) == 0.2257261285527342

  v6 = Vektor((1, 0, 0), 3)
  v7 = Vektor((0, 1, 0), 3)

  assert v6.winkel(v7) == 1.5707963267948966

  g1 = Gerade(v6, v7)
  g2 = Gerade(v7, v6)

  print("g1.schnittpunkt(g2) == Vektor((1, 1, 0), 3), s = ", g1.schnittpunkt(g2))

  assert VekEqual(g1.schnittpunkt(g2), Vektor((1, 1, 0), 3))

  e1 = Ebene(v1, 6)

  assert e1(v1) == False

  e2 = Ebene(v6, 1)

  assert e2(v6) == True

  assert e2(v7) == False  

  assert v1.kreuz(v2).tupel == (-3, 6, -3)
  assert v7.kreuz(v6).tupel == (0, 0, -1)
  
  assert e2.schnittpunkt(g1) == g1.stutz

  v1 = Vektor((-1, 2, 1), 3)
  v2 = Vektor((1, 4, 3), 3)
  e1 = Ebene(v1, 1)
  e2 = Ebene(v2, 7)

  g = e1.schnittgerade(e2)

  print(g)

  v1 = Vektor((-4, 3, 2), 3)
  v2 = Vektor((2, 1, -1), 3)
  e1 = Ebene(v1, 5)
  e2 = Ebene(v2, 0)
  
  g = e1.schnittgerade(e2)

  print(g)

  v1 = Vektor((3, 2, 0), 3)
  v2 = Vektor((-1, 2, 4), 3)
  v3 = Vektor((2, 1, 0), 3)
  v4 = Vektor((-2, 1, 4), 3)

  g1 = Gerade(v1, v2)
  g2 = Gerade(v3, v4)

  v5 = g1.schnittpunkt(g2)

  print(v5)

  print("Alle Tests erfolgreich")



v1 = Vektor((1, 2, 3), 3)
v2 = Vektor((4, 5, 6), 3)

v3 = v1 + v2

print(v3.tupel) # (5, 7, 9)

v4 = v1 - v2

print(v4.tupel) # (-3, -3, -3)

v5 = v1 * 2

print(v5.tupel) # (2, 4, 6)

UnitTest()

