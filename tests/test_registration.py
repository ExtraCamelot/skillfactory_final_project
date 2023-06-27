import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from functions.registration_functions import get_page_name, get_error_text, check_field_errors, \
	check_field_validation, check_region_field, enter_to_registration, get_field_data, clear_field, \
	push_registration_button, check_password_length_hints, check_field_errors_with_clear_field, \
	enter_to_email_tel_confirm, click_name_field, click_registration_button, check_page_agreement, check_modal_closed


@pytest.fixture(autouse=True)
def testing():
	pytest.driver = webdriver.Chrome('./chromedriver.exe')
	pytest.driver.set_window_size(1366, 768)
	pytest.driver.implicitly_wait(10)
	# Переходим на страницу авторизации
	pytest.driver.get('https://b2c.passport.rt.ru')

	yield

	pytest.driver.quit()


# TC-SF-001: Роутинги между формами Авторизации и Регистрации
def test_check_routing():
	page_name = get_page_name("card-container__title")
	assert page_name == 'Авторизация'
	pytest.driver.find_element(By.ID, "kc-register").click()
	page_name = get_page_name("card-container__title")
	assert page_name == 'Регистрация'
	# Переход назад по истории браузера
	pytest.driver.execute_script("window.history.go(-1)")
	page_name = get_page_name("card-container__title")
	assert page_name == 'Авторизация'
	# Переход вперёд по истории браузера
	pytest.driver.execute_script("window.history.go(1)")
	page_name = get_page_name("card-container__title")
	assert page_name == 'Регистрация'


# TC-SF-002: Обязательные поля формы Регистрации
def test_required_fields():
	enter_to_registration()
	# Шаг 1
	pytest.driver.find_element(By.NAME, "register").click()
	error_text = get_error_text('element', '//*[@id="page-right"]/div/div/div/form/div[1]/div[1]/span')
	assert error_text == 'Необходимо заполнить поле кириллицей. От 2 до 30 символов.'
	error_text = get_error_text('element', '//*[@id="page-right"]/div/div/div/form/div[1]/div[2]/span')
	assert error_text == 'Необходимо заполнить поле кириллицей. От 2 до 30 символов.'
	error_text = get_error_text('element', '//*[@id="page-right"]/div/div/div/form/div[3]/div/span')
	assert error_text == 'Введите телефон в формате +7ХХХХХХХХХХ или +375XXXXXXXXX, или email в формате example@email.ru'
	error_text = get_error_text('element', '//*[@id="page-right"]/div/div/div/form/div[4]/div[1]/span')
	assert error_text == 'Длина пароля должна быть не менее 8 символов'
	error_text = get_error_text('element', '//*[@id="page-right"]/div/div/div/form/div[4]/div[2]/span')
	assert error_text == 'Длина пароля должна быть не менее 8 символов'
	page_name = get_page_name("card-container__title")
	assert page_name == 'Регистрация'
	# Шаг 2
	check_field_errors(By.NAME, "firstName", 'Александр', '//*[@id="page-right"]/div/div/div/form/div[1]/div[1]/span',
					   "Имя", enter_to_email_tel_confirm)
	# Шаг 3
	check_field_errors(By.NAME, "lastName", 'Пушкин', '//*[@id="page-right"]/div/div/div/form/div[1]/div[2]/span',
					   "Фамилия", enter_to_email_tel_confirm)
	# Шаг 4
	check_field_errors(By.ID, 'address', 'test@test.test', '//*[@id="page-right"]/div/div/div/form/div[3]/div/span',
					   'E-mail или мобильный телефон', enter_to_email_tel_confirm)
	# Шаг 5
	check_field_errors(By.NAME, "password", 'Qwerty123!!!', '//*[@id="page-right"]/div/div/div/form/div[4]/div[1]/span',
					   "Пароль", enter_to_email_tel_confirm)
	# Шаг 6
	check_field_errors(By.NAME, "password-confirm", 'Qwerty123!!!',
					   '//*[@id="page-right"]/div/div/div/form/div[4]/div[2]/span',
					   "Подтверждение пароля", enter_to_email_tel_confirm)
	page_name = get_page_name("card-container__title")
	assert page_name == 'Подтверждение email'


