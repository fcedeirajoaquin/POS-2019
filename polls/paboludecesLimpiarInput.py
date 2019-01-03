def conseguirInput(cadena):
    inputLimpio=""
    corchetes=0
    encontroInput=False
    pasoLos2Car=False
    conta=0
    for elemento in cadena:
        if encontroInput==True and conta == 2 and elemento=="'":
            return inputLimpio
        if elemento == "[" and encontroInput==False:
            corchetes+=1
        if encontroInput==True and conta<2:
            conta+=1
        if corchetes==2:
            encontroInput=True
        if conta==2:
            if elemento!="'":
                inputLimpio+=elemento

stringuin=r"<QueryDict:%20%7Bu'csrfmiddlewaretoken':%20[u'sSbOWJBDAmLDipnTFe51O8L8Dd0XcTEKT9ET9nJilJsdE74FPDeAQGrhrwQ548ai'],%20u'your_name':%20[u'asdasd']%7D>"
