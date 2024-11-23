import os
import re

# 设置 RIME 配置目录路径
RIME_CONFIG_DIR = os.path.expanduser('./')  # 根据实际路径修改
OUTPUT_DICT_FILE = os.path.expanduser('./rime_zh_simp.dict.yaml')  # 输出字典文件路径


# 读取所有字典文件并提取有效内容
def read_dict_files():
    line_num=0
    dict_entries = {}
    for root, _, files in os.walk(RIME_CONFIG_DIR):
        for file in files:
            if file.endswith('.dict.yaml'):
                dict_file_path = os.path.join(root, file)
                print(f"正在处理字典文件: {dict_file_path}")

                with open(dict_file_path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()

                # 标志变量，用于跳过头部描述部分，只提取字典内容
                processing = False

                for line in lines:
                    line = line.strip()
                    if line == '...':
                        processing = True
                        continue
                    if processing:
                        # 忽略注释行
                        if not (line.startswith('#') or (line.startswith('-'))) and line:
                            line_num+= 1
                            print(f"处理行数:{line_num}\n")
                            # 规范化并使用第一个词作为键，整行作为值存储
                            normalized_line = normalize_line(line.strip())  # 规范化整行内容
                            first_word = normalized_line.split()[0].strip()  # 获取第一个词作为键
                            print(f"文件{dict_file_path}, 行:{normalized_line},第一个词:{first_word}\n")
                            # 如果字典中已经有该键，比较内容，保留更长的内容
                            if first_word in dict_entries:
                                existing_line = dict_entries[first_word]
                                # 比较行长度，保留更长的行
                                if len(normalized_line) > len(existing_line):
                                    dict_entries[first_word] = normalized_line
                            else:
                                dict_entries[first_word] = normalized_line
    print(f"处理总行数:{line_num},dict_entries大小:{len(dict_entries)}")
    return dict_entries

# 规范化行内容，去掉前后空格，并将多个空格替换为单一空格
def normalize_line(line):
    # 去掉前后空格
    line = line.strip()
    # 将多个空格替换为一个空格
    line = re.sub(r'\s+', ' ', line)
    return line


# 写入合并后的字典文件
def write_combined_dict(merged_entries):
    with open(OUTPUT_DICT_FILE, 'w', encoding='utf-8') as f:
        f.write("name: rime_zh_dict\n")
        f.write("version: 1.0\n")
        f.write("author: RIME Community\n")
        f.write("description: 合并后的字典\n")
        f.write("sort: by_weight\n")
        f.write("\n")
        f.write("...\n")
        lines=0
        for line in merged_entries.values():
            lines+= 1
            f.write(line + '\n')
    print(f"字典合并并去重完成，输出字典文件：{OUTPUT_DICT_FILE},字典大小:{lines}")

# 主程序
def main():
    # 读取字典文件内容
    dicts=read_dict_files()
    # 输出合并后的字典文件
    write_combined_dict(dicts)

if __name__ == "__main__":
    main()
