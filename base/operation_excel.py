import xlrd

class OperationExcel():
    def __init__(self):
        self.data = self.get_data()


    #获取excel数据
    def get_data(self,sheet_id = 0):
        workbook = xlrd.open_workbook('../base/test_url.xlsx')
        table = workbook.sheet_by_index(sheet_id)
        return table

    #获取url内容
    def get_url_value(self,row):
        return self.data.cell_value(row,1)

    #获取url备注
    def get_url_explain(self,row):
        return self.data.cell_value(row,2)

    #获取列数
    def get_lines(self):
        return self.data.nrows


    #获取url list
    def get_url_list(self):
        url_list = []
        lins = self.get_lines()
        for i in range(1,lins):
            url = self.get_url_value(i)
            url_list.append(url)
        return url_list






