import json
import requests
import execjs
import time

from DESUtils import TripleDesUtils
from mongo_util import MyMongoDB

mongo = MyMongoDB()

js_text = """
function cipher() {
    var info = {};
	var date = new Date();
	var timestamp = date.getTime().toString();
	var salt = rand_str(24);
	var year = date.getFullYear().toString();
	var month = (date.getMonth() + 1 < 10 ? "0" + (date.getMonth() + 1) : date.getMonth()).toString();
	var day = (date.getDate() < 10 ? "0" + date.getDate() : date.getDate())
			.toString();
	var iv = year + month + day;
	info["timestamp"] = timestamp
	info["salt"] = salt
	info["iv"] = iv
	return info
	
function rand_str(size){
        var str = "",
        arr = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'];
        for(var i=0; i<size; i++){
            str += arr[Math.round(Math.random() * (arr.length-1))];
        }
        return str;
    }
};

function strTobinary(str) {
	var result = [];
	var list = str.split("");
	for (var i = 0; i < list.length; i++) {
		if (i != 0) {
			result.push(" ");
		}
		var item = list[i];
		var binaryStr = item.charCodeAt().toString(2);
		result.push(binaryStr);
	};
	return result.join("");
}
"""

d_time = time.strptime(time.ctime())
v = str(d_time.tm_year) + str(d_time.tm_mon).zfill(2) + str(d_time.tm_mday)


def list_spider(page, cookie):
    DES3 = TripleDesUtils()
    js_var = execjs.compile(js_text)
    ss = js_var.call('cipher')
    print(ss)
    enc = DES3.encryption(ss['timestamp'], ss['salt'], v)
    print(enc)
    dd_str = ss['salt'] + v + enc
    ciphertext = js_var.call('strTobinary', dd_str)
    # print(ciphertext)
    # 参数及过滤条件
    post_data = {
        'pageId': 'eff768e57e9ace92d6e7ab4c2976575b',
        's8': '03',
        'sortFields': 's50:desc',
        'ciphertext': ciphertext,
        'pageNum': str(page),
        'pageSize': '15',
        'queryCondition': '[{"key":"s2","value":"山东省高级人民法院"},{"key":"s8","value":"03"},\
                            {"key":"cprqStart","value":"2021-03-01"},{"key":"cprqEnd","value":"2021-03-31"}]',
        'cfg': 'com.lawyee.judge.dc.parse.dto.SearchDataDsoDTO@queryDoc',
        '__RequestVerificationToken': ss['salt']
    }

    # txt = str(post_data)

    # request = base64.b64encode(txt.encode('utf-8')).decode('utf-8')
    # data = {
    #     'request': request
    # }

    url = "https://wenshu.court.gov.cn/website/parse/rest.q4w"

    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        'Origin': 'https://wenshu.court.gov.cn',
        'Host': 'wenshu.court.gov.cn',
    }

    response = requests.post(url, headers=headers, data=post_data, cookies=cookie)
    if 'HTTP Status 503' in response.text:
        print('请重试')
        exit()
    data = json.loads(response.text)
    content = data.get('result')
    key = data.get('secretKey')
    iv = v
    # print(key)
    # print(content)

    res = DES3.decrypt(content, key, iv)
    print("================第{}页list数据================".format(page))
    res = res.replace("false", "False")
    res = res.replace("null", "None")
    print("解密返回结果：", eval(res))
    # print("解密返回结果：", eval(res)["relWenshu"])
    return eval(res)
