from main import web_app as app
from main import db, config, basedir, permission_manager
from flask import session, request, send_file, send_from_directory
from utils import *
from models import *
from sqlalchemy.sql.expression import *
from common.permission import require_permission
from common.utils import unpack_argument, make_json_response
from typing import List
@app.route("/api/test", methods=["POST"])
@unpack_argument
def test(qwq: int):
    return f"qwqwqwq: {qwq}"


@app.route("/api/admin/show", methods=["POST"])
@require_permission(manager=permission_manager, permission="backend.manage")
def admin_show():
    """
    获取后台信息
    """
    result = {
        "problemCount": db.session.query(Problem).count(),
        "publicProblemCount": db.session.query(Problem).filter(Problem.public == True).count(),
        "submissionCount": db.session.query(Submission).count(),
        "userCount": db.session.query(User).count(),
        "discussionCount": db.session.query(Discussion).count(),
        "acceptedSubmissionCount": db.session.query(Submission).filter(Submission.status == "accepted").count(),
        # "unAuthorizedCount": db.session.query(User).filter(User.auth_token != "").count(),
        "settings": []
    }
    settings = result["settings"]
    for k, v in config.VISIBLE_SETTINGS.items():
        settings.append({
            "key": k,
            "value": getattr(config, k),
            "description": v
        })

    return make_response(0, data=result)


@app.route("/api/admin/rating/remove", methods=["POST"])
@require_permission(permission_manager, permission="backend.manage")
@unpack_argument
def admin_rated_contest_remove(contestID: int):
    """
    删除一场比赛及其之后比赛的rating造成的影响
    {
        "contestID":比赛ID
    }
    """
    from typing import List, Tuple
    contest = Contest.by_id(contestID)

    def drop_contest(contest_id):
        print(f"Droping {contest_id}")
        users: List[Tuple[int]] = db.session.query(Submission.uid).filter(
            Submission.contest_id == contest_id).distinct().all()
        for x in users:
            user: User = User.by_id(x.uid)
            user.rating_history = [
                x for x in user.rating_history.copy() if x["contest_id"] != contest_id]
            user.rating = user.get_rating()
        current_contest: Contest = Contest.by_id(contest_id)
        current_contest.rated = False
        current_contest.rated_time = None
    contests = db.session.query(Contest.id).filter(Contest.rated == True).filter(
        Contest.rated_time >= contest.rated_time).all()
    for x in contests:
        drop_contest(x.id)
    db.session.commit()
    return make_response(0, message="完成")


@app.route("/api/admin/rating/rated_contests", methods=["POST"])
@require_permission(permission_manager, permission="backend.manage")
def admin_rated_contests():
    """ 
    获取rated比赛列表

    [
        {
            "ratedTime":"rated应用时间",
            "contestID":"比赛ID",
            "contestName":"比赛名",
            "contestantCount":"参赛人数"
        }
    ]
    """
    user: User = User.by_id(session.get("uid"))
    query = db.session.query(Contest.id, Contest.name, Contest.rated_time).filter(
        Contest.rated == True).order_by(Contest.rated_time.desc()).all()
    result = [

    ]
    for x in query:
        result.append({
            "ratedTime": x.rated_time,
            "contestID": x.id,
            "contestName": x.name,
            "contestantCount": db.session.query(Submission.uid).filter(Submission.contest_id == x.id).distinct().count()
        })
    return make_response(0, data=result)


@app.route("/api/admin/rating/append", methods=["POST"])
@require_permission(permission_manager, "backend.manage")
@unpack_argument
def admin_rating_append(contestID):
    """
    应用某场比赛的rating
    {
        "contestID":"比赛ID"
    }
    {
        "code","message"
    }
    """
    contest: Contest = Contest.by_id(contestID)
    if not contest:
        return make_response(-1, message="比赛ID不存在")
    if contest.rated:
        return make_response(-1, message="此比赛已rated！")
    if contest.running():
        return make_response(-1, message="比赛还在进行!")
    from routes import get_contest_rank_list
    from cf_rating import Contestant, calculate_rating
    from typing import List
    ranklist = get_contest_rank_list(contest)
    if len(ranklist["ranklist"]) <= 1:
        return make_response(-1, message="至少有2人参加的比赛才可以应用rating")
    contestants = []
    for i, item in enumerate(ranklist["ranklist"]):
        contestants.append(Contestant(
            identifier=item["uid"],
            before_rating=db.session.query(User.rating).filter(
                User.id == item["uid"]).one().rating,
            rank=i+1
        ))
    print(contestants)
    rating_result: List[Contestant] = calculate_rating(contestants)
    print(rating_result)
    for x in rating_result:
        current_user: User = User.by_id(x.identifier)
        old = current_user.rating_history.copy()
        old.append({
            "result": x.after_rating-x.before_rating,
            "contest_id": contest.id
        })
        current_user.rating_history = old
        current_user.rating = current_user.get_rating()
    contest.rated = True
    from datetime import datetime
    contest.rated_time = datetime.now()
    db.session.commit()

    return make_response(0, message="完成")


