import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TkAgg')
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph.exporters


class Program():

    # def write(file_name, lst):
    #     writer = pd.ExcelWriter(file_name, engine='xlsxwriter')
    #     xl = pd.ExcelFile(file_name)
    #
    #     for i in range(len(lst)):
    #         df = xl.parse(xl.sheet_names[i])
    #         df.to_excel(writer, sheet_name=lst[i], index=False, engine='xlsxwriter')
    #
    #     writer.save()
    #     writer.close()

    def data(self, file_name, tap_name):
        sheet = pd.read_excel(file_name, sheet_name=tap_name, skiprows=1, header=None)
        df = sheet.iloc[:, 0::3]  # 3으로 나눴을 때 나머지가 0인 index를 갖는 열의 전체 행을 추출
        df.columns = range(df.shape[1])
        return df

    def data_sum(self, file_name, tap_name):
        sheet = pd.read_excel(file_name, sheet_name=tap_name, header=None)
        df = pd.DataFrame()
        df[0] = sheet.iloc[:, 3]
        df[1] = sheet.iloc[:, 6]
        df[2] = sheet.iloc[:, 7]
        df[3] = sheet.iloc[:, 20]
        df[4] = sheet.iloc[:, 21]
        df[5] = sheet.iloc[:, 22]
        df[6] = sheet.iloc[:, 24]
        df[7] = sheet.iloc[:, 27]
        df[8] = sheet.iloc[:, 29]
        df[9] = df[0] / df[2]
        df[10] = df[1] / df[2]

        lit = []
        for index in range(len(df)):
            if df[9][index] >= 0.1 and df[10][index] >= 0.1:
                lit.append(1)
            else:
                lit.append(0)
        df[11] = lit
        df[12] = sheet.iloc[:, 0]

        df = df.fillna('')
        df = df.T
        # df.drop(df.index[[0,1,2]], inplace=True)
        # df.reset_index(inplace=True, drop=True)
        return df

    # def result(xls, df):
    #     # Create a Pandas Excel writer using XlsxWriter as the engine.
    #     writer = pd.ExcelWriter('result.xlsx', engine='xlsxwriter')
    #
    #     # Add the first dataframe to the worksheet.
    #     xls.to_excel(writer, sheet_name='All', index=False)
    #
    #     offset = len(xls) + 3  # Add extra row for column header.
    #
    #     # Write the datafram without a column header or index.
    #     df.to_excel(writer, sheet_name='All', startrow=offset,
    #                 header=False, index=False)
    #
    #     # Close the Pandas Excel writer and output the Excel file.
    #     writer.save()

    def read_file(self, file):
        xl = pd.ExcelFile(file)
        res = len(xl.sheet_names)

        # lst = []
        # for i in range(1, res, 1):
        #     if i == 1:
        #         lst.append('session%i_sum' % i)
        #     elif i % 2 == 0:
        #         i /= 2
        #         lst.append('session%i' % i)
        #     else:
        #         i = i / 2 + 1
        #         lst.append('session%i_sum' % i)
        #
        # write(file, lst)

        dfs = {}
        for i in range(res - 1):
            if i % 2 == 0:
                dfs[res - 2 - i] = Program.data_sum(self, file, i)
            else:
                dfs[res - 2 - i] = Program.data(self, file, i)

        df = pd.concat({k: pd.DataFrame(v) for k, v in dfs.items()}, axis=0)  # 236 x 2946
        # id_list = pd.DataFrame([id])
        # new_df = df[5].append(id_list)
        # new_df = pd.concat(df, df)
        return df


