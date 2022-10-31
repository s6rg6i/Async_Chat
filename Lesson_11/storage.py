import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import faker
from random import randint

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


def fill_test_data(session_: Session):
    f = faker.Faker()
    session_.add_all([
        Client(login=f.user_name(), email=f.ascii_email()) for _ in range(10)])
    session_.add_all([
        History(time=f.date_time_this_year(), ip=f.ipv4(), client_id=randint(1, 10))
        for _ in range(30)])
    session_.add_all([
        ContactsList(owner_id=3, member_id=i) for i in range(1, 7) if i != 3])
    session_.add_all([
        ContactsList(owner_id=1, member_id=i) for i in range(1, 10) if i != 1])
    session_.commit()  # добавляем данные в таблицу


def print_iter(iter_, info=''):
    print(f"\n        {info}:")
    [print(val) for val in iter_]


if __name__ == '__main__':
    engine = sa.create_engine('sqlite:///:memory:', echo=False)  # in-memory database, print log - false
    Base.metadata.create_all(engine)  # создаем таблицы в БД, определенные с помощью Base
    session: Session = sessionmaker(bind=engine)()  # Создаем объект сессии из фабрики sessionmaker
    fill_test_data(session)

    print_iter(session.query(Client), 'Client: Все записи')
    print_iter(session.query(History).order_by(History.time), 'History: Все записи')
    print_iter(session.query(ContactsList), 'ContactsList: Все записи')

    print_iter(session.query(Client).where(sa.or_(Client.id == 2, Client.id == 5)), 'where: client_id = 2 or 7')
    print_iter(session.query(History).filter(History.client_id == 7).order_by(History.time),
               'filter: подключения client_id = 7 с сортировкой по date')
    print_iter(session.query(History).order_by(History.time.desc()).limit(2),
               'Decs,limit: последние по времени 2 подключения')
    print('\n', '       Количество записей в History = ', session.query(History).count())
    print('\n', '       Владельцы и клиенты из ContactsList:')
    users = {k: val for k, val in session.query(Client.id, Client.login).all()}
    [print(users[i], users[j]) for i, j in session.query(ContactsList.owner_id, ContactsList.member_id).all()]
