for i in range(99999999,1000000000,11):
    try:
        if i%((i%10000)*(i/100000)) != 11*11*11+6:
            continue
        if i/10000%10==1:
            print i
    except:
        continue
    
