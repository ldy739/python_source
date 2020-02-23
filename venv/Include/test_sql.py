# coding:utf-8
import configDB as Mysql_Db
import public_method as public_method
import time,datetime

v5_sqlMapper=Mysql_Db.Mysql('DATABASE_1')
print (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
#数据清空操作
del_webList = v5_sqlMapper.get_all("select new_id from data_conversion_info where new_table='public_web_config'")
print(del_webList)
if del_webList:
    for web_num in range(len(del_webList)):
        del_webId = del_webList[web_num][0]
        # 清除站点数据
        v5_sqlMapper.delete(
            "delete from public_web_config where id=" + str(del_webId)
        )
        # 清除站点配置项数据
        v5_sqlMapper.delete(
            "delete from public_configuration_item where web_id=" + str(del_webId)
        )
        # 清除站点模块配置信息数据
        v5_sqlMapper.delete(
            "delete from public_config_mode where web_id=" + str(del_webId)
        )
        # 清除默认留言配置数据
        v5_sqlMapper.delete(
            "delete from basic_leave_message_config where web_id=" + str(del_webId)
        )
        # 清除系统配置信息license_sys
        v5_sqlMapper.delete(
            "delete from public_web_sys where web_id=" + str(del_webId)
        )
        # 清除用户权限数据
        v5_sqlMapper.delete(
            "delete from public_user_role where user_id in(select id from public_user where web_id="
            + str(del_webId)
            + ")"
        )
        # 清除所有站点用户数据
        v5_sqlMapper.delete(
            "delete from public_user  where web_id=" + str(del_webId)
        )
        # 清除所有站点分组数据
        v5_sqlMapper.delete(
            "delete from public_group where web_id=" + str(del_webId)
        )
        # 清除所有角色资源数据
        v5_sqlMapper.delete(
            "delete from public_role_resource where role_id in(select id from public_role where web_id="
            + str(del_webId)
            + ")"
        )
        # 清除所有角色分类数据
        v5_sqlMapper.delete(
            "delete from public_role_classes where role_id in(select id from public_role where web_id="
            + str(del_webId)
            + ")"
        )
        # 清除角色数据
        v5_sqlMapper.delete(
            "delete from public_role where web_id=" + str(del_webId)
        )
    v5_sqlMapper.delete("delete from data_tables_info")
    v5_sqlMapper.delete("delete from data_conversion_info")
    v5_sqlMapper.dispose()
    print("数据已清除！")
else:
    print("无数据待清理！")

