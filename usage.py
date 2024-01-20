#
#
# import snob as sb
# # from snob import Equity, ETF, Indicator
#
#
# test = sb.Equity(ticker="000660", period=10, freq="d", enddate="20230731")
#
#
# # Show DataFrame
# print(test.ohlcv) # test.ohlcv
# print(test.asset) # test.asset
#
#
# # Show Status
# print(test.ohlcv.status)
# print(test.asset.status)
#
#
# # Show Chart
# test.ohlcv.chart()
# test.asset.chart()
#
#
# # Abbreviation
# test.abbreviate()


# import os
# import shutil
#
# def copy_files(source_path, destination_path):
#     # 소스 경로의 파일 목록 가져오기
#     files = os.listdir(source_path)
#
#     # 대상 경로가 없다면 생성
#     if not os.path.exists(destination_path):
#         os.makedirs(destination_path)
#
#     # 파일을 순번 이름으로 복사
#     for index, file_name in enumerate(files):
#         source_file_path = os.path.join(source_path, file_name)
#         ext = file_name.split(".")[-1]
#         destination_file_path = os.path.join(destination_path, f"{index + 1}.{ext}")
#
#         shutil.copy2(source_file_path, destination_file_path)
#
# if __name__ == "__main__":
#     # 소스 경로와 대상 경로 설정
#     folder = "AIMIX-24-Raw"
#     source_path = rf'C:\Users\wpgur\Downloads\{folder}'
#     destination_path = rf'C:\Users\wpgur\Downloads\{folder.replace("Raw", "Num")}'
#     destination_path2 = rf'C:\Users\wpgur\Downloads\{folder.replace("Raw", "View")}'
#
#     # 파일 복사 실행
#     copy_files(source_path, destination_path)
#     copy_files(source_path, destination_path2)