import configDB as Mysql_Db
import public_method as public_method
v4_sqlMapper=Mysql_Db.Mysql('DATABASE_2')
v5_sqlMapper=Mysql_Db.Mysql('DATABASE_1')
# v4数据库名
old_database = v4_sqlMapper.get_one(' select database() ;')
# v5数据库名
new_database = v5_sqlMapper.get_one(' select database() ;')
# 获取v4站点信息数据
v4_webconfig_list = v4_sqlMapper.get_all(
    "select id,REPLACE(UNIX_TIMESTAMP(CURRENT_TIMESTAMP(3)),'.','') as  sys_num,webName,robotNameDetail as info,SYSDATE() as datetime,invokekey from webconfig where id >100 and status=1;")
# 遍历次数纪录
count = 0
# 警告信息
warningInfo = ''
repeat_userName = v4_sqlMapper.get_all(
    "select userName  from robot_user where userName is not null and  userName !='' and del=0 and status=0 group by userName having count(1)>1;")
repeat_telNum = v4_sqlMapper.get_all(
    "select telNum  from robot_user where telNum is not null and  telNum !='' and del=0 and status=0 group by telNum having count(1)>1;")
repeat_email = v4_sqlMapper.get_all(
    "select email from robot_user where email is not null and  email !='' and del=0 and status=0 group by email having count(1)>1;")
