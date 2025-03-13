import sender_stand_request
import data
import configuration

def get_user_body(first_name):
    current_body = data.user_body.copy()
    current_body["firstName"] = first_name
    return current_body

def positive_assert(first_name):
    user_body = get_user_body(first_name)
    user_response = sender_stand_request.post_new_user(user_body)

    print(user_response.status_code)
    print(user_response.json()['authToken'])

    assert user_response.status_code == 201
    assert user_response.json()["authToken"] != ""

    users_table_response = sender_stand_request.get_users_table()
    str_user = user_body['firstName'] + ',' + user_body['phone'] + ',' \
               + user_body['address'] + ',,,' + user_response.json()['authToken']

    print(str_user)
    print(configuration.DIVIDER)

    assert users_table_response.text.count(str_user) == 1

def test_create_user_2_letter_in_first_name_get_success_response():
    positive_assert("Aa")

def test_create_user_15_letter_in_first_name_get_success_response():
    positive_assert('Aaaaaaaaaaaaaaa')

def negative_assert_symbol(first_name):
    user_body = get_user_body(first_name)
    response = sender_stand_request.post_new_user(user_body)

    print(response.status_code)
    print(f'"{first_name}"')
    print(response.json()['message'])
    print(configuration.DIVIDER)

    assert response.status_code == 400
    assert response.json()['code'] == 400
    assert response.json()['message'] == "Has introducido un nombre de usuario no válido. " \
                                         "El nombre solo puede contener letras del alfabeto latino, " \
                                         "la longitud debe ser de 2 a 15 caracteres."

def test_create_user_1_letter_in_first_name_get_error_response():
    negative_assert_symbol('A')

def test_create_user_16_letter_in_first_name_get_error_response():
    negative_assert_symbol('Aaaaaaaaaaaaaaaa')

def test_create_user_has_space_in_first_name_get_error_response():
    negative_assert_symbol('A Aaa')

def test_create_user_has_special_symbol_in_first_name_get_error_response():
    negative_assert_symbol("\"№%@\",")

def test_create_user_has_number_in_first_name_get_error_response():
    negative_assert_symbol('123')

def negative_assert_no_first_name(user_body):
    response = sender_stand_request.post_new_user(user_body)

    print(response.status_code)
    print(response.json()['message'])
    print(configuration.DIVIDER)

    assert response.status_code == 400
    assert response.json()['code'] == 400
    assert response.json()['message'] == "No se han aprobado todos los parámetros requeridos"

def test_create_user_no_first_name_get_error_response():
    user_body = data.user_body.copy()
    user_body.pop("firstName")
    negative_assert_no_first_name(user_body)

def test_create_user_empty_first_name_get_error_response():
    user_body = get_user_body("")
    negative_assert_no_first_name(user_body)

def test_create_user_number_type_first_name_get_error_response():
    user_body = get_user_body(12)
    response = sender_stand_request.post_new_user(user_body)

    print(response.status_code)
    print(configuration.DIVIDER)

    assert response.status_code == 400
    assert response.json()['code'] == 400

if __name__ == '__main__':
    test_create_user_2_letter_in_first_name_get_success_response()
    test_create_user_15_letter_in_first_name_get_success_response()
    test_create_user_1_letter_in_first_name_get_error_response()
    test_create_user_16_letter_in_first_name_get_error_response()
    #test_create_user_has_space_in_first_name_get_error_response()
    test_create_user_has_special_symbol_in_first_name_get_error_response()
    test_create_user_has_number_in_first_name_get_error_response()
    test_create_user_no_first_name_get_error_response()
    test_create_user_empty_first_name_get_error_response()
    test_create_user_number_type_first_name_get_error_response()