import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


def empty():
	return True


def click_name_field():
	pytest.driver.find_element(By.NAME, "firstName").click()


def click_registration_button():
	pytest.driver.find_element(By.NAME, "register").click()


def enter_to_registration():
	pytest.driver.find_element(By.ID, "kc-register").click()
	page_name = get_page_name("card-container__title")
	assert page_name == 'Регистрация'


def push_registration_button(email_tel):
	pytest.driver.find_element(By.NAME, "register").click()
	page_name = get_page_name("card-container__title")
	if email_tel == 'email':
		assert page_name == 'Подтверждение email'
	elif email_tel == 'tel':
		assert page_name == 'Подтверждение телефона'
	else:
		raise Exception('Invalid arg: only "email" or "tel"')


def get_page_name(class_name):
	page_name = pytest.driver.find_element(By.CLASS_NAME, class_name)
	page_name = page_name.text
	return page_name


def get_error_text(elem, xpath):
	if elem == 'element':
		error_text = pytest.driver.find_element(By.XPATH, xpath)
		error_text = error_text.text
		return error_text
	# вот это, возможно, стоит переработать или вообще убрать
	else:
		raise Exception("Неверное значение elem - должно быть 'element'")


def enter_to_email_tel_confirm():
	pytest.driver.find_element(By.NAME, "register").click()
	pytest.driver.implicitly_wait(5)
	page_name = get_page_name("card-container__title")
	return page_name


def check_field_errors(by, field_locator, field_keys, xpath, field_name, func):
	pytest.driver.find_element(by, field_locator).send_keys(field_keys)
	func()
	error_elements = pytest.driver.find_elements(By.XPATH, xpath)
	if len(error_elements) == 0:
		print("Данные поля валидны")
		return True
	else:
		raise Exception(f"Подсказка для поля {field_name} осталась")


def check_field_validation(by, field_locator, arg, err_xpath, elem):
	pytest.driver.find_element(by, field_locator).send_keys(arg)
	pytest.driver.find_element(By.NAME, "register").click()
	error_text = get_error_text(elem, err_xpath)
	pytest.driver.find_element(by, field_locator).send_keys(Keys.CONTROL + "a")
	pytest.driver.find_element(by, field_locator).send_keys(Keys.DELETE)
	return error_text


def check_region_field(region):
	parent_field_region = pytest.driver.find_element(By.XPATH,
													 '//*[@id="page-right"]/div/div/div/form/div[2]/div/div/span[1]')
	pytest.driver.execute_script("arguments[0].style.display = 'block';", parent_field_region)
	field_region = pytest.driver.find_element(By.XPATH,
											  '//*[@id="page-right"]/div/div/div/form/div[2]/div/div/span[1]/span[1]')
	field_region = field_region.text
	assert field_region == region
	pytest.driver.execute_script("arguments[0].style.display = 'none';", parent_field_region)


def get_field_data(xpath_parent_block, xpath_field_data):
	parent_field_region = pytest.driver.find_element(By.XPATH, xpath_parent_block)
	pytest.driver.execute_script("arguments[0].style.display = 'block';", parent_field_region)
	field_region = pytest.driver.find_element(By.XPATH, xpath_field_data)
	field_region = field_region.text
	pytest.driver.execute_script("arguments[0].style.display = 'none';", parent_field_region)
	return field_region


def clear_field(by, field_locator):
	pytest.driver.find_element(by, field_locator).send_keys(Keys.CONTROL + "a")
	pytest.driver.find_element(by, field_locator).send_keys(Keys.DELETE)


def check_password_length_hints(field_locator, arg, password_hint_xpath):
	pytest.driver.find_element(By.NAME, field_locator).send_keys(arg)
	click_name_field()
	if len(arg) < 8:
		error_text = get_error_text('element', password_hint_xpath)
		assert error_text == 'Длина пароля должна быть не менее 8 символов'
		print(error_text)
		clear_field(By.NAME, field_locator)
	elif len(arg) < 20:
		clear_field(By.NAME, field_locator)
		return True
	elif len(arg) == 20:
		return True
	else:
		error_text = get_error_text('element', password_hint_xpath)
		assert error_text == 'Длина пароля должна быть не более 20 символов'
		print(error_text)
		clear_field(By.NAME, "password")


def check_field_errors_with_clear_field(by, field_locator, arg, func, password_hint_xpath, elem):
	pytest.driver.find_element(by, field_locator).send_keys(arg)
	func()
	error_text = get_error_text(elem, password_hint_xpath)
	if len(error_text) == 0:
		clear_field(by, field_locator)
		return True
	else:
		clear_field(by, field_locator)
		return error_text


def check_page_agreement():
	pytest.driver.switch_to.window(pytest.driver.window_handles[1])
	current_url = pytest.driver.current_url
	assert "https://b2c.passport.rt.ru/sso-static/agreement/agreement.html" in current_url
	page_name = get_page_name('offer-title')
	assert "Публичная оферта о заключении Пользовательского соглашения на использование" in page_name


def check_modal_closed():
	modal = pytest.driver.find_elements(By.CSS_SELECTOR,
										'.rt-tooltip.rt-tooltip--rounded.rt-tooltip--topLeft.rt-cookies-tip')
	if len(modal) == 0:
		return True
	else:
		raise Exception("Модальное окно Cookie открыто")
