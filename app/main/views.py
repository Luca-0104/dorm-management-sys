import time
from datetime import datetime

from flask import request, redirect, render_template, url_for
from flask_login import login_required, current_user

from app.main import main
from app.auth.views import get_role_true

# The index page ----------------------------------------------------------------------------------------------
from app.models import User, Student, Guest, Repair, Complain, DormBuilding, DAdmin


@main.route('/', methods=['GET', 'POST'])
def index():
    get_role_true()  # if we are in the index page, we should get ready for getting the role_id
    return render_template("samples/myindex.html")


# Three home pages for three kinds of users ----------------------------------------------------------------------------------------------
@main.route('/home_stu', methods=['GET', 'POST'])
def home_stu():
    """
    The index page for student users, which is the first page shown after login
    (Some basic information)
    """
    stu_number = current_user.stu_wor_id
    stu = Student.query.filter_by(stu_number=stu_number).first()

    return render_template("samples/studentIndex.html", function="index", stu=stu)  # 待核对完善


# Three home pages for three kinds of users ----------------------------------------------------------------------------------------------
@main.route('/home_stu_bill', methods=['GET', 'POST'])
def home_stu_bill():
    return render_template("samples/studentBills.html", function="bills")  # 待核对


# Three home pages for three kinds of users ----------------------------------------------------------------------------------------------
@main.route('/home_stu_complain', methods=['GET', 'POST'])
def home_stu_complain():
    pagenum = int(request.args.get('page', 1))
    stu_num = current_user.stu_wor_id
    stu = Student.query.filter_by(stu_number=stu_num).first()
    stu_id = stu.id
    pagination = Complain.query.filter_by(stu_id=stu_id).paginate(page=pagenum, per_page=5)
    return render_template("samples/studentComplain.html", pagination=pagination, enterType='home',
                           function="complain")  # 待核对


# Three home pages for three kinds of users ----------------------------------------------------------------------------------------------
@main.route('/home_stu_repair', methods=['GET', 'POST'])
def home_stu_repair():
    pagenum = int(request.args.get('page', 1))
    stu_num = current_user.stu_wor_id
    stu = Student.query.filter_by(stu_number=stu_num).first()
    stu_id = stu.id
    pagination = Repair.query.filter_by(stu_id=stu_id).paginate(page=pagenum, per_page=5)
    return render_template("samples/studentRepair.html", pagination=pagination, enterType='home',
                           function="repair")  # 待核对


# Three home pages for three kinds of users ----------------------------------------------------------------------------------------------
@main.route('/home_stu_message', methods=['GET', 'POST'])
def home_stu_message():
    return render_template("samples/studentMessage.html", function="message")  # 待核对


@main.route('/home_dorm_admin_index', methods=['GET', 'POST'])
def home_dorm_admin_index():
        return render_template('samples/dormIndex.html',function="index")


@main.route('/home_dorm_admin', methods=['GET', 'POST'])
def home_dorm_admin():
    isSuccessful = request.args.get('isSuccessful', "True")
    pagenum = int(request.args.get('page', 1))
    pagination = Student.query.filter_by(is_deleted=False).paginate(page=pagenum, per_page=5)
    return render_template('samples/dormStudents.html', pagination=pagination, enterType='home',
                           isSuccessful=isSuccessful, function='students')


@main.route('/home_dorm_admin_gue', methods=['GET', 'POST'])
def home_dorm_admin_gue():
    isSuccessful = request.args.get('isSuccessful', "True")
    pagenum = int(request.args.get('page', 1))
    pagination = Guest.query.filter_by(is_deleted=False).paginate(page=pagenum, per_page=5)
    return render_template('samples/dormGuests.html', pagination=pagination, enterType='home',
                           isSuccessful=isSuccessful, function="guests")


@main.route('/home_dorm_admin_message', methods=['GET', 'POST'])
def home_dorm_admin_message():
    return render_template('samples/dormMessage.html', function="message")


