from web3 import Web3
from web3.middleware import geth_poa_middleware
from contract import abi,contract_address 

w3= Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)
contract = w3.eth.contract(address=contract_address, abi=abi)




def create_estate(account_user):
    try:
        size = int(input("Введите площадь недвижимости: "))
        photo = input("Введите ссылку на фото недвижимости: ")
        rooms = int(input("Введите количество комнат: "))
        esType = input("Введите тип недвижимости (House, Flat, Loft): ")

        # Преобразование типа недвижимости в числовое значение
        if esType == "House":
            esType = 0
        elif esType == "Flat":
            esType = 1
        elif esType == "Loft":
            esType = 2
        else:
            raise ValueError("Неверный тип недвижимости")

        estate = contract.functions.createEstate(size, photo, rooms, esType).transact({
            "from": account_user
        })
        print("Недвижимость успешно создана")
    except Exception as e:
            print(e)
            return None
#-------------------------
def get_estate(account_user):
    try:
        estate = contract.functions.getEstates().call({
            "from": account_user
        })
        print(estate) #не рабочее говно ошибка в utils.py 482 строка
    except Exception as e:
            print(e)
            return None
#----------------------------------------------
def create_ad(account_user):
    try:
        estate_id = int(input("Введите ID недвижимости: "))
        price = int(input("Введите цену недвижимости: "))
        estate = contract.functions.createAd(estate_id, price).transact({
            "from": account_user
        })
        print("Объявление успешно создано")
    except Exception as e:
            print(e)
            return None
#------
def update_estate_status(account_user):
    try:
        estate_id = int(input("Введите ID недвижимости: "))
        is_active = input("Введите новое значение статуса недвижимости (true или false): ")
        is_active = bool(is_active)
        tx_hash = contract.functions.updateEstateStatus(estate_id).transact({
            "from": account_user
        })
        print("Статус недвижимости успешно обновлен")
    except Exception as e:
            print(e)
            return None
#-------
def update_ad_status(account_user):
    try:
        ad_id = int(input("Введите ID объявления: "))
        tx_hash = contract.functions.updateAdStatus(ad_id).transact({
            "from": account_user
        })

        print("Статус объявления успешно обновлен")
    except Exception as e:
            print(e)
            return None
#------
def withdraw_funds(account_user):
    try:
        amount = int(input("Сумма к выводу: "))
        tx_hash = contract.functions.withDraw(amount).transact({
            "from": account_user
        })
        print("Средства успешно выведены")
    except Exception as e:
            print(e)
            return None
#-----
def get_user_balance(account_user):
    try:   
        tx_hash = contract.functions.getBalance().call({
            "from": account_user
        })
        print("Ваш баланс = ", tx_hash) # та же история ошибка в utiles.py 
    except Exception as e:
            print(e)
            return None
# --------------------------------------------------------------------------------------------------------------------------------

def login_registr():
    print("1. Регистрация")
    print("2. Вход")
    chooise = int(input())
    if chooise == 1:
        print("Введите пароль: ")
        password = input()
        newAcc = w3.eth.account.create(password)
        print("Ваш адрес: ", newAcc.address)
        main()
    elif chooise == 2:
        try:
            login = input("Введите адрес: ")
            password = input("Введите пароль: ")
            w3.geth.personal.unlock_account(login, password)
            print("Успешный вход")
            return login
        except Exception as e:
            print(e)
            return None
    else:
        print("Неверный выбор")
        login_registr()


def print_menu():
    print("1. Создание недвижимости")
    print("2. Создание объявления")
    print("3. Изменение статуса недвижимости")
    print("4. Изменение статуса объявления")
    print("5. баланс пользователя")
    print("6. Вывод средств")
    print("0. Выход")



def main():
    try:
         
        IsDone = False
        while True:
            if IsDone != True:
                account_user = login_registr()
                if account_user is not None:
                    IsDone = True
            else:
                print_menu()
                option = input("Выберите опцию: ")
                if option == "0":
                    break
                elif option == "1":
                    create_estate(account_user)
                elif option == "2":
                    create_ad(account_user)
                elif option == "3":
                    update_estate_status(account_user)
                elif option == "4":
                    update_ad_status(account_user)
                elif option == "5":
                    get_user_balance(account_user)
                elif option == "6":
                    withdraw_funds(account_user)
                elif option == "7":
                    get_estate(account_user)
                else:
                    print("Неверная опция")
    except Exception as e:
        print(e)
        return None






if __name__ == '__main__':
    main()