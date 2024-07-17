from model.PdfData import PdfData
import re


class PdfAnalyser:
    def __init__(self, pdf_data: PdfData = None) -> None:
        self.pdf_data = pdf_data

    def find_toc_pages(self):
        toc_pages = []
        for index, page_text in enumerate():
            if "目录" in page_text or re.search(r"\.\s+\d+", page_text):
                toc_pages.append(index)
        return toc_pages

    def extract_toc_info(toc_pages_text):
        toc_info = []
        for page_text in toc_pages_text:
            lines = page_text.split("\n")
            for line in lines:
                match = re.match(r"(.*?)\s+\.{3,}\s+(\d+)", line)
                if match:
                    title = match.group(1).strip()
                    page_num = int(match.group(2).strip())
                    toc_info.append((title, page_num))
        return toc_info

    def build_result_list(toc_info, total_pages):
        result = []
        for i in range(len(toc_info)):
            title, start_index = toc_info[i]
            if i + 1 < len(toc_info):
                _, end_index = toc_info[i + 1]
                end_index -= 1
            else:
                end_index = total_pages - 1
            result.append({"title": title, "start_index": start_index, "end_index": end_index})
        return result