# df = pd.concat({k: pd.DataFrame(v) for k, v in dfs.items()})                      # 339 x 2946
# df = pd.concat(dfs.values(), ignore_index=True)                                   # 236 X 2946
# df = pd.concat({k: pd.DataFrame(v) for k, v in dfs.items()}, axis=1).stack(0).T   # 2946 x 339

    def sort(self, df):
        dfObj = df.sort_values(by='b', axis=1)
        return dfObj

    def select_session(self, df, session_type, peak_z_score, lower_peak_position, upper_peak_position, trough_z_score,
                       lower_trough_position, upper_trough_position):
        if session_type == 'Session 1':
            # Firing rate (fr) > 0.1 ?  1
            temp_df = df.loc[:, df.loc[1, 11] == 1]
            if peak_z_score != None:
                # Peak Z-score >
                select_df = Program.select_peak(self, temp_df, 1, peak_z_score, lower_peak_position,
                                                upper_peak_position)
                return select_df

            elif trough_z_score != None:
                select_df = Program.select_trough(self, temp_df, 1, trough_z_score, lower_trough_position,
                                                  upper_trough_position)
                return select_df

        elif session_type == 'Session 2':
            temp_df = df.loc[:, df.loc[3, 11] == 1]
            if peak_z_score != None:
                select_df = Program.select_peak(self, temp_df, 3, peak_z_score, lower_peak_position,
                                                upper_peak_position)
                return select_df

            elif trough_z_score != None:
                select_df = Program.select_trough(self, temp_df, 3, trough_z_score, lower_trough_position,
                                                  upper_trough_position)
                return select_df

        elif session_type == 'Session 3':
            temp_df = df.loc[:, df.loc[5, 11] == 1]
            if peak_z_score != None:
                select_df = Program.select_peak(self, temp_df, 5, peak_z_score, lower_peak_position,
                                                upper_peak_position)
                return select_df

            elif trough_z_score != None:
                select_df = Program.select_trough(self, temp_df, 5, trough_z_score, lower_trough_position,
                                                  upper_trough_position)
                return select_df

        elif session_type == 'Session 4':
            temp_df = df.loc[:, df.loc[7, 11] == 1]
            if peak_z_score != None:
                select_df = Program.select_peak(self, temp_df, 7, peak_z_score, lower_peak_position,
                                                upper_peak_position)
                return select_df

            elif trough_z_score != None:
                select_df = Program.select_trough(self, temp_df, 7, trough_z_score, lower_trough_position,
                                                  upper_trough_position)
                return select_df

        elif session_type == 'Session 5':
            temp_df = df.loc[:, df.loc[9, 11] == 1]
            if peak_z_score != None:
                select_df = Program.select_peak(self, temp_df, 9, peak_z_score, lower_peak_position,
                                                upper_peak_position)
                return select_df

            elif trough_z_score != None:
                select_df = Program.select_trough(self, temp_df, 9, trough_z_score, lower_trough_position,
                                                  upper_trough_position)
                return select_df

    def select_peak(self, df, session_num, peak_z_score, lower_peak_position, upper_peak_position):
        # if peak_z_score != None:
        # Peak Z-score >
        select_df = df.loc[:, (pd.to_numeric(df.loc[session_num, 5], errors='coerce') > peak_z_score)]
        # if lower_peak_position != None and upper_peak_position != None:
        # < Peak position <
        new_df = select_df.loc[:, (pd.to_numeric(select_df.loc[session_num, 6], errors='coerce') >
                                   lower_peak_position) &
                                  (pd.to_numeric(select_df.loc[session_num, 6], errors='coerce') <
                                   upper_peak_position)]
        new_df.columns = range(new_df.shape[1])

        for i in range(new_df.index.get_level_values(0).nunique()):
            if i % 2 != 0:
                new_df = new_df.drop([(i, 0), (i, 1), (i, 2)])
        new_df = new_df.sort_values(by=(session_num, 6), axis=1)
        # df1 = pd.DataFrame([[np.nan] * len(new_df.columns)], columns=new_df.columns)
        # df2 = pd.DataFrame([[np.nan] * len(new_df.columns)], columns=new_df.columns)
        # new_df = new_df.append(df1, ignore_index=True)
        # new_df = new_df.append(df2, ignore_index=True)
        new_df.columns = range(new_df.shape[1])
        return new_df

    def select_trough(self, df, session_num, trough_z_score,
                       lower_trough_position, upper_trough_position):
        # if trough_z_score != None:
        # Trough Z-score <
        select_df = df.loc[:, (pd.to_numeric(df.loc[session_num, 7], errors='coerce') < trough_z_score)]
        # if lower_trough_position != None and upper_trough_position != None:
        # < Trough position <
        new_df = select_df.loc[:, (pd.to_numeric(select_df.loc[session_num, 8], errors='coerce') >
                                   lower_trough_position) &
                                  (pd.to_numeric(select_df.loc[session_num, 8], errors='coerce') <
                                   upper_trough_position)]
        new_df.columns = range(new_df.shape[1])

        for i in range(new_df.index.get_level_values(0).nunique()):
            if i % 2 != 0:
                new_df = new_df.drop([(i, 0), (i, 1), (i, 2)])
        new_df = new_df.sort_values(by=(session_num, 8), axis=1)
        df1 = pd.DataFrame([[np.nan] * len(new_df.columns)], columns=new_df.columns)
        df2 = pd.DataFrame([[np.nan] * len(new_df.columns)], columns=new_df.columns)
        new_df = new_df.append(df1, ignore_index=True)
        new_df = new_df.append(df2, ignore_index=True)
        new_df.columns = range(new_df.shape[1])
        return new_df

    def standardization(self, df, mean, sd):
        num = df - mean
        new_df = num.div(sd.replace(0, np.nan)).fillna(0)
        for c in new_df.columns:
            if new_df[c].max() > 30 or new_df[c].min() < -30:
                new_df[c] *= sd[c]

        return new_df

    def mean(self, df):
        return df.mean(axis=1)

    def sem(self, df):
        # sem_df = sd.div(sd.count().pow(0.5).replace(0, np.nan)).fillna(0)
        return df.std(axis=1)

    def graph(self, df, xLower, xUpper, xUnit):
        # fig, ax = plt.subplots()
        x = np.arange(xLower, xUpper, xUnit)
        lst = ['Series%i' % i for i in range(1, 6, 1)]
        # clrs = sns.color_palette("husl", 5)

        plt = pg.plot()
        # plt = pg.GraphicsView()
        plt.setWindowTitle('Graph')
        plt.addLegend()
        plt.setBackground('w')

        for i in range(df.index.get_level_values(0).nunique()):
            y = df[0][i * 2]
            error = df[1][i * 2]
            # ax.plot(x, y, label=lst[i], c=clrs[i])
            # ax.plot(x, y, label=lst[i])
            # plt.plot(x, y, label=lst[i])
            plt.plot(x, y, pen=pg.mkPen(color=(i, 3), width=5), name=lst[i])
            # pen = pg.mkPen('b', width=5)
            # pen = pg.mkPen(color='#025b94', width=1)
            # ax.fill_between(x, y - error, y + error, alpha=0.3)
            # plt.fill_between(x, y - error, y + error, alpha=0.3)
            lowRange = (y - error).values
            highRange = (y + error).values
            phigh = pg.PlotCurveItem(x, highRange, pen=(0, 0, 0, 0))
            plow = pg.PlotCurveItem(x, lowRange, pen=(0, 0, 0, 0))
            brush = pg.intColor(i, 3, alpha=100)
            pfill = pg.FillBetweenItem(phigh, plow, brush=brush)
            plt.addItem(phigh)
            plt.addItem(plow)
            plt.addItem(pfill)
            # ax.fill_between(x, y - error, y + error, alpha=0.5, facecolor=clrs[i])

        # plt.legend()
        # ax.legend()

        # pg.show()
        # plt.show()

        # create an exporter instance, as an argument give it
        # the item you wish to export
        exporter = pg.exporters.ImageExporter(plt.plotItem)
        # set export parameters if needed
        # exporter.parameters()['width'] = 100  # (note this also affects height parameter)
        exporter.params.param('width').setValue(700, blockSignal=exporter.widthChanged)
        exporter.params.param('height').setValue(500, blockSignal=exporter.heightChanged)
        # save to file
        exporter.export('graph.png')

        # fig.savefig('graph.png')
        # plt.savefig('graph.png')


