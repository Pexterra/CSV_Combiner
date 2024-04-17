import sys, glob, os, pandas as pd

from datetime import timedelta
from PySide6.QtCore import QObject, Slot
from PySide6.QtGui import QGuiApplication, QIcon
from PySide6.QtQml import QQmlApplicationEngine, QmlElement
from PySide6.QtQuickControls2 import QQuickStyle

QML_IMPORT_NAME = "io.qt.textproperties"
QML_IMPORT_MAJOR_VERSION = 1

@QmlElement
class CSVCombiner(QObject):
    def __init__(self):
        super().__init__()

    @Slot(str, str, result=str)
    def combineCSV(self, folder, delim):
        files = []
        folder = folder[8:]
        folder_path = folder

        all_files = os.listdir(folder_path)
        
        # Filter out non-CSV files
        csv_files = [f for f in all_files if f.endswith('.csv')]
        
        # Create a list to hold the dataframes
        df_list = []
        
        for csv in csv_files:
            file_path = os.path.join(folder_path, csv)
            try:
                # Try reading the file using default UTF-8 encoding
                df = pd.read_csv(file_path, delimiter=delim)
                df_list.append(df)
            except UnicodeDecodeError:
                try:
                    # If UTF-8 fails, try reading the file using UTF-16 encoding with tab separator
                    df = pd.read_csv(file_path, sep='\t', delimiter=delim, encoding='utf-16')
                    df_list.append(df)
                except Exception as e:
                    print(f"Could not read file {csv} because of error: {e}")
            except Exception as e:
                print(f"Could not read file {csv} because of error: {e}")
        
        # Concatenate all data into one DataFrame
        big_df = pd.concat(df_list, ignore_index=True)
        
        # Save the final result to a new CSV file
        output = os.path.join(folder_path, 'combined_file.csv')
        big_df.to_csv(output, index=False, sep=';')
        return f'Saved combined csv to: {output}'

if __name__ == '__main__':
    app = QGuiApplication(sys.argv)
    #app.setWindowIcon(QIcon('./lib/images/calendar.png'))
    QQuickStyle.setStyle("Material")
    engine = QQmlApplicationEngine()

    qml_file = './lib/qml/gui.qml'
    engine.load(qml_file)

    sys.exit(app.exec())