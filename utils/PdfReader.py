import pdfplumber as ppl


class PdfReader:
    """
    Pdf文件读取类
    """

    def read(self, pdf_path):
        """
        读取指定路径的文件
        :param pdf_path: PDF文件路径
        :return: 包含PDF内容的字典，以索引为Key，以页面文本为Value
        """
        data = {}
        with ppl.open(pdf_path) as p:
            for i, page in enumerate(p.pages):
                data[i] = page.extract_text()

        return data
