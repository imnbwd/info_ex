from utils.PdfReader import PdfReader as pr
import os
import time
from utils.UieHelper import UieHelper
from pprint import pprint
from model.PdfData import PdfData
from model.ExtractedInfo import ExtractedInfo
from utils.PdfAnalyser import PdfAnalyser

def get_pdf_files(pdf_dir):
    '''获取pdf招标文件'''
    pdf_files = []
    # os.walk遍历目录
    for root, dirs, files in os.walk(pdf_dir):
        for file in files:
            # 检查文件扩展名是否为.pdf
            if file.endswith('.pdf'):
                # 将文件路径添加到列表中
                pdf_files.append(os.path.join(root, file))
    return pdf_files


def extract_content_to_json():
    """将标书的内容提取到JSON文件"""

    pdf_dir = "D:/标书/技术标/招标文件-TC识别准确率验证/产品给到的数据/01招标文件-内容样式-0613"  # /02 辽宁
    pdf_files = get_pdf_files(pdf_dir)

    # 读取
    start_time = time.time()  # 开始时间
    page_count = 0
    for file in pdf_files:
        data = pr.read(file)

        pdata = PdfData()
        pdata.source_path = file
        pdata.page_count = len(data)
        pdata.data = data

        json_path = f"./data/{os.path.basename(file)}.json"
        pdata.serialize_to_json(json_path)
        page_count += len(data)

    end_time = time.time()  # 结束时间
    pprint(f"耗时: {end_time - start_time}")
    pprint(f"每页平均：{(end_time - start_time) / page_count}, 总页数：{page_count}")


def extract_info_from_json(items):
    json_dir = "./data"
    target_json_dir = "./extracted"
    # 使用os.listdir获取目录中的所有文件和目录名
    files = [os.path.join(json_dir, file) for file in os.listdir(json_dir) if
             os.path.isfile(os.path.join(json_dir, file)) and "_extracted" not in file]
    start_time = time.time()  # 开始时间

    uie_helper = UieHelper(items)
    for file in files:

        extracted_info = ExtractedInfo()
        extracted_info.file_path = file
        extracted_info.data = {}
        pdata = PdfData.deserialize_from_json(file)
        for index, content in pdata.data.items():
            print(content)
            if len(content) == 0:
                continue
            info = uie_helper.extract(content)
            if len(info) == 0:
                continue
            extracted_info.data[index] = info

        file_name = os.path.basename(file)
        target_json_path = f"{target_json_dir}/{file_name}"
        extracted_info.serialize_to_json(target_json_path)

    end_time = time.time()  # 结束时间
    pprint(f"耗时: {end_time - start_time}")

# def toc_test():
#     pdata = PdfData.deserialize_from_json("./data/辽宁-招02.pdf.json")
#     pdf_helper = PdfAnalyser(pdata)
#     pdf_helper.find_toc_pages(list(pdata.data.values()))


if __name__ == "__main__":
    # 将标书提取成json
    # extract_content_to_json()
    items = ['公司', '组织', '地址', '姓名', '奖项', '身份证号', '电话']
    # extract_info_from_json(items)

    # toc_test()

    # for index, content in data.items():
    #     result = uh.extract(content, items)
    #     pprint(result)