@main.route('/home_da_index', methods=['GET', 'POST'])
def home_da_index():
    """
    A function for showing the data graphs in the initial page of dorm administrator
    Only the data about the building that this dorm administrator takes charge of
    (The index function of dorm administrators)
    """
    # work_num = current_user.stu_wor_id
    # da = DAdmin.query.filter_by(da_number=work_num).first()
    # building = da.building
    #
    # da_list = building.dormAdmins
    # stu_list = building.students
    # gue_list = []
    # for stu in stu_list:
    #     gues = stu.guests
    #     for gue in gues:
    #         if gue not in gue_list:
    #             gue_list.append(gue)
    #
    # # ******************** for graph 1 ********************
    # repair_list = []
    # complain_list = []
    # notification_list = []
    #
    # for stu in stu_list:
    #     repairs = stu.repairs
    #     for repair in repairs:
    #         if repair not in repair_list:
    #             repair_list.append(repair)
    #
    # for stu in stu_list:
    #     complains = stu.complains
    #     for complain in complains:
    #         if complain not in complain_list:
    #             complain_list.append(complain)
    #
    # for da in da_list:
    #     notifications = da.notifications
    #     for n in notifications:
    #         if n not in notification_list:
    #             notification_list.append(n)
    #
    # mes_num = len(repair_list) + len(complain_list) + len(notification_list)
    #
    # # a dict stores the number of students, guests and messages of this building
    # basic_number_dict = {'stu_num': len(stu_list), 'gue_num': len(gue_list), 'mes_num': mes_num}
    #
    # # ******************** for graph 2 ********************
    # floor1 = 0
    # floor2 = 0
    # floor3 = 0
    # floor4 = 0
    # floor5 = 0
    # floor6 = 0
    # for stu in stu_list:
    #     floor = stu.room_number / 100
    #     if floor == 1:
    #         floor1 += 1
    #     elif floor == 2:
    #         floor2 += 1
    #     elif floor == 3:
    #         floor3 += 1
    #     elif floor == 4:
    #         floor4 += 1
    #     elif floor == 5:
    #         floor5 += 1
    #     elif floor == 6:
    #         floor6 += 1
    #
    # # a list of number of students in each floor
    # floor_stu_num_list = [floor1, floor2, floor3, floor4, floor5, floor6]
    #
    # # ******************** for graph 3 ********************
    # bdic = 0
    # fhss = 0
    # fit = 0
    # fmm = 0
    # fuc = 0
    # fs = 0
    # fels = 0
    # cem = 0
    # cad = 0
    # fhc = 0
    #
    # for stu in stu_list:
    #     if stu.college == 'Beijing Dublin International College':
    #         bdic += 1
    #     elif stu.college == 'Faculty of Humanities and Social Sciences':
    #         fhss += 1
    #     elif stu.college == 'Faculty of Information Technology':
    #         fit += 1
    #     elif stu.college == 'Faculty of Materials and Manufacturing':
    #         fmm += 1
    #     elif stu.college == 'Faculty of Urban Construction':
    #         fuc += 1
    #     elif stu.college == 'Faculty of Science':
    #         fs += 1
    #     elif stu.college == 'Faculty of Environment and Life Sciences':
    #         fels += 1
    #     elif stu.college == 'College of Economic and Management':
    #         cem += 1
    #     elif stu.college == 'College of Art and Design':
    #         cad += 1
    #     elif stu.college == 'FanGongXiu Honors College':
    #         fhc += 1
    #
    # # a dict for storing the number of students of each college in this building
    # college_dict = {'BDIC': bdic, 'FHSS': fhss, 'FIT': fit, 'FMM': fmm, 'FUC': fuc, 'FS': fs, 'FELS': fels,
    #                 'CEM': cem, 'CAD': cad, 'FHC': fhc}
    #
    # # ******************** for graph 4 ********************
    # year_now = time.localtime().tm_year % 1000 % 100  # for today, year_now should be 21
    # month_now = time.localtime().tm_mon  # for today, month_now should be 5
    #
    # stage1 = 0
    # stage2 = 0
    # stage3 = 0
    # stage4 = 0
    #
    # for stu in stu_list:
    #     stu_number = stu.stu_number
    #     year = int(stu_number[0:2])
    #
    #     if 9 <= month_now <= 12:  # the first semester of the year
    #         diff = year_now - year
    #         if diff == 0:
    #             stage1 += 1
    #         elif diff == 1:
    #             stage2 += 1
    #         elif diff == 2:
    #             stage3 += 1
    #         elif diff == 3:
    #             stage4 += 1
    #
    #     else:  # the second semester of the year
    #         diff = year_now - year
    #         if diff == 1:
    #             stage1 += 1
    #         elif diff == 2:
    #             stage2 += 1
    #         elif diff == 3:
    #             stage3 += 1
    #         elif diff == 4:
    #             stage4 += 1
    #
    # # a list stores the numbers of students in different stage, ordered from stage1 to stage4
    # stage_list = [stage1, stage2, stage3, stage4]
    #
    # # ******************** for graph 5 ********************
    # gue1 = 0
    # gue2 = 0
    # gue3 = 0
    # gue4 = 0
    # gue5 = 0
    # gue6 = 0
    # gue7 = 0
    #
    # for gue in gue_list:
    #     if (datetime.utcnow() - gue.arrive_time).days == 0:
    #         gue1 += 1
    #     elif (datetime.utcnow() - gue.arrive_time).days == 1:
    #         gue2 += 1
    #     elif (datetime.utcnow() - gue.arrive_time).days == 2:
    #         gue3 += 1
    #     elif (datetime.utcnow() - gue.arrive_time).days == 3:
    #         gue4 += 1
    #     elif (datetime.utcnow() - gue.arrive_time).days == 4:
    #         gue5 += 1
    #     elif (datetime.utcnow() - gue.arrive_time).days == 5:
    #         gue6 += 1
    #     elif (datetime.utcnow() - gue.arrive_time).days == 6:
    #         gue7 += 1
    #
    # # a list stores the numbers of guests in this building in last 7 days, numbers are ordered from today to 7 days ago
    # gue_num_list = [gue1, gue2, gue3, gue4, gue5, gue6, gue7]

    return render_template("samples/systemIndex.html", function="index",    # 模板名待核对
                           # basic_number_dict=basic_number_dict,     # graph1
                           # floor_stu_num_list=floor_stu_num_list,   # graph2
                           # college_dict=college_dict,               # graph3
                           # stage_list=stage_list,                   # graph4
                           # gue_num_list=gue_num_list                # graph5
                           )  # 待核对完善


