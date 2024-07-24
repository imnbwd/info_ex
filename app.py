from flask import Flask, request, jsonify
from model import Result
from loguru import logger
from services import InfoExtractionService
from concurrent.futures import ThreadPoolExecutor

app = Flask(__name__)
executor = ThreadPoolExecutor(max_workers=10)  # 创建一个线程池，最大线程数为5


@app.route('/health', methods=['GET'])
def health():
    return jsonify("OK")


@app.route('/service', methods=['POST'])
def service():
    service_id = request.args.get('id')
    if service_id is None or service_id == "":
        return jsonify(Result(100, "缺少ServiceId").to_dict())
    if request.content_type != "application/json":
        return jsonify(Result(100, "缺少请求内容").to_dict())

    if service_id == str(100):
        # 提取服务

        # 先检查请求内容
        schema = request.json.get("options")
        url = request.json.get("url")
        notify_url = request.json.get("notify_url")
        task_id = request.json.get("task_id")

        check_result = None
        if not schema or not url:
            check_result = Result(-1, "缺少要提取的信息options或url")
        if not notify_url or not task_id:
            check_result = Result(-1, "缺少notify_url或task_id")

        # 判断要提取的内容
        is_valid_schema = isinstance(schema, list) and len(list(schema)) > 0
        if not is_valid_schema:
            check_result = Result(-1, "未指定要提取的项目")

        if check_result is not None:
            # 检查没通过
            return jsonify(check_result.to_dict())

        # 通过线程进行提取
        info_extract_service = InfoExtractionService()
        executor.submit(info_extract_service.get_result, schema, url, notify_url, task_id)
        return jsonify(Result.default_success("请求成功").to_dict())
    else:
        return jsonify(Result(101, "ServiceId不正确").to_dict())


@app.errorhandler(Exception)
def handle_global_exception(e):
    """
    全局异常处理
    :param e:
    :return:
    """
    logger.exception(e)
    return jsonify(Result(-1, "请求出错").to_dict())


# 运行 Flask 应用
if __name__ == '__main__':
    # 设置日志文件每天切割，文件名中包含日期
    logger.add("logs/app_{time:YYYY-MM-DD}.log", rotation="1 day", format="{time} {level} {message}")
    app.run(debug=True)
