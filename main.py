from bs4 import BeautifulSoup
import os
import re

# 定义文件夹名称
folder_name = "放入html文件"

# 检查文件夹是否存在
if not os.path.exists(folder_name):
    # 如果不存在，创建文件夹
    os.makedirs(folder_name)
#    print(f"文件夹 '{folder_name}' 已创建.")
#else:
#    print(f"文件夹 '{folder_name}' 已存在.")

# 输入需要的分辨率
resolution = input("输入需要的分辨率: ")
resolutionX = input("如果没有符合的分辨率，是否使用最高的分辨率(yes/no): ")

# 指定 HTML 文件的目录
directory = "放入html文件"  # 替换为你的目录名

# 检查是否覆盖文件
overwrite = "yes"  # 默认是覆盖
output_file_path = "下载链接.txt"

if os.path.exists(output_file_path) and os.path.getsize(output_file_path) > 0:
    overwrite = input("下载链接.txt 文件已存在且非空，是否覆盖? (yes/no): ")

# 打开下载链接文件，准备写入
with open(output_file_path, 'w' if overwrite.lower() == 'yes' else 'a', encoding='utf-8') as output_file:
    # 遍历目录下的所有文件
    for file_name in os.listdir(directory):
        if file_name.endswith('.html'):  # 检查文件是否为 HTML 文件
            file_path = os.path.join(directory, file_name)  # 完整的文件路径

            # 读取 HTML 文件
            with open(file_path, 'r', encoding='utf-8') as file:
                html_content = file.read()

            # 使用 BeautifulSoup 解析 HTML
            soup = BeautifulSoup(html_content, 'html.parser')

            # 查找所有符合条件的 <a> 标签
            download_links = soup.find_all('a', class_='exoclick-popunder')

            # 提取 href 属性并保存为 url 列表
            urls = []  # 初始化 urls 列表

            for link in download_links:
                href = link.get('href')
                urls.append(href)  # 将 href 的值添加到 urls 列表

            # 现在可以使用 urls 列表
            print(f"提取的下载链接来自 {file_name}:")
            for url in urls:
                print(url)

            urlX = None

            if any(re.search(resolution, url) for url in urls):
                for url in urls:
                    if re.search(resolution, url):
                        print(f"链接包含分辨率 {resolution}: {url}")
                        urlX = url  # 保存匹配的链接
                        break  # 找到后退出循环
            else:
                print(f"{file_name}: 此视频最高不足 {resolution}")

                # 根据 resolutionX 选择最高分辨率
                if resolutionX.lower() == "yes":
                    # 定义分辨率的优先级
                    priority_resolutions = ["1080p", "720p", "480p", "240p"]

                    # 找到最高的分辨率链接
                    for res in priority_resolutions:
                        for url in urls:
                            if re.search(res, url):
                                urlX = url  # 将最高分辨率的链接保存到 urlX
                                break  # 找到后退出内层循环
                        if urlX:  # 找到最高分辨率后退出外层循环
                            break

            if urlX:
                print(f"使用最高分辨率下载链接: {urlX}")
                output_file.write(urlX + '\n')  # 写入下载链接到文件
                print(f"{file_name}: 下载链接已保存到 '下载链接.txt'")
            else:
                print(f"{file_name}: 没有可用的视频链接")

input("脚本已执行完毕，按任意键退出...")