import public_method as public_method
import configDB as Mysql_Db
import public_method as public_method
v4_sqlMapper=Mysql_Db.Mysql('DATABASE_2')
v5_sqlMapper=Mysql_Db.Mysql('DATABASE_1')
newId=1
id=0
new_database='aaa'
old_database='bbb'
#v5_sqlMapper.delete("delete from data_conversion_info")
#v5_sqlMapper.dispose()
public_method.insert_conversion(str(newId), str(id), 'public_web_config', 'webconfig', new_database, old_database,v5_sqlMapper)