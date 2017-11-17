# -*- coding: utf-8 -*-
class UrlParser():
    @classmethod
    def getRankingUrls(cls, datesSet):
        # initUrl = 'http://m.media.daum.net/m/media/ranking/popular?regDate='
        initUrl = 'http://media.daum.net/ranking/popular/?regDate='
        ranking_urls = []
        # for i in datesSet:
        #     for j in range(100, 107):
        #         ranking_urls.append(initUrl+'{0}&date={1}'.format(j, i))
        for i in datesSet:
            ranking_urls.append(initUrl+'{0}'.format(i))

        return ranking_urls

    @classmethod
    def getKkomUrls(cls, datesSet):
        # initUrl = 'http://m.media.daum.net/m/media/ranking/kkomkkom?regDate='
        initUrl = 'http://media.daum.net/ranking/kkomkkom/?regDate='
        kkom_urls = []
        # for i in datesSet:
        #     for j in range(100, 107):
        #         comment_urls.append(initUrl+'{0}&date={1}'.format(j, i))
        for i in datesSet:
            kkom_urls.append(initUrl+'{0}'.format(i))
        return kkom_urls

    @classmethod
    def getCommentUrls(cls, datesSet):
        # initUrl = 'http://m.media.daum.net/m/media/ranking/bestreply?regDate='
        initUrl = 'http://media.daum.net/ranking/bestreply/?regDate='
        comment_urls = []
        # for i in datesSet:
        #     for j in range(100, 107):
        #         comment_urls.append(initUrl+'{0}&date={1}'.format(j, i))
        for i in datesSet:
            comment_urls.append(initUrl+'{0}'.format(i))
        return comment_urls