# TC-SF-003: Валидация поля "Имя" в форме Регистрации
def test_field_name_validation():
	enter_to_registration()
	# Шаг 1
	pytest.driver.find_element(By.NAME, "lastName").send_keys("Пушкин")
	pytest.driver.find_element(By.ID, "address").send_keys('test@test.test')
	pytest.driver.find_element(By.NAME, "password").send_keys("Qwerty123!!!")
	pytest.driver.find_element(By.NAME, "password-confirm").send_keys("Qwerty123!!!")
	error_text = check_field_validation(By.NAME, "firstName", "  ",
										'//*[@id="page-right"]/div/div/div/form/div[1]/div[1]/span', 'element')
	assert error_text == 'Необходимо заполнить поле кириллицей. От 2 до 30 символов.'
	# Шаг 2
	error_text = check_field_validation(By.NAME, "firstName", "qw",
										'//*[@id="page-right"]/div/div/div/form/div[1]/div[1]/span', 'element')
	assert error_text == 'Необходимо заполнить поле кириллицей. От 2 до 30 символов.'
	# Шаг 3
	error_text = check_field_validation(By.NAME, "firstName", "01",
										'//*[@id="page-right"]/div/div/div/form/div[1]/div[1]/span', 'element')
	assert error_text == 'Необходимо заполнить поле кириллицей. От 2 до 30 символов.'
	# Шаг 4
	error_text = check_field_validation(By.NAME, "firstName", "й",
										'//*[@id="page-right"]/div/div/div/form/div[1]/div[1]/span', 'element')
	assert error_text == 'Необходимо заполнить поле кириллицей. От 2 до 30 символов.'
	# Шаг 5
	error_text = check_field_validation(By.NAME, "firstName", "йs",
										'//*[@id="page-right"]/div/div/div/form/div[1]/div[1]/span', 'element')
	assert error_text == 'Необходимо заполнить поле кириллицей. От 2 до 30 символов.'
	# Шаг 6
	error_text = check_field_validation(By.NAME, "firstName", "ЙйфвйййфвйййвйййфвйййфвйййфвйфФ",
										'//*[@id="page-right"]/div/div/div/form/div[1]/div[1]/span', 'element')
	assert error_text == 'Необходимо заполнить поле кириллицей. От 2 до 30 символов.'
	# Шаг 7
	pytest.driver.find_element(By.NAME, "firstName").send_keys("фы")
	pytest.driver.find_element(By.NAME, "register").click()
	pytest.driver.find_element(By.NAME, "register").click()
	page_name = get_page_name("card-container__title")
	assert page_name == 'Подтверждение email'


# TC-SF-004: Валидация поля "Фамилия" в форме Регистрации
def test_field_last_name_validation():
	enter_to_registration()
	# Шаг 1
	pytest.driver.find_element(By.NAME, "firstName").send_keys("Александр")
	pytest.driver.find_element(By.ID, "address").send_keys('test@test.test')
	pytest.driver.find_element(By.NAME, "password").send_keys("Qwerty123!!!")
	pytest.driver.find_element(By.NAME, "password-confirm").send_keys("Qwerty123!!!")
	error_text = check_field_validation(By.NAME, "lastName", "  ",
										'//*[@id="page-right"]/div/div/div/form/div[1]/div[2]/span', 'element')
	assert error_text == 'Необходимо заполнить поле кириллицей. От 2 до 30 символов.'
	# Шаг 2
	error_text = check_field_validation(By.NAME, "lastName", "qw",
										'//*[@id="page-right"]/div/div/div/form/div[1]/div[2]/span', 'element')
	assert error_text == 'Необходимо заполнить поле кириллицей. От 2 до 30 символов.'
	# Шаг 3
	error_text = check_field_validation(By.NAME, "lastName", "01",
										'//*[@id="page-right"]/div/div/div/form/div[1]/div[2]/span', 'element')
	assert error_text == 'Необходимо заполнить поле кириллицей. От 2 до 30 символов.'
	# Шаг 4
	error_text = check_field_validation(By.NAME, "lastName", "й",
										'//*[@id="page-right"]/div/div/div/form/div[1]/div[2]/span', 'element')
	assert error_text == 'Необходимо заполнить поле кириллицей. От 2 до 30 символов.'
	# Шаг 5
	error_text = check_field_validation(By.NAME, "lastName", "йs",
										'//*[@id="page-right"]/div/div/div/form/div[1]/div[2]/span', 'element')
	assert error_text == 'Необходимо заполнить поле кириллицей. От 2 до 30 символов.'
	# Шаг 6
	error_text = check_field_validation(By.NAME, "lastName", "ЙйфвйййфвйййвйййфвйййфвйййфвйфФ",
										'//*[@id="page-right"]/div/div/div/form/div[1]/div[2]/span', 'element')
	assert error_text == 'Необходимо заполнить поле кириллицей. От 2 до 30 символов.'
	# Шаг 7
	pytest.driver.find_element(By.NAME, "lastName").send_keys("фы")
	pytest.driver.find_element(By.NAME, "register").click()
	pytest.driver.find_element(By.NAME, "register").click()
	page_name = get_page_name("card-container__title")
	assert page_name == 'Подтверждение email'


