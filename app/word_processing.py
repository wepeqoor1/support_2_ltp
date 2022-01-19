def process_scratchcards(result: dict) -> dict:

    for item in result:
        item["status_change_date"] = (
            str(item["status_change_date"]).replace("T", " ").split(".")[0]
        )
        status_dict = {
            0: 'Выпущена',
            1: 'Продана, ждет активации',
            2: 'Активарована',
            3: 'Повреждена',
            4: 'Возврат',
            5: 'Выведена из оборота'
        }
        item["status"] = status_dict.get(item["status"])

        rnms_items = []
        if item["items"] is not None:
            for rnm in item["items"]:
                rnms_items.append(rnm["rnm"])
        item["items"] = rnms_items

        if item["items"] == []:
            item["items"] = "-"

        for key, value in item.items():
            if item[key] is None:
                item[key] = "-"
    return result


def process_stat_fiscal_doc_sender_queue(result: list) -> dict:

    for item in result:
        if item["kkts"]:
            item["kkts"] = str(len(item["kkts"]))
        elif item["kkts"] == []:
            item["kkts"] = "-"
        if item["period_stat_start"]:
            item["period_stat_start"] = (
            str(item["period_stat_start"]).replace("T", " ").split(".")[0]
        )
        if item["period_stat_end"]:
            item["period_stat_end"] = (
            str(item["period_stat_end"]).replace("T", " ").split(".")[0]
        )
        if item["time_request"]:
            item["time_request"] = (
            str(item["time_request"]).replace("T", " ").split(".")[0]
        )
        if item["time_finish"]:
            item["time_finish"] = (
            str(item["time_finish"]).replace("T", " ").split(".")[0]
        )
        for key, value in item.items():
            if item[key] is None:
                item[key] = "-"

    return result



def process_kkt(result: list) -> dict:

    for item in result:
        if item["activated"] == True:
            item["activated"] = "Касса активна"
        else:
            item["activated"] = "Касса не активна"
        if item["locked_no_payment"] == True:
            item["locked_no_payment"] = "Финансовая блокировка"
        else:
            item["locked_no_payment"] = "Фин.блок снят"
        if item["start_date"]:
            item["start_date"] = (
            str(item["start_date"]).replace("T", " ").split(".")[0]
        )
        if item["end_date"]:
            item["end_date"] = (
            str(item["end_date"]).replace("T", " ").split(".")[0]
        )
        for key, value in item.items():
            if item[key] is None:
                item[key] = "-"

    return result



def process_super_user_login_password(result: list) -> list:
# [{'contract_id': '001562186253', 'user_password': 'hCl4REOkj', 'user_login': None}]
    for item in result:
        for key, value in item.items():
            if item[key] is None:
                item[key] = "-"

    return result