import hashlib
from typing import Dict, Any, Optional

from app.db import session
from app.models import Personal, Scratchcard, Request, StatFiscalDocSenderQueue, Kkt, User, Company
from app.word_processing import process_scratchcards, process_stat_fiscal_doc_sender_queue, process_kkt, process_super_user_login_password


def get_scratchcards(scratchcard_code: str):
    """Получаем данные по коду скрейтчкарты"""
    hash_object = hashlib.sha1(bytes(scratchcard_code, encoding="utf-8"))
    hex_dig = hash_object.hexdigest().upper()
    result = (
        (
            session.query(
                Scratchcard.status_change_date,
                Scratchcard.status,
                Scratchcard.number,
                Scratchcard.nominalvalue,
                Scratchcard.contragent_sname,
                Scratchcard.contragent_inn,
                Scratchcard.client_sname,
                Scratchcard.client_inn,
                Scratchcard.request_id,
                Request.items,
            ).filter(Scratchcard.hash == hex_dig)
        )
        .outerjoin(Request, Scratchcard.request_id == Request.id)
        .all()
    )
    result = process_scratchcards(result)
    session.rollback()
    return result


def get_scratchcards_number(number_code: str):
    """Получаем данные по номеру скрейтчкарты"""
    result = (
        (
            session.query(
                Scratchcard.status_change_date,
                Scratchcard.status,
                Scratchcard.number,
                Scratchcard.nominalvalue,
                Scratchcard.contragent_sname,
                Scratchcard.contragent_inn,
                Scratchcard.client_sname,
                Scratchcard.client_inn,
                Scratchcard.request_id,
                Request.items,
            ).filter(Scratchcard.number == number_code)
        )
        .outerjoin(Request, Scratchcard.request_id == Request.id)
        .all()
    )
    result = process_scratchcards(result)
    session.rollback()
    return result


def user_login(username, password) -> Optional[Dict[str, Any]]:
    """Получаем статус пользователя (заблокирован/не заблокирован)"""
    logo_pass = {"login": username, "password": password}
    result = (
        session.query(Personal.password, Personal.login.label("username"))
        .filter(
            Personal.password == logo_pass["password"],
            Personal.login == logo_pass["login"],
            Personal.isactive == 1,
        )
        .all()
    )
    if not result:
        return None
    result = [row._asdict() for row in result][0]
    session.rollback()

    return result


def get_user_in_db(login):
    """Проверяем пользователя в базе"""
    logo_pass = {"login": login}
    result = (
        session.query(Personal.login.label("username"))
        .filter(
            Personal.login == logo_pass["login"],
        )
        .all()
    )
    result = [row._asdict() for row in result][0]
    session.rollback()

    return result


def get_stat_fiscal_doc_sender_queue_unloading_checks() -> dict:
    """Получаем незавершенные выгрузки"""
    result = (
        session.query(
            StatFiscalDocSenderQueue.company_caption,
            StatFiscalDocSenderQueue.company_inn,
            StatFiscalDocSenderQueue.user_mail,
            StatFiscalDocSenderQueue.kkts,
            StatFiscalDocSenderQueue.period_stat_start,
            StatFiscalDocSenderQueue.period_stat_end,
            StatFiscalDocSenderQueue.time_request,
            StatFiscalDocSenderQueue.time_finish,
        )
        .filter(
            StatFiscalDocSenderQueue.error_count < 3,
            StatFiscalDocSenderQueue.time_finish == None,
        )
        .order_by(StatFiscalDocSenderQueue.id.desc())
        .limit(200)
    ).all()
    session.rollback()
    result = [row._asdict() for row in result]

    result = process_stat_fiscal_doc_sender_queue(result)
    return result