# TC-SF-005: Выбор Региона в форме Регистрации
def test_field_region():
	# Шаг 1, 2
	enter_to_registration()
	check_region_field('Москва г')
	# Шаг 3
	pytest.driver.find_element(By.NAME, "firstName").send_keys("Александр")
	pytest.driver.find_element(By.NAME, "lastName").send_keys("Пушкин")
	pytest.driver.find_element(By.ID, "address").send_keys('test@test.test')
	pytest.driver.find_element(By.NAME, "password").send_keys("Qwerty123!!!")
	pytest.driver.find_element(By.NAME, "password-confirm").send_keys("Qwerty123!!!")
	# Шаг 4
	pytest.driver.find_element(By.XPATH, '//*[@id="page-right"]/div/div/div/form/div[2]/div/div/input').click()
	pytest.driver.find_element(By.XPATH,
							   '//*[@id="page-right"]/div/div/div/form/div[2]/div[2]/div[2]/div/div[4]').click()
	check_region_field('Алтайский край')
	# Шаг 5
	pytest.driver.find_element(By.XPATH, '//*[@id="page-right"]/div/div/div/form/div[2]/div/div/input').click()
	pytest.driver.find_element(By.XPATH,
							   '//*[@id="page-right"]/div/div/div/form/div[2]/div[2]/div[2]/div/div[2]').click()
	check_region_field('Республика Беларусь')
	# Шаг 6
	pytest.driver.find_element(By.NAME, "register").click()
	page_name = get_page_name("card-container__title")
	assert page_name == 'Подтверждение email'


# TC-SF-007: Валидация поля "E-mail или мобильный телефон" в форме Регистрации". Длина Email
@pytest.mark.parametrize("email", [
	'',
	'email@mailru',
	'emailmail.ru',
	'e m a   il@mail.ru или e mail@mail.ru',
	'email@m a   il.ru',
	'@mail.ru ',
	'email@.ru',
	'email@mail.'
], ids=[
	'Шаг 1 - email: empty',
	'Шаг 2 - email: domain without dot',
	'Шаг 3 - email: without @',
	'Шаг 4 - email: with spaces in account name',
	'Шаг 5 - email: with spaces in domain',
	'Шаг 6 - email: without account name',
	'Шаг 7 - email: account domain 2 lvl',
	'Шаг 8 - email: account domain 1 lvl',
])
def test_field_email_validation(email):
	enter_to_registration()
	pytest.driver.find_element(By.NAME, "firstName").send_keys("Александр")
	pytest.driver.find_element(By.NAME, "lastName").send_keys("Пушкин")
	pytest.driver.find_element(By.NAME, "password").send_keys("Qwerty123!!!")
	pytest.driver.find_element(By.NAME, "password-confirm").send_keys("Qwerty123!!!")

	error_text = check_field_validation(By.ID, "address", email,
										'//*[@id="page-right"]/div/div/div/form/div[3]/div/span', 'element')
	assert error_text == 'Введите телефон в формате +7ХХХХХХХХХХ или +375XXXXXXXXX, или email в формате example@email.ru'