@main.route('/home_sys_admin', methods=['GET', 'POST'])
def home_sys_admin():
    """
    A function for showing the data graphs in the initial page of system administrator
    (The index function of system administrators)
    """
    building_id = request.args.get('building_id',0)
    #
    # # building_id == 0 means this is the initial login status (before selecting a specific dorm building),
    # # which will show the information of all the dorm buildings
    # if building_id == 0:
    #     stu_list = Student.query.all()
    #     da_list = DAdmin.query.all()
    #     gue_list = Guest.query.all()
    # else:
    #     building = DormBuilding.query.filter_by(id=building_id).first()
    #     stu_list = building.students
    #     da_list = building.dormAdmins
    #     gue_list = []
    #     for stu in stu_list:
    #         gues = stu.guests
    #         for gue in gues:
    #             if gue not in gue_list:
    #                 gue_list.append(gue)
    #
    #
    # # ******************** for graph 1 ********************
    # # a dict stores the number of students, dorm administrators and guests
    # basic_number_dict = {'stu_num': len(stu_list), 'da_num': len(da_list), 'gue_num': len(gue_list)}
    #
    # # ******************** for graph 2 ********************
    # floor1 = 0
    # floor2 = 0
    # floor3 = 0
    # floor4 = 0
    # floor5 = 0
    # floor6 = 0
    # for stu in stu_list:
    #     floor = stu.room_number / 100
    #     if floor == 1:
    #         floor1 += 1
    #     elif floor == 2:
    #         floor2 += 1
    #     elif floor == 3:
    #         floor3 += 1
    #     elif floor == 4:
    #         floor4 += 1
    #     elif floor == 5:
    #         floor5 += 1
    #     elif floor == 6:
    #         floor6 += 1
    #
    # # a list of number of students in each floor
    # floor_stu_num_list = [floor1, floor2, floor3, floor4, floor5, floor6]
    #
    # # ******************** for graph 3 ********************
    # bdic = 0
    # fhss = 0
    # fit = 0
    # fmm = 0
    # fuc = 0
    # fs = 0
    # fels = 0
    # cem = 0
    # cad = 0
    # fhc = 0
    #
    # for stu in stu_list:
    #     if stu.college == 'Beijing Dublin International College':
    #         bdic += 1
    #     elif stu.college == 'Faculty of Humanities and Social Sciences':
    #         fhss += 1
    #     elif stu.college == 'Faculty of Information Technology':
    #         fit += 1
    #     elif stu.college == 'Faculty of Materials and Manufacturing':
    #         fmm += 1
    #     elif stu.college == 'Faculty of Urban Construction':
    #         fuc += 1
    #     elif stu.college == 'Faculty of Science':
    #         fs += 1
    #     elif stu.college == 'Faculty of Environment and Life Sciences':
    #         fels += 1
    #     elif stu.college == 'College of Economic and Management':
    #         cem += 1
    #     elif stu.college == 'College of Art and Design':
    #         cad += 1
    #     elif stu.college == 'FanGongXiu Honors College':
    #         fhc += 1
    #
    # # a dict for storing the number of students of each college in this building
    # college_dict = {'BDIC': bdic, 'FHSS': fhss, 'FIT': fit, 'FMM': fmm, 'FUC': fuc, 'FS': fs, 'FELS': fels, 'CEM': cem, 'CAD': cad, 'FHC': fhc}
    #
    # # ******************** for graph 4 ********************
    # year_now = time.localtime().tm_year % 1000 % 100    # for today, year_now should be 21
    # month_now = time.localtime().tm_mon                 # for today, month_now should be 5
    #
    # stage1 = 0
    # stage2 = 0
    # stage3 = 0
    # stage4 = 0
    #
    # for stu in stu_list:
    #     stu_number = stu.stu_number
    #     year = int(stu_number[0:2])
    #
    #     if 9 <= month_now <= 12:    # the first semester of the year
    #         diff = year_now - year
    #         if diff == 0:
    #             stage1 += 1
    #         elif diff == 1:
    #             stage2 += 1
    #         elif diff == 2:
    #             stage3 += 1
    #         elif diff == 3:
    #             stage4 += 1
    #
    #     else:                       # the second semester of the year
    #         diff = year_now - year
    #         if diff == 1:
    #             stage1 += 1
    #         elif diff == 2:
    #             stage2 += 1
    #         elif diff == 3:
    #             stage3 += 1
    #         elif diff == 4:
    #             stage4 += 1
    #
    # # a list stores the numbers of students in different stage, ordered from stage1 to stage4
    # stage_list = [stage1, stage2, stage3, stage4]
    #
    # # ******************** for graph 5 ********************
    # gue1 = 0
    # gue2 = 0
    # gue3 = 0
    # gue4 = 0
    # gue5 = 0
    # gue6 = 0
    # gue7 = 0
    #
    # for gue in gue_list:
    #     if (datetime.utcnow() - gue.arrive_time).days == 0:
    #         gue1 += 1
    #     elif (datetime.utcnow() - gue.arrive_time).days == 1:
    #         gue2 += 1
    #     elif (datetime.utcnow() - gue.arrive_time).days == 2:
    #         gue3 += 1
    #     elif (datetime.utcnow() - gue.arrive_time).days == 3:
    #         gue4 += 1
    #     elif (datetime.utcnow() - gue.arrive_time).days == 4:
    #         gue5 += 1
    #     elif (datetime.utcnow() - gue.arrive_time).days == 5:
    #         gue6 += 1
    #     elif (datetime.utcnow() - gue.arrive_time).days == 6:
    #         gue7 += 1
    #
    # # a list stores the numbers of guests in this building in last 7 days, numbers are ordered from today to 7 days ago
    # gue_num_list = [gue1, gue2, gue3, gue4, gue5, gue6, gue7]


    return render_template("samples/systemIndex.html", function="index",building_id=building_id
                           # basic_number_dict=basic_number_dict,     # graph1
                           # floor_stu_num_list=floor_stu_num_list,   # graph2
                           # college_dict=college_dict,               # graph3
                           # stage_list=stage_list,                   # graph4
                           # gue_num_list=gue_num_list                # graph5
                           )  # 待核对完善


