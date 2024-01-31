"""
Author: Bill LI
File: write_csv.py
Created: 01/07/2024
Description: Write questions to csv
"""

import pandas as pd

def write():
    # Questions extracted from the exam paper
    questions = [
        "如果向西走5m，记作＋5m，那么－15m表示？ A. 向东走15m B. 向南走15m C. 向西走15m D. 向北走15m",
        "下列各对数中，互为相反数的是？ A. -|-7|和+(-7) B. +(-5)和-(+5) C. (-1)^3和-1^3 D. (-1)^2和-1^2",
        "下列比较大小结果正确的是？ A. -3<-4 B. -(-2)<|-2| C. -1/2>-1/3 D. |-1/8>-1/7|",
        "如图，数轴的单位长度为1，如果点A，B表示的数的绝对值相等，那么点A表示的数是？ A. －2 B. －3 C. －4 D. 0",
        "绝对值等于其本身的数有？ A. 1个 B. 2个 C. 0个 D. 无数个",
        "如果两个有理数的积是负数，和是正数，那么这两个有理数？ A. 同号，且均为负数 B. 异号，且正数的绝对值比负数的绝对值大 C. 同号，且均为正数 D. 异号，且负数的绝对值比正数的绝对值大",
        "下列说法正确的是？ A. 三个有理数相乘积为负数，则这三个数一定都是负数 B. 两个有理数的和为零，则这两个数一定互为相反数 C. 零是最小的有理数 D. 两个有理数的和不可能比任何一个加数都小",
        "有理数对应的点在数轴上的位置如图，则下列结论正确的是？ A. a－b＞0 B. |a|＞|b| C. a/b＜0 D. a＋b＜0",
        "若a和b互为相反数，c和d互为倒数，|m|的绝对值为2，则m^2-cd+(a+b)/m的值为？ A. -5 B. 3 C. -3 D. 3或-5",
        "在明代的《算法统宗》一书中将用格子的方法计算两个数相乘称作“铺地锦”，如图1，计算82×34，将乘数82记入上行，乘数34记入右行，然后用乘数82的每位数字乘以乘数34的每位数字，将结果记入相应的格子中，最后按斜行加起来，既得2788．如图2，用“铺地锦”的方法表示两个两位数相乘，下列结论错误的是？ A. b的值为6 B. a为奇数 C. 乘积结果可以表示为101b+10（a+1）-1 D. a的值小于3"
    ]

    # Creating a DataFrame
    df = pd.DataFrame({
        "question_id": range(1, 11),
        "content": questions
    })

    # Saving the DataFrame to a CSV file
    csv_file = "./data/questions.csv"
    df.to_csv(csv_file, index=False, encoding='utf-8-sig')
    print("Write to " + csv_file + " done")


if __name__ == "__main__":
    write()