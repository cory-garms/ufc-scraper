import pandas as pd
import difflib

def cleanodds():

    oddsdf = pd.read_csv('./odds_movement.csv')
    print(f'odds movement rows: {len(oddsdf)} ')

    eventdf = pd.read_csv('../csv/ufc_fight_outcomes.csv')
    print(f'fight detailed events rows: {len(eventdf)} ')

    oddsdf['Date'] = oddsdf['Event'].str.split(' ').str[-3:]
    oddsdf['Event'] = oddsdf['Event'].str.split(' ').str[0:-3]

    oddsdf['Date'] = [' '.join(map(str, l)) for l in oddsdf['Date']]
    oddsdf['Event'] = [' '.join(map(str, l)) for l in oddsdf['Event']]


    print(len(sorted(eventdf['EventName'].unique())))
    print(len(sorted(oddsdf['Event'].unique())))


    oddsdf['Event'] = oddsdf['Event'].str.replace('\d+', '').str.replace(' II', '').str.replace(' :', ':').str.replace('Nurmagomedov','Khabib').str.strip()

    j=0

    events_ufc = sorted(eventdf['EventName'].unique())
    odds_events = sorted(oddsdf['Event'].unique())


    for index, event in enumerate(odds_events):
        matches = difflib.get_close_matches(event, events_ufc, n=1, cutoff=0.75)
        
        if matches:
            j=j+1
            
        else: 
            print('~~~~~~########################~~~~~~~~~~~~~~~')
            print(event)
            print('no match')
            print('~~~~~~########################~~~~~~~~~~~~~~~')
    
    print(f'A total of {str(j)} out of {str(len(odds_events))} were matched' )

    unique_events = eventdf['EventName'].unique()
    unique_names = eventdf['Fighter'].unique()

    ###### use trydifflib function to find closest matching string
    def trydifflib(string, list):
            match = difflib.get_close_matches(string, list, n=1, cutoff=0.75)

            if match:
                 return match[0]
            
    oddsdf['Event_merged'] = oddsdf['Event'].apply(lambda x: trydifflib(x, unique_events))
    oddsdf['Fighter_merged'] = oddsdf['Fighter'].apply(lambda x: trydifflib(x, unique_names))


    new_df2 = pd.merge(eventdf, oddsdf, how='left', left_on=['EventName','Fighter'], right_on = ['Event_merged','Fighter_merged'])

    print(new_df2.isna().sum())

    print(new_df2.dropna())

    new_df2.to_csv('./events_with_odds.csv')


cleanodds()


    # def change_names_back(oddsdf1):
    #     oddsdf1 = oddsdf1.replace('Germaine DeRandamie', 'Germaine de Randamie')
    #     oddsdf1 = oddsdf1.replace('Seung WooChoi', 'Seung Woo Choi')
    #     oddsdf1 = oddsdf1.replace('Daniel DaSilva','Daniel da Silva')
    #     oddsdf1 = oddsdf1.replace('ZarahFairn DosSantos','Zarah Fairn Dos Santos')
    #     oddsdf1 = oddsdf1.replace('Kai KaraFrance','Kai Kara France')
    #     oddsdf1 = oddsdf1.replace('Alex DaSilva','Alex da Silva')
    #     oddsdf1 = oddsdf1.replace('BrunoGustavo DaSilva','Bruno Gustavo da Silva')
    #     oddsdf1 = oddsdf1.replace('Johnny MunozJr','Johnny Munoz Jr.')
    #     oddsdf1 = oddsdf1.replace('AbdulRazak Alhassan','Abdul Razak Alhassan')
    #     oddsdf1 = oddsdf1.replace('MarcosRogerio DeLima','Marcos Rogerio de Lima')
    #     oddsdf1 = oddsdf1.replace('Dricus DuPlessis','Dricus Du Plessis')
    #     oddsdf1 = oddsdf1.replace('Jack DellaMaddalena','Jack Della Maddalena')
    #     oddsdf1 = oddsdf1.replace('Maheshate Maheshate','Maheshate')
    #     oddsdf1 = oddsdf1.replace('Rafael DosAnjos','Rafael Dos Anjos')
    #     oddsdf1 = oddsdf1.replace('Alessio DiChirico','Alessio Di Chirico')
    #     oddsdf1 = oddsdf1.replace('Montana DeLaRosa','Montana de La Rosa')
    #     oddsdf1 = oddsdf1.replace('Ovince St.Preux','Ovince St. Preux')
    #     oddsdf1 = oddsdf1.replace('DooHo Choi','Doo Ho Choi')
    #     oddsdf1 = oddsdf1.replace('Mayra BuenoSilva','Mayra Bueno Silva')
    #     oddsdf1 = oddsdf1.replace('Lina AkhtarLansberg','Lina Akhtar Lansberg')
    #     oddsdf1 = oddsdf1.replace('Elizeu ZaleskiDosSantos','Elizeu Zaleski Dos Santos')
    #     oddsdf1 = oddsdf1.replace('DaUn Jung','Da Un Jung')
    #     oddsdf1 = oddsdf1.replace('James TeHuna','James Te Huna')
    #     oddsdf1 = oddsdf1.replace('Douglas SilvaDeAndrade','Douglas Silva de Andrade')
    #     oddsdf1 = oddsdf1.replace('Anderson DosSantos','Anderson Dos Santos')
    #     oddsdf1 = oddsdf1.replace('AntonioRodrigo Nogueira','Antonio Rodrigo Nogueira')
    #     oddsdf1 = oddsdf1.replace('JiYeon Kim','Ji Yeon Kim')
    #     oddsdf1 = oddsdf1.replace('JinSoo Son','Jin Soo Son')
    #     oddsdf1 = oddsdf1.replace('Yorgan DeCastro','Yorgan de Castro')
    #     oddsdf1 = oddsdf1.replace('Phil DeFries','Phil de Fries')
    #     oddsdf1 = oddsdf1.replace('Junior DosSantos','Junior Dos Santos')