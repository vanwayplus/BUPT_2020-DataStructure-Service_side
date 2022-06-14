


def super_get_logs():
    pass


def get_logs(username):
    File = open("log.txt", "r", encoding="utf-8")
    raw = File.readlines()
    logs = []
    for line in raw:
        user = line.split(" ")[0]
        if user == username:
            logs.append(line.split("\n")[0])
    return logs


def login_log(username, time_cur):
    File = open("log.txt", "a", encoding="utf-8")
    File.write(username + " " + time_cur + " " + "登陆了系统\n")
    File.close()


def board_log(username, time_cur):
    File = open("log.txt", "a", encoding="utf-8")
    File.write(username + " " + time_cur + " " + "查看了课程表\n")
    File.close()


def create_activity_log_success(username, time_cur, actname):
    File = open("log.txt", "a", encoding="utf-8")
    File.write(username + " " + time_cur + " " + "创建活动" + ": " + actname + "成功！\n")
    File.close()


def create_activity_log_fail(username, time_cur, actname):
    File = open("log.txt", "a", encoding="utf-8")
    File.write(username + " " + time_cur + " " + "创建活动" + ": " + actname + "失败！\n")
    File.close()


def upload_homework_log_success(username, time_cur, course, homework):
    File = open("log.txt", "a", encoding="utf-8")
    File.write(username + " " + time_cur + " " + "提交了课程：" + course + "的作业: " + homework + "成功！\n")
    File.close()


def upload_homework_log_fail(username, time_cur, course, homework):
    File = open("log.txt", "a", encoding="utf-8")
    File.write(username + " " + time_cur + " " + "提交了课程：" + course + "的作业: " + homework + "失败！\n")
    File.close()


def update_resource_log_success(username, time_cur, course, resources):
    File = open("log.txt", "a", encoding="utf-8")
    File.write(username + " " + time_cur + " " + "更新了课程：" + course + "的资料: " + resources + "成功！\n")
    File.close()


def update_resource_log_fail(username, time_cur, course, resources):
    File = open("log.txt", "a", encoding="utf-8")
    File.write(username + " " + time_cur + " " + "更新了课程：" + course + "的资料: " + resources + "失败！\n")
    File.close()
