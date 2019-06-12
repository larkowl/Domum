import pickle


def _predict(type, rooms, data):
    file_names = ['apartment_sale', 'apartment_rent_long', 'apartment_rent_short', 'home', 'office']
    results = []
    for i in range(len(rooms)):
        if rooms[i] == 1:
            regressor = read(file_names[type] + '_' + str(i + 1))
            results.append(regressor.predict(data))
    return results


def read(filename):
    return pickle.load(open(filename, 'rb'))

def form_data(options):
    space = options[16:22]
    repairs = options[22:27]
    furniture = options[27]
    districts = options

def type_def(options):
    type = 1
    if options[0] == 1:
        type = 5
        if options[3] == 1:
            type = 3
        elif options[4] == 1:
            type = 2
    elif options[5] == 1:
        type = 4
    return type

def def_rooms(options):
    rooms = options[12:16]
    if sum(rooms) == 0:
        return [1, 1, 1, 1]
    else:
        return rooms

def predict(options):
    type = type_def(options)
    data = form_data(options)
    rooms_number = def_rooms(options)
    results = _predict(type, rooms_number , data)
    print(results)

