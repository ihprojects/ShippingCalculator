"""Program calculates prices for DHL and Hermes 
depending on parcel size and weight, only for DE
User inputs sizes of all three sides in cm in any order
one per each input and weight of parcel in kg.
As a result prices are displayed.

For example:

User inputs:
side1 = 10
side2 = 62
side3 = 20
weight = 5

Results:
L = 30 cm, W = 10 cm, H = 20 cm, weight = 5 kg
DHL : "S" = 4.99€
Hermes : 

Additionally if by descreasing any side by 2 cm of less
price can be less, user gets a warning

WARNING: if you decress length from 62 to 60, 
then DHL : "S" = 4.99 €

DHL	€ 3,79 (Päckchen) / 5,99 / 8,49
DPD	€ 4,39 / 4,99 / 9,90
GLS	€ 4,30 / 4,90 / 9,90
Hermes	€ 4,30 (Päckchen) / 4,95 / 5,95
UPS.de	€ 6,55 / 8,33 / 17,85

"""