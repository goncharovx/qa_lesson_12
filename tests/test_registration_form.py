import os

import allure
from selene import browser, have, be
from selene.support.shared.jquery_style import s


def test_registration_form(setup_browser):
    first_name = "Sonic"
    last_name = "Syndicate"
    file_path = os.path.abspath("tests/resources/pic.png")

    with allure.step('Открыть форму регистрации'):
        browser.open('/automation-practice-form')
        browser.execute_script("document.querySelectorAll('iframe').forEach(iframe => iframe.remove())")
        browser.execute_script("$('footer').remove()")
        browser.execute_script("$('#fixedban').remove()")

    with allure.step('Заполнить ФИО'):
        s('#firstName').type(first_name)
        s('#lastName').type(last_name)

    with allure.step('Заполнить e-mail'):
        s('#userEmail').type('test@mail.ru')

    with allure.step('Выбрать пол'):
        s('[for="gender-radio-1"]').click()

    with allure.step('Заполнить телефон'):
        s('#userNumber').type('9939993388')

    with allure.step('Установить дату рождения'):
        browser.execute_script("arguments[0].scrollIntoView(true);", s('#dateOfBirthInput').locate())
        browser.execute_script("arguments[0].click();", s('#dateOfBirthInput').locate())
        s('.react-datepicker__month-select').click().s('[value="2"]').click()
        s('.react-datepicker__year-select').click().s('[value="1960"]').click()
        s('.react-datepicker__day--003:not(.react-datepicker__day--outside-month)').click()

    with allure.step('Выбрать предмет'):
        s('#subjectsInput').type('Maths').press_enter()

    with allure.step('Выбрать хобби'):
        element = s('[for="hobbies-checkbox-1"]').locate()
        browser.execute_script("arguments[0].scrollIntoView(true);", element)
        s('[for="hobbies-checkbox-1"]').should(be.visible).click()
        # browser.driver.save_screenshot('debug.png')
        s('[for="hobbies-checkbox-1"]').click()
        s('[for="hobbies-checkbox-3"]').click()

    with allure.step('Загрузить файл'):
        s('#uploadPicture').send_keys(file_path)

    with allure.step('Заполнить адрес'):
        s('#currentAddress').type('Moscow 5')

    with allure.step('Выбрать штат'):
        s('#state').click().s('#react-select-3-option-0').click()

    with allure.step('Выбрать город'):
        s('#city').click().s('#react-select-4-option-0').click()

    with allure.step('Подтвердить регистрацию'):
        s('#submit').click()

    with allure.step('Проверить результат'):
        s('.modal-content').should(be.visible)
        s('.modal-content').should(have.text(first_name))
        s('.modal-content').should(have.text(last_name))
