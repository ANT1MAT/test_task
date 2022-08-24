from pymongo import MongoClient
import datetime
import random

client = MongoClient('mongo:27017')
db = client.database
collections_accrual = db.accrual
collections_payment = db.payment
result = db.result


# Функция создающая коллекция Долг и Платежи, данные полей date и month заполняются рандомно
def create_test_db():
    for i in range(5):
        day = random.randrange(1, 25)
        month = random.randrange(1, 12)
        year = random.randrange(2020, 2021)
        collections_accrual.insert_one({'id': i, 'date': datetime.date(year, month, day).isoformat(), 'month': month})
    for i in range(10):
        day = random.randrange(1, 25)
        month = random.randrange(1, 12)
        year = random.randrange(2020, 2021)
        collections_payment.insert_one({'id': i, 'date': datetime.date(year, month, day).isoformat(), 'month': month})


# Функция сопоставляющая имеющиеся долги и поступившие платежи, результатом является коллекция
# с полями id_acrrual - id долга, id_payment - id платежа
def calculated_accrual_payment():
    result_list = []
    unused_payments = []
    payments = list(db.payment.aggregate([{'$sort': {'date': 1}}]))
    accruals = list(db.accrual.aggregate([{'$sort': {'date': 1}}]))
    # С начала проверяются все платежи, которые могут закрыть долг в своём месяце
    for pay in payments:
        current_accruals = list(filter(lambda x: x['month'] == pay['month'], accruals))
        print(current_accruals)
        if len(current_accruals) != 0:
            for c_accrual in current_accruals:
                # Проверяется условие, что полученные элементы по полю month имеют один год с проверяемым платежом
                # и были созданы до появления платежа
                if (datetime.date.fromisoformat(c_accrual['date']).year == datetime.date.fromisoformat(pay['date']).year)\
                        and c_accrual['date'] <= pay['date']:
                    result_list.append({'id_accrual': c_accrual['id'], 'id_payments': pay['id']})
                    accruals.remove(c_accrual)
                    payments.remove(pay)
                    break
    # Если платеж не смог погасить ни один долг в своем месяце, ищется самый старый долг,
    # который он может погасить
    for pay in payments:
        for last_accrual in accruals:
            if last_accrual['date'] < pay['date']:
                result_list.append({'id_accrual': last_accrual['id'], 'id_payments': pay['id']})
                accruals.remove(last_accrual)
                break
            else:
                result_list.append({'id_accrual': None, 'id_payments': pay['id']})
                unused_payments.append(pay['id'])
                break
    print(unused_payments)
    return db.result.insert_many(result_list)

if __name__ == '__main__':
    create_test_db()
    calculated_accrual_payment()





