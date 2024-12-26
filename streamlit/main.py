import streamlit as st
import requests
from streamlit.runtime.scriptrunner import add_script_run_ctx, get_script_run_ctx
from streamlit_cookies_controller import CookieController
import pandas as pd

BASE_URL = "http://127.0.0.1:8000"  # Замените на ваш адрес API
controller = CookieController()

def set_cookie(key, value):
    ctx = get_script_run_ctx()
    if ctx is not None:
        controller.set(key, value)

def get_cookie(key):
    return controller.get(key)

def delete_cookie(key):
    if key in controller.getAll():
        controller.remove(key)

# Функция регистрации
def register_user():
    st.title("Регистрация")
    email = st.text_input("Email")
    phone_number = st.text_input("Номер телефона")
    first_name = st.text_input("Имя")
    last_name = st.text_input("Фамилия")
    password = st.text_input("Пароль", type="password")
    confirm_password = st.text_input("Подтвердите пароль", type="password")

    if st.button("Зарегистрироваться"):
        if email and phone_number and first_name and last_name and password and confirm_password:
            if password != confirm_password:
                st.error("Пароли не совпадают!")
            else:
                try:
                    response = requests.post(f"{BASE_URL}/auth/register/", json={
                        "email": email,
                        "password": password,
                        "phone_number": phone_number,
                        "first_name": first_name,
                        "last_name": last_name,
                    })
                    if response.status_code == 200:
                        st.success("Вы успешно зарегистрировались! Перейдите на страницу входа.")
                    else:
                        err = response.json().get("detail")
                        st.error(err[0]['loc'][1] + ': ' + err[0]['msg'])
                except Exception as e:
                    st.error(f"Ошибка: {e}")
        else:
            st.error("Все поля формы должны быть заполнены!")

# Функция входа
def login_user():
    st.title("Вход")
    email = st.text_input("Email")
    password = st.text_input("Пароль", type="password")

    if st.button("Войти"):
        if email and password:
            try:
                response = requests.post(f"{BASE_URL}/auth/login/", json={
                    "email": email,
                    "password": password
                })
                if response.status_code == 200:
                    data = response.json()
                    set_cookie("users_access_token", data['access_token'])
                    st.success("Вы успешно вошли в систему!")
                    st.stop()
                else:
                    st.error(response.json().get("detail", "Ошибка входа"))
            except Exception as e:
                st.error(f"Ошибка: {e}")
        else:
            st.error("Все поля формы должны быть заполнены!")

# Просмотр таблиц
# Просмотр таблиц
def show_tables():
    st.title("Просмотр таблиц")

    token = get_cookie("users_access_token")
    if not token:
        st.warning("Вы не авторизованы. Пожалуйста, войдите в систему.")
        st.stop()

    headers = {"Authorization": f"Bearer {token}"}

    tables = ["films", "genres", "filmgenres", "filmdirectors", "directors", "actors", "filmgrades"]
    selected_table = st.selectbox("Выберите таблицу", tables)

    if st.button("Загрузить данные"):
        try:
            response = requests.get(f"{BASE_URL}/{selected_table}/", headers=headers)
            if response.status_code == 200:
                data = response.json()
                df = pd.DataFrame(data)
                
                # Проверяем количество строк в DataFrame
                if len(df) > 100:
                    # Если строк больше 100, выводим первые 50 и последние 50 строк
                    first_50 = df.head(50)
                    last_50 = df.tail(50)
                    combined_df = pd.concat([first_50, last_50])
                    st.dataframe(combined_df)
                else:
                    # Если строк меньше или равно 100, выводим все строки
                    st.dataframe(df)
            else:
                st.error("Не удалось загрузить данные таблицы.")
        except Exception as e:
            st.error(f"Ошибка: {e}")
            

# Проверка на администратора
def is_admin(cookies):
    try:
        response = requests.get(f"{BASE_URL}/auth/me/", cookies=cookies)
        # print(response.json())
        if response.status_code == 200:
            return response.json().get("is_admin", False)
        else:
            st.error("Не удалось проверить права пользователя.")
            return False
    except Exception as e:
        st.error(f"Ошибка: {e}")
        return False
    

