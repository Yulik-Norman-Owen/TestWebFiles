from django.shortcuts import render, HttpResponse
from django.http import StreamingHttpResponse
import os

from TestWebFiles.settings import BASE_DIR


def index(request):
    allFileDirRoot = os.path.join(BASE_DIR, "FileFolder")
    if request.method == "POST":
        fileToUpload=request.FILES.get("fileToUpload","")
        fileName = fileToUpload.name
        filePath = os.path.join(allFileDirRoot, fileName)
        if os.path.exists(filePath):
            os.remove(filePath)
        with open(filePath, "wb") as fw:
            for chunk in fileToUpload.chunks():
                fw.write(chunk)
        return HttpResponse("Success")
    else:
        filesNameList = os.listdir(allFileDirRoot)
        return render(request, "index.html", {"filesNameList":filesNameList})


# Create your views here.
def fileDown(request, fileName):
    """
    下载压缩文件
    :param request:
    :name: 文件名
    :return:
    """

    filePath = os.path.join(BASE_DIR, 'FileFolder', fileName)  # 下载文件的绝对路径

    if not os.path.isfile(filePath):  # 判断下载文件是否存在
        return HttpResponse("Sorry but Not Found the File")

    def file_iterator(filePath, chunkSize=512):
        """
        文件生成器,防止文件过大，导致内存溢出
        :param filePath: 文件绝对路径
        :param chunkSize: 块大小
        :return: 生成器
        """
        with open(filePath, mode='rb') as f:
            while True:
                c = f.read(chunkSize)
                if c:
                    yield c
                else:
                    break

    try:
        # 设置响应头
        # StreamingHttpResponse将文件内容进行流式传输，数据量大可以用这个方法
        response = StreamingHttpResponse(file_iterator(filePath))
        # 以流的形式下载文件,这样可以实现任意格式的文件下载
        response['Content-Type'] = 'application/octet-stream'
        # Content-Disposition就是当用户想把请求所得的内容存为一个文件的时候提供一个默认的文件名
        response['Content-Disposition'] = 'attachment;filename="{}"'.format(fileName)
    except:
        return HttpResponse("Sorry but Not Found the File")

    return response
