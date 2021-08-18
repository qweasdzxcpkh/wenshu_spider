from mongo_util import MyMongoDB
import tablib

mapping = {
    "s1": "案件名称",
    "s2": "法院名称",
    "s3": "审理法院",
    "s4": "法院层级",
    "s5": "文书ID",
    "s6": "文书类型",
    "s7": "案号",
    "s8": "案件类型",
    "s9": "审判程序",
    "s10": "审判程序",
    "s11": "案由",
    "s12": "案由",
    "s13": "案由",
    "s14": "案由",
    "s15": "案由",
    "s16": "案由",
    "s17": "当事人",
    "s18": "审判人员",
    "s19": "律师",
    "s20": "律所",
    "s21": "全文",
    "s22": "首部",
    "s23": "诉讼记录",
    "s24": "诉控辩",
    "s25": "事实",
    "s26": "理由",
    "s27": "判决结果",
    "s28": "尾部",
    "s29": "法律依据",
    "s30": "",
    "s31": "裁判日期",
    "s32": "不公开理由",
    "s33": "法院省份",
    "s34": "法院地市",
    "s35": "法院区县",
    "s36": "审理法院",
    "s37": "审理法院",
    "s38": "审理法院",
    "s39": "审理法院",
    "s40": "审理法院",
    "s41": "发布日期",
    "s42": "裁判年份",
    "s43": "公开类型",
    "s44": "案例等级",
    "s45": "关键字",
    "s46": "结案方式",
    "s47": "法律依据",
    "s48": "上网时间",
    "s49": "案例等级排序",
    "s50": "法院层级排序",
    "s51": "裁判日期排序",
    "s52": "审判程序排序",
    "s53": "当事人段",
    "s54": "其他",
    "cprqStart": "裁判日期开始时间",
    "cprqEnd": "裁判日期结束时间",
    "swsjStart": "上网时间开始时间",
    "swsjEnd": "上网时间结束时间",
    "flyj": "法律依据",
    "cprq": "裁判日期"
}


mongo = MyMongoDB()
data = tablib.Dataset()
data.headers = mapping.keys()
data.append(mapping.values())

for doc in mongo.fetch():
    row = []
    for k in mapping.keys():
        if k in doc:
            row.append(doc[k])
        else:
            row.append('')
    data.append(row)
with open('data.xlsx', 'wb') as f:
    f.write(data.export('xlsx'))
