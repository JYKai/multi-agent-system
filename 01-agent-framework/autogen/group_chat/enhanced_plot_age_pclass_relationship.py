# filename: enhanced_plot_age_pclass_relationship.py
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def download_and_preprocess_data(url):
    try:
        data = pd.read_csv(url)
        # 결측치 제거
        data.dropna(subset=['age', 'pclass'], inplace=True)
        return data
    except Exception as e:
        print(f"Error downloading the data: {e}")
        return None

# 데이터셋 URL
url = "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/titanic.csv"

# 데이터 재로드 및 전처리
data = download_and_preprocess_data(url)

if data is not None:
    # Styling and plotting
    sns.set_style("whitegrid")
    plt.figure(figsize=(10, 6))
    violin_plot = sns.violinplot(x='pclass', y='age', data=data, inner='quartile')
    violin_plot.set_title('Enhanced Age Distribution by Passenger Class')
    violin_plot.set_xlabel('Passenger Class')
    violin_plot.set_ylabel('Age')
    violin_plot.figure.savefig('enhanced_age_pclass_relationship.png')
    print('The enhanced chart has been saved as enhanced_age_pclass_relationship.png.')
else:
    print('Failed to process data due to previous errors.')