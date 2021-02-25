# -*-coding:utf-8-*-
# 2021-2-23 22:15:40

class CommentSet:
    import re
    # 芦苇岛的文本导出格式
    pat_title_weed = re.compile(r'(?P<id>\w{7}) \d{4}-\d{2}-\d{2}\([一|二|三|四|五|六|日]\)\d{2}:\d{2}:\d{2} No.(?P<no>\d+)')

    # PC网页的格式
    pat_title_pc = re.compile(r'20\d\d-\d\d-\d\d\([一|二|三|四|五|六|日]\)\d{2}:\d{2}:\d{2} ID:(?P<id>\w{7})\s(?P<po>\(PO主\))?.+No.(?P<no>\d+)')


    def __init__(self,comments=''):
        import os
        self.blackIdList = ['1pGvS00']
        self.comments = ''
        if comments:
            if len(comments)<200 and os.path.isfile(comments):
                with open(comments, "r", encoding='utf-8') as f:
                    self.comments = f.readlines()
            else:
                self.comments = comments.split('\n')

        self.ids = []
        self.nos = []
    

    def parse(self):
        # 从原始文本解析出id&no
        for line in self.comments:
            matchResult = self.pat_title_weed.search(line)
            if matchResult:
                self.ids.append(matchResult['id'])
                self.nos.append(matchResult['no'])
        if not self.ids: # 当pat_title_weed匹配不到任何结果时，尝试另一种模式
            for line in self.comments:
                matchResult = self.pat_title_pc.search(line)
                if matchResult:
                    self.ids.append(matchResult['id'])
                    self.nos.append(matchResult['no'])
                    if matchResult['po'] and not matchResult['id'] in self.blackIdList:
                        self.blackIdList.append(matchResult['id'])

            

    def count_point(self,headshot=None,startn=1,lastn=1,silent=False):
        """
        普通计点
        headshot:int 首个有效位为n时直接结束计点
        startn:int 从n楼开始计算
        lastn:int 取倒数第n个位数
        """

        report = [['id','No','status','sum']]
        count = 0

        self.parse()
        data = []
        for i in range(len(self.ids)):
            data.append([self.ids[i],self.nos[i]])

        ID = 0
        NO = 1
        BLOCKPO = '不计po'
        DUPLICATED = '已roll'
        SKIP = '不计入'
        VALID = '有效  '

        visited_ids = []
        summary = []
        for x in data:
            if x[ID] in self.blackIdList:
                report.append([x[ID],x[NO],BLOCKPO,str(count)])
                continue
            if startn > 1:
                startn -= 1
                report.append([x[ID],x[NO],SKIP,str(count)])
                continue
            if x[ID] in visited_ids:
                report.append([x[ID],x[NO],DUPLICATED,str(count)])
            else:
                visited_ids.append(x[ID])
                count += int(x[NO][-lastn])
                summary.append(x[NO][-lastn])
                report.append([x[ID],x[NO],VALID,str(count)])
                if headshot and count == headshot:
                    summary = 'headshot!'
                    break
                headshot = None

        count = str(count)[-1]

        report_txt = ''
        report_txt = report_txt + ''.join(summary) + '\n'
        report_txt = report_txt + '目前点数：'+count + '\n'
        report_txt = report_txt + '=======以下为详细报告======='+ '\n'

        for i in report:
            report_txt = report_txt + '\t'.join(i) + '\n'
        if not silent:
            print(report_txt)

        return report_txt


if __name__=="__main__":
    test_input = 'test_input_short.txt'
    # test_input = 'test_input_pc.txt'
    cs = CommentSet(test_input)
    report_txt = cs.count_point(headshot=9,startn=1,silent=True)
    print(report_txt)