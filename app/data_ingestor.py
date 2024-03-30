import os
import json
import pandas as pd
from app.constants import CSVColumnNames
from app.events import finished_loading_csv

class Entry:
    def __init__(self, row):
        self.YearStart = row[CSVColumnNames.YEARSTART.value]
        self.YearEnd = row[CSVColumnNames.YEAREND.value]
        self.LocationAbbr = row[CSVColumnNames.LOCATIONABBR.value]
        self.LocationDesc = row[CSVColumnNames.LOCATIONDESC.value]
        self.Datasource = row[CSVColumnNames.DATASOURCE.value]
        self.Class = row[CSVColumnNames.CLASS.value]
        self.Topic = row[CSVColumnNames.TOPIC.value]
        self.Question = row[CSVColumnNames.QUESTION.value]
        self.Data_Value_Unit = row[CSVColumnNames.DATA_VALUE_UNIT.value]
        self.Data_Value_Type = row[CSVColumnNames.DATA_VALUE_TYPE.value]
        self.Data_Value = row[CSVColumnNames.DATA_VALUE.value]
        self.Data_Value_Alt = row[CSVColumnNames.DATA_VALUE_ALT.value]
        self.Data_Value_Footnote_Symbol = row[CSVColumnNames.DATA_VALUE_FOOTNOTE_SYMBOL.value]
        self.Data_Value_Footnote = row[CSVColumnNames.DATA_VALUE_FOOTNOTE.value]
        self.Low_Confidence_Limit = row[CSVColumnNames.LOW_CONFIDENCE_LIMIT.value]
        self.High_Confidence_Limit = row[CSVColumnNames.HIGH_CONFIDENCE_LIMIT.value]
        self.Sample_Size = row[CSVColumnNames.SAMPLE_SIZE.value]
        self.Total = row[CSVColumnNames.TOTAL.value]
        self.Age = row[CSVColumnNames.AGE.value]
        self.Education = row[CSVColumnNames.EDUCATION.value]
        self.Gender = row[CSVColumnNames.GENDER.value]
        self.Income = row[CSVColumnNames.INCOME.value]
        self.Race_Ethnicity = row[CSVColumnNames.RACE_ETHNICITY.value]
        self.Geolocation = row[CSVColumnNames.GEOLOCATION.value]
        self.ClassID = row[CSVColumnNames.CLASSID.value]
        self.TopicID = row[CSVColumnNames.TOPICID.value]
        self.QuestionID = row[CSVColumnNames.QUESTIONID.value]
        self.DataValueTypeID = row[CSVColumnNames.DATAVALUETYPEID.value]
        self.LocationID = row[CSVColumnNames.LOCATIONID.value]
        self.StratificationCategory1 = row[CSVColumnNames.STRATIFICATIONCATEGORY1.value]
        self.Stratification1 = row[CSVColumnNames.STRATIFICATION1.value]
        self.StratificationCategoryId1 = row[CSVColumnNames.STRATIFICATIONCATEGORYID1.value]
        self.StratificationID1 = row[CSVColumnNames.STRATIFICATIONID1.value]

class DataIngestor:
    def __init__(self, csv_path: str):
        # TODO: Read csv from csv_path

        # Store entries in a list
        self.data_entries = []

        # Read the csv in chunks of 1000 rows at a time
        dataframes = pd.read_csv(csv_path, chunksize=1000)
        for df in dataframes:
            for index, row in df.iterrows():
                entry = Entry(row)
                self.data_entries.append(entry)

        # Signal that the csv has been loaded
        finished_loading_csv.set()


        self.questions_best_is_min = [
            'Percent of adults aged 18 years and older who have an overweight classification',
            'Percent of adults aged 18 years and older who have obesity',
            'Percent of adults who engage in no leisure-time physical activity',
            'Percent of adults who report consuming fruit less than one time daily',
            'Percent of adults who report consuming vegetables less than one time daily'
        ]

        self.questions_best_is_max = [
            'Percent of adults who achieve at least 150 minutes a week of moderate-intensity aerobic physical activity or 75 minutes a week of vigorous-intensity aerobic activity (or an equivalent combination)',
            'Percent of adults who achieve at least 150 minutes a week of moderate-intensity aerobic physical activity or 75 minutes a week of vigorous-intensity aerobic physical activity and engage in muscle-strengthening activities on 2 or more days a week',
            'Percent of adults who achieve at least 300 minutes a week of moderate-intensity aerobic physical activity or 150 minutes a week of vigorous-intensity aerobic activity (or an equivalent combination)',
            'Percent of adults who engage in muscle-strengthening activities on 2 or more days a week',
        ]
