from sqlalchemy import (
    ARRAY,
    BigInteger,
    Boolean,
    Column,
    DateTime,
    Integer,
    String,
    text,
    DATETIME,
    Index,
    Text,
    TIMESTAMP,
    ForeignKey
)
from sqlalchemy.orm import relationship
relationship
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.sqltypes import SMALLINT
from sqlalchemy_serializer import SerializerMixin

Base = declarative_base()
metadata = Base.metadata


class Personal(Base, SerializerMixin):
    __tablename__ = "personal"

    email = Column(String(255))
    id = Column(BigInteger)
    isactive = Column(Integer)
    login = Column(String(255), primary_key=True, nullable=False)
    name = Column(String(255))
    password = Column(String(255), primary_key=True, nullable=False)
    position = Column(String(255))
    registr_fns = Column(Boolean, nullable=False, server_default=text("false"))


class Request(Base, SerializerMixin):
    __tablename__ = "request"

    a_id = Column(Integer)
    affected_request_list = Column(ARRAY(Integer()))
    agent_company_id = Column(Integer)
    bill_id = Column(String(255), unique=True)
    bill_sum = Column(BigInteger)
    bill_sum_with_discount = Column(BigInteger)
    codename = Column(String(255))
    company_id = Column(Integer, nullable=False)
    id = Column(Integer, primary_key=True)
    is_ofd = Column(Boolean)
    kkt_list = Column(ARRAY(String(length=255)))
    kkt_list_actual = Column(ARRAY(String(length=255)))
    kkt_objects = Column(JSONB)
    kkt_objects_actual = Column(JSONB)
    number_account = Column(String(255))
    ofd_create = Column(Boolean)
    opt_discount = Column(Integer)
    pdf = Column(String(255))
    promo_discount = Column(Integer)
    sign = Column(String(255))
    status = Column(Integer)
    trade_point = Column(ARRAY(BigInteger()))
    type = Column(String(255))
    type_payment = Column(ARRAY(Integer()))
    u_id = Column(Integer)
    with_nds = Column(Boolean)
    kkt_list_replace = Column(ARRAY(JSONB))
    status_change_date = Column(DateTime)
    date = Column(DateTime)
    signdate = Column(DateTime)
    edit_block = Column(Boolean)
    end_date = Column(DateTime)
    after_payment = Column(Boolean, server_default=text("false"))
    uuid = Column(String(255), server_default=text("uuid_generate_v1()"))
    state_checkbox = Column(Integer, server_default=text("0"))
    count_kkt = Column(Integer)
    items = Column(JSONB)
    deleted = Column(Boolean, server_default=text("false"))
    date_created = Column(DateTime, server_default=text("now()"))


class Scratchcard(Base, SerializerMixin):
    __tablename__ = "scratchcards"

    agent_company_id = Column(Integer)
    change_agent = Column(String(255))
    change_agent_id = Column(Integer)
    client_inn = Column(String(255))
    client_sname = Column(String(255))
    company_id = Column(Integer, nullable=False)
    contragent_inn = Column(String(255))
    contragent_sname = Column(String(255))
    hash = Column(String(255))
    nominal_id = Column(Integer)
    nominalvalue = Column(String(255))
    number = Column(String(255), primary_key=True)
    status = Column(Integer)
    status_change_date = Column(DATETIME)
    request_id = Column(BigInteger)


class StatFiscalDocSenderQueue(Base):
    __tablename__ = "stat_fiscal_doc_sender_queue"

    id = Column(
        BigInteger,
        primary_key=True,
        server_default=text(
            "nextval('stat_fiscal_doc_sender_queue_id_seq'::regclass)"
        ),
    )
    company_caption = Column(String(1024), nullable=False)
    company_id = Column(Integer, nullable=False)
    company_inn = Column(String(255), nullable=False)
    service_name = Column(String(100), nullable=False)
    user_mail = Column(String(255), nullable=False)
    kkts = Column(ARRAY(String(length=30)))
    period_stat_start = Column(DateTime, nullable=False)
    period_stat_end = Column(DateTime)
    time_request = Column(DateTime, nullable=False)
    time_finish = Column(DateTime)
    error_count = Column(SMALLINT)
    report_selected = Column(Integer)
    file_path = Column(String(255))
    filter_map = Column(JSONB)
    unit_id = Column(Integer)


