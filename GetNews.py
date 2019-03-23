import requests,json,re,demjson,jieba,os,time
from bs4 import BeautifulSoup
from gensim import corpora, models, similarities
from app.models import Web,Article,Channels
class GetNews:
    #搜索网站的url
    searchWebUrl = {
        'sina':{
            'base':'http://www.sina.com.cn/',
            'search':"""http://top.tech.sina.com.cn/ws/GetTopDataList.php
                        ?top_type=day
                        &top_cat=tech_it_suda
                        &top_time=today
                        &top_show_num=10
                        &top_order=DESC
                        &js_var=tele_day_data
                        &chars=gbk""",
        },
        'wangyi':{
            'base':'http://news.163.com/',
            'search':"""http://tech.163.com/special/00097UHL/tech_datalist.js?callback=data_callback""",
        },
        'toutiao':{
            'base':'https://www.toutiao.com/',
            'search':"""https://www.toutiao.com/api/pc/feed/
                        ?category=news_tech
                        &utm_source=toutiao
                        &widen=1
                        &max_behot_time=0
                        &max_behot_time_tmp=0
                        &tadrequire=true
                        &as=A125DAC42C89453
                        &cp=5A4CF9F4F5C3EE1
                        &_signature=hUnMegAA3xJDv4CGtRJYZ4VJzG""",
        },
        'tencent':{
            'base':'http://news.qq.com/',
            'search':'http://tech.qq.com/',
        }
    }
    #请求头
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0',
    }
    #频道
    channel = {
        'wangyi':{'tech':'tech'}
    }

    #获取链接信息
    def get_info(self,url,encode = False):
        re = requests.get(url,headers=self.headers, timeout=1)
        if re.status_code == 200 :
            if encode:
                re.encoding = 'utf-8'
            return re.text
        else:
            return False

    def get_article_urls(self,text,type):
        article_urls = []
        if type == 'wangyi':                        #网易
            text = json.loads(text[14:-1])
            for info in text:
                if 'docurl' in info.keys():
                    article_urls += [info['docurl']]
        if type == 'toutiao':                       #头条
            text = json.loads(text)
            if text['message']:
                for info in text['data']:
                    if 'article_genre' in info.keys() and info['article_genre'] != 'article':    #排除头条非文章
                        continue
                    article_urls += [self.searchWebUrl['toutiao']['base']+info['source_url'].replace('/group/','a')]
        if type == 'tencent':                       #腾讯
            text = BeautifulSoup(text, "html.parser")
            text = text.select('.Q-tpListInner > .itemtxt > h3 > a')
            for info in text:   
                article_urls += [info['href']]
        if type == 'sina':                         #新浪
            text = json.loads(text[20:-2])
            for info in text['data']:
                article_urls += [info['url']]
        return article_urls

    def get_article_info(self,url,type):
        title,pubtime,content = '','',''
        encode = False
        if type == 'sina':
            encode = True
        text = self.get_info(url,encode)
        if text == False:
            return title,pubtime,BeautifulSoup('', "html.parser")
        if type == 'toutiao':
            html = BeautifulSoup(text, "html.parser")
            for info in html.select('script'):
                if 'articleInfo' in info.text:
                    result = info.text[15:-1]
                    result = result[:result.find('shareInfo')-5]+'}'
                    jsonInfo = demjson.decode(result)
                    title = jsonInfo['articleInfo']['title']
                    pubtime = jsonInfo['articleInfo']['subInfo']['time']
                    temp = jsonInfo['articleInfo']['content'].replace('&lt;','<').replace('&gt;','>').replace('&quot;','"').replace('&#x3D;','=')
                    content = BeautifulSoup(temp, "html.parser")
                    break
        if type == 'wangyi':
            html = BeautifulSoup(text, "html.parser")
            title = html.select('#epContentLeft h1')[0].text
            pubtime = html.select('#epContentLeft .post_time_source')[0].text[17:36]
            content = html.select('#endText')[0];
        if type == 'sina':
            html = BeautifulSoup(text, "html.parser")
            title = html.select('.main-content h1')[0].text
            pubtime = html.select('#top_bar .date')[0].text.replace('年','-').replace('月','-').replace('日','')+':00'
            content = html.select('#artibody')[0];
        if type == 'tencent':
            html = BeautifulSoup(text, "html.parser")
            title = html.select('.LEFT h1')[0].text
            pubtime = html.select('meta[name="_pubtime"]')[0]['content']
            content = html.select('.content-article')[0]
        if content == '':
            content = BeautifulSoup('', "html.parser")
        return title,pubtime,content

    def get_similarity_gegree(self,originals,exponent):         #获取需要对比文章与其他文章的相似度
        oris = []
        for original in originals:
            oris += [self.get_remove_stop_words_dic(original.text)]
        exp = self.get_remove_stop_words_dic(exponent.text)
        dictionary = corpora.Dictionary(oris)                   #字典集
        query_bow = dictionary.doc2bow(exp)
        doc_vectors = [dictionary.doc2bow(text) for text in oris]   
        tfidf = models.TfidfModel(doc_vectors)                  #建立TTF-IDF模型
        tfidf_vectors = tfidf[doc_vectors]                      
        index = similarities.MatrixSimilarity(tfidf_vectors)
        sim = index[query_bow]
        # lsi = models.LsiModel(tfidf_vectors, id2word=dictionary, num_topics=1)
        # lsi_vector = lsi[tfidf_vectors]
        # index = similarities.MatrixSimilarity(lsi_vector)
        # query_lsi = lsi[query_bow]
        # lsi_sim = index[query_lsi]
        # print(list(enumerate(lsi_sim)))
        return list(enumerate(sim))                #进行对比

    def get_remove_stop_words_dic(self,content):        #获取移除停用词的分词字典
        stop_words = ['的',',','.','，','。','；','"','“','”',"'",'<','>','《','》','——',' ','(',')']
        result = []
        for t in jieba.cut(content):
            if t not in stop_words:
                result += [t]
        return result

    #获取搜索的url
    def get_search_url(self,web,type):
        webObj   = Web.objects
        baseInfo = webObj.get(web=web)
        channelInfo = Channels.objects.get(id=baseInfo.id)
        url = baseInfo.search_url.format(channelInfo.sign)
        print(url)