@app.route("/api/admin/rating/permission_groups/get", methods=["POST"])
def admin_get_permission_groups():
    """
    {
        "code":"",
        "result":[
            {
                "id":"权限组ID",
                "name":"权限组名",
                "permissions":"权限列表(字符串)",
                "inherit":"继承自"
            }
        ]
    }
    """
    result = [

    ]
    for item in db.session.query(PermissionGroup).all():
        result.append({
            "id": item.id,
            "name": item.name,
            "permissions": "\n".join(item.permissions),
            "inherit": item.inherit
        })
    return make_response(0, result=result)


@app.route("/api/admin/rating/permission_groups/update", methods=["POST"])
@unpack_argument
@require_permission(manager=permission_manager, permission="permission.manage")
def admin_update_permission_groups(groups: list):
    """
    [
        {
            "id","name","permissions":"xxx","inherit":""
        }
    ]

    {
        "code":"",
        "message":""
    }
    """

    permission_groups = {current["id"]: {"id": current["id"],
                                         "name": current["name"],
                                         "permissions": current["permissions"].split("\n"),
                                         "inherit": current["inherit"]}
                         for current in groups}
    if "admin" not in permission_groups or "default" not in permission_groups:
        return make_response(-1, message="必须存在 admin 组和 default 组")

    def lookup_circles(current: str, path: list):
        path.append(current)
        if permission_groups[current].get("visited", False):
            return True
        permission_groups[current]["visited"] = True
        if permission_groups[current]["inherit"]:
            if lookup_circles(permission_groups[current]["inherit"], path):
                return True
        return False

    def clear_visited_marks():
        for val in permission_groups.values():
            val["visited"] = False
    for val in permission_groups.values():
        if val["inherit"] and val["inherit"] not in permission_groups:
            return make_response(-1, message="权限组 {} 的父权限组 {} 不存在".format(val["id"], val["inherit"]))
        path = []
        clear_visited_marks()
        if lookup_circles(val["id"], path):
            return make_response(-1, message="存在环形继承: {}".format(path))
    db.session.query(PermissionGroup).delete()
    # for x in groups:
    # print(type(db.session))
    db.session.add_all((PermissionGroup(
        id=x["id"], name=x["name"], permissions=x["permissions"].split("\n"), inherit=x["inherit"]) for x in groups))

    db.session.commit()
    from main import redis_connection_pool
    from redis import Redis
    Redis(connection_pool=redis_connection_pool).flushdb()
    return make_response(0, message="更新成功")


@app.route("/api/admin/get_user_permissions", methods=["POST"])
@unpack_argument
@require_permission(manager=permission_manager, permission="permission.manage")
def admin_get_user_permissions():
    """
    获取所有有个人权限的用户
    List[datatypes.admin.UserPermission]
    """
    from common.datatypes.admin import UserPermission
    result: List[UserPermission] = []
    for user in db.session.query(User.id, User.username, User.permissions).filter(User.permissions != []).all():
        result.append(UserPermission(
            uid=user.id,
            username=user.username,
            permissions=user.permissions
        ))
    return make_json_response(0, data=result)


@app.route("/api/admin/remove_user_permission", methods=["POST"])
@unpack_argument
@require_permission(manager=permission_manager, permission="permission.manage")
def admin_remove_user_permission(uid: int, index: int):
    """
    删除某用户的某条个人权限
    """
    user: User = db.session.query(
        User).filter(User.id == uid).one()
    current_permissions = user.permissions
    user.permissions = [x for i, x in enumerate(
        current_permissions) if i != index]
    db.session.commit()
    permission_manager.refresh_user(user.id)
    return make_json_response(0, message="删除成功")


@app.route("/api/admin/add_user_permission", methods=["POST"])
@unpack_argument
@require_permission(manager=permission_manager, permission="permission.manage")
def admin_add_user_permission(uid: int, permission: str):
    """
    给用户添加个人权限
    """
    user: User = db.session.query(
        User).filter(User.id == uid).one()
    current_permissions = user.permissions
    user.permissions = [*current_permissions, permission]
    db.session.commit()
    permission_manager.refresh_user(user.id)
    return make_json_response(0, message="保存成功")
