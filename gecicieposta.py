import requests, os, time, colorama
def clear_console():
    os.system("cls" if os.name == "nt" else "clear")
colorama.init(autoreset=True)
def create_temp_email():
    try:
        response = requests.get("https://www.1secmail.com/api/v1/?action=genRandomMailbox&count=1")
        response.raise_for_status()
        return response.json()[0]
    except requests.RequestException as e:
        print(f"{colorama.Fore.RED}E-posta oluşturulurken hata: {e}")
        return None
def check_emails(login, domain):
    try:
        response = requests.get(f"https://www.1secmail.com/api/v1/?action=getMessages&login={login}&domain={domain}")
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"{colorama.Fore.RED}E-postaları kontrol ederken hata: {e}")
        return None
def read_email(login, domain, email_id):
    try:
        response = requests.get(f"https://www.1secmail.com/api/v1/?action=readMessage&login={login}&domain={domain}&id={email_id}")
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"{colorama.Fore.RED}E-posta okunurken hata: {e}")
        return None
def show_help():
    commands = {
        "yardim": "Uygulamanın komutlarını gösterir.",
        "hesapac": "Rastgele E-posta Adresi Oluşturur.",
        "emailkontrol": "Gelen E-postaları Kontrol Eder.",
        "emailoku": "Tek E-posta Mesajını Okur.",
        "temizle": "Ekranı Temizler.",
        "cikis": "Uygulamayı kapatır."
    }
    for command, description in commands.items():
        print(f"{colorama.Fore.RED}{command}: {colorama.Fore.GREEN}{description}")
def main():
    temp_email = None

    while True:
        data = input(os.path.dirname(os.path.abspath(__file__)) + "> ").lower()

        if data == "yardim":
            show_help()
        elif data == "temizle":
            clear_console()
        elif data == "hesapac":
            temp_email = create_temp_email()
            if temp_email:
                print(f"{colorama.Fore.GREEN}Geçici E-posta: {temp_email}")
            else:
                print(f"{colorama.Fore.RED}E-posta oluşturulamadı.")

        elif data == "emailkontrol":
            if temp_email:
                login, domain = temp_email.split('@')
                emails = check_emails(login, domain)
                if emails:
                    print(f"{colorama.Fore.GREEN}Gelen E-postalar:")
                    for email in emails:
                        print(f"ID: {email['id']} - Konu: {email['subject']} - Gönderen: {email['from']}")
                else:
                    print(f"{colorama.Fore.YELLOW}Gelen e-posta bulunamadı.")
            else:
                print(f"{colorama.Fore.RED}Önce bir e-posta adresi oluşturmalısınız!")

        elif data == "emailoku":
            if temp_email:
                login, domain = temp_email.split('@')
                email_id = input("Okunacak e-posta ID'sini girin: ")
                email_details = read_email(login, domain, email_id)
                if email_details:
                    print(f"{colorama.Fore.GREEN}E-posta: {email_details['from']}")
                    print(f"Konusu: {email_details['subject']}")
                    print(f"Tarihi: {email_details['date']}")
                    print(f"Mesaj: {email_details['textBody']}")
                else:
                    print(f"{colorama.Fore.YELLOW}E-posta okunamadı.")
            else:
                print(f"{colorama.Fore.RED}Önce bir e-posta adresi oluşturmalısınız!")

        elif data == "cikis":
            print("Uygulama kapatılıyor...")
            break

        else:
            print(f"{colorama.Fore.RED}Geçersiz komut! 'yardim' yazarak komutları görebilirsin.")

if __name__ == "__main__":
    print("Bu program tmertarin tarafından geliştirilmiştir.")
    main()
