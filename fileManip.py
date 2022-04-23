class fileObj:
    def __init__(obj,filename):
    #String adds ./ for file address, will add to common file
        obj.name = './'+filename
        obj.f = open(obj.name,'w')
        obj.f.write('Hazard Type\t|Parameter of Interest\t|Parameter Value\t|Location X Coordinate [cm]\t|Location Y Coordinate [cm]')
    def hazardwrite(obj,data):
    #data must be an array of length 4 with the following values:
        # 1. Type, either 1 for Temperature or 2 for Electrical
        # 2. Intensity
        # 3. X Coordinate
        # 4. Y Coordinate
        if data[0] == 1:
            typ = 'Temperature'
            poi = 'Kelvin [K]'
            pv = data[1]
            locx = data[2]
            locy = data[3]
        else:
            typ = 'Electrical'
            poi = 'Tesla (T)'
            pv = round(data[1] / 1000,4)
            locx = round(data[2],4)
            locy = round(data[3],4)
        string = typ+'\t|'+poi+'\t\t|'+str(pv)+'\t\t\t|'+str(locx)+'\t\t\t\t|'+str(locy)
        obj.f.write('\n'+string)
    def filemode(obj,mode):
    #mode must be of form accepted by open() (ie. 'r', 'w', 'a', etc.)
        obj.f.close()
        obj.f.open(obj.name,mode)
    def close(obj):
    #Be sure to close the file object at the end
        obj.f.close()