@main.route('/home_sys_gue', methods=['GET', 'POST'])
def home_sys_gue():
    building_id = request.args.get('building_id',0)
    return render_template("samples/systemGuests.html", function="guests", building_id=building_id)  # 待核对完善


@main.route('/home_sys_stu', methods=['GET', 'POST'])
def home_sys_stu():
    building_id = request.args.get('building_id',0)
    return render_template("samples/systemStudents.html", function="students",building_id=building_id)  # 待核对完善


@main.route('/home_sys_dorm', methods=['GET', 'POST'])
def home_sys_dorm():
    return render_template("samples/systemDorm.html", function="dormAdmin")  # 待核对完善


# The profile page ----------------------------------------------------------------------------------------------
@main.route('/user/<username>')
def user_profile(username):
    u = User.query.filter_by(user_name=username).first_or_404()
    if u.role_id == 1:
        stu = Student.query.filter_by(stu_number=u.stu_wor_id).first()
        return render_template('student.html', user=u, student=stu)  # 待核对完善
    elif u.role_id == 2:
        return render_template('dormAdmin.html', user=u)  # 待核对完善
    elif u.role_id == 3:
        return render_template('sysAdmin.html', user=u)  # 待核对完善


@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    user_name = current_user.user_name
    stu_wor_id = current_user.stu_wor_id
    phone = current_user.phone
    email = current_user.email
    member_since = current_user.member_since

    role_id = current_user.role_id

    if request.method == 'POST':
        # 待核对完善

        if role_id == 1:
            pass
        elif role_id == 2:
            pass
        elif role_id == 3:
            pass

        user_name = request.form.get('user_name')
        stu_wor_id = request.form.get('stu_wor_id')
        phone = request.form.get('phone')
        email = request.form.get('email')
        about_me = request.form.get('about_me')
        college = request.form.get('college')
        building_id = request.form.get('building_id')
        room_number = request.form.get('room_number')

        user = User.query.filter_by(stu_wor_id=stu_wor_id).first()
        according_stu = Student.query.filter_by(stu_number=stu_wor_id).first()

        # 待补全
        user.user_name = user_name

    return render_template('.html', user_name=user_name, stu_wor_id=stu_wor_id, phone=phone, email=email,
                           member_since=member_since)  # 待核对完善

# -------------------以下部分应该后面写到student蓝本和dormAdmin蓝本中----------------------

# @main.route("/home_stu_message/repair")
# def message_repair():
#     return render_template("samples/messageRepair.html", function="message")

#
# @main.route("/home_stu_message/complain")
# def message_complain():
#     return render_template("samples/messageComplain.html", function="message")
#
#
# @main.route("/home_stu_message/notification")
# def message_notification():
#     return render_template("samples/messageNotification.html", function="message")
#
#
# @main.route("/home_stu_message/others")
# def message_others():
#     return render_template("samples/messageOthers.html", function="message")
#
#
# @main.route("/home_stu_message/details")
# def message_details():
#     return render_template("samples/Message.html", function="message")