# TC-SF-007: Валидация поля "E-mail или мобильный телефон" в форме Регистрации". Маска Email
def test_field_email_mask_validation():
	enter_to_registration()
	# Шаг 1
	pytest.driver.find_element(By.NAME, "firstName").send_keys("Александр")
	pytest.driver.find_element(By.NAME, "lastName").send_keys("Пушкин")
	pytest.driver.find_element(By.NAME, "password").send_keys("Qwerty123!!!")
	pytest.driver.find_element(By.NAME, "password-confirm").send_keys("Qwerty123!!!")
	error_text = check_field_validation(By.ID, "address", "@.",
										'//*[@id="page-right"]/div/div/div/form/div[3]/div/span', 'element')
	assert error_text == 'Введите телефон в формате +7ХХХХХХХХХХ или +375XXXXXXXXX, или email в формате example@email.ru'
	# Шаг 2
	error_text = check_field_validation(By.ID, "address", "       @    .    ",
										'//*[@id="page-right"]/div/div/div/form/div[3]/div/span', 'element')
	assert error_text == 'Введите телефон в формате +7ХХХХХХХХХХ или +375XXXXXXXXX, или email в формате example@email.ru'
	# Шаг 3
	pytest.driver.find_element(By.ID, "address").send_keys('e@m.r')
	# Функции, сохраняющие текущее наполнение полей
	name_data = get_field_data('//*[@id="page-right"]/div/div/div/form/div[1]/div[1]/div/span[1]',
							   '//*[@id="page-right"]/div/div/div/form/div[1]/div[1]/div/span[1]/span[1]')
	assert name_data == "Александр"
	l_name_data = get_field_data('//*[@id="page-right"]/div/div/div/form/div[1]/div[2]/div/span[1]',
								 '//*[@id="page-right"]/div/div/div/form/div[1]/div[2]/div/span[1]/span[1]')
	assert l_name_data == "Пушкин"
	email_data = get_field_data('//*[@id="page-right"]/div/div/div/form/div[3]/div/div/span[1]',
								'//*[@id="page-right"]/div/div/div/form/div[3]/div/div/span[1]/span[1]')
	assert email_data == "e@m.r"
	region_data = get_field_data('//*[@id="page-right"]/div/div/div/form/div[2]/div/div/span[1]',
								 '//*[@id="page-right"]/div/div/div/form/div[2]/div/div/span[1]/span[1]')
	assert region_data == "Москва г"
	#
	push_registration_button('email')
	# # Шаг 4
	pytest.driver.find_element(By.NAME, "otp_back_phone").click()
	page_name = get_page_name("card-container__title")
	assert page_name == 'Регистрация'
	back_name_data = get_field_data('//*[@id="page-right"]/div/div/div/form/div[1]/div[1]/div/span[1]',
									'//*[@id="page-right"]/div/div/div/form/div[1]/div[1]/div/span[1]/span[1]')
	assert name_data == back_name_data
	back_l_name_data = get_field_data('//*[@id="page-right"]/div/div/div/form/div[1]/div[2]/div/span[1]',
									  '//*[@id="page-right"]/div/div/div/form/div[1]/div[2]/div/span[1]/span[1]')
	assert l_name_data == back_l_name_data
	back_email_data = get_field_data('//*[@id="page-right"]/div/div/div/form/div[3]/div/div/span[1]',
									 '//*[@id="page-right"]/div/div/div/form/div[3]/div/div/span[1]/span[1]')
	assert email_data == back_email_data
	back_region_data = get_field_data('//*[@id="page-right"]/div/div/div/form/div[2]/div/div/span[1]',
									  '//*[@id="page-right"]/div/div/div/form/div[2]/div/div/span[1]/span[1]')
	assert region_data == back_region_data
	password_data = get_field_data('//*[@id="page-right"]/div/div/div/form/div[4]/div[1]/div/span[1]',
								   '//*[@id="page-right"]/div/div/div/form/div[4]/div[1]/div/span[1]/span[1]')
	assert password_data == ''
	confirm_password_data = get_field_data('//*[@id="page-right"]/div/div/div/form/div[4]/div[2]/div/span[1]',
										   '//*[@id="page-right"]/div/div/div/form/div[4]/div[2]/div/span[1]/span[1]')
	assert confirm_password_data == ''
	# Шаг 5
	pytest.driver.find_element(By.NAME, "password").send_keys("Qwerty123!!!")
	pytest.driver.find_element(By.NAME, "password-confirm").send_keys("Qwerty123!!!")
	clear_field(By.ID, "address")
	pytest.driver.find_element(By.ID, "address").send_keys('email@mail.ruuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuu'
														   'uuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuu'
														   'uuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuu'
														   'uuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuu'
														   'uuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuus')
	push_registration_button('email')