if __name__ == "__main__":
    p = Program()
    df = p.read_file('AP18_CC_10s_temp_w_robot_temp.xls')
    # print(df.loc[1, 11])    # select one row

    new_df = p.select_session(df, 'Session 3', 3, -0.1, 0.1, None, None, None)
    # new_df.to_excel('Data.xlsx', sheet_name='All')

    stand_df = {}
    for i in range(new_df.index.get_level_values(0).nunique()):
        if i % 2 == 0:
            stand_df[i] = p.standardization(new_df.loc[i], new_df.loc[i+1, 3], new_df.loc[i+1, 4])
    stand_df = pd.concat({k: pd.DataFrame(v) for k, v in stand_df.items()}, axis=0)
    # stand_df.to_excel('Standard Data.xlsx', sheet_name='All')

    # mean_sem = p.mean(stand_df), p.sem(stand_df)
    mean_sem = stand_df.mean(axis=1), stand_df.sem(axis=1)
    temp_df = pd.DataFrame(list(mean_sem)).T
    # temp_df.to_excel('Mean_SEM.xlsx', sheet_name='All')

    p.graph(temp_df, -0.50, 0.50, 0.01)

    # df = pd.DataFrame(np.array(temp_df).reshape(100, temp_df.index.get_level_values(0).nunique() * 2))
    # df = df.T
    # df = np.array_split(temp_df, temp_df.index.get_level_values(0).nunique())
    # print(df)

    # df.to_excel('Data.xlsx', sheet_name='All')