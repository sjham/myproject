
class UrlParser():
    @classmethod
    def getRankingUrls(cls, datesSet):
        initUrl = 'http://m.news.naver.com/rankingList.nhn?sid1='
        ranking_urls = []
        for i in datesSet:
            for j in range(100, 110):
                ranking_urls.append(initUrl+'{0}&date={1}'.format(j, i))
        return ranking_urls

    @classmethod
    def getCommentUrls(cls, datesSet):
        initUrl = 'http://m.news.naver.com/memoRankingList.nhn?sid1='
        comment_urls = []
        for i in datesSet:
            for j in range(100, 110):
                comment_urls.append(initUrl+'{0}&date={1}'.format(j, i))
        return comment_urls
