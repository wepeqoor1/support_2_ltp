def process_scratchcards(result: dict) -> dict:

    for item in result:
        item['status_change_date'] = (
            str(item['status_change_date']).replace('T', ' ').split('.')[0]
        )
        status_dict = {
            0: 'Выпущена',
            1: 'Продана, ждет активации',
            2: 'Активарована',
            3: 'Повреждена',
            4: 'Возврат',
            5: 'Выведена из оборота'
        }
        item['status'] = status_dict.get(item['status'])

        rnms_items = []
        if item['items'] is not None:
            for rnm in item['items']:
                rnms_items.append(rnm['rnm'])
        item['items'] = rnms_items

        if item['items'] == []:
            item['items'] = '-'

        for key, value in item.items():
            if item[key] is None:
                item[key] = '-'
    return result


def process_stat_fiscal_doc_sender_queue(result: list) -> list:

    for item in result:
        if item['kkts']:
            item['kkts'] = str(len(item['kkts']))
        elif not item['kkts']:
            item['kkts'] = '-'
        if item['period_stat_start']:
            item['period_stat_start'] = (
            str(item['period_stat_start']).replace('T', ' ').split('.')[0]
        )
        if item['period_stat_end']:
            item['period_stat_end'] = (
            str(item['period_stat_end']).replace('T', ' ').split('.')[0]
        )
        if item['time_request']:
            item['time_request'] = (
            str(item['time_request']).replace('T', ' ').split('.')[0]
        )
        if item['time_finish']:
            item['time_finish'] = (
            str(item['time_finish']).replace('T', ' ').split('.')[0]
        )
        for key, value in item.items():
            if item[key] is None:
                item[key] = '-'

    return result



def process_kkt(result: list) -> list:

    for item in result:
        item['activated'] = 'Касса активна' if item['activated'] else 'Касса не активна'
        item['locked_no_payment'] = 'Финансовая блокировка' if item['locked_no_payment'] else 'Фин.блок снят'
        item['start_date'] = change_date_to_human(item['start_date']) if item['start_date'] else '-'
        item['end_date'] = change_date_to_human(item['end_date']) if item['end_date'] else '-'

    return result


def process_super_user_login_password(result: list) -> list:
    for item in result:
        for key, value in item.items():
            if item[key] is None:
                item[key] = '-'

    return result


def change_date_to_human(date):
    return str(date).replace('T', ' ').split('.')[0]
