def process_scratchcards(result: dict) -> dict:

    for item in result:
        item['status_change_date'] = (
            str(item['status_change_date']).replace('T', ' ').split('.')[0]
        )
        scratchcard_status = {
            0: 'Выпущена',
            1: 'Продана, ждет активации',
            2: 'Активарована',
            3: 'Повреждена',
            4: 'Возврат',
            5: 'Выведена из оборота'
        }
        item['status'] = scratchcard_status.get(item['status'])

        rnms_items = []
        if item['items'] is not None:
            for rnm in item['items']:
                rnms_items.append(rnm['rnm'])
        item['items'] = rnms_items

        if not item['items']:
            item['items'] = '-'

        for key, value in item.items():
            if item[key] is None:
                item[key] = '-'

    return result


def process_stat_fiscal_doc_sender_queue(result: list) -> list:

    for item in result:
        item['kkts'] = str(len(item['kkts'])) if item['kkts'] else '-'
        item['period_stat_start'] = date_to_human(item['period_stat_start']) if item['period_stat_start'] else '-'
        item['period_stat_end'] = date_to_human(item['period_stat_end']) if item['period_stat_end'] else '-'
        item['time_request'] = date_to_human(item['time_request']) if item['time_request'] else '-'
        item['time_finish'] = date_to_human(item['time_finish']) if item['time_finish'] else '-'

        for key, value in item.items():
            if item[key] is None:
                item[key] = '-'

    return result


def process_kkt(result: list) -> list:

    for item in result:
        item['activated'] = 'Касса активна' if item['activated'] else 'Касса не активна'
        item['locked_no_payment'] = 'Финансовая блокировка' if item['locked_no_payment'] else 'Фин.блок снят'
        item['start_date'] = date_to_human(item['start_date']) if item['start_date'] else '-'
        item['end_date'] = date_to_human(item['end_date']) if item['end_date'] else '-'

    return result


def process_super_user_login_password(result: list) -> list:

    for item in result:
        for key, value in item.items():
            if item[key] is None:
                item[key] = '-'

    return result


def date_to_human(date):
    return str(date).replace('T', ' ').split('.')[0]



