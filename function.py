###
#Author:Daili
#Github:
from pyquery import PyQuery as pq;
import pymysql;
import math;
def getInfo(url: str):
    ## 用来提取此页有用信息并打包成一个list
    # @url <clss : str>
    # return @infos <class : list>

    doc = pq(url, encoding="utf-8", header={"User-Agent": "Baiduspider+(+http://www.baidu.com/search/spider.htm)"});
    s = doc.find(".search-list-item")
    infos = [];
    for item in s.items():
        info = {};
        item.find(".project-list-item-tags-img span i").remove()
        #title
        info['title'] = item.find(".project-list-item-title").html();
        if(info['title']==None):
            print("")
        else :
            if (len(info['title']) > 50):
                info['title'] = info['title'][:50];
            info['title'] = info['title'].replace("'", "‘").replace('"', "”").replace('\\','\\\\');
        #status
        if(item.find(".project-list-item-status-yes")):
            info['status'] = 'yes';
        else:
            info['status'] = 'no';
        #province
        info['province']=item.find(".project-list-item-tags-text span").eq(1).html();
        #school
        info['school'] = item.find(".project-list-item-tags-text span").eq(0).html();
        #type
        info['type'] = item.find(".project-list-item-tags-text span").eq(2).html();
        #tag
        info['tag']='';
        for t in item.find(".project-list-item-tags-img span").items():
            info['tag']=info['tag']+","+t.html();
        info['tag']=info['tag'].lstrip(',');
        #link
        info['link'] = item.find("a").attr("href");

        infos.append(info);
    return infos;

def insertData(infos:dict,dbconfig:dict):
    ##用来将获取的数据存入Mysql数据库
    # @info <class : dict>
    # @dvconfig <class : dict>
    # return none
    count = 0;
    fail  = 0;
    jump = 0;
    faillist = []
    conn = pymysql.connect(**dbconfig)
    sql = "INSERT INTO `tb_infos` (`title`, `status`, `province`, `school`, `type`, `tag`, `link`) VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}')";
    for info in infos:
        test = "select * from `tb_infos` WHERE link = '{0}'";
        test = test.format(info['link']);
        j = conn.query(test);
        if(j):
            jump+=1;
        else:
            currentSql = sql.format(info['title'],
                                    info['status'],
                                    info['province'],
                                    info['school'],
                                    info['type'],
                                    info['tag'],
                                    info['link']);
            result = conn.query(currentSql);
            if(result):
                count+=1;
            else:
                fail+=1;
                faillist.append(info['title']);
    print("------>跳过",jump,"条数据")
    print("------>成功写入",count,"条记录。\n"+
          "------>写入",fail,"条记录失败。\n\n============================================\n")


def getRange():
    ## 用来获取总页数
    # return range <class : int>
    url = "http://cy.ncss.org.cn/search/projectcount?name=&industryCode=&typeCode=&wasBindUniTechnology=-9&investStageCode=&provinceCode=";
    doc = pq(url, encoding="utf-8", header={"User-Agent": "Baiduspider+(+http://www.baidu.com/search/spider.htm)"});
    range = doc.html();
    range = int(range);
    range = math.ceil(range/100);
    return range;

def dbInit(dbConfig:dict):
    ## 用来初始化数据库
    # return none
    sql1 = "Create Table If Not Exists `{0}`.`{1}`( `id` INT(100) NOT NULL AUTO_INCREMENT , `title` VARCHAR(100) NOT NULL , `status` VARCHAR(4) NOT NULL , `province` VARCHAR(20) NOT NULL , `school` VARCHAR(50) NOT NULL , `type` VARCHAR(50) NOT NULL , `tag` VARCHAR(50) NOT NULL , `link` VARCHAR(100) NOT NULL , PRIMARY KEY (`id`), UNIQUE (`link`)) CHARACTER SET utf8 COLLATE utf8_general_ci;"
    sql1 = sql1.format(dbConfig['db'],"tb_infos")
    conn = pymysql.connect(**dbConfig)
    conn.query(sql1);
    conn.close();
    print("------>数据库初始化完毕\n")
