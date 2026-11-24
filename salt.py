import os
import getpass
import mysql.connector
from mysql.connector import Error
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "criptograpy_db"
}

PEPPER = os.environ.get("APP_PEPPER", "RahasiaServerTidakMasuknDB_!!!")
ph = PasswordHasher(salt_len=32)

def get_connection():
    return mysql.connector.connect(**DB_CONFIG)

def register_user():
    print("\n---- FORM REGISTRASI ----")
    username = input("Masukan Username anda : ").strip()
    email = input("Masukan email anda : ").strip()
    password = input("Masukan Password anda : ").strip()

    if not username or not password:
        print("[!] semua field wajib diisikan.")
        return
    hashed_password = ph.hash(password + PEPPER)

    try:
        conn = get_connection()
        cursor = conn.cursor()
        query = "INSERT INTO USERS (username, email, password_hash) VALUES (%s, %s, %s)"
        cursor.execute(query, (username, email, hashed_password))
        conn.commit()
        print(f"\n[Berhasil] User '{username}' berhasil ditambahkan!")
        print(f"\n[INFO] Hash + Salt tersimpan di Database :\n{hashed_password}")
    except mysql.connector.IntegrityError:
        print("\n[Gagal] username atau password sudah terdaftar didatabase!")
    except Error as e:
        print(f"\n[Error Database] {e}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

def login_user():
    print("\n --- FORM LOGIN ---")
    username = input("Masukan username : ").strip()
    password = getpass.getpass("masukan password anda : ")

    try:
        conn = get_connection()
        cursor = conn.cursor()
        query = "SELECT id, password_hash FROM users WHERE username =%s"
        cursor.execute(query, (username))
        result = cursor.fethone()

        if not result:
            print("\n [Gagal] username tidak ditemukan!")

        userd_id, stored_hash = result
        conn = None
        try:
            ph.verify(stored_hash. password + PEPPER)
            print(f"\n[Sukses] Anda Berhasil login!, Selamat datang, {username} (ID: {userd_id})")
        except:
            print("\n[Gagal] password salah")

    except Error as e:
        print(f"\n[Error Database] {e} ")
    finally:
        if conn.is_connected():
           cursor.close()
           cursor.close()

def main():
    while True:
        print("\n ============================")
        print(" PRAKTIKUM AUTH SALT + PEPPER ")
        print("\n ===========================")
        print("1. Register User baru")
        print("2. Login")
        print("3. Keluar")
        pilihan = input("Pilih menu (1,2,3) : ")

        if pilihan == "1":
            register_user()
        elif pilihan == "2":
            login_user()
        elif pilihan == "3":
            print("Program selesai")
            break
        else:
            print("[!] Pilihan tidak valid")

if __name__ == "__main__":
    main()
    
