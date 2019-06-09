from .search_module import _define_real_type
ADD_STR = ['0', '1', '1', '0', '1', '0', '0', '1', '0', '0', '0', '0', '0', '0', '0', '1', '0', '0', '0',
           '0', '0', '0', '0', '0', '1', '0', '0', '0', '0', '0']

def _evaluate_announcement_form(form):
    form_data = dict()

    def get(attr_name, form_attr_name):
        try:
            form_data[attr_name] = int(form[form_attr_name])
        except:
            form_data[attr_name] = 0
    get('goal', 'goal')
    get('term', 'term')
    get('type', 'type')
    get('floor', 'floor')
    get('rooms', 'rooms_number')
    get('space', 'living_space')
    get('repair', 'repair_rate')
    form_data['furniture'] = list(map(int, form.getlist('extra_options')))
    save = form_data['furniture'].copy()
    if 0 in save:
        form_data['furniture'] = True
    else:
        form_data['furniture'] = False
    if 1 in save:
        form_data['garage'] = True
    else:
        form_data['garage'] = False
    get('beds', 'beds_number')
    get('district', 'district')
    get('metro', 'minutes_to_metro')
    get('price', 'price')
    form_data['metro_id'] = form['station'].split(':')[0][7:]
    form_data['metro_name'] = form['station'].split(':')[1]
    form_data['comment'] = form['apartment_description']
    form_data['street_type'] = form.get('street_type')
    form_data['street'] = form['address1']
    form_data['home_number'] = form['address2']
    form_data['type'] = _define_real_type(form_data['goal'], form_data['term'], form_data['type'])
    return form_data


def form_announcement_str(options):
    result = ADD_STR.copy()
    if options['goal'] == 0:
        result[0], result[1] = '1', '0'
    if options['term'] == 1:
        result[2], result[3] = '0', '1'
    if options['type'] == 5 or options['type'] == 6:
        result[4], result[5], result[6] = '0', '0', '1'
    elif options['type'] == 4:
        result[4], result[5], result[6] = '0', '1', '0'
    result[7] = '0'
    result[7 + options['repair']] = '1'
    result[13] = str(int(options['furniture']))
    result[14] = str(int(options['garage']))
    result[15] = '0'
    result[15 + options['district']] = '1'
    result[24] = '0'
    d = {1: 0, 3: 1, 5: 2, 10: 3, 20: 4, 30: 5}
    result[24 + d[options['metro']]] = '1'
    result += options['metro_id']
    return result


def announcement_form(form):
    options = _evaluate_announcement_form(form)
    return options, form_announcement_str(options)

