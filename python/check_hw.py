from collections import Counter
import os
import shutil
import xlrd
import xlwt

current_path = os.path.dirname(__file__)

def make_report_dir(path):
    """
    创建报告目录，如果该目录已存在，先删除。
    """
    if os.path.isdir(path):
        shutil.rmtree(path) # 递归删去目录及下所有文件
    
    os.mkdir(path)

def get_all_homework(path):
    """
    获取所有作业文件的绝对路径，返回列表。
    """
    files = os.listdir(path)
    file_full_path_lst = list()
    for f in files:
        file_full_path = os.path.join(path, f)
        file_full_path_lst.append(file_full_path)
    return file_full_path_lst
    

def get_answer_dict(answer_file):
    """
    将答案内容写入一个字典，{"题号": "答案"}，返回字典
    """
    ans_dict = dict()
    workbook = xlrd.open_workbook(answer_file)
    sheet = workbook.sheet_by_index(0)

    nrows = sheet.nrows
    for row in range(nrows):
        # rowd = sheet.row_values(row)
        # rowdata = [x.lower().strip() for x in rowd]
        # # ans_dict[row+1] = sheet.cell_value(rowx=row, colx=0).lower().strip()
        # ans_dict[row+1] = rowdata
        rowd = sheet.row_values(row)
        rowdata = [x.lower().strip() for x in rowd]
        ans_dict[row+1] = rowdata

    return ans_dict


def compare_answer(hw_file, correct_dict):
    """
    比较作业答案和标准答案，返回元组（姓名，错题号列表，错题字典）
    """
    base = os.path.basename(hw_file)
    name = os.path.splitext(base)[0]
    wrong_lst = list()
    wrong_dict = dict()

    try:
        hw_dict = get_answer_dict(hw_file)

        if hw_dict != correct_dict:
            for i in range(1, len(correct_dict)+1):
                if hw_dict[i][0] not in correct_dict[i]:   
                    wrong_lst.append(i)
                    wrong_dict[i] = hw_dict[i]

        format_report("correct", name)
    except:
        format_report("error", name)

    return name, wrong_lst, wrong_dict

def format_report(r_type, name):
    file_name = r_type + ".txt"
    fp = open(os.path.join(report_path, file_name),"a",encoding="utf-8")
    fp.write(name)
    fp.write('\r\n')
    fp.close()


def write_personal_report(data, correct_dict):
    """
    生成个人错误报告文件
    """
    name, wrong_lst, wrong_dict = data
    report_name = name+".xls"
    head = [u"错误题目", u"提交答案", u"正确答案"]
    workbook = xlwt.Workbook(encoding='UTF-8')
    worksheet = workbook.add_sheet('Sheet1')
    for j in range(len(head)):
        worksheet.write(0,j,label=head[j])
    if wrong_lst:
        for i in range(len(wrong_lst)):
            string = " "
            correct_ans = string.join(correct_dict[wrong_lst[i]])
            worksheet.write(i+1, 0, label=wrong_lst[i])
            worksheet.write(i+1, 1, label=wrong_dict[wrong_lst[i]])
            worksheet.write(i+1, 2, label=correct_ans)
    else:
        worksheet.write(1, 0, label="None")

    workbook.save(os.path.join(report_path, report_name))            

def write_total_report(data):
    all_wrong_lst = list()
    for item in data:
        all_wrong_lst.extend(item[1])
    
    cnt = Counter()
    for item in all_wrong_lst:
        cnt[item] += 1
    total_result_dict = dict(cnt)
    sort_num_lst = sorted(total_result_dict)

    report_name = "Total_report.xls"
    head = [u"错误题目", u"错误人数"]
    workbook = xlwt.Workbook(encoding='UTF-8')
    worksheet = workbook.add_sheet('Sheet1')
    for j in range(len(head)):
        worksheet.write(0,j,label=head[j])

    for i in range(len(sort_num_lst)):
        worksheet.write(i+1, 0, sort_num_lst[i])
        worksheet.write(i+1, 1, total_result_dict[sort_num_lst[i]])

    workbook.save(os.path.join(report_path, report_name))  


def main():
    make_report_dir(report_path)

    homework_files = get_all_homework(homework_path)

    correct_dict = get_answer_dict(correct_answer_file)
 
    all_result_lst = list()
    for homework_file in homework_files:
        result = compare_answer(homework_file, correct_dict)
        all_result_lst.append(result)
        write_personal_report(result, correct_dict)


    write_total_report(all_result_lst)


if __name__ == "__main__":
    report_path = os.path.join(current_path, "report")
    homework_path = os.path.join(current_path, "homework")
    correct_answer_file = os.path.join(current_path, "Answer.xlsx")

    main()
