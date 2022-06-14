def set_bell(user, time, date, mode):
    with open("bell.txt", "a", encoding="utf-8") as f:
        f.write(user + ' ' + time + ' ' + date + ' ' + mode+ "\n")
        f.close()


def get_bell(user, cur_date, cur_time):
    with open("bell.txt", "r", encoding="utf-8") as f:
        bells_raw = f.readlines()
        bells = []
        date_c = ' '+cur_date+' '
        for i in range(len(bells_raw)):
            if "\n" in bells_raw[i]:
                bells_raw[i] = bells_raw[i].split("\n")[0]
        for bell in bells_raw:
            if user in bell and date_c in bell and cur_time in bell:
                print(bells_raw)
                return 1
        f.close()

    return 0


if __name__ == "__main__":
    set_bell("2020211101", "12:30", "1", "daily")
    get_bell("2020211101", "1", "12:30")

"""        if mode == 'weekly':
            f.write(user + ' ' + time + ' ' + mode)
        elif mode == 'daily':
            f.write(user + ' ' + time + ' ' + mode)"""