# Редактирование таблиц
def edit_tables():
    st.title("Изменение таблиц")

    token = get_cookie("users_access_token")
    if not token:
        st.warning("Вы не авторизованы. Пожалуйста, войдите в систему.")
        st.stop()
        
    cookies = {"users_access_token": f"{token}"}
    # print(cookies)
    
    if not is_admin(cookies):
        st.warning("У вас недостаточно прав для редактирования таблиц.")
        return

    tables = ["films", "genres", "filmgenres", "users", "filmdirectors", "directors", "actors", "filmgrades", "favoritefilms"]
    m2m_tables = ["filmgenres", "filmdirectors", "filmactors", "filmgrades", "favoritefilms"]
    selected_table = st.selectbox("Выберите таблицу для редактирования", tables)

    column_mappings_for_user = {
        "films": ["Название фильма", "Ссылка на фильм", "Средний рейтинг", "Описание", "Количество оценок"],
        "genres": ["Название жанра"],
        "filmgenres": ["ID фильма", "ID жанра"],
        "users": ["Номер телефона", "Имя", "Фамилия", "Email", "Админ"],
        "directors": ["Имя", "Фамилия"],
        "actors": ["Имя", "Фамилия"],
        "filmdirectors": ["ID фильма", "ID режиссера"],
        "filmactors": ["ID фильма", "ID актера"],
        "filmgrades": ["ID фильма", "ID пользователя", "Оценка"],
        "favoritefilms": ["ID фильма", "ID пользователя"],
        
    }

    column_mappings_for_db = {
        "films": ["title", "film_link", "average_rating", "description", "vote_count"],
        "genres": ["name"],
        "filmgenres": ["film_id", "genre_id"],
        "users": ["phone_number", "first_name", "last_name", "email", "is_admin"],
        "directors": ["name", "surname"],
        "filmdirectors": ["film_id", "director_id"],
        "actors": ["name", "surname"],
        "filmactors": ["film_id", "actor_id"],
        "filmgrades": ["film_id", "user_id", "grade"],
        "favoritefilms": ["film_id", "user_id"]
    }

    if st.button("Загрузить данные"):
        try:
            response = requests.get(f"{BASE_URL}/{selected_table}/", cookies=cookies)
            if response.status_code == 200:
                data = response.json()
                df = pd.DataFrame(data)
                
                # Проверяем количество строк в DataFrame
                if len(df) > 100:
                    # Если строк больше 100, выводим первые 50 и последние 50 строк
                    first_50 = df.head(50)
                    last_50 = df.tail(50)
                    combined_df = pd.concat([first_50, last_50])
                    st.session_state[f"{selected_table}_data"] = combined_df
                else:
                    # Если строк меньше или равно 100, выводим все строки
                    st.session_state[f"{selected_table}_data"] = df
            else:
                st.error("Не удалось загрузить данные таблицы.")
        except Exception as e:
            st.error(f"Ошибка: {e}")

    if f"{selected_table}_data" in st.session_state:
        st.dataframe(st.session_state[f"{selected_table}_data"])
    if selected_table != 'users':
        with st.expander("Добавить запись", expanded=True):
            form_data = {}
            validation_failed = False
            for i in range(0, len(column_mappings_for_user[selected_table])):
                value = st.text_input(
                    f"{column_mappings_for_user[selected_table][i]}",
                    key=f"{selected_table}_add_{i}"
                )
                if not value:
                    validation_failed = True
                form_data[column_mappings_for_db[selected_table][i]] = value

            if st.button("Сохранить запись", key=f"{selected_table}_save_record"):
                if validation_failed:
                    st.error("Все поля формы должны быть заполнены!")
                else:
                    try:
                        response = requests.post(f"{BASE_URL}/{selected_table}/add/", json=form_data, cookies=cookies)
                        if response.status_code == 200:
                            st.success("Запись добавлена!")
                            # st.experimental_rerun()
                        else:
                            st.error(f"Ошибка при добавлении записи: {response.json().get('detail', 'Неизвестная ошибка')}")
                    except Exception as e:
                        st.error(f"Ошибка: {e}")
    else:
        st.warning("В таблицу users нельзя добавить пользователя. Сделайте это через регистрацию")

    if selected_table not in m2m_tables:
        with st.expander("Изменить запись", expanded=True):
            record_id = st.text_input("Введите ID записи для изменения", key=f"{selected_table}_edit_id")
            if st.button("Загрузить запись", key=f"{selected_table}_load_record"):
                if record_id:
                    try:
                        response = requests.get(f"{BASE_URL}/{selected_table}/{record_id}", cookies=cookies)
                        if response.status_code == 200:
                            st.session_state[f"{selected_table}_edit_record"] = response.json()
                        else:
                            st.error(f"Ошибка загрузки записи: {response.json().get('detail', 'Неизвестная ошибка')}")
                    except Exception as e:
                        st.error(f"Ошибка: {e}")
                else:
                    st.error("Все поля формы должны быть заполнены!")

            if f"{selected_table}_edit_record" in st.session_state:
                form_data = st.session_state[f"{selected_table}_edit_record"]
                updated_data = {}
                validation_failed = False 
                for i, key in enumerate(column_mappings_for_user[selected_table]):
                    value = st.text_input(
                        f"Изменить {key}",
                        value=form_data.get(column_mappings_for_db[selected_table][i], ""),
                        key=f"{selected_table}_edit_{i}"
                    )
                    if not value:
                        validation_failed = True 
                    updated_data[column_mappings_for_db[selected_table][i]] = value

                if st.button("Сохранить изменения", key=f"{selected_table}_update_record"):
                    if validation_failed:
                        st.error("Все поля формы должны быть заполнены!")
                    else:
                        send_data = {"id": int(record_id)} | updated_data
                        try:
                            response = requests.put(f"{BASE_URL}/{selected_table}/update/", json=send_data,
                                cookies=cookies)
                            if response.status_code == 200:
                                st.success("Запись успешно обновлена!")
                                # st.experimental_rerun()
                            else:
                                st.error(f"Ошибка при обновлении записи: {response.json().get('detail', 'Неизвестная ошибка')}")
                        except Exception as e:
                            st.error(f"Ошибка: {e}")


        with st.expander("Удалить запись", expanded=True):
            record_id = st.text_input("Введите ID записи для удаления", key=f"{selected_table}_delete_id")
            if st.button("Удалить запись", key=f"{selected_table}_delete_record"):
                if record_id:
                    try:
                        response = requests.delete(f"{BASE_URL}/{selected_table}/del/{record_id}", cookies=cookies)
                        if response.status_code == 200:
                            st.success("Запись удалена!")
                            st.stop()
                        else:
                            st.error(f"Ошибка при удалении записи: {response.json().get('detail', 'Неизвестная ошибка')}")
                    except Exception as e:
                        st.error(f"Ошибка: {e}")
                else:
                    st.error("Все поля формы должны быть заполнены!")
    else:
        with st.expander("Изменить запись", expanded=True):
            record_id1 = st.text_input(f"Введите {column_mappings_for_user[selected_table][0]} для изменения", key=f"{selected_table}_edit_id1")
            record_id2 = st.text_input(f"Введите {column_mappings_for_user[selected_table][1]} для изменения", key=f"{selected_table}_edit_id2")

            if st.button("Загрузить запись", key=f"{selected_table}_load_record"):
                if record_id1 and record_id2:
                    try:
                        response = requests.get(f"{BASE_URL}/{selected_table}/{record_id1}/{record_id2}", cookies=cookies)
                        if response.status_code == 200:
                            st.session_state[f"{selected_table}_edit_record"] = response.json()
                        else:
                            st.error(f"Ошибка загрузки записи: {response.json().get('detail', 'Неизвестная ошибка')}")
                    except Exception as e:
                        st.error(f"Ошибка: {e}")
                else: 
                    st.error("Все поля формы должны быть заполнены!")

            if f"{selected_table}_edit_record" in st.session_state:
                form_data = st.session_state[f"{selected_table}_edit_record"]
                updated_data = {}
                validation_failed = False 
                for i, key in enumerate(column_mappings_for_user[selected_table]):
                    value  = st.text_input(
                        f"Изменить {key}",
                        value=form_data.get(column_mappings_for_db[selected_table][i], ""),
                        key=f"{selected_table}_edit_{i}"
                    )
                    if not value:
                        validation_failed = True 
                    updated_data[column_mappings_for_db[selected_table][i]] = value

                if st.button("Сохранить изменения", key=f"{selected_table}_update_record"):
                    if validation_failed:
                        st.error("Все поля формы должны быть заполнены!")
                    else:
                        send_data = {"id1": int(record_id1), "id2": int(record_id2)} | updated_data
                        try:
                            response = requests.put(f"{BASE_URL}/{selected_table}/update/", json=send_data,
                                cookies=cookies)
                            if response.status_code == 200:
                                st.success("Запись успешно обновлена!")
                                # st.experimental_rerun()
                            else:
                                st.error(f"Ошибка при обновлении записи: {response.json().get('detail', 'Неизвестная ошибка')}")
                        except Exception as e:
                            st.error(f"Ошибка: {e}")


        with st.expander("Удалить запись", expanded=True):
            record_id1 = st.text_input(f"Введите {column_mappings_for_user[selected_table][0]} для удаления", key=f"{selected_table}_delete_id1")
            record_id2 = st.text_input(f"Введите {column_mappings_for_user[selected_table][1]} для удаления", key=f"{selected_table}_delete_id2")

            if st.button("Удалить запись", key=f"{selected_table}_delete_record"):
                if record_id1 and record_id2:
                    try:
                        response = requests.delete(f"{BASE_URL}/{selected_table}/del/{record_id1}/{record_id2}", cookies=cookies)
                        if response.status_code == 200:
                            st.success("Запись удалена!")
                            st.stop()
                        else:
                            st.error(f"Ошибка при удалении записи: {response.json().get('detail', 'Неизвестная ошибка')}")
                    except Exception as e:
                        st.error(f"Ошибка: {e}")
                else:
                    st.error("Все поля формы должны быть заполнены!")