try:
    # 遍历v4站点信息
    for web in v4_webconfig_list:
        # 插入数据条数
        insert_count = 0
        count = count + 1
        # 插入v5 public_web_config表数据
        id = web[0]
        sys_num = int(web[1]) + count
        webName = web[2]
        info = web[3]
        datetime = web[4]
        invokekey = web[5]
        # 插入新站点数据sql
        sqls = "INSERT INTO public_web_config(sys_num ,name,  client_name,create_time,invoke_key)VALUES" + \
               "(" + str(sys_num) + ',' + "'" + webName + "'" + ",'" + info + "'" + ",'" + str(
            datetime) + "','" + invokekey + "'" + ");"
        # 执行插入新站点数据
        newId = v5_sqlMapper.insert_id(sqls)
        # 行数据插入信息记录
        v5_sqlMapper.insert(public_method.insert_conversion(newId, id, 'public_web_config', 'webconfig', new_database, old_database))
        sqls = "INSERT INTO public_configuration_item (configuration_id, config_mode, status, web_id) select id,config_mode,if(resource_id is null,0,1)," + str(newId) + " from public_configuration WHERE config_mode = 'channel_type';"
        # 插入站点字典资源数据并记录插入条数
        insert_count = v5_sqlMapper.insert(sqls)
        v5_sqlMapper.insert(public_method.insert_tables('public_configuration_item', '', new_database, old_database, insert_count))

        # 插入站点配置表
        sqls = "INSERT INTO public_config_mode (code, int_value, string_value,type, info, web_id, user_id, user_name, status, date_time, modular,hid,ability,param_info) " + \
               "SELECT code, 1, string_value,type, info, " + str(
            newId) + ", user_id, user_name, status, SYSDATE(), modular,hid,ability,param_info FROM public_config_mode WHERE CODE IN ('switch.question.effextive.roles') AND (web_id = - 1 OR web_id = " + str(
            newId) + ");"
        # insert_count=v5_sqlMapper.insert(sqls)
        # public_method.insert_tables('public_config_mode','',new_database,old_database,insert_count)

        # 插入默认留言配置信息
        sqls = "INSERT INTO basic_leave_message_config (field_name, field_english_name, field_type, field_value, required, enable, initial, web_id, create_user_id, create_time, parentid, display_field_name,is_number,is_english,is_chinese,is_char,max_input,is_query_condition) " + \
               "SELECT  field_name, field_english_name, field_type, field_value, required, enable, initial, " + str(
            newId) + ", -100, create_time, parentid, display_field_name,is_number,is_english,is_chinese,is_char,max_input,is_query_condition FROM basic_leave_message_config  WHERE web_id =-1 AND initial = 1;"
        insert_count = v5_sqlMapper.insert(sqls)
        v5_sqlMapper.insert(public_method.insert_tables('basic_leave_message_config', '', new_database, old_database, insert_count))

        # 添加站点对应系统配置信息license_sys
        sqls = "INSERT INTO public_web_sys (web_id, sys_id)VALUES(" + str(newId) + ",1),(" + str(newId) + ",2),(" + str(
            newId) + ",3);"
        insert_count = v5_sqlMapper.insert(sqls)
        v5_sqlMapper.insert(public_method.insert_tables('public_web_sys', '', new_database, old_database, insert_count))

        # 添加站点答案类型回复形式配置项
        sqls = "INSERT INTO public_configuration_item (configuration_id, config_mode, status, web_id) select id,config_mode,status," + str(
            newId) + " from public_configuration where config_mode in('answer_type','visitor_field','customer_service_type','customer_extract');"
        insert_count = v5_sqlMapper.insert(sqls)
        v5_sqlMapper.insert(public_method.insert_tables('public_configuration_item', '', new_database, old_database, insert_count))

        # 添加默认配置项参数
        sqls = "INSERT INTO public_config_mode (code, int_value, string_value,type, info, web_id, user_id, user_name, status, date_time, modular,hid,ability,param_info)" + \
               "select code, int_value, string_value,type, info, " + str(
            newId) + ", user_id, user_name, status, date_time, modular,hid,ability,param_info from public_config_mode where web_id=-1 and " + \
               "code in('conf.unknown.confirm.ask.mode','conf.wx.count','switch.guess.answer.show.question','switch.question.show.participle', " + \
               "'switch.question.effextive.roles', 'switch.question.effextive.area', 'switch.customer.skill.group', 'switch.third.customer', 'switch.question.multiple.answers', 'conf.support.language', " + \
               "'switch.wx.show.voice.msg', 'switch.exclusive.p.tag', 'conf.adjust.grade.by.word.length', 'conf.lucene.intent.order', 'switch.change.url.to.html', 'conf.improve.later.word.weight', " + \
               "'conf.similar.recommend.score', 'switch.flow.item.to.text', 'switch.robot.guide.unknown', 'conf.vague.direct.answer', 'conf.select.search.word2vec', 'conf.sentence.similar.optimize.guide', " + \
               "'switch.query.wx.nick.name', 'switch.voice.to.text', 'switch.wx.download.media', 'conf.option.more.answer.mode', 'conf.rel.word.py', 'conf.guide.filter.score', 'conf.intent.sureordeny.result'," + \
               "'conf.scene.jump.out.mode', 'conf.language.config.mode', 'conf.scene.intent.identify.ratio', 'conf.unknown.judge.no.match.word'," + \
               "'switch.applet.voice.recognition', 'switch.smart.knowledge', 'conf.search.help.first.spell', 'plant.data.chat');"
        insert_count = v5_sqlMapper.insert(sqls)
        v5_sqlMapper.insert(public_method.insert_tables('public_config_mode', '', new_database, old_database, insert_count))

        # 关闭生效角色的配置
        sqls = "update public_config_mode set status=1 where code='switch.question.effextive.roles' and web_id=" + str(
            newId) + ";"
        v5_sqlMapper.update(sqls)

        # 创建站点用户信息
        sqls = "select id,userName,email,telNum,name from robot_user where webId=" + str(
            id) + " and userName is not null and userName !='' and userLevel=1 and status=0 and del=0"
        webUserList = v4_sqlMapper.get_all(sqls)
        default_passwd = '83e4a1cb50a1633cb3cf2d3a28f760a3'
        for mainUser in webUserList:
            web_uid = mainUser[0]
            web_userName = mainUser[1]
            web_uemail = mainUser[2] if mainUser[2] != None else ''
            web_utelNum = mainUser[3] if mainUser[3] != None else ''
            web_uname = mainUser[4] if mainUser[4] != None else ''
            sqls = "INSERT INTO public_user(name, email,PASSWORD,mobile_phone, remind, create_time, nickname, web_id, type)VALUES(" + \
                   "'" + web_userName + "'," + "if(''='" + web_uemail + "',null,'" + web_uemail + "')," + "'" + default_passwd + "'," + "if(''='" + str(
                web_utelNum) + "',null,'" + str(web_utelNum) + "'),1,sysdate()," + "'" + web_uname + "'," + str(
                newId) + ",1)"
            new_uid = v5_sqlMapper.insert_id(sqls)
            v5_sqlMapper.insert(public_method.insert_conversion(new_uid, web_uid, 'public_user', 'robot_user', new_database, old_database))
            # 站点用户角色添加
            sqls = "INSERT INTO public_user_role(user_id, role_id) VALUES (" + str(new_uid) + ", '-4');"
            insert_count = v5_sqlMapper.insert(sqls)
            # 站点用户添加组织信息
            sqls = "INSERT INTO public_group (name,parent_id,order_id,web_id, del, create_user_id, create_time)VALUES ('默认组织',0,0,'" + str(
                newId) + "',  0," + str(new_uid) + ",SYSDATE()) ;"
            newGropId = v5_sqlMapper.insert_id(sqls)
            # 站点用户添加角色分类信息
            sqls = "INSERT INTO public_role(name, defaulted, create_time, web_id,create_user_id) VALUES('默认角色', 0, SYSDATE(), " + str(
                newId) + "," + str(new_uid) + ") ;"
            newRoleId = v5_sqlMapper.insert_id(sqls)
            # 添加角色资源数据信息
            sqls = "INSERT INTO public_role_resource(role_id, resource_id) select " + str(
                newRoleId) + ",id from public_resource where sys_id=1 " + \
                   "and id not in(16,25,1209,1409,1808,2008,2402,2501,2502,110206,110404,110405,120901,120902,120903,140206,180801,180802,250101,250102,250103,250104,250105,250106," + \
                   "250201,250202,250203,250204,250205,17010101,17010103,17010108,17010109,17010208,17010209,17010301,17010303,17010401,17010403,17010501,17010503,17020101," + \
                   "17030101,17030103,17030201,17030203,18080101,18080102,19030491,24010201,24010202,24010203,24010204,24010237,1205020320);"
            insert_resourceCount = v5_sqlMapper.insert(sqls)
            v5_sqlMapper.insert(public_method.insert_tables('public_role_resource', '', new_database, old_database, insert_resourceCount))
            # 添加角色权限分类信息
            sqls = "INSERT INTO public_role_classes (role_id, classes_id)VALUES (" + str(newRoleId) + ", 0) , (" + str(
                newRoleId) + ", -100) , (" + str(newRoleId) + ", -200) , (" + str(newRoleId) + ", -300);"
            insert_classesCount = v5_sqlMapper.insert(sqls)
            v5_sqlMapper.insert(public_method.insert_tables('public_role_classes', '', new_database, old_database, insert_classesCount))
            # 进行站点子用户操作
            sqls = "select id,userName,email,telNum,name from robot_user where webId=" + str(
                id) + " and userName is not null and userName !='' and userLevel=2 and status=0 and del=0"
            sonUserList = v4_sqlMapper.get_all(sqls)
            for ui in range(len(sonUserList)):
                son_userName_count = 1
                son_uid = sonUserList[ui][0]
                son_userName = sonUserList[ui][1]
                son_uemail = sonUserList[ui][2] if sonUserList[ui][2] != None else ''
                son_utelNum = sonUserList[ui][3] if sonUserList[ui][3] != None else ''
                son_uname = sonUserList[ui][4] if sonUserList[ui][4] != None else ''

                if son_userName == web_userName:
                    continue
                for i in range(len(repeat_userName)):
                    if son_userName == repeat_userName[i][0]:
                        son_userName_count = son_userName_count + 1
                        break
                if son_userName_count > 1:
                    print("用户名已存在！", son_userName)
                    warningInfo = warningInfo + son_userName
                    continue
                for ei in range(len(repeat_email)):
                    if son_uemail == repeat_email[ei][0]:
                        son_uemail = ''
                        print("存在重复邮箱,初始化为null")
                        break
                for ti in range(len(repeat_telNum)):
                    if son_utelNum == repeat_telNum[ti][0]:
                        son_utelNum = ''
                        print("存在重复电话,初始化为null！")
                        break
                    # if(''='',null,2)
                sqls = "INSERT INTO public_user(name, email,PASSWORD,mobile_phone, remind, create_time, nickname, web_id, type,create_user_id)VALUES(" + \
                       "'" + son_userName + "'," + "if(''='" + son_uemail + "',null,'" + son_uemail + "')," + "'" + default_passwd + "'," + "if(''='" + str(
                    son_utelNum) + "',null,'" + str(son_utelNum) + "'),1,sysdate()," + "'" + son_uname + "'," + str(
                    newId) + ",2," + str(new_uid) + ")"
                new_son_uid = v5_sqlMapper.insert_id(sqls)
                v5_sqlMapper.insert(public_method.insert_conversion(new_son_uid, son_uid, 'public_user', 'robot_user', new_database,
                                                old_database))
                # 站点用户角色添加
                sqls = "INSERT INTO public_user_role(user_id, role_id) VALUES (" + str(new_son_uid) + ", " + str(
                    newRoleId) + ");"
                v5_sqlMapper.insert(sqls)

    # 数据表插入记录
    v5_sqlMapper.insert(public_method.insert_tables('public_web_config', 'webconfig', new_database, old_database, count))
    v4_sqlMapper.dispose()
    v5_sqlMapper.dispose()
