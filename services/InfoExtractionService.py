from flask import Flask, request, jsonify
from model.Result import Result
from utils import PdfAnalyser, PdfReader, UieHelper


class InfoExtractionService:
    """提取信息"""

    def __init__(self, http_request):
        self.request = http_request
        pass

    def get_result(self):
        """进行提取"""
        request_body = self.request.json
        if "options" not in request_body:
            return Result(-1, "未指定要提取的内容")

        schema = self.request.json["options"]
        # 判断要提取的内容
        is_valid_schema = schema is not None and isinstance(schema, list) and len(list(schema)) > 0
        if not is_valid_schema:
            return Result(-1, "未指定要提取的内容")

        # 获取指定的url
        # if "url" not in request_body:
        #     return Result(-1, "未指定要提取的内容")

        # 先从本地获取文件
        uie_helper = UieHelper.get_instance()
        uie_helper.set_schema(schema)

        return "OK"

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
