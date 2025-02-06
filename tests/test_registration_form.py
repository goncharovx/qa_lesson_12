import os
import allure
from selene import browser, have, be
from selene.support.shared.jquery_style import s


def test_registration_form(setup_browser):
    first_name = "Sonic"
    last_name = "Syndicate"
    email = "test@mail.ru"
    phone = "9939993388"
    subject = "Maths"
    address = "Moscow 5"
    state = "#react-select-3-option-0"
    city = "#react-select-4-option-0"
    gender = '[for="gender-radio-1"]'
    hobbies = ['[for="hobbies-checkbox-1"]', '[for="hobbies-checkbox-3"]']
    file_path = os.path.abspath("tests/resources/pic.png")

    with allure.step('Открыть форму регистрации'):
        print("Открытие формы регистрации")
        browser.open('/automation-practice-form')

        browser.execute_script("document.querySelectorAll('iframe').forEach(iframe => iframe.remove())")
        browser.execute_script("$('footer').remove()")
        browser.execute_script("$('#fixedban').remove()")

    with allure.step('Заполнить ФИО'):
        print(f"Заполнение имени: {first_name}, фамилии: {last_name}")
        s('#firstName').type(first_name)
        s('#lastName').type(last_name)

    with allure.step('Заполнить e-mail'):
        print(f"Заполнение email: {email}")
        s('#userEmail').type(email)

    with allure.step('Выбрать пол'):
        print("Выбор пола: Мужчина")
        s(gender).click()

    with allure.step('Заполнить телефон'):
        print(f"Заполнение номера телефона: {phone}")
        s('#userNumber').type(phone)

    with allure.step('Установить дату рождения'):
        print("Установка даты рождения: 3 марта 1960")
        browser.execute_script("arguments[0].scrollIntoView(true);", s('#dateOfBirthInput').locate())
        browser.execute_script("arguments[0].click();", s('#dateOfBirthInput').locate())
        s('.react-datepicker__month-select').click().s('[value="2"]').click()
        s('.react-datepicker__year-select').click().s('[value="1960"]').click()
        s('.react-datepicker__day--003:not(.react-datepicker__day--outside-month)').click()

    with allure.step('Выбрать предмет'):
        print(f"Выбор предмета: {subject}")
        s('#subjectsInput').type(subject).press_enter()

    with allure.step('Выбрать хобби'):
        print("Выбор хобби: Спорт и Музыка")
        for hobby in hobbies:
            s(hobby).should(be.visible).click()

    with allure.step('Загрузить файл'):
        print(f"Загрузка файла: {file_path}")
        s('#uploadPicture').send_keys(file_path)

    with allure.step('Заполнить адрес'):
        print(f"Заполнение адреса: {address}")
        s('#currentAddress').type(address)

    with allure.step('Выбрать штат'):
        print("Выбор штата")
        s('#state').click().s(state).click()

    with allure.step('Выбрать город'):
        print("Выбор города")
        s('#city').click().s(city).click()

    with allure.step('Подтвердить регистрацию'):
        print("Подтверждение формы")
        s('#submit').click()

    with allure.step('Проверить результат'):
        print("Проверка модального окна результатов")
        s('.modal-content').should(be.visible)
        s('.modal-content').should(have.text(first_name))
        s('.modal-content').should(have.text(last_name))
        s('.modal-content').should(have.text(email))