# TC-SF-008: Валидация поля "E-mail или мобильный телефон" в форме Регистрации". Автоподстановка кода страны (+7)
def test_field_email_tel_code():
	enter_to_registration()
	# Шаг 1
	pytest.driver.find_element(By.NAME, "firstName").send_keys("Александр")
	pytest.driver.find_element(By.NAME, "lastName").send_keys("Пушкин")
	pytest.driver.find_element(By.NAME, "password").send_keys("Qwerty123!!!")
	pytest.driver.find_element(By.NAME, "password-confirm").send_keys("Qwerty123!!!")
	error_text = check_field_validation(By.ID, "address", "1884441122",
										'//*[@id="page-right"]/div/div/div/form/div[3]/div/span', 'element')
	assert error_text == 'Введите телефон в формате +7ХХХХХХХХХХ или +375XXXXXXXXX, или email в формате example@email.ru'
	# Шаг 2
	clear_field(By.ID, "address")
	# Шаг 3
	pytest.driver.find_element(By.ID, "address").send_keys('9884441122')
	pytest.driver.find_element(By.NAME, "firstName").click()
	tel_data = get_field_data('//*[@id="page-right"]/div/div/div/form/div[3]/div/div/span[1]',
							  '//*[@id="page-right"]/div/div/div/form/div[3]/div/div/span[1]/span[1]')
	# Проверить форматирование телефона
	assert tel_data == '+7 988 444-11-22'
	push_registration_button('tel')


# TC-SF-009: Валидация поля "E-mail или мобильный телефон" в форме Регистрации". Автоподстановка кода страны (+375)
def test_field_email_tel_code_bel():
	enter_to_registration()
	# Шаг 1
	pytest.driver.find_element(By.NAME, "firstName").send_keys("Александр")
	pytest.driver.find_element(By.NAME, "lastName").send_keys("Пушкин")
	pytest.driver.find_element(By.NAME, "password").send_keys("Qwerty123!!!")
	pytest.driver.find_element(By.NAME, "password-confirm").send_keys("Qwerty123!!!")
	error_text = check_field_validation(By.ID, "address", "291234567",
										'//*[@id="page-right"]/div/div/div/form/div[3]/div/span', 'element')
	assert error_text == 'Введите телефон в формате +7ХХХХХХХХХХ или +375XXXXXXXXX, или email в формате example@email.ru'
	# Шаг 2
	clear_field(By.ID, "address")
	# Шаг 3
	pytest.driver.find_element(By.ID, "address").send_keys('375291234567')
	pytest.driver.find_element(By.NAME, "firstName").click()
	tel_data = get_field_data('//*[@id="page-right"]/div/div/div/form/div[3]/div/div/span[1]',
							  '//*[@id="page-right"]/div/div/div/form/div[3]/div/div/span[1]/span[1]')
	# Проверить форматирование телефона
	assert tel_data == '+375 29 123-45-67'
	push_registration_button('tel')


# TC-SF-010: Валидация поля "Пароль" в форме "Регистрации" по длине
def test_field_password_length():
	enter_to_registration()
	pytest.driver.find_element(By.NAME, "firstName").send_keys("Александр")
	pytest.driver.find_element(By.NAME, "lastName").send_keys("Пушкин")
	pytest.driver.find_element(By.ID, "address").send_keys('test@test.test')
	pytest.driver.find_element(By.NAME, "password-confirm").send_keys("Qwerty123!!!")
	# Шаг 1-2
	password_hint_xpath = '//*[@id="page-right"]/div/div/div/form/div[4]/div[1]/span'
	print('\n')
	check_password_length_hints("password", 'q', password_hint_xpath)
	# Шаг 3-4
	check_password_length_hints("password", 'Qwertyy', password_hint_xpath)
	# Шаг 5-6
	check_password_length_hints("password", 'Qwerty12', password_hint_xpath)
	# Шаг 7
	check_password_length_hints("password", 'Qwerty78901234567890', password_hint_xpath)
	# Шаг 8
	pytest.driver.find_element(By.NAME, "password").send_keys("1")
	pytest.driver.find_element(By.NAME, "password-confirm").click()
	error_text = get_error_text('element', password_hint_xpath)
	assert error_text == 'Длина пароля должна быть не более 20 символов'
	print(error_text)


