
# from date_parser import DateParser as dp


class UrlParser():
    @classmethod
    def getSearchUrls(cls, newsDates):
        initUrl = 'http://news.naver.com/main/ranking/searchWeek.nhn?mid=etc&rankingType=search_week&date='
        search_urls = []
        for i in newsDates:
            search_urls.append(initUrl+'{0}'.format(i))
        return search_urls

    @classmethod
    def getCommentUrls(cls, newsDates):
        initUrl = 'http://news.naver.com/main/ranking/memoWeek.nhn?rankingType=memo_week&sectionId='
        comment_urls = []
        for i in newsDates:
            for j in range(100, 106):
                comment_urls.append(initUrl+'{0}&date={1}'.format(j, i))
        for i in newsDates:
            comment_urls.append(initUrl+'115&date={0}'.format(i))
        return comment_urls

    @classmethod
    def getCommentTotalUrls(cls, newsDates):
        initUrl = 'http://news.naver.com/main/ranking/memoWeek.nhn?rankingType=memo_week&sectionId=000&date='
        comment_total_urls = []
        for i in newsDates:
            comment_total_urls.append(initUrl+'{0}'.format(i))
        return comment_total_urls


    @classmethod
    def getClickUrls(cls, newsDates):
        initUrl = 'http://news.naver.com/main/ranking/popularWeek.nhn?rankingType=popular_week&sectionId='
        click_urls = []
        for i in newsDates:
            for j in range(100, 108):
                click_urls.append(initUrl+'{0}&date={1}'.format(j, i))
        for i in newsDates:
            click_urls.append(initUrl+'115&date={0}'.format(i))
        return click_urls

    @classmethod
    def getClickTotalUrls(cls, newsDates):
        initUrl = 'http://news.naver.com/main/ranking/popularWeek.nhn?mid=etc&rankingType=popular_week&sectionId=000&date='
        click_total_urls = []
        for i in newsDates:
            click_total_urls.append(initUrl+'{0}'.format(i))
        return click_total_urls
#     #
# if __name__ == '__main__':
#     sd = input("Start Date(yyyy,m,d): ")
#     ed = input("End Date(yyyy,m,d): ")
#     a = UrlParser()
#     print(a.getCommentUrls(dp.getTargetdate(dp.getDate(sd, ed))))
