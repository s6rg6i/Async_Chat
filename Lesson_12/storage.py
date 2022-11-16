from pathlib import Path

import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import faker
from random import randint

DB_PROTOCOL = 'sqlite:///'
DB_PATH = DB_PROTOCOL + str(Path.cwd() / 'chat.db')

Base = declarative_base()


class Client(Base):
    __tablename__ = 'client'
    __tableargs__ = {'comment': 'Информация о клиенте'}
    id = sa.Column(sa.Integer, primary_key=True)
    login = sa.Column(sa.String)
    email = sa.Column(sa.String)

    def __repr__(self):
        return f'Client(id={self.id}, login={self.login}, email={self.email})'


class History(Base):
    __tablename__ = 'history'
    __tableargs__ = {'comment': 'История подключений клиенте'}

    id = sa.Column(sa.Integer, primary_key=True)
    time = sa.Column(sa.DateTime)
    ip = sa.Column(sa.String)
    client_id = sa.Column(sa.Integer, sa.ForeignKey('client.id'))

    def __repr__(self):
        return f'History(id={self.id}, time={self.time}, ip={self.ip},  client_id={self.client_id})'


class ContactsList(Base):
    __tablename__ = 'contact_list'
    __tableargs__ = {'comment': 'список_контактов'}
    owner_id = sa.Column(sa.Integer, sa.ForeignKey('client.id'), primary_key=True)
    member_id = sa.Column(sa.Integer, sa.ForeignKey('client.id'), primary_key=True)

    def __repr__(self):
        return f'ContactsList(owner_id={self.owner_id}, member_id={self.member_id})'


class MessagesList(Base):
    __tablename__ = 'messages_list'
    __tableargs__ = {'comment': 'запись чата'}
    id = sa.Column(sa.Integer, primary_key=True)
    msg = sa.Column(sa.String)

    def __repr__(self):
        return f'MessagesList(Msg={self.msg})'


class DbChat:
    def __init__(self, url=DB_PATH, echo=False):
        """Создаем подключение к БД"""
        engine = sa.create_engine(url=url, echo=echo)  # in-memory database, print log - false
        Base.metadata.create_all(engine)  # создаем таблицы в БД, определенные с помощью Base
        self.session: Session = sessionmaker(bind=engine)()  # Создаем объект сессии из фабрики

    def insert_message(self, msg: str):
        self.session.add(MessagesList(msg=msg))
        self.session.commit()

    def add_contact(self, login: str, email=''):
        self.session.add(Client(login=login, email=email))
        self.session.commit()

    def del_contact(self, login: str):
        self.session.query(Client).filter(Client.login == login).delete()
        self.session.commit()

    def last_entries(self):
        iter_ = self.session.query(MessagesList.msg).order_by(MessagesList.id.desc()).limit(10).all()[::-1]
        return [i[0] for i in iter_]

    def list_of_users(self):
        iter_ = self.session.query(Client.login).all()
        return [i[0] for i in iter_]

    def statistics_by_client(self, client_id: int):
        return self.session.query(History.id, History.time, History.ip).filter(History.client_id == client_id)

    def statistics_by_clients_all(self):
        dict_cl = {}
        for id_, login_ in [i for i in self.session.query(Client.id, Client.login)]:
            dict_cl.update({(id_, login_): [i for i in self.statistics_by_client(id_)]})
        return dict_cl


if __name__ == '__main__':
    def fill_test_data(session_: Session):
        f = faker.Faker()
        session_.add_all([Client(login=f.user_name(), email=f.ascii_email()) for _ in range(10)])
        session_.add_all([
            History(time=f.date_time_this_year(), ip=f.ipv4(), client_id=randint(1, 10))
            for _ in range(30)])
        session_.add_all([ContactsList(owner_id=3, member_id=i) for i in range(1, 7) if i != 3])
        session_.add_all([ContactsList(owner_id=1, member_id=i) for i in range(1, 10) if i != 1])
        # session.add_all([MessagesList(msg=f'Message {i:3}') for i in range(1, 50)])
        session_.commit()  # добавляем данные в таблицу


    def print_iter(iter_, info=''):
        print(f"\n        {info}:")
        [print(val) for val in iter_]


    # engine = sa.create_engine('sqlite:///:memory:', echo=False)  # in-memory database, print log - false
    # engine = sa.create_engine('sqlite:///chat.db', echo=False)  # in-memory database, print log - false
    # Base.metadata.create_all(engine)  # создаем таблицы в БД, определенные с помощью Base
    # session: Session = sessionmaker(bind=engine)()  # Создаем объект сессии из фабрики

    db_chat = DbChat()
    session = db_chat.session

    # fill_test_data(session)

    print_iter(session.query(Client), 'Client: Все записи')
    print_iter(session.query(History).order_by(History.time), 'History: Все записи')
    print_iter(session.query(ContactsList), 'ContactsList: Все записи')
    print_iter(session.query(MessagesList), 'MessagesList: Все записи')
    print('\nПоследние записи\n', db_chat.last_entries())
    print('\nСписок пользователей\n', db_chat.list_of_users())

    print_iter(session.query(Client).where(sa.or_(Client.id == 2, Client.id == 5)), 'where: client_id = 2 or 7')
    print_iter(session.query(History).filter(History.client_id == 7).order_by(History.time),
               'filter: подключения client_id = 7 с сортировкой по date')
    print_iter(session.query(History).order_by(History.time.desc()).limit(2),
               'Decs,limit: последние по времени 2 подключения')
    print('\n', '       Количество записей в History = ', session.query(History).count())
    print('\n', '       Владельцы и клиенты из ContactsList:')
    users = {k: val for k, val in session.query(Client.id, Client.login).all()}
    # db_chat.add_contact('caroline_watson')
    # db_chat.del_contact('caroline_watson')
    # print_iter(db_chat.statistics_by_client(1))
    # print(db_chat.statistics_by_clients_all())
    [print(users[i], users[j]) for i, j in session.query(ContactsList.owner_id, ContactsList.member_id).all()]
