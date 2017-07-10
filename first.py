from function import insertData;
from function import getInfo;
from function import getRange;
from function import dbInit;
dbconfig = {
'host':'127.0.0.1',#数据库地址
'port':3306,#数据库端口
'user':'root',#数据库用户名
'password':'root',#数据库密码
'charset':"utf8",#数据库连接时所用编码
'db':'spider',#数据库名。
}

dbInit(dbconfig);
print("------>开始获取页数...\n")
ra = getRange();
print("------>页数获取成功目前共",ra,"页\n");
print("------>开始抓取...\n")
for i in range(1238,ra):
    page = i+1;
    print("--->正在抓取第",page,"页<---\n")
    url = "http://cy.ncss.org.cn/search/projectlist?name=&industryCode=&typeCode=&wasBindUniTechnology=-9&" \
          "investStageCode=&provinceCode=&pageIndex={0}&pageSize=100";
    url = url.format(i);
    infos = getInfo(url);
    insertData(infos,dbconfig);

print("------>过程结束，数据已入库！")