# TC-SF-011: Валидация поля "Пароль" в форме "Регистрации" по допустимым символам
def test_field_password_symbols():
	enter_to_registration()
	pytest.driver.find_element(By.NAME, "firstName").send_keys("Александр")
	pytest.driver.find_element(By.NAME, "lastName").send_keys("Пушкин")
	pytest.driver.find_element(By.ID, "address").send_keys('test@test.test')
	pytest.driver.find_element(By.NAME, "password-confirm").send_keys("Qwerty123!!!")
	# Шаг 1-2
	password_hint_xpath = '//*[@id="page-right"]/div/div/div/form/div[4]/div[1]/span'
	error_text = check_field_errors_with_clear_field(By.NAME, 'password', 'фываячсм', click_name_field,
													 password_hint_xpath, 'element')
	assert error_text == 'Пароль должен содержать только латинские буквы'
	print('\n' + error_text)
	# Шаг 3-4
	error_text = check_field_errors_with_clear_field(By.NAME, 'password', 'qwertyas', click_name_field,
													 password_hint_xpath, 'element')
	assert error_text == 'Пароль должен содержать хотя бы 1 спецсимвол или хотя бы одну цифру'
	print(error_text)
	# Шаг 5-6
	error_text = check_field_errors_with_clear_field(By.NAME, 'password', 'qwerty12', click_name_field,
													 password_hint_xpath, 'element')
	assert error_text == 'Пароль должен содержать хотя бы одну заглавную букву'
	print(error_text)
	# Шаг 7-8
	error_text = check_field_errors_with_clear_field(By.NAME, 'password', 'qwerty!@', click_name_field,
													 password_hint_xpath, 'element')
	assert error_text == 'Пароль должен содержать хотя бы одну заглавную букву'
	print(error_text)
	# Шаг 9
	check_field_errors(By.NAME, "password", "Qwerty12", '//*[@id="page-right"]/div/div/div/form/div[4]/div[1]/span',
					   "Пароль", click_name_field)
	# Шаг 10
	clear_field(By.NAME, "password")
	# Шаг 11
	check_field_errors(By.NAME, "password", "Qwerty!№", '//*[@id="page-right"]/div/div/div/form/div[4]/div[1]/span',
					   "Пароль", click_name_field)


# TC-SF-012: Валидация поля "Подтверждение пароля" в форме "Регистрации" по длине
def test_field_password_confirm_length():
	enter_to_registration()
	pytest.driver.find_element(By.NAME, "firstName").send_keys("Александр")
	pytest.driver.find_element(By.NAME, "lastName").send_keys("Пушкин")
	pytest.driver.find_element(By.ID, "address").send_keys('test@test.test')
	pytest.driver.find_element(By.NAME, "password").send_keys("Qwerty123!!!")
	# Шаг 1-2
	print('\n')
	password_hint_xpath = '//*[@id="page-right"]/div/div/div/form/div[4]/div[2]/span'
	check_password_length_hints("password-confirm", 'q', password_hint_xpath)
	# Шаг 3-4
	check_password_length_hints("password-confirm", 'Qwertyy', password_hint_xpath)
	# Шаг 5-6
	check_password_length_hints("password-confirm", 'Qwerty12', password_hint_xpath)
	# Шаг 7
	check_password_length_hints("password-confirm", 'Qwerty78901234567890', password_hint_xpath)
	# Шаг 8
	pytest.driver.find_element(By.NAME, "password-confirm").send_keys("1")
	click_name_field()
	error_text = get_error_text('element', password_hint_xpath)
	assert error_text == 'Длина пароля должна быть не более 20 символов'
	print(error_text)


# TC-SF-013: Валидация поля "Подтверждение пароля" в форме "Регистрации" по допустимым символам
def test_field_password_confirm_symbols():
	enter_to_registration()
	pytest.driver.find_element(By.NAME, "firstName").send_keys("Александр")
	pytest.driver.find_element(By.NAME, "lastName").send_keys("Пушкин")
	pytest.driver.find_element(By.ID, "address").send_keys('test@test.test')
	pytest.driver.find_element(By.NAME, "password").send_keys("Qwerty123!!!")
	# Шаг 1-2
	password_hint_xpath = '//*[@id="page-right"]/div/div/div/form/div[4]/div[2]/span'
	error_text = check_field_errors_with_clear_field(By.NAME, 'password-confirm',
													 'фываячсм', click_name_field, password_hint_xpath, 'element')
	assert error_text == 'Пароль должен содержать только латинские буквы'
	print('\n' + error_text)
	# Шаг 3-4
	error_text = check_field_errors_with_clear_field(By.NAME, 'password-confirm',
													 'qwertyas', click_name_field, password_hint_xpath, 'element')
	assert error_text == 'Пароль должен содержать хотя бы 1 спецсимвол или хотя бы одну цифру'
	print(error_text)
	# Шаг 5-6
	error_text = check_field_errors_with_clear_field(By.NAME, 'password-confirm',
													 'qwerty12', click_name_field, password_hint_xpath, 'element')
	assert error_text == 'Пароль должен содержать хотя бы одну заглавную букву'
	print(error_text)
	# Шаг 7-8
	error_text = check_field_errors_with_clear_field(By.NAME, 'password-confirm',
													 'qwerty!@', click_name_field, password_hint_xpath, 'element')
	assert error_text == 'Пароль должен содержать хотя бы одну заглавную букву'
	print(error_text)
	# Шаг 9
	check_field_errors(By.NAME, "password-confirm", "Qwerty12",
					   '//*[@id="page-right"]/div/div/div/form/div[4]/div[1]/span', "Пароль", click_name_field)
	# Шаг 10
	clear_field(By.NAME, "password-confirm")
	# Шаг 11
	check_field_errors(By.NAME, "password-confirm", "Qwerty!№",
					   '//*[@id="page-right"]/div/div/div/form/div[4]/div[1]/span', "Пароль", click_name_field)