except BaseException as e:
    print('操作失败！！！', "\n", "BaseException(异常原因):", e)
    # 异常时情况清空已插入数据
    del_webList = v5_sqlMapper.get_all(
        "select new_id from data_conversion_info where new_table='public_web_config'")
    for web_num in range(len(del_webList)):
        del_webId = del_webList[web_num][0]
        # 清除站点数据
        v5_sqlMapper.delete("delete from public_web_config where id=" + str(del_webId))
        # 清除站点配置项数据
        v5_sqlMapper.delete("delete from public_configuration_item where web_id=" + str(del_webId))
        # 清除站点模块配置信息数据
        v5_sqlMapper.delete("delete from public_config_mode where web_id=" + str(del_webId))
        # 清除默认留言配置数据
        v5_sqlMapper.delete("delete from basic_leave_message_config where web_id=" + str(del_webId))
        # 清除系统配置信息license_sys
        v5_sqlMapper.delete("delete from public_web_sys where web_id=" + str(del_webId))
        # 清除用户权限数据
        v5_sqlMapper.delete(
            "delete from public_user_role where user_id in(select id from public_user where web_id=" + str(
                del_webId) + ")")
        # 清除所有站点用户数据
        v5_sqlMapper.delete("delete from public_user  where web_id=" + str(del_webId))
        # 清除所有站点分组数据
        v5_sqlMapper.delete("delete from public_group where web_id=" + str(del_webId))
        # 清除所有角色资源数据
        v5_sqlMapper.delete(
            "delete from public_role_resource where role_id in(select id from public_role where web_id=" + str(
                del_webId) + ")")
        # 清除所有角色分类数据
        v5_sqlMapper.delete(
            "delete from public_role_classes where role_id in(select id from public_role where web_id=" + str(
                del_webId) + ")")
        # 清除角色数据
        v5_sqlMapper.delete("delete from public_role where web_id=" + str(del_webId))
    v5_sqlMapper.delete("delete from data_tables_info")
    v5_sqlMapper.delete("delete from data_conversion_info")
    v5_sqlMapper.dispose()
    print('数据已清除！')
else:
    if warningInfo == '':
        warningInfo = "无"
    print('操作成功！！！警告信息:', warningInfo)


