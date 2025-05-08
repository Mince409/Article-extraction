import os


# 定义一个函数用于按章节拆分文本文件，并将拆分后的内容保存到指定目录
def split_chapters(file_path, save_directory):
    # 检查要处理的文件是否存在
    if not os.path.exists(file_path):
        print(f"文件 {file_path} 不存在，请检查路径和文件名。")
        return
    # 检查指定的保存目录是否存在，如果不存在则创建该目录
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)
    try:
        # 以只读模式打开指定的文件，并使用 UTF-8 编码读取文件内容
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        # 定义第一部分章节的起始和结束标识
        start_chapter1, end_chapter1 = "第491章 敲门", "陈伶望着那隐藏着炼金术阵的乌云中央，眼眸中精芒闪烁。"
        # 查找第一部分章节起始标识在文件内容中的位置
        start_index1 = content.find(start_chapter1)
        # 查找第一部分章节结束标识在文件内容中的位置，并加上结束标识的长度
        end_index1 = content.find(end_chapter1) + len(end_chapter1)
        # 检查是否找到了第一部分章节的起始和结束标识，如果没找到则输出提示信息并返回
        if start_index1 == -1 or end_index1 == -1 + len(end_chapter1):
            print("未找到第491章到第700章的内容，请检查章节标识。")
            return
        # 从文件内容中提取第 491 章到第 700 章的内容
        part1_content = content[start_index1:end_index1]
        # 构建第一部分章节内容保存的完整文件路径，将保存目录和文件名组合
        part1_file_path = os.path.join(save_directory, '我不是戏神491 - 700章.txt')
        # 以写入模式打开第一部分章节内容保存的文件，并使用 UTF-8 编码写入内容
        with open(part1_file_path, 'w', encoding='utf-8') as part1_file:
            part1_file.write(part1_content)

        # 定义第二部分章节的起始和结束标识
        start_chapter2, end_chapter2 = "第701章", "“白银之王外出，无极君受限……诸位，各凭本事的时候到了。”"
        # 查找第二部分章节起始标识在文件内容中的位置
        start_index2 = content.find(start_chapter2)
        # 查找第二部分章节结束标识在文件内容中的位置，并加上结束标识的长度
        end_index2 = content.find(end_chapter2) + len(end_chapter2)
        # 检查是否找到了第二部分章节的起始和结束标识，如果没找到则输出提示信息并返回
        if start_index2 == -1 or end_index2 == -1 + len(end_chapter2):
            print("未找到第701章到第1000章的内容，请检查章节标识。")
            return
        # 从文件内容中提取第 701 章到第 1000 章的内容
        part2_content = content[start_index2:end_index2]
        # 构建第二部分章节内容保存的完整文件路径，将保存目录和文件名组合
        part2_file_path = os.path.join(save_directory, '我不是戏神701 - 1000章.txt')
        # 以写入模式打开第二部分章节内容保存的文件，并使用 UTF-8 编码写入内容
        with open(part2_file_path, 'w', encoding='utf-8') as part2_file:
            part2_file.write(part2_content)
        # 若所有操作都成功完成，输出章节拆分完成的提示信息
        print("章节拆分完成。")
    except Exception as e:
        # 若在处理文件过程中出现异常，输出错误信息
        print(f"处理文件时出现错误: {e}")


if __name__ == "__main__":
    # 指定要处理的文件的完整路径
    file_path = r"C:\Users\cisco\Desktop\word.txt"
    # 指定拆分后的章节内容文件要保存的目录
    save_directory = r"C:\Users\cisco\Desktop\wordPin"
    # 调用 split_chapters 函数进行章节拆分操作
    split_chapters(file_path, save_directory)