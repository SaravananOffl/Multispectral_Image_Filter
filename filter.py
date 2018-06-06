import numpy as np
import gdal
import os
import warnings
import xlwt
import matplotlib.pyplot as plt

class filter(object):
        def __init__(self, in_folder, band_no, threshold, out_folder, excel_name ):
                self.in_folder = in_folder
                self.band_no = band_no
                self.threshold = threshold
                self.out_folder = out_folder
                self.excel_name = excel_name
                self.book = xlwt.Workbook()
                self.sheet = self.book.add_sheet(excel_name)
                self.model()
        
        def setup_excel(self):

            column_names = ["Input File", "B1_Mean", "B2_Mean","B3_Mean","B4_Mean","B1_Median","B2_Median","B3_Median",
                        "B4_Median","B1_STD","B2_STD","B3_STD","B4_STD"]
            for no,column_name in enumerate(column_names):
                self.sheet.write(0,no,column_name)
            
                

        def write_mean(self,stats,row_no):
            for no, band in enumerate(stats):
                self.sheet.write(row_no+1,no+1,float(band))
                    
        def write_median(self,stats,row_no):
            for no, band in enumerate(stats):
                self.sheet.write(row_no+1,no+5,float(band))

        def write_std(self,stats,row_no):
            for no, band in enumerate(stats):
                self.sheet.write(row_no+1,no+9,float(band))
                    
        def findFiles(self,path):
            tif_files = []
            for file in os.listdir("{}".format(path)):
                if file.endswith('.tif'):
                    tif_files.append(file)
            return tif_files

        

        def model(self):
            print("Started....")
            self.setup_excel()
            row_no = 0
            for file in self.findFiles(self.in_folder):
                raster = gdal.Open(f'{file}')

                band = []
                for i in range(raster.RasterCount):
                    band.append(np.absolute(raster.GetRasterBand(i+1).ReadAsArray()))
                
                band1 = band[0]
                band2 = band[1]
                band3 = band[2] 
                band4 = band[3]

                for i in range(band1.shape[0]):
                    for j in range(band1.shape[1]):
                        if(band1[i][j]>=0.061):
                            band1[i][j] = 0
                            band2[i][j] = 0
                            band3[i][j] = 0
                            band4[i][j] = 0
                band1 = np.array(band1,dtype=np.float64)
                band2 = np.array(band2,dtype=np.float64)
                band3 = np.array(band3,dtype=np.float64)
                band4 = np.array(band4,dtype=np.float64)
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore", category=RuntimeWarning)
                    mean = [np.nanmean(band1,dtype=np.float64),np.nanmean(band2,dtype=np.float64),np.nanmean(band3,dtype=np.float64),
                            np.nanmean(band4,dtype=np.float64)]
                    median = [np.median(band1[np.nonzero(band1)]),np.median(band2[np.nonzero(band2)]),np.median(band3[np.nonzero(band3)])
                        ,np.median(band4[np.nonzero(band4)])]
                    std_dev = [np.std(band1[np.nonzero(band1)]),np.std(band2[np.nonzero(band2)]),np.std(band3[np.nonzero(band3)]),
                            np.std(band4[np.nonzero(band4)])]    
                    
                        
                self.sheet.write(row_no+1,0,file)
                self.write_mean(mean,row_no)
                self.write_median(median,row_no)
                self.write_std(std_dev, row_no)
        #         visualise(band1) 
                row_no = row_no  +1
                

            self.book.save('718_std.xls')
            
            

            
            
