from .models import Announcement
from copy import deepcopy
from django.db.models import Q

STANDART_STR = ['0', '1', '1', '0', '1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0',
                '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0',
                '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0']


def _define_real_type(a, b, c):
    if a == 0:
        if b == 0:
            if c == 0:
                return 2
            else:
                return 6
        else:
            if c == 0:
                return 3
            else:
                return 5
    else:
        if c == 0:
            return 1
        else:
            return 4


def _search_form(form):
    form_data = dict()
    form_data['goal'] = int(form['goal'])
    try:
        form_data['term'] = int(form['term'])
    except:
        form_data['term'] = 0
    form_data['type'] = int(form['type'])
    form_data['floor'] = list(map(int, form.getlist('floor')))
    if len(form_data['floor']) == 0:
        form_data['floor'] = [1, 2, 3, 4, 5]
    form_data['rooms'] = list(map(int, form.getlist('rooms_number')))
    if len(form_data['rooms']) == 0:
        form_data['rooms'] = [1, 2, 3, 4, 5, 6]
    form_data['space'] = list(map(int, form.getlist('living_space')))
    if len(form_data['space']) == 0:
        form_data['space'] = [0, 1, 2, 3, 4, 5]
    form_data['repair'] = list(map(int, form.getlist('repair_rate')))
    if len(form_data['repair']) == 0:
        form_data['repair'] = [0, 1, 2, 3, 4, 5]
    form_data['furniture'] = list(map(int, form.getlist('extra_options')))
    save = deepcopy(form_data['furniture'])
    if 0 in save:
        form_data['furniture'] = True
    else:
        form_data['furniture'] = False
    if 1 in save:
        form_data['garage'] = True
    else:
        form_data['garage'] = False
    form_data['beds'] = list(map(int, form.getlist('beds_number')))
    if len(form_data['beds']) == 0:
        form_data['beds'] = [1, 2, 3, 4, 5, 6]
    form_data['district'] = list(map(int, form.getlist('district')))
    if len(form_data['district']) == 0:
        form_data['district'] = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    form_data['metro'] = list(map(int, form.getlist('minutes_to_metro')))
    if len(form_data['metro']) == 0:
        form_data['metro'] = [1, 3, 5, 10, 20, 30]
    form_data['metro_ids'] = [i.split(':')[0] for i in form.getlist('station')]
    form_data['metro_names'] = [i.split(':')[1] for i in form.getlist('station')]
    form_data['type'] = _define_real_type(form_data['goal'], form_data['term'], form_data['type'])
    return form_data


def form_str(options):
    result = STANDART_STR.copy()

    def fill(par, lim, start):
        if len(options[par]) != lim:
            for i in options[par]:
                result[start + i] = '1'

    if options['goal'] == 0:
        result[0], result[1] = '1', '0'
    if options['term'] == 1:
        result[2], result[3] = '0', '1'
    if options['type'] == 5 or options['type'] == 6:
        result[4], result[5], result[6] = '0', '0', '1'
    elif options['type'] == 4:
        result[4], result[5], result[6] = '0', '1', '0'
    fill('floor', 5, 6)
    fill('rooms', 6, 11)
    fill('space', 6, 18)
    fill('repair', 6, 24)
    if options['furniture']:
        result[30] = '1'
    if options['garage']:
        result[31] = '1'
    fill('beds', 6, 31)
    fill('district', 9, 38)
    if len(options['metro']) != 6:
        d = {1: 0, 3: 1, 5: 2, 10: 3, 20: 4, 30: 5}
        for i in options['metro']:
            result[47 + d[i]] = '1'
    result += options['metro_ids']
    return result


def search(form):
    options = _search_form(form)
    qs = Announcement.objects.filter(real_type=options['type'])

    if len(options['metro_names']) != 0:
        query = Q(station__name=options['metro_names'][0])
        for i in range(1, len(options['metro_names'])):
            query.add(Q(station__name=options['metro_names'][i]), Q.OR)
        qs = qs.filter(query)
    query = Q(floor=options['floor'][0])
    for i in range(1, len(options['floor'])):
        query.add(Q(floor=options['floor'][i]), Q.OR)
    if 5 in options['floor']:
        query.add(Q(floor__gte=5), Q.OR)
    qs = qs.filter(query)

    query = Q(distance_to_metro=options['metro'][0])
    for i in range(1, len(options['metro'])):
        query.add(Q(distance_to_metro=options['metro'][i]), Q.OR)
    qs = qs.filter(query)

    query = Q(district=options['district'][0])
    for i in range(1, len(options['district'])):
        query.add(Q(district=options['district'][i]), Q.OR)
    qs = qs.filter(query)

    query = (Q(area__gte=options['space'][0] * 20) & Q(area__lte=options['space'][0] * 20 + 20))
    for i in range(1, len(options['space'])):
        query.add((Q(area__gte=options['space'][i] * 20) & Q(area__lte=options['space'][i] * 20 + 20)), Q.OR)
    if 5 in options['space']:
        query.add(Q(area__gte=100), Q.OR)
    qs = qs.filter(query)

    query = Q(rooms_number=options['rooms'][0])
    for i in range(1, len(options['rooms'])):
        query.add(Q(rooms_number=options['rooms'][i]), Q.OR)
    if 6 in options['rooms']:
        query.add(Q(rooms_number__gte=6), Q.OR)
    qs = qs.filter(query)

    query = Q(repairs=options['repair'][0])
    for i in range(1, len(options['repair'])):
        query.add(Q(repairs=options['repair'][i]), Q.OR)
    qs = qs.filter(query)

    if options['furniture']:
        qs = qs.filter(furniture=options['furniture'])

    if options['type'] == 4 and options['garage']:
        qs = qs.filter(garage=options['garage'])
    elif options['type'] in [2, 3]:
        query = Q(beds=options['beds'][0])
        for i in range(1, len(options['beds'])):
            query.add(Q(beds=options['beds'][i]), Q.OR)
        if 6 in options['beds']:
            query.add(Q(beds__gte=6), Q.OR)
        qs = qs.filter(query)
    return qs, form_str(options)

