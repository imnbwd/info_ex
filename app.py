from flask import Flask, request, jsonify
from model import Result
from loguru import logger
from services import InfoExtractionService

app = Flask(__name__)


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
        info_extract_service = InfoExtractionService(request)
        result = info_extract_service.get_result()
        return jsonify(result.to_dict())
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