class Kkt(Base):
    __tablename__ = 'kkt'
    __table_args__ = (
        Index('idx_kkt_reg_data', 'factory_number_fn', 'register_number_kkt', 'activated', 'company_id'),
    )

    activated = Column(Boolean, server_default=text("false"))
    company_id = Column(Integer, nullable=False)
    diaglastreq = Column(String(255))
    diagstatus = Column(String(255))
    factory_number_fn = Column(String(255))
    factory_number_kkt = Column(String(255))
    human_name = Column(String(1024))
    is_signed = Column(Boolean)
    register_number_kkt = Column(String(255), nullable=False, unique=True)
    request_id = Column(BigInteger)
    trade_point = Column(Integer, index=True)
    last_fd_datetime = Column(BigInteger)
    valid_status = Column(Integer)
    edit_log = Column(ARRAY(JSONB(astext_type=Text())))
    end_date = Column(DateTime)
    status_fns = Column(BigInteger)
    signed = Column(Boolean)
    locked_no_payment = Column(Boolean, server_default=text("false"))
    start_date = Column(DateTime)
    agent_company_id = Column(Integer, server_default=text("'-1'::integer"))
    id = Column(Integer, primary_key=True, server_default=text("nextval('kkt_id_seq'::regclass)"))
    replaced = Column(Boolean, server_default=text("false"))
    deactivation_date = Column(DateTime)
    fns_status_reg = Column(Integer, server_default=text("0"))
    fns_status_reg_check_counter = Column(Integer, server_default=text("0"))
    crpt = Column(Boolean, server_default=text("false"))
    send_fd = Column(Boolean, nullable=False, server_default=text("true"))
    kpp = Column(String(255))
    kkt_model = Column(String(100))
    create_date = Column(DateTime(True), index=True, server_default=text("CURRENT_TIMESTAMP"))
    change_date = Column(DateTime(True), index=True, server_default=text("CURRENT_TIMESTAMP"))
    tag_1050 = Column(Boolean, server_default=text("false"))
    tag_1051 = Column(Boolean, server_default=text("false"))
    tag_1052 = Column(Boolean, server_default=text("false"))
    registration_date = Column(DateTime(True))





class Company(Base):
    __tablename__ = 'company'

    caption = Column(String(1024))
    caption_short = Column(String(256))
    company_email = Column(String(1024))
    company_inn = Column(String(1024), nullable=False)
    company_kpp = Column(String(1024))
    company_ogrn = Column(String(1024))
    company_okpo = Column(String(1024))
    company_telephone = Column(String(1024))
    contract_id = Column(String(1024), nullable=False)
    id = Column(Integer, primary_key=True)
    kkt_list = Column(ARRAY(String(length=255)))
    shop_list = Column(ARRAY(String(length=255)))
    agent_id = Column(BigInteger)
    inn = Column(String(1024))
    api_client_key = Column(String(255))
    kladr_id = Column(String(255))
    kladr_id_fact = Column(String(255))
    abonentid = Column(String(255))
    x5 = Column(Boolean, server_default=text("false"))
    api_client_key_time = Column(TIMESTAMP)
    b_auto_confirm = Column(Boolean, server_default=text("false"))
    okved = Column(String(8))
    okved_type = Column(Integer)
    create_date = Column(DateTime(True), index=True, server_default=text("CURRENT_TIMESTAMP"))
    change_date = Column(DateTime(True), index=True, server_default=text("CURRENT_TIMESTAMP"))


class User(Base):
    __tablename__ = 'users'

    a_id = Column(Integer)
    bloced = Column(Boolean)
    blocked = Column(Boolean)
    company_id = Column(Integer, nullable=False)
    company_telephone = Column(String(1024))
    deleted = Column(Boolean)
    diagnost = Column(Boolean)
    duty = Column(String(1024))
    email = Column(String(1024))
    id = Column(Integer, primary_key=True)
    made_id = Column(Integer)
    mobil_telephone = Column(String(1024))
    timezone = Column(String(1024))
    unit_id = Column(Integer)
    user_firstname = Column(String(1024))
    user_lastname = Column(String(1024))
    user_login = Column(String(1024))
    user_middlename = Column(String(1024))
    user_password = Column(String(1024))
    register_date = Column(DateTime)
    block_count = Column(Integer)
    block_date = Column(DateTime)
    blocked_by = Column(Integer)
    is_send_email = Column(Boolean, nullable=False, server_default=text("false"))
    is_send_sms = Column(Boolean, nullable=False, server_default=text("false"))
    date_send_bill = Column(DateTime(True))
    create_date = Column(DateTime(True), index=True, server_default=text("CURRENT_TIMESTAMP"))
    change_date = Column(DateTime(True), index=True, server_default=text("CURRENT_TIMESTAMP"))
    granter_id = Column(Integer)
    email_notification = Column(String(255))


class Contract(Base):
    __tablename__ = 'contracts'
    __table_args__ = {'schema': 'public'}

    agent_company_id = Column(Integer)
    contract = Column(JSONB(astext_type=Text()))
    contract_pack_info = Column(JSONB(astext_type=Text()))
    contract_status = Column(Integer)
    id = Column(String(255), primary_key=True)
    onpaper = Column(Boolean)
    pdf = Column(String(255))
    sended = Column(BigInteger)
    sign = Column(String(255))
    tmp_agent_company_id = Column(Integer)
    tmp_agent_id = Column(Integer)
    signdate = Column(TIMESTAMP)
    edit_block = Column(Boolean)
    end_date = Column(TIMESTAMP)
    status_fns = Column(BigInteger)
    tarif_id = Column(ForeignKey('public.company_tarifs.id'), server_default=text("1"))
    kkt_tarif_id = Column(ForeignKey('public.kkt_tarifs.id'), server_default=text("1"))
    fns_response = Column(String(255), server_default=text("NULL::character varying"))
    create_date = Column(DateTime(True), index=True, server_default=text("CURRENT_TIMESTAMP"))
    change_date = Column(DateTime(True), index=True, server_default=text("CURRENT_TIMESTAMP"))

    kkt_tarif = relationship('KktTarif')
    tarif = relationship('CompanyTarif')

    