def my_profile():
    st.title("Мой профиль")

    token = get_cookie("users_access_token")
    if not token:
        st.warning("Вы не авторизованы. Пожалуйста, войдите в систему.")
        st.stop()

    cookies = {"users_access_token": f"{token}"}

    try:
        response = requests.get(f"{BASE_URL}/auth/me/", cookies=cookies)
        if response.status_code == 200:
            user_data = response.json()
            is_admin = user_data.pop("is_admin", None)

            st.write("Информация о вашем профиле:")
            for key, value in user_data.items():
                st.text_input(key, value, key=f"profile_{key}", disabled=key == "email")  # email нельзя изменить

            if st.button("Сохранить изменения"):
                updated_data = {key: st.session_state[f"profile_{key}"] for key in user_data.keys()}
                updated_data = updated_data | {"is_admin": is_admin}
                try:
                    update_response = requests.put(f"{BASE_URL}/auth/update_profile/", json=updated_data, cookies=cookies)
                    if update_response.status_code == 200:
                        st.success("Данные успешно обновлены!")
                    else:
                        st.error("Ошибка при обновлении данных.")
                except Exception as e:
                    st.error(f"Ошибка: {e}")
        else:
            st.error("Не удалось загрузить данные профиля.")
    except Exception as e:
        st.error(f"Ошибка: {e}")


if __name__ == "__main__":
    page = st.sidebar.radio(
        "Навигация",
        ["Вход", "Регистрация", "Просмотр таблиц", "Редактирование таблиц", "Мой профиль"],
        index=0,
    )
    st.sidebar.button("Выйти", on_click=lambda: delete_cookie("users_access_token"))

    if page == "Вход":
        login_user()
    elif page == "Регистрация":
        register_user()
    elif page == "Просмотр таблиц":
        show_tables()
    elif page == "Редактирование таблиц":
        edit_tables()
    elif page == "Мой профиль":
        my_profile()

