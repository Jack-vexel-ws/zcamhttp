#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ZCAM相机格式信息采集脚本
通过HTTP命令获取相机支持的分辨率、帧率等信息，并生成JSON文件
"""

import json
import requests
import sys
import time
from typing import Dict, List, Any, Optional

# HTTP请求超时时间（毫秒）
TIMEOUT_MS = 10000  # 10000毫秒 = 10秒（相机操作可能需要较长时间）
# 转换为秒（requests库使用秒作为单位）
TIMEOUT = TIMEOUT_MS / 1000.0

# 设置操作后的等待时间（秒），确保相机有足够时间处理
SET_WAIT_TIME = 1.5


def print_response(url: str, response: requests.Response) -> None:
    """打印HTTP请求和响应信息"""
    print(f"\n{'='*60}")
    print(f"请求URL: {url}")
    print(f"状态码: {response.status_code}")
    print(f"响应内容:")
    try:
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))
    except:
        print(response.text)
    print(f"{'='*60}\n")


def http_get(base_url: str, endpoint: str, check_code: bool = True) -> Optional[Dict]:
    """
    发送HTTP GET请求并返回JSON响应
    
    Args:
        base_url: 相机IP地址
        endpoint: 请求端点
        check_code: 是否检查响应中的code字段（默认为True）
    
    Returns:
        成功时返回JSON数据，失败时返回None
    """
    url = f"http://{base_url}{endpoint}"
    try:
        response = requests.get(url, timeout=TIMEOUT)
        print_response(url, response)
        if response.status_code == 200:
            data = response.json()
            # 如果需要检查code字段
            if check_code and "code" in data:
                if data.get("code", -1) != 0:
                    print(f"警告: 请求失败，响应code: {data.get('code')}")
                    return None
            return data
        else:
            print(f"警告: 请求失败，状态码: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"错误: 请求失败 - {e}")
        return None


def http_set_resolution(base_url: str, resolution: str) -> bool:
    """发送HTTP SET请求设置分辨率"""
    url = f"http://{base_url}/ctrl/set?resolution={resolution}"
    try:
        response = requests.get(url, timeout=TIMEOUT)
        print_response(url, response)
        if response.status_code == 200:
            data = response.json()
            if data.get("code", -1) == 0:
                # 等待相机响应
                time.sleep(SET_WAIT_TIME)
                return True
            else:
                print(f"警告: 设置失败，响应code: {data.get('code')}")
                return False
        else:
            print(f"警告: 设置失败，状态码: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"错误: 设置失败 - {e}")
        return False


def http_set_project_fps(base_url: str, fps: str) -> bool:
    """发送HTTP SET请求设置project_fps"""
    url = f"http://{base_url}/ctrl/set?project_fps={fps}"
    try:
        response = requests.get(url, timeout=TIMEOUT)
        print_response(url, response)
        if response.status_code == 200:
            data = response.json()
            if data.get("code", -1) == 0:
                # 等待相机响应
                time.sleep(SET_WAIT_TIME)
                return True
            else:
                print(f"警告: 设置project_fps失败，响应code: {data.get('code')}")
                return False
        else:
            print(f"警告: 设置project_fps失败，状态码: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"错误: 设置project_fps失败 - {e}")
        return False


def parse_fps_value(fps_str: str) -> Optional[float]:
    """将FPS字符串转换为浮点数"""
    try:
        # 处理 "Off" 等非数字值
        if fps_str.lower() == "off":
            return None
        return float(fps_str)
    except (ValueError, TypeError):
        return None


def format_fps_string(fps_value: float) -> str:
    """将FPS值格式化为字符串：整数去小数，小数保留"""
    # 判断是否为整数（考虑浮点数精度问题）
    if abs(fps_value - round(fps_value)) < 0.001:
        # 是整数，返回整数形式的字符串
        return str(int(round(fps_value)))
    else:
        # 是小数，保留小数部分
        return str(fps_value)


def merge_fps_lists(fps_list: List[str], vfr_list: List[str]) -> List[str]:
    """合并fps和vfr列表，筛选出大于等于23.98的帧率值，返回字符串列表"""
    all_fps = set()
    
    # 处理fps列表
    for fps_str in fps_list:
        fps_value = parse_fps_value(fps_str)
        if fps_value is not None and fps_value >= 23.98:
            all_fps.add(fps_value)
    
    # 处理vfr列表
    for vfr_str in vfr_list:
        vfr_value = parse_fps_value(vfr_str)
        if vfr_value is not None and vfr_value >= 23.98:
            all_fps.add(vfr_value)
    
    # 排序并格式化为字符串列表
    sorted_fps = sorted(list(all_fps))
    return [format_fps_string(fps) for fps in sorted_fps]


def get_camera_info(base_url: str) -> Optional[Dict]:
    """步骤1: 获取相机基本信息"""
    print("\n[步骤1] 获取相机基本信息...")
    data = http_get(base_url, "/info", check_code=False)
    if not data:
        return None
    
    result = {
        "model": data.get("model", ""),
        "sw": data.get("sw", ""),
        "nickName": data.get("nickName", ""),
        "allfmt": data.get("feature", {}).get("snapSupportFmt", {}).get("fmt", [])
    }
    return result


def get_movfmt(base_url: str) -> List[str]:
    """步骤2: 获取支持的movfmt列表"""
    print("\n[步骤2] 获取支持的movfmt列表...")
    data = http_get(base_url, "/ctrl/get?k=movfmt")
    if not data:
        return []
    return data.get("opts", [])


def get_resolutions(base_url: str) -> List[str]:
    """步骤3: 获取支持的分辨率列表"""
    print("\n[步骤3] 获取支持的分辨率列表...")
    data = http_get(base_url, "/ctrl/get?k=resolution")
    if not data:
        return []
    return data.get("opts", [])


def construct_movfmt(resolution: str, fps: str, movfmt_list: List[str]) -> Optional[str]:
    """
    根据规则构造movfmt，如果构造的movfmt在movfmt_list中则返回，否则返回None
    
    Args:
        resolution: 分辨率名称
        fps: 帧率字符串
        movfmt_list: 相机支持的movfmt列表
    
    Returns:
        如果构造的movfmt在列表中则返回，否则返回None
    """
    movfmt_set = set(movfmt_list)
    
    # 规则5: S16 16:9 或 S16 -> resolution + fps (无P)
    if resolution.startswith("S16"):
        constructed = f"{resolution} {fps}"
        if constructed in movfmt_set:
            return constructed
    
    # 规则4: 包含 " (Low Noise)" -> 名称 + P + fps + " (Low Noise)"
    if " (Low Noise)" in resolution:
        base_name = resolution.replace(" (Low Noise)", "")
        constructed = f"{base_name}P{fps} (Low Noise)"
        if constructed in movfmt_set:
            return constructed
    
    # 规则3: 1920x1080 -> 1080 + P + fps
    if resolution == "1920x1080":
        constructed = f"1080P{fps}"
        if constructed in movfmt_set:
            return constructed
    
    # 规则2: 宽度x高度且宽高相同 -> 宽度 + P + fps
    if "x" in resolution:
        try:
            parts = resolution.split("x")
            if len(parts) == 2:
                width = parts[0].strip()
                height = parts[1].strip()
                if width == height:
                    constructed = f"{width}P{fps}"
                    if constructed in movfmt_set:
                        return constructed
        except:
            pass
    
    # 规则1: 基本规则 resolution + P + fps
    constructed = f"{resolution}P{fps}"
    if constructed in movfmt_set:
        return constructed
    
    # 如果都不匹配，返回None
    return None


def get_resolution_details(base_url: str, resolution: str, movfmt_list: List[str]) -> Optional[Dict]:
    """步骤4: 获取指定分辨率的详细信息"""
    print(f"\n[步骤4] 获取分辨率 '{resolution}' 的详细信息...")
    
    # 设置分辨率
    print(f"  设置分辨率为: {resolution}")
    if not http_set_resolution(base_url, resolution):
        print(f"  警告: 设置分辨率失败")
        return None
    
    # 获取project_fps
    print(f"  获取project_fps...")
    fps_data = http_get(base_url, "/ctrl/get?k=project_fps")
    fps_list = []
    if fps_data:
        fps_list = fps_data.get("opts", [])
    
    # 获取movvfr
    print(f"  获取movvfr...")
    vfr_data = http_get(base_url, "/ctrl/get?k=movvfr")
    vfr_list = []
    if vfr_data:
        vfr_list = vfr_data.get("opts", [])
    
    # 合并并筛选user_fps_list
    user_fps_list = merge_fps_lists(fps_list, vfr_list)
    
    # 获取流设置（width和height）
    print(f"  获取流设置...")
    stream_data = http_get(base_url, "/ctrl/stream_setting?index=stream0&action=query", check_code=False)
    width = None
    height = None
    if stream_data:
        width = stream_data.get("width")
        height = stream_data.get("height")
    
    # 转换fps和vfr为字符串列表（整数去小数，小数保留）
    fps_string_list = []
    for fps_str in fps_list:
        fps_value = parse_fps_value(fps_str)
        if fps_value is not None:
            fps_string_list.append(fps_value)
    fps_string_list = sorted(fps_string_list)
    fps_string_list = [format_fps_string(fps) for fps in fps_string_list]
    
    vfr_string_list = []
    for vfr_str in vfr_list:
        vfr_value = parse_fps_value(vfr_str)
        if vfr_value is not None:
            vfr_string_list.append(vfr_value)
    vfr_string_list = sorted(vfr_string_list)
    vfr_string_list = [format_fps_string(vfr) for vfr in vfr_string_list]
    
    # 遍历每个fps值，获取对应的movfmt
    print(f"  遍历fps列表，获取每个fps对应的movfmt...")
    movfmt_result_list = []
    for i, fps in enumerate(fps_string_list, 1):
        print(f"    处理fps {i}/{len(fps_string_list)}: {fps}")
        
        # 先尝试根据规则构造movfmt
        constructed_movfmt = construct_movfmt(resolution, fps, movfmt_list)
        if constructed_movfmt:
            movfmt_result_list.append(constructed_movfmt)
            print(f"      通过规则构造movfmt: {constructed_movfmt}")
        else:
            # 如果规则构造失败，使用原来的方式：设置project_fps然后查询
            print(f"      规则构造失败，使用设置project_fps方式查询...")
            if not http_set_project_fps(base_url, fps):
                print(f"        警告: 设置project_fps={fps}失败，跳过")
                continue
            
            # 获取当前的movfmt
            movfmt_data = http_get(base_url, "/ctrl/get?k=movfmt")
            if movfmt_data:
                current_movfmt = movfmt_data.get("value", "")
                if current_movfmt:
                    movfmt_result_list.append(current_movfmt)
                    print(f"        获取到movfmt: {current_movfmt}")
                else:
                    print(f"        警告: 未获取到movfmt值")
            else:
                print(f"        警告: 获取movfmt失败")
    
    # 确保movfmt_result_list的长度与fps_string_list一致
    if len(movfmt_result_list) != len(fps_string_list):
        print(f"  警告: movfmt列表长度({len(movfmt_result_list)})与fps列表长度({len(fps_string_list)})不一致")
    
    return {
        "resolution": resolution,
        "width": width,
        "height": height,
        "movfmt": movfmt_result_list,
        "fps": fps_string_list,
        "vfr": vfr_string_list,
        "user_fps_list": user_fps_list
    }


def generate_json_output(camera_info: Dict, movfmt: List[str], 
                        resolutions: List[str], details_list: List[Dict]) -> Dict:
    """生成最终的JSON输出"""
    return {
        "camera_model": camera_info.get("model", ""),
        "camera_nickName": camera_info.get("nickName", ""),
        "camera_sw": camera_info.get("sw", ""),
        "allfmt": camera_info.get("allfmt", []),
        "movfmt": movfmt,
        "resolution": resolutions,
        "details_list": details_list
    }


def check_format(details_list: List[Dict], movfmt: List[str]) -> bool:
    """
    检查输出结果是否正确
    验证details_list中每个resolution和fps组合的movfmt是否在movfmt列表中
    
    返回: True表示检查通过，False表示有错误
    """
    print("\n" + "="*60)
    print("开始检查格式正确性...")
    print("="*60)
    
    errors = []  # 存储错误信息: [(resolution, fps, expected_movfmt), ...]
    movfmt_set = set(movfmt)  # 转换为set以提高查找效率
    
    for detail in details_list:
        resolution = detail.get("resolution", "")
        fps_list = detail.get("fps", [])
        
        for fps in fps_list:
            # 组合movfmt: resolution + "P" + fps
            expected_movfmt = f"{resolution}P{fps}"
            
            # 检查是否在movfmt列表中
            if expected_movfmt not in movfmt_set:
                errors.append((resolution, fps, expected_movfmt))
    
    # 报告检查结果
    if len(errors) == 0:
        print("\n✓ 检查通过！所有resolution和fps的组合都在movfmt列表中。")
        return True
    else:
        print(f"\n✗ 发现 {len(errors)} 个错误：")
        print("\n错误详情：")
        print("-" * 60)
        
        # 按resolution分组显示错误
        error_by_resolution = {}
        for resolution, fps, expected_movfmt in errors:
            if resolution not in error_by_resolution:
                error_by_resolution[resolution] = []
            error_by_resolution[resolution].append((fps, expected_movfmt))
        
        for resolution, fps_errors in sorted(error_by_resolution.items()):
            print(f"\n分辨率: {resolution}")
            for fps, expected_movfmt in fps_errors:
                print(f"  - FPS: {fps}")
                print(f"    期望的movfmt: {expected_movfmt}")
                print(f"    状态: 不在movfmt列表中")
        
        print("\n" + "-" * 60)
        return False


def check_native_format(allfmt: List[str], movfmt: List[str]) -> bool:
    """
    比较allfmt和movfmt两个列表，查看是否完全相同
    如有不同，打印差异信息
    
    返回: True表示完全相同，False表示有差异
    """
    print("\n" + "="*60)
    print("开始检查allfmt和movfmt是否完全相同...")
    print("="*60)
    
    allfmt_set = set(allfmt)
    movfmt_set = set(movfmt)
    
    # 找出在allfmt中但不在movfmt中的项
    only_in_allfmt = allfmt_set - movfmt_set
    # 找出在movfmt中但不在allfmt中的项
    only_in_movfmt = movfmt_set - allfmt_set
    
    if len(only_in_allfmt) == 0 and len(only_in_movfmt) == 0:
        print("\n✓ 检查通过！allfmt和movfmt完全相同。")
        print(f"  共同项数量: {len(allfmt_set)}")
        return True
    else:
        print(f"\n✗ 发现差异！")
        print(f"  allfmt总数: {len(allfmt)}")
        print(f"  movfmt总数: {len(movfmt)}")
        print(f"  共同项数量: {len(allfmt_set & movfmt_set)}")
        
        if len(only_in_allfmt) > 0:
            print(f"\n  仅在allfmt中的项 (共 {len(only_in_allfmt)} 个):")
            print("-" * 60)
            for item in sorted(only_in_allfmt):
                print(f"    - {item}")
        
        if len(only_in_movfmt) > 0:
            print(f"\n  仅在movfmt中的项 (共 {len(only_in_movfmt)} 个):")
            print("-" * 60)
            for item in sorted(only_in_movfmt):
                print(f"    - {item}")
        
        print("\n" + "-" * 60)
        return False


def main():
    """主函数"""
    print("="*60)
    print("ZCAM相机格式信息采集工具")
    print("="*60)
    
    # 获取用户输入
    camera_ip = input("\n请输入相机IP地址 (例如: 192.168.1.103): ").strip()
    if not camera_ip:
        print("错误: IP地址不能为空")
        sys.exit(1)
    
    output_path = input("请输入输出JSON文件路径 (例如: output.json): ").strip()
    if not output_path:
        print("错误: 输出文件路径不能为空")
        sys.exit(1)
    
    # 记录开始时间
    start_time = time.time()
    print(f"\n开始执行... (开始时间: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(start_time))})")
    
    base_url = camera_ip
    
    # 步骤1: 获取相机基本信息
    camera_info = get_camera_info(base_url)
    if not camera_info:
        print("错误: 无法获取相机信息，请检查IP地址和网络连接")
        sys.exit(1)
    
    # 步骤2: 获取movfmt列表
    movfmt = get_movfmt(base_url)
    
    # 步骤3: 获取分辨率列表
    resolutions = get_resolutions(base_url)
    if not resolutions:
        print("错误: 无法获取分辨率列表")
        sys.exit(1)
    
    # 步骤4: 遍历每个分辨率获取详细信息
    details_list = []
    print(f"\n开始遍历 {len(resolutions)} 个分辨率...")
    for i, resolution in enumerate(resolutions, 1):
        print(f"\n处理分辨率 {i}/{len(resolutions)}: {resolution}")
        details = get_resolution_details(base_url, resolution, movfmt)
        if details:
            details_list.append(details)
        else:
            print(f"警告: 无法获取分辨率 '{resolution}' 的详细信息，跳过")
    
    # 步骤5: 生成JSON文件
    print("\n[步骤5] 生成JSON文件...")
    output_data = generate_json_output(camera_info, movfmt, resolutions, details_list)
    
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=4, ensure_ascii=False)
        print(f"\n成功! JSON文件已保存到: {output_path}")
    except Exception as e:
        print(f"\n错误: 保存JSON文件失败 - {e}")
        sys.exit(1)
    
    # 步骤6: 检查格式正确性
    # 考虑到相机的movfmt名称表述存在多种不同组合表述，所以这里不进行检查
    # print("\n[步骤6] 检查格式正确性...")
    # check_passed = check_format(details_list, movfmt)
    # if not check_passed:
    #   print("\n警告: 格式检查未通过，请检查上述错误信息。")
    
    # 步骤7: 检查allfmt和movfmt是否相同
    print("\n[步骤7] 检查allfmt和movfmt是否完全相同...")
    allfmt_list = camera_info.get("allfmt", [])
    native_check_passed = check_native_format(allfmt_list, movfmt)
    
    if not native_check_passed:
        print("\n警告: allfmt和movfmt存在差异，请检查上述信息。")
    
    if native_check_passed:
        print("\n所有检查完成！")
    
    # 计算并显示总耗时
    end_time = time.time()
    elapsed_time = end_time - start_time
    hours = int(elapsed_time // 3600)
    minutes = int((elapsed_time % 3600) // 60)
    seconds = int(elapsed_time % 60)
    milliseconds = int((elapsed_time % 1) * 1000)
    
    print("\n" + "="*60)
    print("时间统计")
    print("="*60)
    print(f"开始时间: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(start_time))}")
    print(f"结束时间: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(end_time))}")
    print(f"总耗时: {hours:02d}:{minutes:02d}:{seconds:02d}.{milliseconds:03d} ({elapsed_time:.3f} 秒)")
    print("="*60)


if __name__ == "__main__":
    main()