# TC-SF-014: Валидация подверждения пароля в форме "Регистрации"
def test_field_password_confirmation():
	enter_to_registration()
	pytest.driver.find_element(By.NAME, "firstName").send_keys("Александр")
	pytest.driver.find_element(By.NAME, "lastName").send_keys("Пушкин")
	pytest.driver.find_element(By.ID, "address").send_keys('test@test.test')
	# Шаг 1
	pytest.driver.find_element(By.NAME, "password").send_keys("Qwerty!№")
	# Шаг 2-3
	password_hint_xpath = '//*[@id="page-right"]/div/div/div/form/div[4]/div[2]/span'
	error_text = check_field_errors_with_clear_field(By.NAME, 'password-confirm', 'Qwerty!*', click_registration_button,
													 password_hint_xpath, 'element')
	assert error_text == 'Пароли не совпадают'
	print('\n' + error_text)
	# Шаг 4
	pytest.driver.find_element(By.NAME, "password-confirm").send_keys("Qwerty!№")
	push_registration_button('email')


# TC-SF-015: Надёжность пароля в форме "Регистрации"
def test_field_password_defense():
	enter_to_registration()
	pytest.driver.find_element(By.NAME, "firstName").send_keys("Александр")
	pytest.driver.find_element(By.NAME, "lastName").send_keys("Пушкин")
	pytest.driver.find_element(By.ID, "address").send_keys('test@test.test')
	# Шаг 1
	password = "Qwerty123"
	pytest.driver.find_element(By.NAME, "password").send_keys(password)
	# Шаг 2
	password_hint_xpath = '//*[@id="form-error-message"]'
	error_text = check_field_errors_with_clear_field(By.NAME, 'password-confirm', password, click_registration_button,
													 password_hint_xpath, 'element')
	assert error_text == 'Пароль ненадежный. Необходимо придумать более сложный пароль.'


# TC-SF-016: Открытие документов "Пользовательское соглашение"
def test_docs_agreement():
	enter_to_registration()
	# Шаг 1
	pytest.driver.find_element(By.CSS_SELECTOR, ".rt-link.rt-link--orange").click()
	check_page_agreement()
	# Шаг 2
	pytest.driver.close()
	pytest.driver.switch_to.window(pytest.driver.window_handles[0])
	# Шаг 3
	pytest.driver.find_element(By.XPATH, '//*[@id="rt-footer-agreement-link"]/span[2]').click()
	check_page_agreement()


# TC-SF-017: Открытие документа "Политика конфиденциальности"
def test_docs_privacy():
	enter_to_registration()
	# Шаг 1
	pytest.driver.find_element(By.XPATH, '//*[@id="rt-footer-agreement-link"]/span[1]').click()
	# Баг: неверная ссылка на документ
	check_page_agreement()


# TC-SF-018: Возможность набора номера телефона
def test_tel_number():
	enter_to_registration()
	# Шаг 1
	pytest.driver.find_element(By.CLASS_NAME, 'rt-footer-right__support-phone').is_enabled()
	pytest.driver.find_element(By.CLASS_NAME, 'rt-footer-right__support-phone').click()


# TC-SF-020: Повторный запрос кода
def test_tel_code_negative():
	enter_to_registration()
	# Шаг 1
	pytest.driver.find_element(By.NAME, "firstName").send_keys("Александр")
	pytest.driver.find_element(By.NAME, "lastName").send_keys("Пушкин")
	pytest.driver.find_element(By.ID, "address").send_keys('9884441122')
	password = "Qwerty12!"
	pytest.driver.find_element(By.NAME, "password").send_keys(password)
	pytest.driver.find_element(By.NAME, "password-confirm").send_keys(password)
	# Шаг 2
	push_registration_button('tel')
	# Шаг 3
	timer = get_page_name('code-input-container__timeout')
	assert "Получить код повторно" in timer
	time.sleep(121)
	# Шаг 4
	pytest.driver.find_element(By.CLASS_NAME, "code-input-container__resend").click()
	timer = get_page_name('code-input-container__timeout')
	assert "Получить код повторно" in timer