def get_stat_fiscal_doc_sender_queue_user_email(user_mail: str) -> dict:
    """Получаем выгрузки по почете пользователя"""
    result = (
        session.query(
            StatFiscalDocSenderQueue.company_caption,
            StatFiscalDocSenderQueue.company_inn,
            StatFiscalDocSenderQueue.user_mail,
            StatFiscalDocSenderQueue.kkts,
            StatFiscalDocSenderQueue.period_stat_start,
            StatFiscalDocSenderQueue.period_stat_end,
            StatFiscalDocSenderQueue.time_request,
            StatFiscalDocSenderQueue.time_finish,
        )
        .filter(
            StatFiscalDocSenderQueue.user_mail == user_mail,
            StatFiscalDocSenderQueue.error_count < 3,
        )
        .order_by(StatFiscalDocSenderQueue.id.desc())
        .limit(50)
    ).all()
    session.rollback()
    result = [row._asdict() for row in result]

    result = process_stat_fiscal_doc_sender_queue(result)
    return result


def get_stat_fiscal_doc_sender_queue_user_inn(user_inn: str) -> dict:
    """Получаем выгрузки пользователя по ИНН"""
    result = (
        session.query(
            StatFiscalDocSenderQueue.company_caption,
            StatFiscalDocSenderQueue.company_inn,
            StatFiscalDocSenderQueue.user_mail,
            StatFiscalDocSenderQueue.kkts,
            StatFiscalDocSenderQueue.period_stat_start,
            StatFiscalDocSenderQueue.period_stat_end,
            StatFiscalDocSenderQueue.time_request,
            StatFiscalDocSenderQueue.time_finish,
        )
        .filter(
            StatFiscalDocSenderQueue.company_inn == user_inn,
            StatFiscalDocSenderQueue.error_count < 3,
        )
        .order_by(StatFiscalDocSenderQueue.id.desc())
        .limit(50)
    ).all()
    session.rollback()
    result = [row._asdict() for row in result]
    result = process_stat_fiscal_doc_sender_queue(result)

    return result


def get_kkt_for_rnm(rnm: str) -> dict:
    """Получаем данные кассы из РНМ"""
    result = (
        session.query(
            Kkt.register_number_kkt,
            Kkt.factory_number_kkt,
            Kkt.factory_number_fn,
            Kkt.activated,
            Kkt.locked_no_payment,
            Kkt.start_date,
            Kkt.end_date,
        )
        .filter(Kkt.register_number_kkt == rnm)
        .order_by(Kkt.id.desc())
    ).all()
    session.rollback()
    result = [row._asdict() for row in result]
    result = process_kkt(result)

    return result


def get_kkt_for_fn(fn: str) -> dict:
    """Получаем данные кассы из ФН"""
    result = (
        session.query(
            Kkt.register_number_kkt,
            Kkt.factory_number_kkt,
            Kkt.factory_number_fn,
            Kkt.activated,
            Kkt.locked_no_payment,
            Kkt.start_date,
            Kkt.end_date,
        )
        .filter(Kkt.factory_number_fn == fn)
        .order_by(Kkt.id.desc())
    ).all()
    session.rollback()
    result = [row._asdict() for row in result]
    result = process_kkt(result)

    return result


def get_kkt_for_zn(zn: str) -> dict:
    """Получаем данные кассы из ЗН"""
    result = (
        session.query(
            Kkt.register_number_kkt,
            Kkt.factory_number_kkt,
            Kkt.factory_number_fn,
            Kkt.activated,
            Kkt.locked_no_payment,
            Kkt.start_date,
            Kkt.end_date,
        )
        .filter(Kkt.factory_number_kkt == zn)
        .order_by(Kkt.id.desc())
    ).all()
    session.rollback()
    result = [row._asdict() for row in result]
    result = process_kkt(result)

    return result


def get_super_user_login_password(user_inn: str) -> dict:
    """Получаем логин и пароль супераользователя"""
    result = (
        (
            session.query(
                Company.contract_id,
                User.user_password,
                User.user_login,
            ).filter(Company.company_inn == user_inn)
        )
        .outerjoin(Company, Company.id == User.company_id)
        .order_by(User.id)
        .limit(1)
        .all()
    )

    session.rollback()
    result = [row._asdict() for row in result]
    result = process_super_user_login_password(result)

    return result