if __name__ == '__main__':
    getnews = GetNews()
    url = "http://www.toutiao.com/search_content/?offset={}&format=json&keyword={}&autoload=true&count=10&cur_tab=1"
    text = getnews.get_info('http://tech.163.com/special/00097UHL/tech_datalist.js?callback=data_callback')
    #text = getnews.get_info('https://www.toutiao.com/api/pc/feed/?category=news_tech&utm_source=toutiao&widen=1&max_behot_time=0&max_behot_time_tmp=0&tadrequire=true&as=A125DAC42C89453&cp=5A4CF9F4F5C3EE1&_signature=hUnMegAA3xJDv4CGtRJYZ4VJzG')
    #text = getnews.get_info('http://top.tech.sina.com.cn/ws/GetTopDataList.php?top_type=day&top_cat=tech_it_suda&top_time=today&top_show_num=10&top_order=DESC&js_var=tele_day_data&chars=gbk',True)
    #取qq的第一篇文章
    #text = getnews.get_info('http://tech.qq.com/')
    urls = getnews.get_article_urls(text,'wangyi')
    print(urls[0])
    title,pubtime,content = getnews.get_article_info(urls[0],'wangyi')
    print(title)
    o_urls = getnews.get_article_urls(getnews.get_info(url.format('0',title)),'toutiao')
    ors = []
    for o_url in o_urls:
        time.sleep(3)
        title,pubtime,o_content = getnews.get_article_info(o_url,'toutiao')
        print(title)
        ors += [o_content]
    si = getnews.get_similarity_gegree(ors,content)
    print(si)