# TC-SF-021: Изменение Email после отправки кода
def test_button_change_mail():
	enter_to_registration()
	# Шаг 1
	first_name, last_name, address = "Александр", "Пушкин", '79884441122'
	password = "Qwerty12!"
	region_1 = get_field_data('//*[@id="page-right"]/div/div/div/form/div[2]/div/div/span[1]',
							'//*[@id="page-right"]/div/div/div/form/div[2]/div/div/span[1]/span[1]')
	pytest.driver.find_element(By.NAME, "firstName").send_keys(first_name)
	name_1 = get_field_data('//*[@id="page-right"]/div/div/div/form/div[1]/div[1]/div/span[1]',
							'//*[@id="page-right"]/div/div/div/form/div[1]/div[1]/div/span[1]/span[1]')
	pytest.driver.find_element(By.NAME, "lastName").send_keys(last_name)
	last_name_1 = get_field_data('//*[@id="page-right"]/div/div/div/form/div[1]/div[2]/div/span[1]',
							'//*[@id="page-right"]/div/div/div/form/div[1]/div[2]/div/span[1]/span[1]')
	pytest.driver.find_element(By.ID, "address").send_keys(address)
	address_1 = get_field_data('//*[@id="page-right"]/div/div/div/form/div[3]/div/div/span[1]',
								 '//*[@id="page-right"]/div/div/div/form/div[3]/div/div/span[1]/span[1]')
	pytest.driver.find_element(By.NAME, "password").send_keys(password)
	pytest.driver.find_element(By.NAME, "password-confirm").send_keys(password)
	# Шаг 2
	push_registration_button('tel')
	timer = get_page_name('code-input-container__timeout')
	assert "Получить код повторно" in timer
	# Шаг 3
	pytest.driver.find_element(By.NAME, "otp_back_phone").click()
	page_name = get_page_name("card-container__title")
	assert page_name == 'Регистрация'
	region_2 = get_field_data('//*[@id="page-right"]/div/div/div/form/div[2]/div/div/span[1]',
							'//*[@id="page-right"]/div/div/div/form/div[2]/div/div/span[1]/span[1]')
	assert region_1 == region_2
	name_2 = get_field_data('//*[@id="page-right"]/div/div/div/form/div[1]/div[1]/div/span[1]',
							'//*[@id="page-right"]/div/div/div/form/div[1]/div[1]/div/span[1]/span[1]')
	assert name_1 == name_2
	last_name_2 = get_field_data('//*[@id="page-right"]/div/div/div/form/div[1]/div[2]/div/span[1]',
							'//*[@id="page-right"]/div/div/div/form/div[1]/div[2]/div/span[1]/span[1]')
	assert last_name_1 == last_name_2
	address_2 = get_field_data('//*[@id="page-right"]/div/div/div/form/div[3]/div/div/span[1]',
								 '//*[@id="page-right"]/div/div/div/form/div[3]/div/div/span[1]/span[1]')
	assert address_1 == address_2
	password_empty = get_field_data('//*[@id="page-right"]/div/div/div/form/div[4]/div[1]/div/span[1]',
							   '//*[@id="page-right"]/div/div/div/form/div[4]/div[1]/div/span[1]/span[1]')
	assert password_empty is None or password_empty == ""
	password_confirm_empty = get_field_data('//*[@id="page-right"]/div/div/div/form/div[4]/div[2]/div/span[1]',
									'//*[@id="page-right"]/div/div/div/form/div[4]/div[2]/div/span[1]/span[1]')
	assert password_confirm_empty is None or password_confirm_empty == ""


# TC-SF-022: Открытие документов "Пользовательское соглашение"
def test_modal_cookie():
	enter_to_registration()
	# Шаг 1
	pytest.driver.find_element(By.ID, "cookies-tip-open").click()
	modal_header = get_page_name("rt-tooltip__title")
	assert modal_header == 'Мы используем Cookie'
	# Шаг 2
	pytest.driver.find_element(By.ID, "page-left").click()
	check_modal_closed()
	# Шаг 3
	pytest.driver.find_element(By.ID, "cookies-tip-open").click()
	modal_header = get_page_name("rt-tooltip__title")
	assert modal_header == 'Мы используем Cookie'
	# Шаг 4
	pytest.driver.find_element(By.CLASS_NAME, "rt-tooltip__close").click()
	check_modal_closed()
