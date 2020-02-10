# 公共条用方法
import Include.configDB as Mysql_Db

v5_sqlMapper = Mysql_Db.Mysql('DATABASE_1')


# 行数据插入信息记录
def insert_conversion(newId, oldId, newTable, oldTable, newDatabases, oldDatabase):
    # 插入记录sql信息
    sqls = "insert into data_conversion_info(new_id,old_id,new_table,old_table,new_database,old_database,datetime)VALUES(" + str(
        newId) + "," + str(
        oldId) + "," + "'" + newTable + "','" + oldTable + "','" + newDatabases + "','" + oldDatabase + "',sysdate());"
    print(sqls)
    # 执行插入数据记录信息
    v5_sqlMapper.insert(sqls)
    v5_sqlMapper.dispose()


# 数据表插入记录
def insert_tables(newTable, oldTable, newDatabases, oldDatabase, recordCount):
    # 记录表操作信息sql
    sqls = "insert into data_tables_info(new_table,old_table,new_database,old_database,extract_count,now_status,datetime)VALUES" \
           "(" + "'" + newTable + "','" + oldTable + "','" + newDatabases + "','" + oldDatabase + "'," + str(recordCount) + ",1,sysdate());"
    v5_sqlMapper.insert(sqls)
    v5_sqlMapper.dispose()

