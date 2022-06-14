import pandas as pd
df = pd.read_excel('list ersali.xlsx')
columns = df.columns.values


def LenOfColumns():
    return len(columns)


# for j in range(len(columns)):
#     try:
#         print('\n',columns[j])
#         input("start ?")
#         # for i in df.index.values:
#         #     try:
#         #         phone = '+98' + str(int(df[columns[j]][i]))
#         #         print(j, i, phone)
#         #
#         #     except:
#         #         pass
#     except:
#         pass


def GetNumberInColumnFromExcel(j):

    for i in df.index.values:
        try:
            phone = '+98' + str(int(df[columns[j]][i]))
            # print(j, i, phone)
            yield phone
        except:
            pass